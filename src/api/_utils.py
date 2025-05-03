from fastapi import HTTPException

from services.ai import IssueSolver
from services.github import GitHubApp, GitHubDownloader, GitHubAPI
from services.scanner import Scanner
from models import Issue


async def solve_issue(request_body: dict) -> None:
    # Getting the token for requests to GitHub API
    installation_id = request_body.get("installation", {}).get("id")

    if not installation_id:
        raise HTTPException(status_code=400, detail="Missing installation.id in payload")

    gh_access_token = await GitHubApp.get_installation_access_token(installation_id)

    # Downloading the repo
    repo_fullname = request_body.get("repository", {}).get("full_name")
    if not repo_fullname:
        raise HTTPException(status_code=400, detail="Missing repository.full_name in payload")
    saved_repo_path = GitHubDownloader(gh_access_token).download(repo_fullname)

    # Building data for the prompt
    issue_dict: dict = request_body.get("issue")
    if not issue_dict:
        raise HTTPException(status_code=400, detail="Missing issue in payload")
    issue_obj = Issue(title=issue_dict.get("title"), body=issue_dict.get("body", ""))
    repo_files = Scanner.scan_dir(saved_repo_path)

    print("Solving", issue_obj.title)
    updated_files = IssueSolver().solve_issues(issue_obj, repo_files)
    if not updated_files:
        return

    gh_api = GitHubAPI(gh_access_token, repo_fullname)
    try:
        issue_number = issue_dict.get("number")
        commit_message = f"NoIDE fix #{issue_number}"
        branch_name = f"noide-issue-{issue_number}"
        base_branch = request_body.get("repository", {}).get("default_branch", "main")
        print("Creating commit to", branch_name, "from", base_branch)
        commit_sha = await gh_api.create_commit(updated_files.files, branch=branch_name, message=commit_message)
        pr_url = await gh_api.create_pull_request(
            head_branch=branch_name,
            base_branch=base_branch,
            title=commit_message
        )
        print("Pull Request created:", pr_url)
    finally:
        await gh_api.aclose()

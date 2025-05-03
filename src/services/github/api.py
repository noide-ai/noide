import asyncio

import httpx

from models import File


class GitHubAPI:
    def __init__(self, token: str, repo_fullname: str):
        self.token = token
        self.repo = repo_fullname  # format: owner/repo
        self.api_url = f"https://api.github.com/repos/{self.repo}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def aclose(self):
        await self.client.aclose()

    async def _get(self, url: str):
        resp = await self.client.get(url)
        resp.raise_for_status()
        return resp.json()

    async def _post(self, url: str, json: dict):
        resp = await self.client.post(url, json=json)
        resp.raise_for_status()
        return resp.json()

    async def _patch(self, url: str, json: dict):
        resp = await self.client.patch(url, json=json)
        resp.raise_for_status()
        return resp.json()

    async def _get_branch_sha(self, branch: str) -> str | None:
        try:
            ref_data = await self._get(f"{self.api_url}/git/ref/heads/{branch}")
            return ref_data["object"]["sha"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def _create_branch(self, new_branch: str, base_branch: str | None = None):
        if base_branch is None:
            # Fetch default branch from repo metadata
            repo_data = await self._get(f"https://api.github.com/repos/{self.repo}")
            base_branch = repo_data["default_branch"]

        base_sha = await self._get_branch_sha(base_branch)
        if not base_sha:
            raise Exception(f"Base branch '{base_branch}' not found")

        url = f"{self.api_url}/git/refs"
        data = {
            "ref": f"refs/heads/{new_branch}",
            "sha": base_sha
        }
        await self._post(url, data)

    async def create_commit(
        self,
        files: list[File],
        branch: str,
        from_branch: str | None = None,
        message: str = "NoIDE commit",
    ) -> str:
        branch_sha = await self._get_branch_sha(branch)
        if not branch_sha:
            await self._create_branch(branch, from_branch)
            branch_sha = await self._get_branch_sha(branch)

        # Get latest commit
        ref_data = await self._get(f"{self.api_url}/git/ref/heads/{branch}")
        base_commit_sha = ref_data["object"]["sha"]

        commit_data = await self._get(f"{self.api_url}/git/commits/{base_commit_sha}")
        base_tree_sha = commit_data["tree"]["sha"]

        # Create blobs
        blob_tasks = [
            self._post(f"{self.api_url}/git/blobs", {
                "content": file.content,
                "encoding": "utf-8"
            }) for file in files
        ]
        blob_results = await asyncio.gather(*blob_tasks)
        tree_items = [
            {"path": file.path, "mode": "100644", "type": "blob", "sha": blob["sha"]}
            for file, blob in zip(files, blob_results)
        ]

        # Create tree
        tree_data = await self._post(f"{self.api_url}/git/trees", {
            "base_tree": base_tree_sha,
            "tree": tree_items
        })
        tree_sha = tree_data["sha"]

        # Create commit
        commit = await self._post(f"{self.api_url}/git/commits", {
            "message": message,
            "tree": tree_sha,
            "parents": [base_commit_sha]
        })
        new_commit_sha = commit["sha"]

        # Update branch
        await self._patch(f"{self.api_url}/git/refs/heads/{branch}", {
            "sha": new_commit_sha,
            "force": False
        })

        return new_commit_sha

    async def create_pull_request(self, head_branch: str, base_branch: str = "master", title: str = "Automated PR") -> str:
        data = {
            "title": title,
            "head": head_branch,
            "base": base_branch,
            "body": "This pull request was created programmatically by NoIDE."
        }
        pr_data = await self._post(f"{self.api_url}/pulls", data)
        return pr_data["html_url"]

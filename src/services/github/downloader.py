import os
import shutil

import git

from . import _utils


class GitHubDownloader:

    def __init__(self, access_token: str | None = None):
        self._access_token = access_token

    def download(self, repo_fullname: str, delete_dotgit: bool = True) -> str:
        repo_path = self._get_repo_save_path(repo_fullname)
        _utils.delete_dir_if_exists(repo_path)

        repo_url = self._build_clone_url(repo_fullname)
        git.Repo.clone_from(repo_url, repo_path)

        if delete_dotgit:
            self._delete_dotgit(repo_path)

        return repo_path

    @staticmethod
    def _get_repo_save_path(repo_fullname: str, save_dir = "./saved-repositories",) -> str:
        owner, repo = repo_fullname.split("/")
        return os.path.join(save_dir, repo)

    def _build_clone_url(self, repo_fullname: str) -> str:
        if self._access_token:
            return f"https://x-access-token:{self._access_token}@github.com/{repo_fullname}.git"
        else:
            return f"https://github.com/{repo_fullname}.git"

    @staticmethod
    def _delete_dotgit(repo_path: str) -> None:
        # Remove .git directory to discard version control data
        _utils.delete_dir_if_exists(repo_path + ".git")
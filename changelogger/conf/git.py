from pathlib import Path

from git.repo import Repo


class _Git:
    KEY_URL = "url"
    GITHUB_HTTPS_PREFIX = "https://github.com/"
    GITHUB_SSH_PREFIX = "git@github.com:"
    GIT_SUFFIX = ".git"

    def __init__(self) -> None:
        self._repo = Repo(
            Path.cwd(),
        )

    def _get_git_repo(self) -> str:
        git_url = self._repo.remotes.origin.config_reader.get(
            self.KEY_URL,
        )
        return (
            git_url.lstrip(
                self.GITHUB_HTTPS_PREFIX,
            )
            .lstrip(
                self.GITHUB_SSH_PREFIX,
            )
            .rstrip(
                self.GIT_SUFFIX,
            )
        )

    def _get_first_commit(self) -> str:
        commits = list(self._repo.iter_commits())
        return commits[-1].hexsha[:10]

    def get_ctx(self) -> dict:
        return dict(
            repo=self._get_git_repo(),
            first_commit=self._get_first_commit(),
        )


get_ctx = _Git().get_ctx

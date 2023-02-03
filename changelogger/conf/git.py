from os import getcwd

from git.repo import Repo


KEY_URL = "url"
GITHUB_HTTPS_PREFIX = "https://github.com/"
GITHUB_SSH_PREFIX = "git@github.com:"
GIT_SUFFIX = ".git"


def get_git_repo() -> str:
    git_url = Repo(
        getcwd(),
    ).remotes.origin.config_reader.get(KEY_URL)
    return (
        git_url.lstrip(
            GITHUB_HTTPS_PREFIX,
        )
        .lstrip(
            GITHUB_SSH_PREFIX,
        )
        .rstrip(
            GIT_SUFFIX,
        )
    )

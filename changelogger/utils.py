from pathlib import Path
import re
from functools import cache
from typing import Generator, Pattern,  TextIO
from contextlib import contextmanager
from os import getcwd

from git.repo import Repo


KEY_URL = "url"
GITHUB_HTTPS_PREFIX = "https://github.com/"
GITHUB_SSH_PREFIX = "git@github.com:"
GIT_SUFFIX = ".git"

MODE_READ_AND_WRITE = "r+"


@cache
def cached_compile(pattern: str) -> Pattern:
    return re.compile(pattern)


@contextmanager
def open_rw(
    filename: str | Path,
) -> Generator[tuple[TextIO, str], None, None]:
    with open(filename, MODE_READ_AND_WRITE) as f:
        content = f.read()
        f.seek(0)
        yield (f, content)


def get_git_repo() -> str:
    git_url = Repo(
        getcwd(),
    ).remotes.origin.config_reader.get(KEY_URL)
    return git_url.lstrip(
        GITHUB_HTTPS_PREFIX,
    ).lstrip(
        GITHUB_SSH_PREFIX,
    ).rstrip(
        GIT_SUFFIX,
    )

import re
from functools import cache
from typing import IO, Any, Generator, Pattern
from contextlib import contextmanager
from os import getcwd

from pydantic import FilePath
from git.repo import Repo


@cache
def cached_compile(pattern: str) -> Pattern:
    return re.compile(pattern)


@contextmanager
def open_rw(filename: str | FilePath) -> Generator[tuple[IO[Any], str], None, None]:
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0)
        yield (f, content)


def get_git_repo() -> str:
    git_url = Repo(getcwd()).remotes.origin.config_reader.get("url")
    return git_url.lstrip(
        "https://github.com/",
    ).lstrip(
        "git@github.com:",
    ).rstrip(".git")

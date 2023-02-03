import re
from functools import cache
from typing import IO, Any, Generator, Pattern
from contextlib import contextmanager

from pydantic import FilePath

@cache
def cached_compile(pattern: str) -> Pattern:
    return re.compile(pattern)

@contextmanager
def open_rw(filename: str | FilePath) -> Generator[tuple[IO[Any], str], None, None]:
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0)
        yield (f, content)

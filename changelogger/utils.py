import re
from contextlib import contextmanager
from functools import cache
from pathlib import Path
from typing import Generator, Pattern, TextIO

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

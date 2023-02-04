import re
from functools import cache
from typing import Pattern

MODE_READ_AND_WRITE = "r+"


@cache
def cached_compile(pattern: str) -> Pattern:
    return re.compile(pattern)

import re
import secrets
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from changelogger.utils import MODE_READ_AND_WRITE, cached_compile, open_rw


class TestUtils:
    READ_DATA = "read data"

    @pytest.fixture
    def mock_compile(self):
        with patch.object(re, "compile") as mock:
            yield mock

    @pytest.fixture
    def mock_builtin_open(self):
        with patch(
            "builtins.open",
            mock_open(read_data=self.READ_DATA),
        ) as mock:
            yield mock

    def test_cached_compile_called_twice_same_pattern(
        self,
        mock_compile: MagicMock,
    ) -> None:
        pattern = secrets.token_hex(5)
        cached_compile(pattern)
        cached_compile(pattern)

        mock_compile.assert_called_once_with(pattern)

    def test_cached_compile_called_twice_diff_pattern(
        self,
        mock_compile: MagicMock,
    ) -> None:
        pattern1 = secrets.token_hex(5)
        pattern2 = secrets.token_hex(5)

        cached_compile(pattern1)
        cached_compile(pattern2)

        mock_compile.assert_has_calls(
            [
                call(pattern1),
                call(pattern2),
            ]
        )

    def test_open_rw(
        self,
        mock_builtin_open,
    ):
        filename = "some_file_name.txt"
        with open_rw(filename) as (f, content):
            f.read.assert_called_once_with()
            f.seek.assert_called_once_with(0)
            assert content == self.READ_DATA

        mock_builtin_open.assert_called_once_with(
            filename, MODE_READ_AND_WRITE
        )

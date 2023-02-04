import re
import secrets
from unittest.mock import MagicMock, call, patch

import pytest

from changelogger.utils import cached_compile


class TestUtils:
    READ_DATA = "read data"

    @pytest.fixture
    def mock_compile(self):
        with patch.object(re, "compile") as mock:
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

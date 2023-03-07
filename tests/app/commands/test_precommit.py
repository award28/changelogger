from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import semver

from changelogger.app.commands.precommit import precommit


class TestManageVersionsCommand:
    VERSIONS = [semver.VersionInfo(v) for v in reversed(range(100))]

    @pytest.fixture
    def mock_check(self):
        with patch("changelogger.app.commands.precommit.check") as mock:
            yield mock

    @pytest.fixture
    def mock_settings(self):
        with patch("changelogger.app.commands.precommit.settings") as mock:
            yield mock

    def test_precommit_files_not_found(
        self,
        mock_check: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        mock_file = MagicMock()
        mock_file.rel_path = Path("some_path.md")
        mock_settings.VERSIONED_FILES = [mock_file]

        files: list[str] = []

        precommit(files)
        mock_check.assert_not_called()

    def test_precommit_files_found(
        self,
        mock_check: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        mock_file = MagicMock()
        mock_file.rel_path = Path("some_path.md")
        mock_settings.VERSIONED_FILES = [mock_file]

        files = [str(mock_file.rel_path)]

        precommit(files)
        mock_check.assert_called_once_with(
            sys_exit=True,
            files=files,
        )

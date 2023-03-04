from unittest.mock import MagicMock, patch

import pytest
import semver

from changelogger.app.manage._commands.versions import versions


class TestManageVersionsCommand:
    VERSIONS = [semver.VersionInfo(v) for v in reversed(range(100))]

    @pytest.fixture
    def mock_changelog(self):
        with patch(
            "changelogger.app.manage._commands.versions.changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.manage._commands.versions.print") as mock:
            yield mock

    def test_versions(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        versions(latest=False, show_all=False, num_versions=10)
        mock_print.assert_called_once_with(
            "\n".join(map(str, self.VERSIONS[:10]))
        )

    def test_versions_latest(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_latest_version.side_effect = (self.VERSIONS[0],)
        versions(latest=True, show_all=False, num_versions=10)
        mock_print.assert_called_once_with(self.VERSIONS[0])

    def test_versions_show_all(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        versions(latest=False, show_all=True, num_versions=10)
        mock_print.assert_called_once_with("\n".join(map(str, self.VERSIONS)))

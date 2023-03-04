from unittest.mock import MagicMock, patch

import pytest
import semver

from changelogger.app.commands.versions import versions


class TestManageVersionsCommand:
    VERSIONS = [semver.VersionInfo(v) for v in reversed(range(100))]

    @pytest.fixture
    def mock_changelog(self):
        with patch("changelogger.app.commands.versions.changelog") as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.commands.versions.print") as mock:
            yield mock

    def test_versions(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        versions(latest=False, show_all=False, start=0, offset=10)
        mock_print.assert_called_once_with(
            "\n".join(map(str, self.VERSIONS[:10]))
        )

    def test_versions_latest(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_latest_version.side_effect = (self.VERSIONS[0],)
        versions(latest=True, show_all=False, start=0, offset=10)
        mock_print.assert_called_once_with(self.VERSIONS[0])

    def test_versions_show_all(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        versions(latest=False, show_all=True, start=0, offset=10)
        mock_print.assert_called_once_with("\n".join(map(str, self.VERSIONS)))

    @pytest.mark.parametrize(
        "start,offset",
        [
            (0, 100),
            (100, 100),
            (100, 1000),
            (1000, 1000),
            (2, 35),
            (70, 80),
            (80, 70),
        ],
    )
    def test_versions_start_and_offset(
        self,
        start: int,
        offset: int,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        versions(latest=False, show_all=False, start=start, offset=offset)
        mock_print.assert_called_once_with(
            "\n".join(list(map(str, self.VERSIONS))[start : start + offset])
        )

from unittest.mock import MagicMock, call, patch

import pytest
from click.exceptions import Abort

from changelogger.app.commands.notes import notes
from changelogger.models.domain_models import VersionInfo


class TestManageContentCommand:
    VERSIONS = ["0.2.0", "0.1.1", "0.1.0"]

    @pytest.fixture
    def mock_changelog(self):
        with patch("changelogger.app.commands.notes.changelog") as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.commands.notes.print") as mock:
            yield mock

    @pytest.mark.parametrize(
        "version,prev_version,pretty",
        [
            (version, prev_version, pretty)
            for version, prev_version in zip(VERSIONS, VERSIONS[1:] + [None])
            for pretty in (True, False)
        ],
    )
    def test_notes(
        self,
        version: str,
        prev_version: str,
        pretty: bool,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        expected = "MARKDOWN CONTENT"
        mock_changelog.get_all_versions.side_effect = (
            [VersionInfo.parse(v) for v in self.VERSIONS],
        )
        mock_release_notes = mock_changelog.get_release_notes()
        mock_release_notes.markdown.side_effect = (expected,)
        notes(
            version,
            pretty=pretty,
        )

        mock_changelog.get_all_versions.assert_called_once()
        mock_changelog.get_release_notes.assert_has_calls(
            [
                call(),
                call(
                    VersionInfo.parse(version),
                    (
                        VersionInfo.parse(prev_version)
                        if prev_version
                        else None
                    ),
                ),
                call().markdown(),
            ]
        )
        mock_release_notes.markdown.assert_called_once()
        assert mock_print.call_args.args
        if pretty:
            assert mock_print.call_args.args[0].markup == expected
        else:
            assert mock_print.call_args.args[0] == expected

    def test_notes_version_not_found(
        self,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        version = "0.0.0"
        with pytest.raises(Abort):
            notes(version)

        expected = f"Could not find version {version}."
        mock_print.assert_called_once_with(expected)

    @pytest.mark.parametrize(
        "pretty,markdown,expected",
        [
            (True, "", "# There are no unreleased changes."),
            (True, "notes", "notes"),
            (False, "", "There are no unreleased changes."),
            (False, "notes", "notes"),
        ],
    )
    def test_unreleased_notes(
        self,
        pretty: bool,
        markdown: str,
        expected: str,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        topmost_version = "0.1.1"
        mock_changelog.get_all_versions.side_effect = (
            [topmost_version, "0.2.0", "0.1.0"],
        )
        mock_release_notes = mock_changelog.get_release_notes()
        mock_release_notes.markdown.side_effect = (markdown,)
        notes("unreleased", pretty=pretty)

        mock_changelog.get_all_versions.assert_called_once()
        mock_changelog.get_release_notes.assert_has_calls(
            [
                call(),
                call("Unreleased", topmost_version),
                call().markdown(),
            ]
        )
        mock_release_notes.markdown.assert_called_once()
        assert mock_print.call_args.args
        if pretty:
            assert mock_print.call_args.args[0].markup == expected
        else:
            assert mock_print.call_args.args[0] == expected

from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from changelogger.app.commands.check import (
    _check_changelog,
    _check_versioned_file,
    check,
)
from changelogger.exceptions import ValidationException
from changelogger.models.domain_models import ReleaseNotes


class TestManageCheckCommand:
    @pytest.fixture
    def mock_check_changelog(self):
        with patch("changelogger.app.commands.check._check_changelog") as mock:
            yield mock

    @pytest.fixture
    def mock_check_versioned_files(self):
        with patch(
            "changelogger.app.commands.check._check_versioned_files"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_changelog(self):
        with patch("changelogger.app.commands.check.changelog") as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.commands.check.print") as mock:
            yield mock

    @pytest.fixture
    def mock_cached_compile(self):
        with patch("changelogger.app.commands.check.cached_compile") as mock:
            yield mock

    @pytest.fixture
    def mock_templating(self):
        with patch("changelogger.app.commands.check.templating") as mock:
            yield mock

    @pytest.fixture
    def mock_settings(self):
        with patch("changelogger.app.commands.check.settings") as mock:
            yield mock

    @pytest.fixture
    def mock_versioned_files(self, mock_settings: MagicMock):
        mock_versioned_file = MagicMock()
        mock_versioned_file.rel_path = mock_settings.CHANGELOG_PATH
        mock_settings.VERSIONED_FILES = [mock_versioned_file]

    def test_check_changelog_no_errors(
        self,
        mock_check_versioned_files: MagicMock,
        mock_versioned_files: MagicMock,
        mock_check_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        check(files=[])
        mock_check_changelog.assert_called_once_with()
        mock_print.assert_called_once()
        assert "Versioned files are valid!" in mock_print.call_args.args[0]

    def test_check_changelog_with_errors(
        self,
        mock_check_versioned_files: MagicMock,
        mock_versioned_files: MagicMock,
        mock_check_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        exc_note = "Some validation exception"
        mock_check_changelog.side_effect = ValidationException(exc_note)
        check(sys_exit=False, files=[])
        mock_print.assert_called_once()
        assert exc_note in mock_print.call_args.args[0]

    def test_check_changelog_with_error_and_exit(
        self,
        mock_check_versioned_files: MagicMock,
        mock_versioned_files: MagicMock,
        mock_check_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        exc_note = "Some validation exception"
        mock_check_changelog.side_effect = ValidationException(exc_note)

        with pytest.raises(Exit):
            check(sys_exit=True, files=[])

        mock_print.assert_called_once()
        assert exc_note in mock_print.call_args.args[0]

    def test_check_versioned_file(
        self,
        mock_templating: MagicMock,
        mock_cached_compile: MagicMock,
    ) -> None:
        mock_search = mock_cached_compile().search
        mock_search.side_effect = (None,)

        with pytest.raises(ValidationException):
            _check_versioned_file(
                MagicMock(),
                MagicMock(),
            )

    @pytest.mark.parametrize(
        "point_of_failure,exc_note",
        enumerate(
            [
                "Expected there to be at least 1 version; None found.",
                "Failed to validate notes for version",
                "Could not find the link for version",
                "Link is incorrect for version",
                "Could not find the link for unreleased changes.",
                "Link is incorrect for the unreleased changes.",
                "Could not find the link for version",
            ]
        ),
    )
    def test_check_changelog_point_of_failure(
        self,
        point_of_failure: int,
        exc_note: str,
        mock_changelog: MagicMock,
    ):
        validation_stepper(mock_changelog, point_of_failure)
        with pytest.raises(ValidationException) as exc_info:
            _check_changelog()

        assert exc_note in exc_info.value.args[0]

    def test_check_changelog_valid(
        self,
        mock_changelog: MagicMock,
    ):
        validation_stepper(mock_changelog, 7)
        _check_changelog()


def validation_stepper(mock_changelog: MagicMock, pof: int):
    # Point of Failure 0
    if pof < 1:
        mock_changelog.get_all_versions.side_effect = ([],)
        return

    versions = ["0.2.0", "0.1.0"]
    mock_changelog.get_all_versions.side_effect = (versions,)

    # Point of Failure 1
    if pof < 2:
        mock_changelog.get_release_notes.side_effect = Exception()
        return

    release_notes = ReleaseNotes(added=["added something"])
    mock_changelog.get_release_notes.side_effect = lambda *_: release_notes

    sorted_versions = sorted(versions)
    mock_changelog.get_sorted_versions.side_effect = (sorted_versions,)

    # Point of Failure 2
    if pof < 3:
        mock_changelog.get_all_links.side_effect = (dict(),)
        return

    # Point of Failure 3
    if pof < 4:
        all_links = {
            version: f"https://example.com/" for version in sorted_versions
        }
        mock_changelog.get_all_links.side_effect = (all_links,)

        return

    all_links = {
        version: f"https://example.com/{old_version}...{version}"
        for old_version, version in zip(sorted_versions, sorted_versions[1:])
    }

    # Point of Failure 4
    if pof < 5:
        mock_changelog.get_all_links.side_effect = (all_links,)
        return

    all_links["Unreleased"] = "https://example.com/"

    # Point of Failure 5
    if pof < 6:
        mock_changelog.get_all_links.side_effect = (all_links,)
        return

    all_links["Unreleased"] = f"https://example.com/{versions[0]}...HEAD"

    # Point of Failure 6
    if pof < 7:
        mock_changelog.get_all_links.side_effect = (all_links,)
        return

    # No point of failure (7+)
    all_links[sorted_versions[0]] = "https://example.com/commit/abc123"
    mock_changelog.get_all_links.side_effect = (all_links,)

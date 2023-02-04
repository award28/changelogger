from unittest.mock import MagicMock, call, patch

import pytest

from changelogger.app.manage.commands.content import content
from changelogger.exceptions import CommandException


class TestUnreleasedContent:
    VERSIONS = ["0.1.1", "0.2.0", "0.1.0"]

    @pytest.fixture
    def mock_changelog(self):
        with patch(
            "changelogger.app.manage.commands.content.changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.manage.commands.content.print") as mock:
            yield mock

    @pytest.mark.parametrize(
        "version,prev_version,pretty",
        [
            (version, prev_version, pretty)
            for version, prev_version in zip(
                VERSIONS, VERSIONS[1:] + ["LINKS"]
            )
            for pretty in (True, False)
        ]
        # [
        #     (True, "", "# There are no unreleased changes."),
        #     (True, "content", "content"),
        #     (False, "", "There are no unreleased changes."),
        #     (False, "content", "content"),
        # ],
    )
    def test_content(
        self,
        version: str,
        prev_version: str,
        pretty: bool,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
    ) -> None:
        expected = "MARKDOWN CONTENT"
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        mock_release_notes = mock_changelog.get_release_notes()
        mock_release_notes.markdown.side_effect = (expected,)
        content(
            version,
            pretty=pretty,
        )

        mock_changelog.get_all_versions.assert_called_once()
        mock_changelog.get_release_notes.assert_has_calls(
            [
                call(),
                call(version, prev_version),
                call().markdown(),
            ]
        )
        mock_release_notes.markdown.assert_called_once()
        assert mock_print.call_args.args
        if pretty:
            assert mock_print.call_args.args[0].markup == expected
        else:
            assert mock_print.call_args.args[0] == expected

    def test_content_version_not_found(
        self,
        mock_changelog,
    ) -> None:
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        version = "VERSION_DNE"
        with pytest.raises(CommandException) as excinfo:
            content(version)

        expected = f"Could not find version {version}."
        assert excinfo.value.args[0] == expected

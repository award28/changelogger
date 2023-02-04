from unittest.mock import MagicMock, call, patch

import pytest

from changelogger.app.unreleased.commands.content import content


class TestUnreleasedContent:
    @pytest.fixture
    def mock_changelog(self):
        with patch(
            "changelogger.app.unreleased.commands.content.changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch(
            "changelogger.app.unreleased.commands.content.print"
        ) as mock:
            yield mock

    @pytest.mark.parametrize(
        "pretty,markdown,expected",
        [
            (True, "", "# There are no unreleased changes."),
            (True, "content", "content"),
            (False, "", "There are no unreleased changes."),
            (False, "content", "content"),
        ],
    )
    def test_content(
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
        content(pretty=pretty)

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

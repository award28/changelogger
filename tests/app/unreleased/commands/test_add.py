from unittest.mock import MagicMock, patch

import pytest

from changelogger.app.unreleased.commands.add import add


class TestUnreleasedAddCommand:
    VERSIONS = ["0.1.1", "0.2.0", "0.1.0"]

    EMPTY_OPTIONS: list[list[str]] = [[]] * 6
    ALL_OPTIONS = dict(
        added=["something"],
        changed=[],
        deprecated=[],
        removed=[],
        fixed=[],
        security=[],
    )
    SINGLE_OPTION = dict(
        added=["something"],
        changed=["something"],
        deprecated=["something"],
        removed=["something"],
        fixed=["something"],
        security=["something"],
    )

    @pytest.fixture
    def mock_changelog(self):
        with patch(
            "changelogger.app.unreleased.commands.add.changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_prompt_unreleased_changelog(self):
        with patch(
            "changelogger.app.unreleased.commands.add.prompt_unreleased_changelog"
        ) as mock:
            yield mock

    def test_add_prompts_on_no_options(
        self,
        mock_changelog: MagicMock,
        mock_prompt_unreleased_changelog: MagicMock,
    ):
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        mock_prompt_unreleased_changelog.side_effect = lambda x: x
        add(*self.EMPTY_OPTIONS)
        mock_changelog.get_all_versions.assert_called_once()
        mock_changelog.get_release_notes.assert_called()
        mock_prompt_unreleased_changelog.assert_called_once()

    @pytest.mark.parametrize(
        "options",
        [ALL_OPTIONS, SINGLE_OPTION],
    )
    def test_add_no_prompts_on_options(
        self,
        options,
        mock_changelog: MagicMock,
        mock_prompt_unreleased_changelog: MagicMock,
    ):
        mock_changelog.get_all_versions.side_effect = (self.VERSIONS,)
        mock_prompt_unreleased_changelog.side_effect = lambda x: x
        add(**options)
        mock_prompt_unreleased_changelog.assert_not_called()

        mock_changelog.update_versioned_files.assert_called_once()
        assert (
            "update" in mock_changelog.update_versioned_files.call_args.kwargs
        )
        actual_update = mock_changelog.update_versioned_files.call_args.kwargs[
            "update"
        ]
        for option, expected in options.items():
            assert actual_update.release_notes[option] == expected

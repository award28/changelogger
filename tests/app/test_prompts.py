from unittest.mock import MagicMock, patch

import pytest

from changelogger.app import prompts
from changelogger.exceptions import RollbackException, UpgradeException
from changelogger.models.domain_models import ChangelogUpdate, ReleaseNotes


class TestPrompts:
    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.prompts.print") as mock:
            yield mock

    @pytest.fixture
    def mock_input(self):
        with patch("builtins.input") as mock:
            yield mock

    def test_prompt_unreleased_changelog_no_additions(
        self,
        mock_print,
        mock_input,
    ):
        mock_input.side_effect = lambda _: ""
        update = ChangelogUpdate(
            new_version="0.2.0",
            old_version="0.1.0",
            release_notes=ReleaseNotes(),
        )
        actual = prompts.prompt_unreleased_changelog(update)
        assert update == actual
        assert not actual.release_notes

    def test_prompt_unreleased_changelog_with_added(
        self,
        mock_print,
        mock_input,
    ):
        added = "Some note"
        mock_input.side_effect = [
            added,
        ] + [""] * 6
        update = ChangelogUpdate(
            new_version="0.2.0",
            old_version="0.1.0",
            release_notes=ReleaseNotes(),
        )
        actual = prompts.prompt_unreleased_changelog(update)
        assert update == actual
        assert actual.release_notes
        assert added in actual.release_notes.added

    def test_rollback_handler_upgrade_exc(
        self,
        mock_print: MagicMock,
    ):
        exc_arg = "Some upgrade exception"
        try:
            with prompts.rollback_handler():
                raise UpgradeException(exc_arg)
        finally:
            mock_print.assert_called_once_with(
                f"[bold red]Failed to update.[/bold red] {exc_arg}"
            )

    def test_rollback_handler_rollback_exc(
        self,
        mock_print: MagicMock,
    ):
        exc_arg = "Some rollback exception"
        try:
            with prompts.rollback_handler():
                raise RollbackException(exc_arg)
        finally:
            assert len(mock_print.call_args_list) == 2

            first_call = mock_print.call_args_list[0].args
            assert first_call
            assert exc_arg in first_call[0]

            second_call = mock_print.call_args_list[1].args
            assert second_call
            assert "MANUAL INTERVENTION REQUIRED" in second_call[0]

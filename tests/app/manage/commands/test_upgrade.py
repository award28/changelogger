from unittest.mock import MagicMock, patch

import pytest

from changelogger.app.manage.commands.upgrade import upgrade
from changelogger.models.domain_models import (
    ChangelogUpdate,
    ReleaseNotes,
    SemVerType,
)


class TestManageUpgradeCommand:
    VERSIONS = ["0.1.1", "0.2.0", "0.1.0"]

    @pytest.fixture
    def mock_changelog(self):
        with patch(
            "changelogger.app.manage.commands.upgrade.changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch("changelogger.app.manage.commands.upgrade.print") as mock:
            yield mock

    @pytest.fixture
    def mock_prompt_unreleased_changelog(self):
        with patch(
            "changelogger.app.manage.commands.upgrade.prompt_unreleased_changelog"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_typer(self):
        with patch("changelogger.app.manage.commands.upgrade.typer") as mock:
            yield mock

    @pytest.mark.parametrize(
        "new_version,version_to_bump,prompt_changelog,confirm,markdown",
        [
            (new_version, version_to_bump, prompt_changelog, confirm, markdown)
            for new_version, version_to_bump in zip(
                ["1.0.0", "0.2.0", "0.1.1"],
                list(SemVerType),
            )
            for prompt_changelog in (True, False)
            for confirm in (True, False)
            for markdown in ("", "content")
        ],
    )
    def test_upgrade(
        self,
        new_version: str,
        version_to_bump: SemVerType,
        prompt_changelog: bool,
        confirm: bool,
        markdown: str,
        mock_changelog: MagicMock,
        mock_print: MagicMock,
        mock_typer: MagicMock,
        mock_prompt_unreleased_changelog: MagicMock,
    ):
        release_notes = ReleaseNotes(
            added=[markdown] if markdown else [],
        )
        expected_update = ChangelogUpdate(
            old_version="0.1.0",
            new_version=new_version,
            release_notes=release_notes,
        )

        mock_changelog.get_latest_version.side_effect = (
            expected_update.old_version,
        )
        mock_changelog.get_release_notes.side_effect = (release_notes,)
        mock_prompt_unreleased_changelog.side_effect = lambda x: x
        mock_typer.confirm.side_effect = (True,)

        upgrade(
            version_to_bump,
            prompt_changelog=prompt_changelog,
            confirm=confirm,
        )

        if prompt_changelog:
            mock_prompt_unreleased_changelog.assert_called_with(
                expected_update
            )

        if confirm:
            mock_typer.confirm.assert_called()

        assert mock_print.call_args.args
        markup = mock_print.call_args.args[0].markup
        markdown = markdown or "No notes found or added"
        assert markdown in markup

        mock_changelog.update_versioned_files.assert_called()

from unittest.mock import MagicMock, patch

import pytest

from changelogger.app.commands import init as init_cmd


class TestInitCommand:
    @pytest.fixture
    def mock_render_jinja(self):
        with patch("changelogger.app.commands.init.render_jinja") as mock:
            yield mock

    @pytest.fixture
    def mock_typer(self):
        with patch("changelogger.app.commands.init.typer") as mock:
            yield mock

    @pytest.fixture
    def mock_settings(self):
        with patch("changelogger.app.commands.init.settings") as mock:
            yield mock

    @pytest.fixture
    def mock_init_changelog(self):
        with patch("changelogger.app.commands.init._init_changelog") as mock:
            yield mock

    @pytest.fixture
    def mock_init_changelogger(self):
        with patch(
            "changelogger.app.commands.init._init_changelogger"
        ) as mock:
            yield mock

    @pytest.mark.parametrize(
        "prompt_changelog,prompt_versioned_files",
        [(bool(i), bool(j)) for i in range(2) for j in range(2)],
    )
    def test_init_entrypoint(
        self,
        prompt_changelog: bool,
        prompt_versioned_files: bool,
        mock_init_changelog: MagicMock,
        mock_init_changelogger: MagicMock,
    ) -> None:
        init_cmd.init(
            prompt_changelog=prompt_changelog,
            prompt_versioned_files=prompt_versioned_files,
        )

        if prompt_changelog:
            mock_init_changelog.assert_called_once()
        else:
            mock_init_changelog.assert_not_called()

        if prompt_versioned_files:
            mock_init_changelogger.assert_called_once()
        else:
            mock_init_changelogger.assert_not_called()

    def test_init_changelog(
        self,
        mock_typer,
        mock_settings,
        mock_render_jinja,
    ) -> None:
        ...
        mock_console = MagicMock()
        init_cmd._init_changelog(mock_console)
        mock_render_jinja.assert_called_once()

    @pytest.mark.parametrize(
        "changelog_exists,expected_substr",
        [
            (True, "looks like you've already"),
            (False, "Would you like to generate"),
        ],
    )
    def test_init_changelog_cancelled(
        self,
        changelog_exists: bool,
        expected_substr: str,
        mock_typer: MagicMock,
        mock_settings: MagicMock,
        mock_render_jinja: MagicMock,
    ) -> None:
        mock_settings.CHANGELOG_PATH.exists.side_effect = (changelog_exists,)
        mock_typer.confirm.side_effect = (False,)
        mock_console = MagicMock()
        init_cmd._init_changelog(mock_console)

        assert expected_substr in mock_typer.confirm.call_args.args[0]
        mock_render_jinja.assert_not_called()

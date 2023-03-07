from functools import partial, wraps
from pathlib import Path
from typing import Callable

import typer
from git.exc import InvalidGitRepositoryError
from git.repo import Repo
from rich import print

from changelogger.app.commands.add import add
from changelogger.app.commands.check import check
from changelogger.app.commands.init import init
from changelogger.app.commands.notes import notes
from changelogger.app.commands.precommit import precommit
from changelogger.app.commands.upgrade import upgrade
from changelogger.app.commands.versions import versions
from changelogger.conf import settings


class App(typer.Typer):
    def add_command(
        self,
        cmd: Callable,
        alias: str | None = None,
        **extra,
    ) -> None:
        """Adds the provided callable as command on this App instance.
        If an alias is provided, the command can be invoked with that
        name as well.
        """
        self.command(**extra)(cmd)

        if not alias:
            return

        alias_cmd = wraps(cmd)(partial(cmd))
        alias_cmd.__doc__ = (
            f"Alias for the `{cmd.__name__}` command. {cmd.__doc__}"
        )

        # Alias commands
        self.command(alias, rich_help_panel="Aliases", **extra)(alias_cmd)


app = App()

app.add_command(add)
app.add_command(check, "ch")
app.add_command(init)
app.add_command(notes)
app.add_command(upgrade, "up")
app.add_command(versions)
app.add_command(precommit, hidden=True)


def version_callback(value: bool):
    if not value:
        return

    print(settings.CHANGELOGGER_VERSION)
    raise typer.Exit()


@app.callback()
def changelogger(
    ctx: typer.Context,
    _: bool = typer.Option(
        False,
        "-v",
        "--version",
        help="The version of Changelogger you have installed.",
        callback=version_callback,
    ),
):
    if (
        not ctx.invoked_subcommand == init.__name__
        and not settings.CHANGELOG_PATH.exists()
    ):
        print(
            "[bold red]Error: [/bold red]"
            f"Could not find changelog file [bold]{settings.CHANGELOG_PATH}[/bold]."
        )
        raise typer.Abort()

    if settings.HAS_DEFAULTS:
        try:
            __ = Repo(Path.cwd()).git_dir
        except InvalidGitRepositoryError:
            print(
                "[bold red]Error: [/bold red]"
                "Must be in a git repo to use the default behavior."
            )
            raise typer.Abort()


changelogger.__doc__ = f"""
Automated management of your changelog and other versioned files, following the
principles of Keep a Changelog and Semantic Versioning.\n
version: {settings.CHANGELOGGER_VERSION}
"""
changelogger.__doc__ += "\nIN DEBUG MODE" if settings.DEBUG else ""

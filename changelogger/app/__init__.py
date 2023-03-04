from pathlib import Path

import typer
from git.exc import InvalidGitRepositoryError
from git.repo import Repo
from rich import print

from changelogger.app._commands.init import init
from changelogger.app.manage import app as manage_app
from changelogger.app.manage._commands.check import check
from changelogger.app.manage._commands.content import content
from changelogger.app.manage._commands.upgrade import upgrade
from changelogger.app.manage._commands.versions import versions
from changelogger.app.unreleased import app as unrealeased_app
from changelogger.conf import settings

app = typer.Typer()

# TODO: Remove this in version 0.12.0
app.add_typer(manage_app)
app.add_typer(unrealeased_app)


# Initialization Commands
app.command()(init)


# Management Commands
app.command()(upgrade)
app.command()(check)
app.command()(content)
app.command()(versions)


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
{settings.CHANGELOGGER_DESCRIPTION}\n
version: {settings.CHANGELOGGER_VERSION}
"""
changelogger.__doc__ += "\nIN DEBUG MODE" if settings.DEBUG else ""

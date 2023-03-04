from pathlib import Path

import typer
from git.exc import InvalidGitRepositoryError
from git.repo import Repo
from rich import print

from changelogger.app._commands.init import init
from changelogger.app.manage import app as manage_app
from changelogger.app.unreleased import app as unrealeased_app
from changelogger.conf import settings

app = typer.Typer()
app.add_typer(manage_app)
app.add_typer(unrealeased_app)

app.command()(init)


def version_callback(value: bool):
    if value:
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

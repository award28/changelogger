from os import getcwd

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


@app.callback()
def changelogger(ctx: typer.Context):
    """Automated management of your CHANGELOG.md and other versioned files,
    following the principles of Keep a Changelog and Semantic Versioning."""
    if (
        not ctx.invoked_subcommand == init.__name__
        and settings.CHANGELOG_PATH.exists()
    ):
        print(
            "[bold red]Error: [/bold red]"
            f"Could not find changelog file [bold]{settings.CHANGELOG_PATH}[/bold]."
        )
        exit(1)

    if settings.HAS_DEFAULTS:
        try:
            _ = Repo(getcwd()).git_dir
        except InvalidGitRepositoryError:
            print(
                "[bold red]Error: [/bold red]"
                "Must be in a git repo to use the default behavior."
            )
            exit(1)

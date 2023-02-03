from os import getcwd

import typer
from git.exc import InvalidGitRepositoryError
from git.repo import Repo
from rich import print

from changelogger.app.manage import app as manage_app
from changelogger.app.unreleased import app as unrealeased_app
from changelogger.conf import settings

app = typer.Typer()
app.add_typer(manage_app)
app.add_typer(unrealeased_app)


@app.callback()
def changelogger():
    """Changelogger app help goes here."""
    if not settings.CHANGELOG_PATH.exists():
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

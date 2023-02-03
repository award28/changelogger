from os import getcwd
import typer
from rich import print

from git.repo import Repo
from git.exc import InvalidGitRepositoryError

from changelogger.app.manage import app as manage_app
from changelogger import settings


app = typer.Typer()
app.add_typer(manage_app)

@app.callback()
def changelogger():
    """Changelogger app help goes here.
    """
    if not settings.CHANGELOG_FILE.exists():
        print(
            "[bold red]Error: [/bold red]"
            f"Could not find changelog file [bold]{settings.CHANGELOG_FILE}[/bold]."
        )
        exit(1)

    if settings.DEFAULT_BEHAVIOR:
        try:
            _ = Repo(getcwd()).git_dir
        except InvalidGitRepositoryError:
            print(
                "[bold red]Error: [/bold red]"
                "Must be in a git repo to use the default behavior."
            )
            exit(1)

from os import getcwd
import typer
from rich import print

import git

from .apps.manage import app as manage_app
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
            _ = git.Repo(getcwd()).git_dir
        except git.exc.InvalidGitRepositoryError:
            print(
                "[bold red]Error: [/bold red]"
                "Must be in a git repo to use the default behavior."
            )
            exit(1)



# @app.command()
# def upgrade(
#     version_to_bump: SemVerType,
#     confirm: bool = True,
#     prompt_changelog: bool = True,
#     use_standard_upgrade_config: bool = True,
#     version_upgrade_config: str = '.version_upgrade_config.yml',
#     changelog_file: str = 'CHANGELOG.md',
# ) -> None:
#     """This command will bump the provided version_to_bump for all of the
#     required files. This command expects there to be a CHANGELOG.md file at the
#     top level. Any additional files can be added to the configuration yaml.
# 
#     Importantly, this script parses the changelog.md's unreleased changes, and
#     properly incorporates these changes inthe bumped versions changelog.md
#     section and any other specified changelog files in the configuration file.
#     The script will further prompt the user for any additional changelog changes,
#     according to the
#     [Keep a changelog: How do I make a good changelog?](https://keepachangelog.com/en/1.0.0/#how)
#     section.
#     """
#     try:
#         Changelogger(
#             changelog_file,
#             use_standard_upgrade_config,
#         ).upgrade(
#             version_to_bump,
#             confirm,
#             prompt_changelog,
#             version_upgrade_config,
#         )
#     except CommandException as e:
#         print(f"\n:boom:\n{str(e)}\n[bold red]Aborted![/bold red]")
#         raise
# 
# 
# @app.command()
# def validate(
#     changelog_file: str = 'CHANGELOG.md',
#     exit_: bool = True,
# ) -> None:
#     try:
#         Changelogger(changelog_file).validate()
#     except ValidationException as e:
#         print(str(e))
#         if exit_:
#             exit(1)
# 
# 
# @app.command()
# def content(
#     version: str,
#     pretty: bool = True,
#     changelog_file: str = 'CHANGELOG.md',
# ) -> None:
#     try:
#         Changelogger(changelog_file).content_for_version(version, pretty=pretty)
#     except CommandException as e:
#         print(f"[bold red]Error[/bold red]: {str(e)}")

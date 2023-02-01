import typer
from rich import print

from .commands.exceptions import (
    CommandException,
    ValidationException,
)
from .commands.domain_models import SemVerType
from .commands.changelogger import Changelogger


app = typer.Typer()


@app.command()
def upgrade(
    version_to_bump: SemVerType,
    confirm: bool = True,
    prompt_changelog: bool = True,
    use_standard_upgrade_config: bool = True,
    version_upgrade_config: str | None = None,
    changelog_file: str = 'CHANGELOG.md',
) -> None:
    """This command will bump the provided version_to_bump for all of the
    required files. This command expects there to be a CHANGELOG.md file at the
    top level. Any additional files can be added to the configuration yaml.

    Importantly, this script parses the changelog.md's unreleased changes, and
    properly incorporates these changes inthe bumped versions changelog.md
    section and any other specified changelog files in the configuration file.
    The script will further prompt the user for any additional changelog changes,
    according to the
    [Keep a changelog: How do I make a good changelog?](https://keepachangelog.com/en/1.0.0/#how)
    section.
    """
    try:
        Changelogger(
            changelog_file,
            use_standard_upgrade_config,
        ).upgrade(
            version_to_bump,
            confirm,
            prompt_changelog,
            version_upgrade_config,
        )
    except CommandException as e:
        print(f"\n:boom:\n{str(e)}\n[bold red]Aborted![/bold red]")
        raise


@app.command()
def validate(
    changelog_file: str = 'CHANGELOG.md',
    exit_: bool = True,
) -> None:
    try:
        Changelogger(changelog_file).validate()
    except ValidationException as e:
        print(str(e))
        if exit_:
            exit(1)


@app.command()
def content(
    version: str,
    pretty: bool = True,
    changelog_file: str = 'CHANGELOG.md',
) -> None:
    try:
        Changelogger(changelog_file).content_for_version(version, pretty=pretty)
    except CommandException as e:
        print(f"[bold red]Error[/bold red]: {str(e)}")

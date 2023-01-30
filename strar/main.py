import typer

from .commands.exceptions import UpgradeException
from .commands.domain_models import SemVerType
from .commands.cmd import upgrade as upgrade_cmd
from .commands.cmd import validate as validate_cmd
from .commands.cmd import changelog_content

app = typer.Typer()

@app.command()
def upgrade(
    version_to_bump: SemVerType,
    confirm: bool = True,
    prompt_changelog: bool = True,
    version_upgrade_config: str = '.version_upgrade_config.yml',
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
        upgrade_cmd(version_to_bump, confirm, prompt_changelog, version_upgrade_config)
    except UpgradeException as e:
        print(f"\n:boom:\n{str(e)}\n[bold red]Aborted![/bold red]")

changelog_app = typer.Typer()
app.add_typer(changelog_app, name="changelog")

@changelog_app.command()
def validate(exit: bool = True) -> None:
    try:
        validate_cmd()
    except Exception as e:
        print(str(e))
        if exit:
            raise


@changelog_app.command()
def content(version: str) -> None:
    try:
        changelog_content(version)
    except Exception as e:
        print(str(e))
        if exit:
            raise

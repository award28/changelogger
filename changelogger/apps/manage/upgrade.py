import typer
import semver

from rich import print
from rich.markdown import Markdown

from changelogger.management import changelog
from changelogger.models.config import ChangeloggerConfig
from changelogger.models.domain_models import ChangelogUpdate, SemVerType


def upgrade(
    version_to_bump: SemVerType,
    confirm: bool = typer.Option(
        True,
        help="Confirm the release notes before applying them.",
    ),
    prompt_changelog: bool =  typer.Option(
        True,
        help="Prompt for additional release notes before applying them.",
    ),
) -> None:
    """Upgrades all versioned files, as specified in the changelogger config file.
    """
    old_version = changelog.get_latest_version()
    bump = getattr(semver, f"bump_{version_to_bump.value}")
    new_version = bump(old_version)
    print(new_version)

    release_notes = changelog.get_release_notes("Unreleased", old_version)
    update = ChangelogUpdate(
        old_version=old_version,
        new_version=new_version,
        release_notes=release_notes,
    )

    if prompt_changelog:
        update = _prompt_unreleased_changelog(update)

    print(f"Upgrading {old_version} ==> {new_version}")
    md = f"\n# Changelog updates for [{new_version}]\n"
    if (update_md := update.release_notes.markdown()):
        md += update_md
    else:
        md += "\n*No notes found or added*"

    md += "\n---\n"
    print(Markdown(md))

    if confirm:
        typer.confirm("Do these changes look correct?", abort=True)

    config = ChangeloggerConfig.from_settings()
    changelog.update_versioned_files(config, update)

def _prompt_unreleased_changelog(update: ChangelogUpdate) -> ChangelogUpdate:
    for name, notes in update.release_notes.dict().items():
        done = False
        print(Markdown(f"## Updating **{name.title()}**"))
        while not done:
            print(
                f"Any further additions for [bold]{name.title()}[/bold]?"
            )
            print(notes)
            if (new_note := input("New note [Enter to continue]: ")):
                notes.append(new_note)
            else:
                done = True
        update.release_notes[name] = notes
    return update

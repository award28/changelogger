import typer
from rich import print
from rich.markdown import Markdown

from changelogger import changelog
from changelogger.app.prompts import (
    prompt_unreleased_changelog,
    rollback_handler,
)
from changelogger.conf import settings
from changelogger.models.domain_models import ChangelogUpdate, VersionInfo


def force(
    forced_version: str,
    confirm: bool = typer.Option(
        True,
        help="Confirm the release notes before applying them.",
    ),
    prompt_changelog: bool = typer.Option(
        True,
        help="Prompt for additional release notes before applying them.",
    ),
) -> None:
    """Force a version override for the upgrade."""
    old_version = changelog.get_latest_version()
    new_version = VersionInfo.parse(forced_version)

    release_notes = changelog.get_release_notes("Unreleased", old_version)
    update = ChangelogUpdate(
        old_version=old_version,
        new_version=new_version,
        release_notes=release_notes,
    )

    if prompt_changelog:
        update = prompt_unreleased_changelog(update)

    print(f"Upgrading {old_version} ==> {new_version}")
    md = f"\n# Changelog updates for [{new_version}]\n"
    if update_md := update.release_notes.markdown():
        md += update_md
    else:
        md += "\n*No notes found or added*"

    md += "\n---\n"
    print(Markdown(md))

    if confirm:
        typer.confirm("Do these changes look correct?", abort=True)

    with rollback_handler():
        changelog.update_versioned_files(
            update,
            settings.VERSIONED_FILES,
        )

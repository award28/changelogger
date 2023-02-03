import typer
from rich import print
from changelogger import changelog
from changelogger.conf import settings
from changelogger.conf.models import VersionedFile
from changelogger.models.domain_models import ChangelogUpdate

ADDED_HELP = "For new features."
CHANGED_HELP = "For changes in existing functionality."
DEPRECATED_HELP = "For soon-to-be removed features."
REMOVED_HELP = "For now removed features."
FIXED_HELP = "For any bug fixes."
SECURITY_HELP = "In case of vulnerabilities."

def add(
    added: list[str] = typer.Option([], help=ADDED_HELP),
    changed: list[str] = typer.Option([], help=CHANGED_HELP),
    deprecated: list[str] = typer.Option([], help=DEPRECATED_HELP),
    removed: list[str] = typer.Option([], help=REMOVED_HELP),
    fixed: list[str] = typer.Option([], help=FIXED_HELP),
    security: list[str] = typer.Option([], help=SECURITY_HELP),
) -> None:
    """Retrieves the changelog content for the specified version.
    """
    if not (added or changed or deprecated or removed or fixed or security):
        print("No changes to apply.")
        raise typer.Abort()

    all_versions = changelog.get_all_versions()
    topmost_version = all_versions[0]
    release_notes = changelog.get_release_notes("Unreleased", topmost_version)

    # Update the existing unreleased changes with the added notes
    release_notes.added.extend(added)
    release_notes.changed.extend(changed)
    release_notes.deprecated.extend(deprecated)
    release_notes.removed.extend(removed)
    release_notes.fixed.extend(fixed)
    release_notes.security.extend(security)

    update = ChangelogUpdate(
        new_version="",
        old_version=topmost_version,
        release_notes=release_notes,
    )

    chnagelog_file = VersionedFile(
        rel_path=settings.CHANGELOG_PATH,
        pattern=settings.OVERVIEW_JINJA_PATTERN,
        jinja_rel_path=settings.OVERVIEW_JINJA_PATH,
    )

    changelog.update_versioned_files(
        update=update,
        versioned_files=[chnagelog_file],
    )

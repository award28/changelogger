import typer

from changelogger import changelog
from changelogger.app.prompts import (
    prompt_unreleased_changelog,
    rollback_handler,
)
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
    """Add changes to the unreleased section of your changelog file. If no
    options are provided, you will be prompted for changes.
    """
    all_versions = changelog.get_all_versions()
    old_version = all_versions[0]
    release_notes = changelog.get_release_notes("Unreleased", old_version)

    update = ChangelogUpdate(
        new_version=None,
        old_version=old_version,
        release_notes=release_notes,
    )

    if added or changed or deprecated or removed or fixed or security:
        # Update the existing unreleased changes with the added notes
        update.release_notes.added.extend(added)
        update.release_notes.changed.extend(changed)
        update.release_notes.deprecated.extend(deprecated)
        update.release_notes.removed.extend(removed)
        update.release_notes.fixed.extend(fixed)
        update.release_notes.security.extend(security)
    else:
        update = prompt_unreleased_changelog(update)

    changelog_file = VersionedFile(
        rel_path=settings.CHANGELOG_PATH,
        pattern=settings.OVERVIEW_JINJA_PATTERN,
        template=settings.OVERVIEW_TEMPLATE,
    )

    with rollback_handler():
        changelog.update_versioned_files(
            update=update,
            versioned_files=[changelog_file],
        )

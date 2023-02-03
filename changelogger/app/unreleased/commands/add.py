import typer
from rich import print
from rich.markdown import Markdown
from changelogger.exceptions import CommandException
from changelogger import changelog

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
    all_versions = changelog.get_all_versions()

    # all_versions[0] is the topmost version in the changelog file.
    release_notes = changelog.get_release_notes("Unreleased", all_versions[0])

    # Update the existing unreleased changes with the added notes
    release_notes.added.extend(added)
    release_notes.changed.extend(changed)
    release_notes.deprecated.extend(deprecated)
    release_notes.removed.extend(removed)
    release_notes.fixed.extend(fixed)
    release_notes.security.extend(security)

    print(Markdown(release_notes.markdown()))

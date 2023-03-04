import typer
from rich import print
from rich.markdown import Markdown

from changelogger import changelog
from changelogger.models.domain_models import ReleaseNotes, VersionInfo

VERSION_HELP = """
The version notes you would like to retrieve.

\b
\nAdditionally, you use these shortcuts.
\nlatest: Retrieves the latest versions notes.
\nunreleased: Retrieves any unreleased notes. This is the default behaviour
if no value is provided.

"""


def notes(
    version: str = typer.Argument(
        "unreleased",
        help=VERSION_HELP,
    ),
    pretty: bool = typer.Option(
        True,
        help="Prints the content in a more legible format if selected.",
    ),
) -> None:
    """Retrieves the changelog content for the specified version."""
    prefix = "# " if pretty else ""

    release_notes = None
    if version == "unreleased":
        release_notes = (
            _unreleased_notes().markdown()
            or f"{prefix}There are no unreleased changes."
        )

    if release_notes is None:
        parsed_version = (
            changelog.get_latest_version()
            if version == "latest"
            else VersionInfo.parse(version)
        )
        release_notes = (
            _released_notes(parsed_version).markdown()
            or f"{prefix}There are no notes for version {version}."
        )

    print(Markdown(release_notes) if pretty else release_notes)


def _unreleased_notes() -> ReleaseNotes:
    all_versions = changelog.get_all_versions()

    # all_versions[0] is the topmost version in the changelog file.
    return changelog.get_release_notes("Unreleased", all_versions[0])


def _released_notes(version: VersionInfo) -> ReleaseNotes:
    all_versions = changelog.get_all_versions()
    if version not in all_versions:
        print(f"Could not find version {version}.")
        raise typer.Abort()

    i = all_versions.index(version)
    (prev_version,) = all_versions[i + 1 : i + 2] or (None,)
    return changelog.get_release_notes(version, prev_version)

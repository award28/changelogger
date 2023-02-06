import typer
from rich import print
from rich.markdown import Markdown

from changelogger import changelog


def content(
    pretty: bool = typer.Option(
        True,
        help="Prints the content in a more legible format if selected.",
    ),
) -> None:
    """Retrieves the unreleased changes from the changelog file."""
    # Get all versions
    all_versions = changelog.get_all_versions()

    # all_versions[0] is the topmost version in the changelog file.
    release_notes = changelog.get_release_notes("Unreleased", all_versions[0])
    md = release_notes.markdown()
    if not md:
        prefix = "# " if pretty else ""
        md = f"{prefix}There are no unreleased changes."

    if pretty:
        print(Markdown(md))
    else:
        print(md)

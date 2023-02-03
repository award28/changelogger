from rich import print
from rich.markdown import Markdown
from changelogger import changelog


def content(
    pretty: bool = True,
) -> None:
    """Retrieves the changelog content for the specified version.
    """
    # Get all versions
    all_versions = changelog.get_all_versions()

    # all_versions[0] is the topmost version in the changelog file.
    release_notes = changelog.get_release_notes("Unreleased", all_versions[0])
    md = release_notes.markdown()
    if not md:
        md = f"{'# ' if pretty else ''}There are no unreleased changes."

    if pretty:
        md =Markdown(md)

    print(md)
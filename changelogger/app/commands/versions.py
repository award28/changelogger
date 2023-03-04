from rich import print
from typer import Option

from changelogger import changelog


def versions(
    latest: bool = Option(
        False,
        "--latest",
        "-l",
        help="Gets the latest version in the changelog file",
    ),
    show_all: bool = Option(
        False,
        "--all",
        "-a",
        help="Get all versions.",
    ),
    start: int = Option(
        0,
        "--start",
        "-s",
        help="What version number to start on.",
    ),
    offset: int = Option(
        10,
        "--offset",
        "-o",
        help="The offset from the start.",
    ),
) -> None:
    """Retrieves the versions found in the changelog file."""
    if latest:
        print(changelog.get_latest_version())
        return

    all_versions = changelog.get_all_versions()
    if show_all:
        print("\n".join(map(str, all_versions)))
        return

    print("\n".join(map(str, all_versions[start : start + offset])))

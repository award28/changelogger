from rich import print
from typer import Option

from changelogger import changelog


def versions(
    latest: bool = Option(
        False, help="Gets the latest version in the changelog file"
    ),
    show_all: bool = Option(False, help="Get all versions."),
    num_versions: int = Option(10, help="The number of versions to get."),
) -> None:
    """Retrieves the versions found in the changelog file."""
    if latest:
        print(changelog.get_latest_version())
        return

    all_versions = changelog.get_all_versions()
    end = len(all_versions) if show_all else num_versions
    print("\n".join(map(str, all_versions[:end])))

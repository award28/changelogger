from rich import print
from rich.markdown import Markdown

from changelogger import changelog
from changelogger.exceptions import CommandException
from changelogger.models.domain_models import VersionInfo


def content(
    version: str,
    pretty: bool = True,
) -> None:
    vinfo = VersionInfo.parse(version)
    """Retrieves the changelog content for the specified version."""
    all_versions = changelog.get_all_versions()
    if vinfo not in all_versions:
        raise CommandException(f"Could not find version {version}.")

    i = all_versions.index(vinfo)
    prev_version = all_versions[i + 1] if i + 1 < len(all_versions) else None
    release_notes = changelog.get_release_notes(vinfo, prev_version)

    md = release_notes.markdown()
    if pretty:
        print(Markdown(md))
    else:
        print(md)

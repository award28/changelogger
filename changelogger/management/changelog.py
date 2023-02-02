from changelogger.commands.domain_models import ReleaseNotes
from changelogger.commands.exceptions import UpgradeException
from changelogger.commands.utils import cached_compile
from changelogger import settings


def get_all_links() -> dict[str, str]:
    with open(settings.CHANGELOG_FILE) as f:
        lines = f.readlines()

    links = {}
    for line in lines:
        match = cached_compile(
            r"\[([\d.]+|Unreleased)]: (.*)",
        ).search(
            line,
        )

        if not match:
            continue

        links[match[1]] = match[2]

    return links


def get_all_versions() -> list[str]:
    with open(settings.CHANGELOG_FILE) as f:
        lines = f.readlines()

    versions = []
    for line in lines:
        match = cached_compile(
            r"### \[([\d.]+)]",
        ).search(
            line,
        )

        if not match:
            continue

        versions.append(match[1])
    return versions

def get_sorted_versions() -> list[str]:
    versions = get_all_versions()
    sorted_versions = sorted(
        (tuple(map(int, version.split('.'))) for version in versions)
    )
    return ['.'.join(map(str, v)) for v in sorted_versions]

def get_latest_version() -> str:
    versions = get_sorted_versions()
    if not versions:
        raise UpgradeException(
            f"This changelog has no versions currently."
        )
    return versions[-1]

def get_release_notes(version: str, prev_version: str) -> ReleaseNotes:
    version = version.replace(".", r"\.")

    with open(settings.CHANGELOG_FILE) as f:
        content = f.read()

    match = cached_compile(
        fr"### \[{version}\]( - \d+-\d+-\d+)?([\s\S]*)### \[{prev_version}\]",
    ).search(
        content,
    )
    if not match:
        raise UpgradeException("Could not extract release notes.")

    raw_notes = match[2]
    raw_sections = cached_compile("[#]+").split(raw_notes)

    release_notes = ReleaseNotes()
    for section in raw_sections:
        section = section.replace("\n", "").lstrip()
        if not section:
            continue

        section_name, *notes = section.split('-')
        attr = section_name.lower()
        notes = [note.lstrip() for note in notes]
        release_notes[attr] = notes

    return release_notes

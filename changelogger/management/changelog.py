from pathlib import Path
from changelogger.commands.domain_models import ChangelogUpdate, ReleaseNotes
from changelogger.commands.exceptions import UpgradeException
from changelogger.commands.utils import cached_compile, open_rw
from changelogger import settings
from changelogger.models.config import ChangeloggerConfig, get_git_repo


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


def _rollback(rollback: dict[Path, str]) -> None:
    for filename, content in rollback.items():
        with open(filename, "w") as f:
            f.write(content)


def update_versioned_files(config: ChangeloggerConfig, update: ChangelogUpdate) -> None:
    rollback: dict[Path, str] = {}

    try:
        for file, update_fn in config.versioned_files():
            with open_rw(file.rel_path) as (f, content):
                rollback[file.rel_path] = content
                new_content = update_fn(content, update)
                f.write(new_content)
    except Exception as e:
        print(
            f"[bold red]Failed to update.[/bold red]"
            " Attempting to roll back..."
        )
        _rollback(rollback)

        print("Rollback successful.")
        raise
        raise UpgradeException(
            "There may be an issue with your search pattern."
        ) from e

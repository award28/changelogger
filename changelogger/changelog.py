from pathlib import Path

from changelogger.conf import settings
from changelogger.conf.models import VersionedFile
from changelogger.exceptions import RollbackException, UpgradeException
from changelogger.models.domain_models import ChangelogUpdate, ReleaseNotes, VersionInfo
from changelogger.templating import update_with_jinja
from changelogger.utils import cached_compile


def get_all_links() -> dict[str, str]:
    lines = settings.CHANGELOG_PATH.read_text().split("\n")

    links = {}
    for line in lines:
        match = cached_compile(
            r"\[(.*)]: (.*)",
        ).search(
            line,
        )

        if not match:
            continue

        links[match[1]] = match[2]

    return links


def get_all_versions() -> list[VersionInfo]:
    lines = settings.CHANGELOG_PATH.read_text().split("\n")
    versions = []
    for line in lines:
        match = cached_compile(
            r"### \[(.*)]",
        ).search(
            line,
        )

        if not match:
            continue

        version_str = match[1]

        match = VersionInfo._REGEX.fullmatch(version_str)
        if not match:
            continue

        versions.append(VersionInfo.parse(version_str))
    return versions


def get_sorted_versions() -> list[VersionInfo]:
    return sorted(get_all_versions())


def get_latest_version() -> VersionInfo:
    versions = get_sorted_versions()
    if not versions:
        raise UpgradeException(f"This changelog has no versions currently.")
    return versions[-1]


def get_release_notes(
    new_version: VersionInfo,
    old_version: VersionInfo,
) -> ReleaseNotes:
    new_version_pattern = str(new_version).replace(".", r"\.")
    old_version_pattern = str(old_version).replace(".", r"\.")

    content = settings.CHANGELOG_PATH.read_text()

    match = cached_compile(
        rf"### \[{new_version_pattern}\]( - \d+-\d+-\d+)?([\s\S]*)### \[{old_version_pattern}\]",
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

        section_name, *notes = section.split("-")
        attr = section_name.lower()
        notes = [note.lstrip() for note in notes]
        release_notes[attr] = notes

    return release_notes


def _rollback(rollback: list[tuple[Path, str]]) -> None:
    for path, content in rollback:
        path.write_text(content)


def update_versioned_files(
    update: ChangelogUpdate,
    versioned_files: list[VersionedFile],
) -> None:
    rollback: list[tuple[Path, str]] = []
    try:
        for file in versioned_files:
            update_fn = update_with_jinja(file)
            content = file.rel_path.read_text()
            rollback.append((file.rel_path, content))
            new_content = update_fn(content, update)
            file.rel_path.write_text(new_content)
    except Exception as upgrade_exc:
        try:
            # Need to reverse rollback list for proper rollback
            _rollback(rollback[::-1])
        except Exception as rollback_exc:
            raise RollbackException(
                "An exception occured while upgrading; rollback unsuccessful."
            ) from rollback_exc

        raise UpgradeException(
            "An exception occured while upgrading; rollback successful."
        ) from upgrade_exc

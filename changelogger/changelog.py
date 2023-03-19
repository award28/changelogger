from pathlib import Path
from typing import Literal

from changelogger import templating
from changelogger.conf import settings
from changelogger.conf.models import VersionedFile
from changelogger.exceptions import (
    CommandException,
    RollbackException,
    UpgradeException,
)
from changelogger.models.domain_models import (
    ChangelogUpdate,
    ReleaseNotes,
    VersionInfo,
)
from changelogger.utils import cached_compile

CHANGELOG_PARTITION_RELEASE_NOTES = "RELEASE NOTES"
CHANGELOG_PARTITION_LINKS = "LINKS"


def _get_changelog_parition(partition: str) -> str:
    changelog_content = settings.CHANGELOG_PATH.read_text()

    start_partition = f"<!-- BEGIN {partition} -->"
    end_partition = f"<!-- END {partition} -->"
    partition_re = cached_compile(
        rf"{start_partition}([\s\S]*){end_partition}"
    )

    match = partition_re.search(changelog_content)
    if not match:
        raise CommandException(
            f"Expected partition for `{partition}`; None found."
        )
    return match[1]


def _get_release_notes_parition() -> str:
    return _get_changelog_parition(CHANGELOG_PARTITION_RELEASE_NOTES)


def _get_links_parition() -> str:
    return _get_changelog_parition(CHANGELOG_PARTITION_LINKS)


def get_all_links() -> dict[VersionInfo | str, str]:
    lines = _get_links_parition().split("\n")

    links = {}
    for line in lines:
        match = cached_compile(
            r"\[(.*)]: (.*)",
        ).search(
            line,
        )

        if not match:
            continue

        version_str = match[1]
        link = match[2]

        if version_str == "Unreleased":
            links[version_str] = link
            continue

        match = VersionInfo._REGEX.fullmatch(version_str)
        if not match:
            continue

        links[VersionInfo.parse(version_str)] = link

    return links


def get_all_versions() -> list[VersionInfo]:
    lines = _get_release_notes_parition().split("\n")
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
    new_version: VersionInfo | Literal["Unreleased"],
    old_version: VersionInfo | None,
) -> ReleaseNotes:
    new_version_pattern = str(new_version).replace(".", r"\.")

    content = _get_release_notes_parition()

    pattern = rf"### \[{new_version_pattern}\]( - \d+-\d+-\d+)?([\s\S]*)"
    if old_version:
        old_version_pattern = str(old_version).replace(".", r"\.")
        pattern += rf"### \[{old_version_pattern}\]"
    match = cached_compile(
        pattern,
    ).search(
        content,
    )
    if not match:
        raise UpgradeException("Could not extract release notes.")

    raw_notes = match[2]
    raw_sections = cached_compile("[#]+").split(raw_notes)

    release_notes = ReleaseNotes()
    for section in raw_sections:
        section_name, *notes = section.split("\n")
        if not section_name:
            continue

        notes = [
            match[1].strip()
            for note in notes
            if (
                match := cached_compile(
                    r"\- (.*)",
                ).search(note)
            )
        ]

        attr = section_name.strip().lower()
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
            content = file.rel_path.read_text()
            rollback.append((file.rel_path, content))
            new_content = templating.update(file, update, content)
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
            f"An exception occured while upgrading; rollback successful.\n\nException: {repr(upgrade_exc)}"
        ) from upgrade_exc

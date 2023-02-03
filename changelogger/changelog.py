from datetime import date
from pathlib import Path
from typing import Any

import typer
from changelogger.conf.models import VersionedFile
from changelogger.models.domain_models import ChangelogUpdate, ReleaseNotes
from changelogger.exceptions import RollbackException, UpgradeException
from changelogger.templating import update_with_jinja
from changelogger.utils import cached_compile, open_rw
from changelogger.conf import settings


def get_all_links() -> dict[str, str]:
    lines = settings.CHANGELOG_PATH.read_text().split('\n')

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
    lines = settings.CHANGELOG_PATH.read_text().split('\n')

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


    content = settings.CHANGELOG_PATH.read_text()

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


def update_versioned_files(update: ChangelogUpdate) -> dict[Path, str] | None:
    rollback: dict[Path, str] = {}
    try:
        for file in settings.VERSIONED_FILES:
            update_fn = update_with_jinja(file)
            with open_rw(file.rel_path) as (f, content):
                rollback[file.rel_path] = content
                new_content = update_fn(content, update)
                f.write(new_content)
        typer.confirm("Do these changes look good?", abort=True)
    except Exception as upgrade_exc:
        try:
            _rollback(rollback)
        except Exception as rollback_exc:
            raise RollbackException(
                "An exception occured while upgrading; rollback unsuccessful."
            ) from rollback_exc

        raise UpgradeException(
            "An exception occured while upgrading; rollback successful."
        ) from upgrade_exc

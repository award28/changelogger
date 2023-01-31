from pathlib import Path
import yaml
import semver
from rich import print
from rich.markdown import Markdown
from .domain_models import (
    ReleaseNotes,
    ChangelogUpdate,
    SemVerType,
    VersionUpgradeConfig,
)
from .exceptions import (
    CommandException,
    UpgradeException,
    ValidationException,
)
from .utils import (
    cached_compile,
    open_rw,
)


class Changelogger:
    def __init__(self, changelog_file: str) -> None:
        if not Path(changelog_file).is_file():
            raise CommandException(f"Could not find Changelog file {changelog_file}.")

        self.changelog_file = changelog_file

    @staticmethod
    def _confirm(new_version: str):
        confirm_version = input("Confirm new version: ")
        if confirm_version != new_version:
            raise UpgradeException("Failed confirmation.")

        print("[bold green]Version Confirmed![/bold green] Updating files...")

    @staticmethod
    def _prompt_unreleased_changelog(update: ChangelogUpdate) -> ChangelogUpdate:
        for name, notes in update.release_notes.dict().items():
            done = False
            print(Markdown(f"## Updating **{name.title()}**"))
            while not done:
                print(
                    f"Any further additions for [bold]{name.title()}[/bold]?"
                )
                print(notes)
                if (new_note := input("New note [Enter to continue]: ")):
                    notes.append(new_note)
                else:
                    done = True
            update.release_notes[name] = notes
        return update

    @staticmethod
    def _update_versioned_files(config: VersionUpgradeConfig, update: ChangelogUpdate) -> None:
        rollback = {}
        try:
            for filename, update_fn in config.versioned_files().items():
                with open_rw(filename) as (f, content):
                    rollback[filename] = content
                    new_content = update_fn(content, update)
                    f.write(new_content)
        except Exception as e:
            print(
                f"[bold red]Failed to update.[/bold red]"
                " Attempting to roll back..."
            )
            for filename, content in rollback.items():
                with open(filename, "w") as f:
                    f.write(content)

            raise UpgradeException(e)

    def _get_all_links(self) -> dict[str, str]:
        with open(self.changelog_file) as f:
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


    def _get_all_versions(self) -> list[str]:
        with open(self.changelog_file) as f:
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

    def _get_sorted_versions(self) -> list[str]:
        versions = self._get_all_versions()
        sorted_versions = sorted(
            (tuple(map(int, version.split('.'))) for version in versions)
        )
        return ['.'.join(map(str, v)) for v in sorted_versions]

    def _get_latest_version(self) -> str:
        versions = self._get_sorted_versions()
        if not versions:
            raise UpgradeException(
                f"This changelog has no versions currently."
            )
        return versions[-1]

    def _get_release_notes(self, version: str, prev_version: str) -> ReleaseNotes:
        version = version.replace(".", r"\.")

        with open(self.changelog_file) as f:
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


    def content_for_version(self, version: str) -> None:
        all_versions = self._get_all_versions()
        i = all_versions.index(version)
        prev_version = all_versions[i + 1]
        release_notes = self._get_release_notes(version, prev_version)
        print(release_notes.markdown())

    def validate(self) -> None:
        # Validate there's at least 1 version
        all_versions = self._get_all_versions()
        if not all_versions:
            raise ValidationException("Expected there to be at least 1 version; None found.")

        # Validate all release notes are parseable for all versions
        changelog_versions = ["Unreleased", *all_versions, "NOTE"]
        for version, prev_version in zip(changelog_versions, changelog_versions[1:]):
            try:
                self._get_release_notes(version, prev_version)
            except:
                raise ValidationException(f"Failed to validate notes for version {version}")

        # Validate there are links in the expected format for all versions
        sorted_versions = self._get_sorted_versions()
        all_links = self._get_all_links()
        for idx, version in enumerate(sorted_versions[1:], start=1):
            link = all_links.get(version)
            if not link:
                raise ValidationException(f"Could not find the link for version {version}")

            prev_version = sorted_versions[idx-1]
            if f"{prev_version}...{version}" not in link:
                raise ValidationException(f"Link is incorrect for version {version}")

        link = all_links.get("Unreleased")
        if not link:
            raise ValidationException(f"Could not find the link for unreleased changes.")

        if f"{all_versions[0]}...HEAD" not in link:
            raise ValidationException(f"Link is incorrect for the unreleased changes.")

        if sorted_versions[0] not in all_links:
            raise ValidationException(f"Could not find the link for version {sorted_versions[0]}")

        print(":white_heavy_check_mark: [bold green]validated![/bold green]")

    def upgrade(
        self,
        version_to_bump: SemVerType,
        confirm: bool,
        prompt_changelog: bool,
        version_upgrade_config_file: str,
    ) -> None:
        old_version = self._get_latest_version()
        release_notes = self._get_release_notes("Unreleased", old_version)
        bump = getattr(semver, f"bump_{version_to_bump.value}")
        new_version = bump(old_version)
        update = ChangelogUpdate(
            old_version=old_version,
            new_version=new_version,
            release_notes=release_notes,
        )
        if prompt_changelog:
            update = self._prompt_unreleased_changelog(update)

        print(f"Upgrading {old_version} ==> {new_version}")
        md = f"\n# Changelog updates for [{new_version}]\n"
        if (update_md := update.release_notes.markdown()):
            md += update_md
        else:
            md += "\n*No notes found or added*"

        md += "\n---\n"
        print(Markdown(md))
        if confirm:
            self._confirm(new_version)

        with open(version_upgrade_config_file) as f:
            raw_config = yaml.safe_load(f)

        config = VersionUpgradeConfig(**raw_config)
        self._update_versioned_files(config, update)
        print("[bold green]Upgrade complete![/bold green] Please commit your changes to source control.")

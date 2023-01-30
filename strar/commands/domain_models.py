from collections.abc import Callable
from datetime import date
from enum import Enum
from pydantic import BaseModel, FilePath
from jinja2 import FileSystemLoader, Environment, Template
from .utils import (
    cached_compile,
)



class ReleaseNotes(BaseModel):
    added: list[str] = []
    changed: list[str] = []
    deprecated: list[str] = []
    removed: list[str] = []
    fixed: list[str] = []
    security: list[str] = []

    def __getitem__(self, attr: str) -> list[str]:
        return getattr(self, attr)


    def __setitem__(self, attr: str, value: list[str]) -> None:
        return setattr(self, attr, value)


    @classmethod
    def sections(cls) -> list[str]:
        return list(cls.__fields__.keys())

    def markdown(self) -> str:
        sections = self.dict()
        md = ""
        for name, notes in sections.items():
            if not notes:
                continue

            formatted_notes = "- " + '\n- '.join(notes)
            md += f"""#### {name.title()}

            {formatted_notes}

            """
        return "\n".join(s.lstrip() for s in md.split("\n"))


class ChangelogUpdate(BaseModel):
    old_version: str
    new_version: str
    release_notes: ReleaseNotes

    def overview_txt(self) -> str:
        md = "== Changelog ==\n"
        md += f"= {self.new_version} {date.today()} =\n"
        sections = self.release_notes.dict()
        for name, notes in sections.items():
            for note in notes:
                md += f"* {name.title()} - {note}\n"
        return md

    def link_markdown(self) -> str:
        base_url = "https://github.com/klaviyo/woocommerce-klaviyo/compare"
        links = {
            "Unreleased": (self.new_version, "HEAD"),
            self.new_version: (self.old_version, self.new_version),
        }

        return "\n".join(
            f"[{title}]: {base_url}/{start}...{end}"
            for title, (start, end) in links.items()
        ) + "\n"

    def overview_markdown(self) -> str:
        md = f"""### [Unreleased]

        ### [{self.new_version}] - {date.today()}

        {self.release_notes.markdown()}### [{self.old_version}]"""
        return '\n'.join(s.lstrip() for s in md.split('\n'))


class VersionUpgradeFileConfig(BaseModel):
    rel_path: FilePath
    pattern: str
    jinja_file: FilePath | None



class VersionUpgradeConfig(BaseModel):
    files: list[VersionUpgradeFileConfig]

    def versioned_files(self) -> dict[FilePath, Callable]:
        versioned_files = {}
        for file in self.files:
            if file.jinja_file:
                versioned_files[file.rel_path] = self._update_with_jinja(file.pattern, file.jinja_file)
            else:
                versioned_files[file.rel_path] = self._update_with_regex(file.pattern)

        return versioned_files

    @staticmethod
    def _update_with_regex(pattern: str) -> Callable:

        def inner(content: str, update: ChangelogUpdate) -> str:
            old_version = pattern.replace("{{ version }}", update.old_version)
            new_version = pattern.replace("{{ version }}", update.new_version)
            return content.replace(old_version, new_version)

        return inner

    @classmethod
    def _update_with_jinja(cls, pattern: str, jinja_file: FilePath) -> Callable:
        def inner(content: str, update: ChangelogUpdate) -> str:
            tmpl = cls._tmpl(jinja_file)
            replacement = tmpl.render(
                version=update.new_version,
                today=date.today(),
                sections=update.release_notes.dict(),
            )
            return cached_compile(pattern).sub(
                replacement,
                content,
            )
        return inner

    @staticmethod
    def _tmpl(jinja_file: FilePath) -> Template:
        templateLoader = FileSystemLoader(searchpath="./")
        templateEnv = Environment(loader=templateLoader)
        return templateEnv.get_template(str(jinja_file))


class SemVerType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

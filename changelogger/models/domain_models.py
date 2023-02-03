from collections.abc import Callable
from datetime import date
from enum import Enum
from typing import Any
from pydantic import BaseModel, FilePath
from jinja2 import BaseLoader, Environment, Template


from changelogger.utils import cached_compile


class SemVerType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


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
    jinja: str | None
    jinja_rel_path: FilePath | None
    context: dict = {}


class VersionUpgradeConfig(BaseModel):
    files: list[VersionUpgradeFileConfig]

    def versioned_files(self) -> list[tuple[VersionUpgradeFileConfig, Callable]]:
        versioned_files = []
        for file in self.files:
            versioned_files.append((file, self._update_with_jinja(file)))

        return versioned_files

    @classmethod
    def _update_with_jinja(cls, file: VersionUpgradeFileConfig) -> Callable:

        assert file.jinja or file.jinja_rel_path, "No valid jinja template found."

        replacement_str = file.jinja
        if not replacement_str and file.jinja_rel_path:
            replacement_str = file.jinja_rel_path.read_text()

        def inner(content: str, update: ChangelogUpdate) -> str:
            assert replacement_str
            render_kwargs = cls._render_kwargs(file, update)

            pattern = cls._tmpl(file.pattern).render(**render_kwargs)
            replacement = cls._tmpl(replacement_str).render(**render_kwargs)

            return cached_compile(pattern).sub(replacement, content)
        return inner

    @staticmethod
    def _tmpl(jinja: str) -> Template:
        template_env = Environment(loader=BaseLoader())
        return template_env.from_string(jinja)

    @staticmethod
    def _render_kwargs(
        file: VersionUpgradeFileConfig,
        update: ChangelogUpdate,
    ) -> dict[str, Any]:
        return dict(
                new_version=update.new_version,
                old_version=update.old_version,
                today=date.today(),
                sections=update.release_notes.dict(),
                context=file.context,
        )

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import DefaultDict

import yaml  # type: ignore
from pydantic import BaseModel

from changelogger.conf import git
from changelogger.conf.defaults import (
    CHANGELOGGER_PATH,
    DEFAULT_CHANGELOG_PATH,
    DEFAULT_LINKS_JINJA_PATTERN,
    DEFAULT_LINKS_TEMPLATE,
    DEFAULT_OVERVIEW_JINJA_PATTERN,
    DEFAULT_OVERVIEW_TEMPLATE,
    DEFAULT_RELEASE_NOTES_TEMPLATE,
    DEFAULT_TEMPLATES_DIR,
)


class VersionedFile(BaseModel):
    rel_path: Path
    pattern: str
    jinja: str | None = None
    template: Path | None = None
    context: dict = {}

    def simple_dict(self) -> dict:
        return {
            k: v if not isinstance(v, Path) else str(v)
            for k, v in self.dict().items()
            if v
        }


class ChangelogSegment(BaseModel):
    pattern: str
    template: Path


_default_overview_segment = ChangelogSegment(
    pattern=DEFAULT_OVERVIEW_JINJA_PATTERN,
    template=DEFAULT_OVERVIEW_TEMPLATE,
)

_default_release_notes_segment = ChangelogSegment(
    pattern="",
    template=DEFAULT_RELEASE_NOTES_TEMPLATE,
)

_default_links_segment = ChangelogSegment(
    pattern=DEFAULT_LINKS_JINJA_PATTERN,
    template=DEFAULT_LINKS_TEMPLATE,
)


class Changelog(BaseModel):
    rel_path: Path = Path(DEFAULT_CHANGELOG_PATH)
    release_notes: ChangelogSegment = _default_release_notes_segment
    overview: ChangelogSegment = _default_overview_segment
    links: ChangelogSegment = _default_links_segment

    def has_defaults(self) -> bool:
        return (
            self.overview == _default_overview_segment
            or self.links == _default_links_segment
        )

    def as_versioned_files(self) -> list[VersionedFile]:
        context: DefaultDict = defaultdict(dict)
        if self.has_defaults():
            context["git"] = git.get_ctx()

        return [
            VersionedFile(
                rel_path=self.rel_path,
                pattern=segment.pattern,
                template=segment.template,
                context=context,
            )
            for segment in (self.overview, self.links)
        ]


class ChangeloggerConfig(BaseModel):
    changelog: Changelog = Changelog()
    versioned_files: list[VersionedFile] = []
    templates_dir: Path = DEFAULT_TEMPLATES_DIR

    @classmethod
    def from_config_or_default(cls) -> "ChangeloggerConfig":
        if not CHANGELOGGER_PATH.exists():
            return cls()

        raw_config = yaml.safe_load(
            CHANGELOGGER_PATH.read_text(),
        )
        return cls(**raw_config)

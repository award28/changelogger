from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel
from changelogger.conf.git import get_git_repo


from changelogger.conf._defaults import (
    CHANGELOGGER_PATH,
    DEFAULT_CHANGELOG_PATH,
    DEFAULT_OVERVIEW_JINJA_PATTERN,
    DEFAULT_OVERVIEW_JINJA_PATH,
    DEFAULT_LINKS_JINJA_PATTERN,
    DEFAULT_LINKS_JINJA_PATH,
)


class VersionedFile(BaseModel):
    rel_path: Path
    pattern: str
    jinja: str | None = None
    jinja_rel_path: Path  | None = None
    context: dict = {}


class ChangelogSegment(BaseModel):
    pattern: str
    jinja_rel_path: Path
    _default: bool = False


class Changelog(BaseModel):
    rel_path: Path = Path(DEFAULT_CHANGELOG_PATH)
    overview: ChangelogSegment = ChangelogSegment(
        pattern=DEFAULT_OVERVIEW_JINJA_PATTERN,
        jinja_rel_path=DEFAULT_OVERVIEW_JINJA_PATH,
        _default = True,
    )
    links: ChangelogSegment = ChangelogSegment(
        pattern=DEFAULT_LINKS_JINJA_PATTERN,
        jinja_rel_path=DEFAULT_LINKS_JINJA_PATH,
        _default = True,
    )

    def has_defaults(self) -> bool:
        return self.overview._default or self.links._default

    def as_versioned_files(self) -> list[VersionedFile]:
        context = {}
        if self.has_defaults():
            context['git']['repo'] =get_git_repo()

        return [
            VersionedFile(
                rel_path=self.rel_path,
                pattern=segment.pattern,
                jinja_rel_path=segment.jinja_rel_path,
                context=context,
            )
            for segment in (self.overview, self.links)
        ]


class ChangeloggerConfig(BaseModel):
    changelog: Changelog = Changelog()
    versioned_files: list[VersionedFile] = []

    @classmethod
    def from_config_or_default(cls) -> Self:
        if not CHANGELOGGER_PATH.exists():
            return cls()

        raw_config = yaml.safe_load(
            CHANGELOGGER_PATH.read_text(),
        )
        return cls(**raw_config)

import tomllib
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict

import yaml  # type: ignore
from pydantic import BaseModel, validator
from semver import VersionInfo

from changelogger.conf import git
from changelogger.conf.defaults import (
    CHANGELOGGER_PATH,
    DEFAULT_CHANGELOG_PATH,
    DEFAULT_LINKS_JINJA_PATH,
    DEFAULT_LINKS_JINJA_PATTERN,
    DEFAULT_OVERVIEW_JINJA_PATH,
    DEFAULT_OVERVIEW_JINJA_PATTERN,
)


class VersionedFile(BaseModel):
    rel_path: Path
    pattern: str
    jinja: str | None = None
    jinja_rel_path: Path | None = None
    context: dict = {}

    def simple_dict(self) -> dict:
        return {
            k: v if not isinstance(v, Path) else str(v)
            for k, v in self.dict().items()
            if v
        }


class ChangelogSegment(BaseModel):
    pattern: str
    jinja_rel_path: Path


_default_overview = ChangelogSegment(
    pattern=DEFAULT_OVERVIEW_JINJA_PATTERN,
    jinja_rel_path=DEFAULT_OVERVIEW_JINJA_PATH,
)

_default_links = ChangelogSegment(
    pattern=DEFAULT_LINKS_JINJA_PATTERN,
    jinja_rel_path=DEFAULT_LINKS_JINJA_PATH,
)


class Changelog(BaseModel):
    rel_path: Path = Path(DEFAULT_CHANGELOG_PATH)
    overview: ChangelogSegment = _default_overview
    links: ChangelogSegment = _default_links

    def has_defaults(self) -> bool:
        return (
            self.overview == _default_overview or self.links == _default_links
        )

    def as_versioned_files(self) -> list[VersionedFile]:
        context: DefaultDict = defaultdict(dict)
        if self.has_defaults():
            context["git"] = git.get_ctx()

        return [
            VersionedFile(
                rel_path=self.rel_path,
                pattern=segment.pattern,
                jinja_rel_path=segment.jinja_rel_path,
                context=context,
            )
            for segment in (self.overview, self.links)
        ]


class ProjectMetadata(BaseModel):
    version: VersionInfo
    description: str

    class Config:
        arbitrary_types_allowed = True

    @validator("version", pre=True)
    def to_version_info(cls, v: str) -> VersionInfo:
        return VersionInfo.parse(v)

    @classmethod
    def build(cls) -> "ProjectMetadata":
        metadata = tomllib.loads(
            Path("pyproject.toml").read_text(),
        )
        return cls(**metadata["tool"]["poetry"])


class ChangeloggerConfig(BaseModel):
    changelog: Changelog = Changelog()
    versioned_files: list[VersionedFile] = []
    metadata: ProjectMetadata = ProjectMetadata.build()

    @classmethod
    def from_config_or_default(cls) -> "ChangeloggerConfig":
        if not CHANGELOGGER_PATH.exists():
            return cls()

        raw_config = yaml.safe_load(
            CHANGELOGGER_PATH.read_text(),
        )
        return cls(**raw_config)

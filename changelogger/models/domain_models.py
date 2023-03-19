from enum import Enum
from typing import Union

import semver
from pydantic import BaseModel, validator

from changelogger.conf import settings


class BumpTarget(Enum):
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

    def __bool__(self) -> bool:
        return bool(
            self.added
            or self.changed
            or self.deprecated
            or self.removed
            or self.fixed
            or self.security
        )

    @classmethod
    def sections(cls) -> list[str]:
        return list(cls.__fields__.keys())

    def markdown(self) -> str:
        return settings.TMPL_ENV.get_template(
            str(settings.RELEASE_NOTES_TEMPLATE),
        ).render(
            sections=self.dict(),
        )


class VersionInfo(semver.VersionInfo):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @validator("*")
    def validate(cls, v: Union[str, "VersionInfo"]) -> "VersionInfo":
        return isinstance(v, VersionInfo) and v or cls.parse(v)


class ChangelogUpdate(BaseModel):
    new_version: VersionInfo | None
    old_version: VersionInfo | None
    release_notes: ReleaseNotes

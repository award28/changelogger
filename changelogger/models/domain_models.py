from enum import Enum
from typing import Union

import semver
from pydantic import BaseModel, validator


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
        sections = self.dict()
        md = ""
        for name, notes in sections.items():
            if not notes:
                continue

            formatted_notes = "- " + "\n- ".join(notes)
            md += f"""#### {name.title()}

            {formatted_notes}

            """
        return "\n".join(s.lstrip() for s in md.split("\n"))


class VersionInfo(semver.VersionInfo):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @validator("*")
    def validate(cls, v: Union[str, "VersionInfo"]) -> "VersionInfo":
        if isinstance(v, VersionInfo):
            return v
        return cls.parse(v)


class ChangelogUpdate(BaseModel):
    new_version: VersionInfo | None
    old_version: VersionInfo | None
    release_notes: ReleaseNotes

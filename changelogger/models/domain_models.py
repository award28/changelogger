from enum import Enum
from pydantic import BaseModel


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

            formatted_notes = "- " + "\n- ".join(notes)
            md += f"""#### {name.title()}

            {formatted_notes}

            """
        return "\n".join(s.lstrip() for s in md.split("\n"))


class ChangelogUpdate(BaseModel):
    new_version: str
    old_version: str
    release_notes: ReleaseNotes

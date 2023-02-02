from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _Ctx:
    config_file: Path | None
    changelog_file: Path
    default_behavior: bool = True


class ManageCtx:
    _ctx = ContextVar('manage_context')

    @classmethod
    def set(
        cls,
        config_file: str = "",
        changelog_file: str = "CHANGELOG.md",
        default_behavior: bool = True,
    ) -> None:
        ctx = _Ctx(
            default_behavior=default_behavior,
            config_file=Path(config_file) if config_file else None,
            changelog_file=Path(changelog_file),
        )
        cls._ctx.set(ctx)

    @classmethod
    def _get(cls) -> _Ctx:
        return cls._ctx.get(
            _Ctx(None, Path("CHANGELOG.md")),
        )

    @classmethod
    def get_default_behavior(cls) -> bool:
        return cls._get().default_behavior

    @classmethod
    def get_config_file(cls) -> Path | None:
        return cls._get().config_file

    @classmethod
    def get_changelog_file(cls) -> Path:
        return cls._get().changelog_file

from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any, Self
from jinja2 import BaseLoader, Environment, Template
from pydantic import BaseModel, Field, root_validator, validator
import yaml
from changelogger import settings

from changelogger.models.domain_models import ChangelogUpdate
from changelogger.utils import (
    cached_compile,
    get_git_repo,
)


class VersionedFileConfig(BaseModel):
    rel_path: Path
    pattern: str
    jinja: str | None
    jinja_rel_path: Path | None
    context: dict = {}

    @root_validator
    def xor_jinja(cls, values: dict) -> dict:
        jinja = values.get('jinja')
        jinja_rel_path = values.get('jinja_rel_path')

        if jinja and jinja_rel_path:
            raise ValueError(
                "Both `jinja` and `jinja_rel_path` can't be set"
            )
        elif jinja_rel_path and not jinja_rel_path.exists():
            raise ValueError(
                "The jinja template `{jinja_rel_path}` could not be found."
            )

        return values


class _DefaultConfig(BaseModel):
    files: list[VersionedFileConfig] = Field([], alias="changelog")

    @validator('files', pre=True)
    def set_rel_path_to_changelog(cls, v):
        repo = get_git_repo()
        for d in v:
            d['rel_path'] = settings.CHANGELOG_FILE
            ctx = d.get('context', {})
            ctx['git'] = dict(repo=repo)
            d['context'] = ctx
            if (jinja_rel_path := d.get('jinja_rel_path')):
                d['jinja_rel_path'] = settings.ASSETS.joinpath(jinja_rel_path)

        return v


class ChangeloggerConfig(BaseModel):
    files: list[VersionedFileConfig] = []

    @classmethod
    def from_settings(cls) -> Self:
        config = cls(
            **yaml.safe_load(
                settings.CHANGELOGGER_FILE.read_text(),
            ),
        )
        if settings.DEFAULT_BEHAVIOR:
            default_config = _DefaultConfig(
                **yaml.safe_load(
                    settings.DEFAULT_CHANGELOGGER_FILE.read_text(),
                )
            )
            config.files.extend(default_config.files)

        return config

    def versioned_files(self) -> list[tuple[VersionedFileConfig, Callable]]:
        versioned_files = []
        for file in self.files:
            versioned_files.append((file, self._update_with_jinja(file)))

        return versioned_files

    @classmethod
    def _update_with_jinja(cls, file: VersionedFileConfig) -> Callable:

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
        file: VersionedFileConfig,
        update: ChangelogUpdate,
    ) -> dict[str, Any]:
        return dict(
                new_version=update.new_version,
                old_version=update.old_version,
                today=date.today(),
                sections=update.release_notes.dict(),
                context=file.context,
        )

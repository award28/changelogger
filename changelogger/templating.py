from datetime import date
from typing import Any
from changelogger.conf.models import VersionedFile
from jinja2 import BaseLoader, Environment, Template
from changelogger.models.domain_models import ChangelogUpdate
from changelogger.utils import cached_compile
from collections.abc import Callable


def _tmpl(jinja: str) -> Template:
    template_env = Environment(loader=BaseLoader())
    return template_env.from_string(jinja)


def _render_variables(
    versioned_file: VersionedFile,
    update: ChangelogUpdate,
) -> dict[str, Any]:
    return dict(
        new_version=update.new_version,
        old_version=update.old_version,
        today=date.today(),
        sections=update.release_notes.dict(),
        context=versioned_file.context,
    )


def update_with_jinja(
    file: VersionedFile,
) -> Callable:

    assert file.jinja or file.jinja_rel_path, "No valid jinja template found."

    replacement_str = file.jinja
    if not replacement_str and file.jinja_rel_path:
        replacement_str = file.jinja_rel_path.read_text()

    def inner(content: str, update: ChangelogUpdate) -> str:
        assert replacement_str
        render_kwargs = _render_variables(file, update)

        pattern = _tmpl(file.pattern).render(**render_kwargs)
        replacement = _tmpl(replacement_str).render(**render_kwargs)

        return cached_compile(pattern).sub(replacement, content)
    return inner
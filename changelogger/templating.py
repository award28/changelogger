from datetime import date
from typing import Any

from jinja2 import BaseLoader, Environment, Template

from changelogger.conf.models import VersionedFile
from changelogger.models.domain_models import ChangelogUpdate
from changelogger.utils import cached_compile


def update(
    file: VersionedFile,
    update: ChangelogUpdate,
    content: str,
) -> str:
    """Replaces the versioned files rendered pattern in the supplied content."""

    replacement_str = file.jinja
    if not replacement_str:
        assert file.jinja_rel_path, "No valid jinja template found."
        replacement_str = file.jinja_rel_path.read_text()

    variables = _get_variables(file, update)
    pattern = render_jinja(file.pattern, variables)
    replacement = render_jinja(replacement_str, variables)

    return cached_compile(pattern).sub(replacement, content)


def render_pattern(
    file: VersionedFile,
    update: ChangelogUpdate,
) -> str:
    variables = _get_variables(file, update)
    return render_jinja(file.pattern, variables)


def render_jinja(tmpl: str, variables: dict[str, Any]) -> str:
    return _tmpl(tmpl).render(**variables)


def _tmpl(jinja: str) -> Template:
    template_env = Environment(loader=BaseLoader())
    return template_env.from_string(jinja)


def _get_variables(
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

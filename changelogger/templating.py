from datetime import date
from functools import partial
from importlib import resources
from re import Match
from typing import Any

from jinja2 import Environment, FileSystemLoader

from changelogger.conf import settings
from changelogger.conf.models import VersionedFile
from changelogger.models.domain_models import ChangelogUpdate
from changelogger.utils import cached_compile

with resources.as_file(
    resources.files("changelogger").joinpath("templates"),
) as package_templates:
    TMPL_ENV = Environment(
        loader=FileSystemLoader(
            [
                settings.TEMPLATES_DIR,
                package_templates,
            ]
        )
    )


def update(
    file: VersionedFile,
    update: ChangelogUpdate,
    content: str,
) -> str:
    """Replaces the versioned files rendered pattern in the supplied content."""

    render = None
    if file.jinja_rel_path:
        render = partial(render_template, str(file.jinja_rel_path))
    elif file.jinja:
        render = partial(render_jinja, file.jinja)

    assert render, "No valid jinja template found."

    var_getter = partial(_get_variables, file, update)
    pattern = render_jinja(file.pattern, var_getter())

    # re.sub can take a callable as the replacement argument rather than a
    # string. This callable accepts a match and returns a string. For each
    # match which is found, re.sub will call repl with the match, and
    # replace the found pattern with the output string of the user supplied
    # repl function.
    repl = lambda m: render(var_getter(m))
    return cached_compile(pattern).sub(repl, content)


def render_pattern(
    file: VersionedFile,
    update: ChangelogUpdate,
) -> str:
    variables = _get_variables(file, update)
    return render_jinja(file.pattern, variables)


def render_jinja(tmpl_str: str, variables: dict[str, Any]) -> str:
    return TMPL_ENV.from_string(tmpl_str).render(**variables)


def render_template(template: str, variables: dict[str, Any]) -> str:
    breakpoint()
    return TMPL_ENV.get_template(template).render(**variables)


def _get_variables(
    versioned_file: VersionedFile,
    update: ChangelogUpdate,
    match: Match | None = None,
) -> dict[str, Any]:
    return dict(
        new_version=update.new_version,
        old_version=update.old_version,
        today=date.today(),
        sections=update.release_notes.dict(),
        context=versioned_file.context,
        match=match,
    )

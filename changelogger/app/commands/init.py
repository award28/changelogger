import re
from datetime import date
from pathlib import Path
from textwrap import dedent
from typing import Any

import typer
import yaml  # type: ignore
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from changelogger import changelog
from changelogger.conf import git, settings
from changelogger.conf.models import VersionedFile
from changelogger.templating import render_jinja
from changelogger.utils import cached_compile


def init(
    prompt_changelog: bool = True,
    prompt_versioned_files: bool = True,
):
    """Setup a git repository to work with Changelogger or reinitialize
    an existing one.
    """

    console = Console()
    if prompt_changelog:
        _init_changelog(console)

    if prompt_versioned_files:
        _init_changelogger(console)


def _init_changelog(console: Console) -> None:
    # If they don't already have a changelog file or want to create a new one
    changelog_exists = settings.CHANGELOG_PATH.exists()
    if changelog_exists:
        if not typer.confirm(
            "It looks like you've already specified your changelog "
            f'as "{settings.CHANGELOG_PATH}"; are you sure you want to '
            "create a new one?"
        ):
            return
    elif not typer.confirm(
        f'Would you like to generate a "{settings.CHANGELOG_PATH}" file?'
    ):
        return

    # Wants to replace/create a CHANGELOG.md
    settings.DEFAULT_CHANGELOG_PATH.write_text(
        render_jinja(
            settings.CHANGELOG_JINJA.read_text(),
            dict(
                today=date.today(),
                context=dict(git=git.get_ctx()),
            ),
        )
    )
    console.clear()

    console.print(f'"{settings.CHANGELOG_PATH}" successfully created!')


def _init_changelogger(console: Console) -> None:
    # If they don't already have a changelogger file or want to create a new one
    changelogger_exists = settings.CHANGELOGGER_PATH.exists()
    if changelogger_exists:
        if not typer.confirm(
            "It looks like you've already specified your changelogger "
            f'as "{settings.CHANGELOGGER_PATH}"; are you sure you want to '
            "replace it?"
        ):
            return

    if not typer.confirm(
        "Would you like Changelogger to monitor and update any files in "
        'addition to "CHANGELOG.md"?'
    ):
        return

    versioned_files: list[VersionedFile] = []
    while True:
        if versioned_file := _prompt_versioned_file(console):
            versioned_files.append(versioned_file)

        if not typer.confirm("Any other versioned files?"):
            break

    settings.CHANGELOGGER_PATH.write_text(
        yaml.safe_dump(
            dict(
                versioned_files=[
                    versioned_file.simple_dict()
                    for versioned_file in versioned_files
                ],
            ),
        )
    )
    console.clear()

    console.print(f'"{settings.CHANGELOGGER_PATH}" successfully created!')


def _prompt_versioned_file(console: Console) -> VersionedFile | None:
    console.clear()
    rel_path = typer.prompt(
        "What is the relative path of this versioned file?", type=Path
    )
    if not rel_path.exists():
        print(f'[bold]Could not find[/bold] "{rel_path}"; Skipping this file.')
        return None

    console.clear()
    pattern = typer.prompt(
        "What pattern should changelogger use to find and replace the "
        "versioned information?"
    )

    # TODO
    # This doesn't encapsulate state which will be available during the actual
    # Upgrade process. This confirmation could be more accurate.
    rendered_pattern = render_jinja(
        pattern,
        dict(
            old_version=changelog.get_latest_version(),
            today=date.today(),
        ),
    )
    num_matches = len(re.findall(rendered_pattern, rel_path.read_text()))
    match = cached_compile(rendered_pattern).search(rel_path.read_text())
    if not match:
        print(
            f'Could not find a match in "{rel_path}" using the rendered '
            f"pattern [bold]{rendered_pattern}[/bold]; skipping this file."
        )
        return None

    console.clear()
    num_matches = len(re.findall(rendered_pattern, rel_path.read_text()))
    title = f"{num_matches} Match{'es' if num_matches > 1 else ''} Found!"

    print(
        Panel.fit(
            match[0],
            title=f"[bold green]{title}[/bold green]",
            subtitle=":backhand_index_pointing_up: First Match",
            padding=1,
        )
    )

    context = _prompt_context()
    console.clear()

    metadata = yaml.safe_dump(
        dict(
            rel_path=str(rel_path),
            pattern=pattern,
            context=context or None,
        )
    )
    print(
        Panel.fit(
            Syntax(metadata, "yaml"),
            title=f"[bold]{rel_path} Metadata[/bold]",
            padding=1,
        )
    )

    if not typer.confirm(
        "Does everything look good? If so, we'll prompt you for the "
        "replacement jinja."
    ):
        print("Skipping this file.")
        return None

    console.clear()
    jinja = _prompt_jinja(rel_path, pattern, context)
    if not jinja:
        print("No jinja entered; skipping this file.")
        return None

    console.clear()
    template = None
    if "\n" in jinja:
        if typer.confirm(
            "It looks like your jinja is multiple lines; "
            "do you want to save this in its own file?"
        ):
            default_path = settings.TEMPLATES_DIR.joinpath(
                f"{rel_path}.jinja2"
            )
            template = typer.prompt(
                "Where do you want to save the template?",
                default=default_path,
                type=Path,
            )

            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_text(jinja)
            print(f'Successfully saved jinja to "{template}"!')

    return VersionedFile(
        rel_path=rel_path,
        pattern=pattern,
        jinja=jinja if not template else None,
        template=template,
        context=context,
    )


def _prompt_context() -> dict[str, Any]:
    if not typer.confirm(
        "Do you want to add context to use in your jinja " "template?"
    ):
        return {}

    CONTEXT_MARKER = dedent(
        """
        # Provide any context in the above context object to make it available
        # in your jinja file.
        #
        # -- EXAMPLE --
        # context:
        #   pet_names:
        #   - friday
        #   - lucy
        #
        # -- USAGE --
        # {% for pet_name in  context.pet_names %}
        # ...
        # {% endfor %}
        """
    )
    ctx_str = typer.edit("context:\n\n" + CONTEXT_MARKER, extension=".yml")
    try:
        return yaml.safe_load(ctx_str) if ctx_str else {}
    except yaml.error.YAMLError:
        print("Unable to extract context; Skipping context.")
        return {}


def _prompt_jinja(
    rel_path: Path,
    pattern: str,
    context: dict[str, Any],
) -> str | None:
    MARKER = (
        dedent(
            f"""
        {{#
        Enter the jinja replacement above.

        rel_path: {rel_path}
        pattern: {pattern}
        """
        )
        + yaml.safe_dump(dict(context=context or None))
        + "#}"
    )

    message = typer.edit("\n\n" + MARKER, extension=".jinja2")
    if not message:
        print("No jinja supplied. Skipping file.")
        return None

    return message.split(MARKER)[0].rstrip()

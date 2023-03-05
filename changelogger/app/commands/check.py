import typer
from rich import print

from changelogger import changelog, templating
from changelogger.app.commands.notes import _unreleased_notes
from changelogger.conf import settings
from changelogger.conf.models import VersionedFile
from changelogger.exceptions import ValidationException
from changelogger.models.domain_models import ChangelogUpdate
from changelogger.utils import cached_compile


def check(
    sys_exit: bool = typer.Option(
        False,
        "--sys-exit",
        "--fail",
        help="Exit with a status of 2 if any versioned files are invalid.",
    ),
) -> None:
    """Checks the versioned files for any unparsable sections which do not match
    the Changelogger configuration and reports them.
    """
    try:
        _check_changelog()
        _check_versioned_files()
    except ValidationException as e:
        print(f"[bold red]Error:[/bold red] {str(e)}")
        if sys_exit:
            raise typer.Exit(code=2)
    else:
        print(
            ":white_heavy_check_mark: [bold green]All versioned files are valid![/bold green]"
        )


def _check_changelog() -> None:
    """Validates the specified versioned files are parsable and updatable."""
    # Validate there's at least 1 version
    # Point of Failure 0
    all_versions = changelog.get_all_versions()
    if not all_versions:
        raise ValidationException(
            "Expected there to be at least 1 version; None found."
        )

    # Validate all release notes are parseable for all versions
    # Point of Failure 1
    changelog_versions = ["Unreleased", *all_versions, None]
    for new_version, old_version in zip(
        changelog_versions, changelog_versions[1:]
    ):
        try:
            changelog.get_release_notes(new_version, old_version)  # type: ignore
        except Exception as e:
            raise ValidationException(
                f"Failed to validate notes for version {new_version}: {str(e)}."
            )

    # Validate there are links in the expected format for all versions
    # Point of Failure 2
    sorted_versions = changelog.get_sorted_versions()
    all_links = changelog.get_all_links()
    for prev_version, version in zip(sorted_versions, sorted_versions[1:]):
        link = all_links.get(version)
        if not link:
            raise ValidationException(
                f"Could not find the link for version {version}"
            )

        # Point of Failure 3
        if f"{prev_version}...{version}" not in link:
            raise ValidationException(
                f"Link is incorrect for version {version}"
            )

    link = all_links.get("Unreleased")
    # Point of Failure 4
    if not link:
        raise ValidationException(
            "Could not find the link for unreleased changes."
        )

    # Point of Failure 5
    if f"{all_versions[0]}...HEAD" not in link:
        raise ValidationException(
            "Link is incorrect for the unreleased changes."
        )

    # Point of Failure 6
    if sorted_versions[0] not in all_links:
        raise ValidationException(
            f"Could not find the link for version {sorted_versions[0]}"
        )


def _check_versioned_files() -> None:
    """For each of the user-specified and default versioned files, check
    that a search for the pattern over the files content results in a find.
    """

    # Contrive a fake update so we can check if the pattern would have been
    # found.
    old_version = changelog.get_latest_version()
    update = ChangelogUpdate(
        new_version=old_version.bump_minor(),
        old_version=old_version,
        release_notes=_unreleased_notes(),
    )

    for version_file in settings.VERSIONED_FILES:
        _check_versioned_file(version_file, update)


def _check_versioned_file(
    file: VersionedFile, update: ChangelogUpdate
) -> None:
    """Renders the versioned files pattern with an update and confirms
    there's a match.
    """

    pattern = templating.render_pattern(file, update)
    content = file.rel_path.read_text()
    if cached_compile(pattern).search(content):
        return

    raise ValidationException(
        f"Could not find the pattern `[bright_blue]{file.pattern}[/bright_blue]` "
        f'in the versioned file "{file.rel_path}".\n\n'
        f"Rendered pattern used when searching: [bright_blue]{pattern}[/bright_blue]."
    )

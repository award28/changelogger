from rich import print

from changelogger import changelog
from changelogger.exceptions import ValidationException


def check(
    sys_exit: bool = False,
) -> None:
    """Checks the Changelog file for any parts which do not meet changelogger's
    expectations and reports them to the user. Can optionally system exit
    for CI/CD failure.
    """
    try:
        _check()
    except ValidationException as e:
        print(f"[bold red]Error:[/bold red] {str(e)}")
        if sys_exit:
            exit(1)
    else:
        print(
            ":white_heavy_check_mark: [bold green]All versioned files are valid![/bold green]"
        )


def _check() -> None:
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

from rich import print
from changelogger.commands.exceptions import ValidationException
from changelogger.management import changelog

def check(
    sys_exit: bool = False,
) -> None:
    try:
        _check()
    except ValidationException as e:
        print(f"[bold red]Error: [/bold red] {str(e)}")
        if sys_exit:
            exit(1)

def _check() -> None:
    """Validates the specified versioned files are parsable and updatable.
    """
    # Validate there's at least 1 version
    all_versions = changelog.get_all_versions()
    if not all_versions:
        raise ValidationException("Expected there to be at least 1 version; None found.")

    # Validate all release notes are parseable for all versions
    changelog_versions = ["Unreleased", *all_versions, "LINKS"]
    for version, prev_version in zip(changelog_versions, changelog_versions[1:]):
        try:
            changelog.get_release_notes(version, prev_version)
        except:
            raise ValidationException(f"Failed to validate notes for version {version}")

    # Validate there are links in the expected format for all versions
    sorted_versions = changelog.get_sorted_versions()
    all_links = changelog.get_all_links()
    for prev_idx, version in enumerate(sorted_versions[1:]):
        link = all_links.get(version)
        if not link:
            raise ValidationException(f"Could not find the link for version {version}")

        prev_version = sorted_versions[prev_idx]
        if f"{prev_version}...{version}" not in link:
            raise ValidationException(f"Link is incorrect for version {version}")

    link = all_links.get("Unreleased")
    if not link:
        raise ValidationException(f"Could not find the link for unreleased changes.")

    if f"{all_versions[0]}...HEAD" not in link:
        raise ValidationException(f"Link is incorrect for the unreleased changes.")

    if sorted_versions[0] not in all_links:
        raise ValidationException(f"Could not find the link for version {sorted_versions[0]}")

    print(":white_heavy_check_mark: [bold green]validated![/bold green]")

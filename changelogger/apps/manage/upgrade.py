import semver

from changelogger.commands.domain_models import ChangelogUpdate, SemVerType

from changelogger.management import changelog


def upgrade(
    version_to_bump: SemVerType,
    confirm: bool = True,
    prompt_changelog: bool = True,
) -> None:
    """Upgrades all versioned files, as specified in the changelogger config file.
    """
    old_version = changelog.get_latest_version()
    bump = getattr(semver, f"bump_{version_to_bump.value}")
    new_version = bump(old_version)
    print(new_version)

    release_notes = changelog.get_release_notes("Unreleased", old_version)
    update = ChangelogUpdate(
        old_version=old_version,
        new_version=new_version,
        release_notes=release_notes,
    )

    print(update)
    # if prompt_changelog:
    #     update = mgmt_prompts.prompt_unreleased_changelog(update)

    # if confirm:
    #     prompts.confirm(update)

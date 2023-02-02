import semver

from dataclasses import dataclass
from changelogger.commands.domain_models import SemVerType

from changelogger.manage import utils


@dataclass
class UpgradeRequest:
    version_to_bump: SemVerType
    confirm: bool = True
    prompt_changelog: bool = True


def upgrade(
    version_to_bump: SemVerType,
    confirm: bool = True,
    prompt_changelog: bool = True,
) -> None:
    """Upgrades all versioned files, as specified in the changelogger config file.
    """
    req = UpgradeRequest(
        version_to_bump=version_to_bump,
        confirm=confirm,
        prompt_changelog=prompt_changelog,
    )
    _upgrade(req)

def _upgrade(req: UpgradeRequest) -> None:
    old_version = utils.get_latest_version()
    bump = getattr(semver, f"bump_{req.version_to_bump.value}")
    new_version = bump(old_version)
    print(new_version)

    release_notes = utils.get_release_notes("Unreleased", old_version)
    print(release_notes)

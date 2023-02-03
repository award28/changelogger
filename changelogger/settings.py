from importlib import resources
from pathlib import Path

from pydantic import BaseModel

import yaml


DEFAULT_CHANGELOG_FILE = "CHANGELOG.md"

CHANGELOGGER_FILE_NAME = ".changelogger.yml"
CHANGELOGGER_FILE = Path(CHANGELOGGER_FILE_NAME)

ASSETS = resources.files('assets')
DEFAULT_CHANGELOGGER_FILE = ASSETS.joinpath(CHANGELOGGER_FILE_NAME)


class _Config(BaseModel):
    changelog_file: Path = Path(DEFAULT_CHANGELOG_FILE)
    default_behavior: bool = True


_config = _Config()
if CHANGELOGGER_FILE.exists():
    changelogger = yaml.safe_load(CHANGELOGGER_FILE.read_text())
    _config = _Config(**changelogger.get('config', {}))


CHANGELOG_FILE = _config.changelog_file
DEFAULT_BEHAVIOR = _config.default_behavior

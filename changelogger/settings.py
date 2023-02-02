from pathlib import Path

from pydantic import BaseModel

import yaml

DEFAULT_CHANGELOG_FILE = "CHANGELOG.md"
CHANGELOGGER_FILE = ".changelogger.yml"

class _Config(BaseModel):
    changelog_file: Path = Path(DEFAULT_CHANGELOG_FILE)
    default_behavior: bool = True


_config = _Config()
if (changelogger_file := Path(CHANGELOGGER_FILE)).exists():
    changelogger = yaml.safe_load(changelogger_file.read_text())
    _config = _Config(**changelogger.get('config', {}))


CHANGELOG_FILE = _config.changelog_file
DEFAULT_BEHAVIOR = _config.default_behavior


"""
default_behavior: bool = typer.Option(
    True,
    envvar="CHANGELOGGER_DEFAULT_BEHAVIOR",
    help="If true, the default behaviour for the changelog file will be used.",
),
config_file: str = typer.Option(
    ".changelogger.yml",
    envvar="CHANGELOGGER_FILE",
    help="The relative path of the changelogger config file.",
),
changelog_file: str = typer.Option(
    "CHANGELOG.md",
    envvar="CHANGELOGGER_CHANGELOG_FILE",
    help="The relative path of the changelog file.",
)
"""

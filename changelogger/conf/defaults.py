from importlib import resources
from pathlib import Path

DEFAULT_CHANGELOG_PATH = Path("CHANGELOG.md")

DEFAULT_OVERVIEW_JINJA_PATTERN = (
    r"### \[Unreleased\]([\s\S]*)### \[{{ old_version }}]"
)
DEFAULT_LINKS_JINJA_PATTERN = r"\[Unreleased\]:.*\n"

DEFAULT_OVERVIEW_JINJA_PATH = resources.files("changelogger").joinpath(
    "assets/.cl.overview.jinja2"
)
DEFAULT_LINKS_JINJA_PATH = resources.files("changelogger").joinpath(
    "assets/.cl.links.jinja2"
)

CHANGELOGGER_PATH = Path(".changelogger.yml")

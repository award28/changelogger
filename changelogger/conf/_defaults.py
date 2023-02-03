from importlib import resources
from pathlib import Path


DEFAULT_CHANGELOG_PATH = Path("CHANGELOG.md")

DEFAULT_OVERVIEW_JINJA_PATTERN = r"### \[Unreleased\]([\s\S]*)### \[{{ old_version }}]"
DEFAULT_LINKS_JINJA_PATTERN = r"\[Unreleased\]:.*\n"

with (
    resources.path("assets", ".cl.overview.jinja2") as overview_path,
    resources.path("assets", ".cl.links.jinja2") as links_path,
):
    DEFAULT_OVERVIEW_JINJA_PATH = overview_path
    DEFAULT_LINKS_JINJA_PATH = links_path


CHANGELOGGER_PATH = Path(".changelogger.yml")

from pathlib import Path

DEFAULT_CHANGELOG_PATH = Path("CHANGELOG.md")

DEFAULT_OVERVIEW_JINJA_PATTERN = (
    r"### \[Unreleased\]([\s\S]*)### \[{{ old_version }}]"
)
DEFAULT_LINKS_JINJA_PATTERN = r"\[Unreleased\]:.*\n"

DEFAULT_OVERVIEW_JINJA_PATH = Path(".cl.overview.jinja2")
DEFAULT_LINKS_JINJA_PATH = Path(".cl.links.jinja2")

DEFAULT_TEMPLATES_DIR = Path(".changelogger/templates/")

CHANGELOGGER_NAME = ".changelogger.yml"

CHANGELOGGER_PATH = (
    (p1 := Path(CHANGELOGGER_NAME)).exists()
    and p1
    or (p2 := Path(".changelogger/").joinpath(CHANGELOGGER_NAME)).exists()
    and p2
    or (p3 := Path(".github/").joinpath(CHANGELOGGER_NAME)).exists()
    and p3
    or p1
)

CHANGELOGGER_VERSION = "0.11.4"

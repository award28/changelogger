from importlib import resources

from changelogger.conf.models import ChangeloggerConfig

_config = ChangeloggerConfig.from_config_or_default()

DEBUG = False

CHANGELOG_PATH = _config.changelog.rel_path

CHANGELOG_JINJA = resources.files("changelogger").joinpath(
    "templates/changelog.md.jinja2",
)

TEMPLATES_DIR = _config.templates_dir

OVERVIEW_JINJA_PATTERN = _config.changelog.overview.pattern
OVERVIEW_JINJA_PATH = _config.changelog.overview.jinja_rel_path

LINKS_JINJA_PATTERN = _config.changelog.links.pattern
LINKS_JINJA_PATH = _config.changelog.links.jinja_rel_path

VERSIONED_FILES = _config.versioned_files
VERSIONED_FILES.extend(_config.changelog.as_versioned_files())

HAS_DEFAULTS = _config.changelog.has_defaults()

# THIS MUST BE IMPORTED LAST
try:
    from changelogger.conf._settings_override import *  # nopycln: import
except:
    pass

from changelogger.conf.models import ChangeloggerConfig

_config = ChangeloggerConfig.from_config_or_default()

CHANGELOG_PATH = _config.changelog.rel_path

OVERVIEW_JINJA_PATTERN = _config.changelog.overview.pattern
OVERVIEW_JINJA_PATH = _config.changelog.overview.jinja_rel_path

LINKS_JINJA_PATTERN = _config.changelog.links.pattern
LINKS_JINJA_PATH = _config.changelog.links.jinja_rel_path

VERSIONED_FILES = _config.versioned_files
VERSIONED_FILES.extend(_config.changelog.as_versioned_files())

HAS_DEFAULTS = _config.changelog.has_defaults()

DEBUG = True

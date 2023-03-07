from changelogger.app.commands.check import check
from changelogger.conf import settings


def precommit(files: list[str]) -> None:
    if any(str(file.rel_path) in files for file in settings.VERSIONED_FILES):
        check(sys_exit=True, files=files)

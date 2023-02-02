import typer

from changelogger.manage.context import ManageCtx
from changelogger.manage.upgrade import upgrade
from changelogger.manage.check import check
from changelogger.manage.content import content


app = typer.Typer()
app.command()(upgrade)
app.command()(check)
app.command()(content)

@app.callback()
def manage(
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
):
    """Management commands for changelog and other versioned files,
    as specified in the changelogger config file.
    """
    ManageCtx.set(
        default_behavior=default_behavior,
        config_file=config_file,
        changelog_file=changelog_file,
    )

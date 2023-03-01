import typer

from changelogger.app.manage.commands.check import check
from changelogger.app.manage.commands.content import content
from changelogger.app.manage.commands.upgrade import upgrade
from changelogger.app.manage.commands.versions import versions

app = typer.Typer()
app.command()(upgrade)
app.command()(check)
app.command()(content)
app.command()(versions)


@app.callback()
def manage():
    """Management commands for changelog and other versioned files,
    as specified in the changelogger config file.
    """

import typer

from changelogger.apps.manage.commands.upgrade import upgrade
from changelogger.apps.manage.commands.check import check
from changelogger.apps.manage.commands.content import content


app = typer.Typer()
app.command()(upgrade)
app.command()(check)
app.command()(content)

@app.callback()
def manage():
    """Management commands for changelog and other versioned files,
    as specified in the changelogger config file.
    """


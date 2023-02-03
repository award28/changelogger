import typer

from .upgrade import upgrade
from .check import check
from .content import content


app = typer.Typer()
app.command()(upgrade)
app.command()(check)
app.command()(content)

@app.callback()
def manage():
    """Management commands for changelog and other versioned files,
    as specified in the changelogger config file.
    """


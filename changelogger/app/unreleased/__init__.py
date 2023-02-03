import typer

from changelogger.app.unreleased.commands.add import add
from changelogger.app.unreleased.commands.content import content

app = typer.Typer()
app.command()(add)
app.command()(content)


@app.callback()
def unreleased():
    """Commands for the unreleased section of the changelog."""

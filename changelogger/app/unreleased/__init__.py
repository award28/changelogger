import typer

from changelogger.app.unreleased._commands.add import add

app = typer.Typer()
app.command()(add)


@app.callback()
def unreleased():
    """Commands for the unreleased section of the changelog."""

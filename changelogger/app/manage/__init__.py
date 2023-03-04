import typer

from changelogger.app.manage._commands.check import check
from changelogger.app.manage._commands.notes import notes
from changelogger.app.manage._commands.upgrade import upgrade
from changelogger.app.manage._commands.versions import versions

app = typer.Typer()
app.command()(upgrade)
app.command()(check)
app.command()(notes)
app.command()(versions)


@app.callback()
def manage():
    """Management commands for changelog and other versioned files,
    as specified in the changelogger config file.

    WARNING:
    This command has been deprecated and will be removed in version 0.12.0.
    All subcommands will now be available as top-level commands under
    the "changelogger" command.
    """

from pydantic import BaseModel
import typer

app = typer.Typer()

class UpgradeCmd(BaseModel):
    version_to_bump: str
    confirm: bool = True
    prompt_changelog: bool = True
    use_default_upgrade_config: bool = True
    changelogger_config_file: str | None = None
    changelog_file: str = 'CHANGELOG.md'


def config(
    version_to_bump: str,
    confirm: bool = True,
    prompt_changelog: bool = True,
    use_default_upgrade_config: bool = True,
    changelogger_config_file: str | None = None,
    changelog_file: str = 'CHANGELOG.md',
) -> 

@app.command()
def upgrade(

import typer
from rich import print

app = typer.Typer()

@app.command()
def hello() -> None:
    print(f"[bold red]Hello[/bold red]!")

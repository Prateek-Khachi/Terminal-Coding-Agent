import typer
from rich.console import Console

console = Console()

app = typer.Typer(
    name="codingagent",
    help="🤖 Terminal Coding Agent",
    no_args_is_help=True,
)


@app.command()
def version():
    """Show the application version."""
    console.print("[bold green]Terminal Coding Agent[/bold green]")
    console.print("Version: 0.1.0")


@app.command()
def doctor():
    """Check whether the coding agent environment is configured correctly."""
    console.print("[bold green]✓ Coding Agent is running[/bold green]")
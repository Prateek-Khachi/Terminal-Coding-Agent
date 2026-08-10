import typer
from rich.console import Console
from coding_agent.config import get_settings
from pathlib import Path

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

    settings = get_settings()

    console.print("[bold]Terminal Coding Agent — Environment Check[/bold]\n")

    # Configuration
    console.print("[green]✓[/green] Configuration loaded")

    # Workspace
    workspace = Path(settings.workspace).resolve()

    if workspace.exists() and workspace.is_dir():
        console.print(
            f"[green]✓[/green] Workspace accessible: {workspace}"
        )
    else:
        console.print(
            f"[red]✗[/red] Workspace not accessible: {workspace}"
        )

    # API key
    if settings.openai_api_key:
        console.print("[green]✓[/green] OpenAI API key configured")
    else:
        console.print("[yellow]⚠[/yellow] OpenAI API key not configured")
import typer

app = typer.Typer(
    help="🤖 Terminal Coding Agent"
)


@app.command()
def hello():
    """Simple test command."""
    print("Hello from Coding Agent!")


if __name__ == "__main__":
    app()
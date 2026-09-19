"""Command-line interface for ReproAgent."""

from typing import Annotated

import typer

from . import __version__

app = typer.Typer(
    name="reproagent",
    help="Audit whether open-source software can be reproduced.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Print the ReproAgent version."""

    typer.echo(f"ReproAgent {__version__}")


@app.command()
def run(
    repository_url: Annotated[
        str,
        typer.Argument(help="URL of the repository to reproduce."),
    ],
) -> None:
    """Show the Phase 0 placeholder for a reproduction run."""

    typer.echo(
        "The reproduction engine is not implemented yet; "
        f"no repository was cloned: {repository_url}"
    )


if __name__ == "__main__":
    app()

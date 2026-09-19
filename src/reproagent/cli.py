"""Command-line interface for ReproAgent."""

from pathlib import Path
from typing import Annotated

import typer

from . import __version__
from .config import get_settings
from .repo.clone import (
    CloneError,
    RunWorkspaceError,
    clone_repository,
    create_run_workspace,
)
from .repo.manifest import ManifestError, build_manifest
from .repo.urls import RepositoryUrlError, parse_github_url

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
    """Clone a GitHub repository and generate its structural manifest."""

    try:
        repository = parse_github_url(repository_url)
        run_workspace = create_run_workspace(get_settings().runs_dir)
        clone = clone_repository(
            repository.normalized_url,
            run_workspace.repository_path,
        )
        manifest = build_manifest(repository, clone)
    except (CloneError, ManifestError, RepositoryUrlError, RunWorkspaceError) as exc:
        typer.echo(f"Repository intake failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    workspace_path = manifest.workspace_path
    try:
        display_workspace = workspace_path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        display_workspace = workspace_path.as_posix()

    typer.echo("Repository intake complete.\n")
    typer.echo(f"Repository: {manifest.owner}/{manifest.repository_name}")
    typer.echo(f"Commit: {manifest.commit_sha}")
    typer.echo(f"Branch: {manifest.branch or '(detached)'}\n")
    typer.echo("Detected:")
    typer.echo(f"  README files       {len(manifest.documentation_files)}")
    typer.echo(f"  Dependency files   {len(manifest.dependency_files)}")
    typer.echo(f"  Tests              {'yes' if manifest.has_tests else 'no'}")
    typer.echo(f"  Dockerfile         {'yes' if manifest.has_dockerfile else 'no'}")
    typer.echo(f"  CI workflows       {'yes' if manifest.has_ci_workflows else 'no'}\n")
    typer.echo("Workspace:")
    typer.echo(display_workspace)


if __name__ == "__main__":
    app()

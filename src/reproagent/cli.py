"""Command-line interface for ReproAgent."""

import json
import re
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

_SUPPORTED_GOALS = {"auto", "install", "tests", "demo"}
_SAFE_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")

app = typer.Typer(
    name="reproagent",
    help="Audit whether open-source software can be reproduced.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"ReproAgent {__version__}")
        raise typer.Exit()


@app.callback()
def _main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the installed ReproAgent version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Reproducibility auditing commands."""


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
    goal: Annotated[
        str,
        typer.Option(
            "--goal",
            help="Target workflow: auto, install, tests, or demo.",
        ),
    ] = "auto",
    runs_dir: Annotated[
        Path | None,
        typer.Option(
            "--runs-dir",
            help="Directory in which to create the isolated intake workspace.",
            path_type=Path,
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit one machine-readable JSON result."),
    ] = False,
) -> None:
    """Clone a GitHub repository and generate its structural manifest.

    Intake does not install dependencies or execute target code.
    """

    normalized_goal = goal.strip().lower()
    if normalized_goal not in _SUPPORTED_GOALS:
        raise typer.BadParameter(
            f"must be one of: {', '.join(sorted(_SUPPORTED_GOALS))}",
            param_hint="--goal",
        )

    try:
        repository = parse_github_url(repository_url)
        configured_runs_dir = runs_dir if runs_dir is not None else get_settings().runs_dir
        run_workspace = create_run_workspace(configured_runs_dir)
        clone = clone_repository(
            repository.normalized_url,
            run_workspace.repository_path,
        )
        manifest = build_manifest(repository, clone)
    except (CloneError, ManifestError, RepositoryUrlError, RunWorkspaceError) as exc:
        _error(f"Repository intake failed: {exc}", json_output=json_output)
        raise typer.Exit(code=1) from exc

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "command": "run",
                    "goal": normalized_goal,
                    "manifest": manifest.model_dump(mode="json"),
                    "run_id": run_workspace.run_id,
                    "run_directory": str(run_workspace.run_dir),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return

    workspace_path = manifest.workspace_path
    try:
        display_workspace = workspace_path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        display_workspace = workspace_path.as_posix()

    typer.echo("Repository intake complete.\n")
    typer.echo(f"Goal: {normalized_goal}")
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


@app.command()
def report(
    run_id: Annotated[
        str,
        typer.Argument(help="Run identifier whose report should be displayed."),
    ],
    runs_dir: Annotated[
        Path | None,
        typer.Option(
            "--runs-dir",
            help="Directory containing run artifacts.",
            path_type=Path,
        ),
    ] = None,
) -> None:
    """Display a completed run's human-readable report."""

    run_directory = _resolve_run_directory(run_id, runs_dir)
    report_path = run_directory / "report.md"
    if not report_path.is_file():
        _error(
            f"No report.md artifact exists for run {run_id!r}.",
            json_output=False,
        )
        raise typer.Exit(code=1)
    try:
        content = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        _error(f"Could not read report for run {run_id!r}: {exc}", json_output=False)
        raise typer.Exit(code=1) from exc
    typer.echo(content, nl=not content.endswith("\n"))


@app.command("runs")
def list_runs(
    runs_dir: Annotated[
        Path | None,
        typer.Option(
            "--runs-dir",
            help="Directory containing run artifacts.",
            path_type=Path,
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit one machine-readable JSON result."),
    ] = False,
) -> None:
    """List run directories that contain persisted report artifacts."""

    root = (runs_dir if runs_dir is not None else get_settings().runs_dir).expanduser()
    try:
        root = root.resolve()
        entries = sorted(
            (
                entry
                for entry in root.iterdir()
                if entry.is_dir()
                and not entry.is_symlink()
                and _SAFE_RUN_ID.fullmatch(entry.name)
                and (entry / "report.md").is_file()
            ),
            key=lambda entry: entry.name,
        )
    except OSError as exc:
        _error(f"Could not list runs: {exc}", json_output=json_output)
        raise typer.Exit(code=1) from exc

    rows = [
        {
            "run_id": entry.name,
            "report": str(entry / "report.md"),
        }
        for entry in entries
    ]
    if json_output:
        typer.echo(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    elif not rows:
        typer.echo("No completed runs found.")
    else:
        for row in rows:
            typer.echo(f"{row['run_id']}  {row['report']}")


def _resolve_run_directory(run_id: str, runs_dir: Path | None) -> Path:
    if not _SAFE_RUN_ID.fullmatch(run_id):
        _error("Run ID contains unsupported path characters.", json_output=False)
        raise typer.Exit(code=1)
    root = (runs_dir if runs_dir is not None else get_settings().runs_dir).expanduser()
    root = root.resolve()
    candidate = (root / run_id).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        _error("Run ID escapes the configured runs directory.", json_output=False)
        raise typer.Exit(code=1)
    if not candidate.is_dir():
        _error(f"Run directory not found for {run_id!r}.", json_output=False)
        raise typer.Exit(code=1)
    return candidate


def _error(message: str, *, json_output: bool) -> None:
    if json_output:
        typer.echo(json.dumps({"error": message}, ensure_ascii=False), err=True)
    else:
        typer.echo(message, err=True)


if __name__ == "__main__":
    app()

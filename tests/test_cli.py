from typer.testing import CliRunner

from reproagent.cli import app

runner = CliRunner()


def test_help_command_exits_successfully() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Audit whether open-source software can be reproduced" in result.stdout


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "ReproAgent 0.1.0"


def test_run_command_is_a_placeholder() -> None:
    repository_url = "https://github.com/example/project"
    result = runner.invoke(app, ["run", repository_url])

    assert result.exit_code == 0
    assert "reproduction engine is not implemented yet" in result.stdout
    assert repository_url in result.stdout

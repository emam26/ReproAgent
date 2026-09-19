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


def test_run_command_rejects_unsupported_url() -> None:
    result = runner.invoke(app, ["run", "https://gitlab.com/example/project"])

    assert result.exit_code == 1
    assert "Only HTTPS GitHub repository URLs are supported" in result.stderr

# ReproAgent

ReproAgent is a Python project for auditing whether open-source software can be
reproduced from a clean environment. The long-term project will inspect a
repository, execute its documented workflow in isolation, and produce
evidence-backed results.

## Development status

Phase 0 (Project Foundation) is complete. The current CLI only provides the
project version and a placeholder `run` command; repository intake and the
reproduction engine are not implemented yet.

## Installation

ReproAgent requires Python 3.11 or newer. Create and activate a virtual
environment, then install the project with its development dependencies:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
```

Run the test suite and linter with:

```bash
pytest
ruff check .
```

## CLI

```bash
reproagent --help
reproagent version
reproagent run https://github.com/example/project
```

The `run` command is currently a placeholder and does not clone or execute a
repository.

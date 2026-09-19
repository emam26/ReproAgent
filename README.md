# ReproAgent

ReproAgent is a Python project for auditing whether open-source software can be
reproduced from a clean environment. The long-term project will inspect a
repository, execute its documented workflow in isolation, and produce
evidence-backed results.

## Development status

Phase 0 (Project Foundation) and Phase 1 (Repository Intake & Manifest) are
complete. The current CLI accepts supported public GitHub URLs, clones them
into an isolated run workspace, and generates a deterministic structural
manifest. Full reproduction, dependency installation, and execution are not
implemented yet.

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

The `run` command performs repository intake only. It does not install
dependencies, execute target code, run target tests, or perform reproduction.

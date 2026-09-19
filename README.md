# ReproAgent

ReproAgent is a Python project for auditing whether open-source software can be
reproduced from a clean environment. The long-term project will inspect a
repository, execute its documented workflow in isolation, and produce
evidence-backed results.

## Development status

Phases 0–4 are complete. The current CLI accepts supported public GitHub URLs,
clones them into an isolated run workspace, and generates a deterministic
structural manifest. Docker sandbox infrastructure is available for future
execution phases, but full reproduction, dependency installation, and CLI
execution are not implemented yet.

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

## Docker sandbox

Phase 2 adds reusable Docker sandbox infrastructure for future execution
phases. It uses disposable, labeled containers based on `python:3.11-slim`,
mounts only the requested workspace at `/workspace`, and applies CPU, memory,
PID, timeout, capability, and `no-new-privileges` limits. Docker must be
available for sandbox integration tests. The sandbox never falls back to host
execution and only removes containers it created. Docker isolation is not a
complete security boundary; later phases will add stronger policy controls.

## Run state and event log

Phase 3 adds a local SQLite control plane for typed run snapshots, legal
lifecycle transitions, and append-only audit events. It does not add LLM
reasoning, autonomous execution, or alter the Docker sandbox. See
[`docs/STATE_AND_EVENTS.md`](docs/STATE_AND_EVENTS.md) for the lifecycle,
persistence guarantees, and API boundary.

## LLM provider layer

Phase 4 adds strict provider-independent request, decision, response, usage,
error, and retry models with offline mocks plus explicit Gemini and Groq REST
adapters. It does not perform analysis or autonomous execution. See
[`docs/LLM_PROVIDERS.md`](docs/LLM_PROVIDERS.md) for configuration and
structured-output guarantees.

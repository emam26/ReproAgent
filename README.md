# ReproAgent

ReproAgent is a local reproducibility auditor for public Python and AI/ML
repositories. It asks a practical question:

> Can a new user reproduce this project from a clean environment, and what
> objective evidence supports the answer?

The system performs deterministic repository intake and analysis, creates a
bounded documented-first plan, runs target commands only inside Docker,
captures failures and diagnosis evidence, objectively verifies recorded facts,
reruns successful workflows in a fresh clean-room workspace, and writes a
schema-versioned report. An LLM may interpret ambiguity; it never decides
whether reproduction succeeded.

This is research and engineering software, not a hosted service. PyPI
publication, public dashboard hosting, paper-result reproduction, and
production multi-tenant execution are not included.

## Current capabilities

* public HTTPS GitHub intake with exact commit capture and structural manifests;
* deterministic-first Python project analysis and finite plan generation;
* Docker-only sequential execution with resource, timeout, network, and output
  bounds;
* typed diagnostics, optional provider-independent LLM reasoning, controlled
  repair primitives, objective verification, final status, clean-room reruns,
  observability, evaluation contracts, and evidence-backed reports;
* a local CLI, optional local FastAPI control API, and local React/TypeScript
  dashboard;
* offline mock-provider tests and controlled Docker fixtures.

The public `audit` workflow records deterministic diagnosis when a run fails.
It does not invent or silently apply an automatic source repair: the existing
repair tools are exposed as bounded library capabilities and a future phase can
wire a complete repair policy into the public workflow when that is justified.

## Installation from source

Python 3.11 or newer and Docker are required for target execution. Docker is
not required for deterministic unit tests.

```bash
git clone https://github.com/emam26/ReproAgent.git
cd ReproAgent
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -e .
```

For development and API tests:

```bash
python -m pip install -e ".[dev]"
```

The optional API runtime is isolated from CLI-only users:

```bash
python -m pip install -e ".[api]"
```

## Quick start

Inspect a repository without executing its code:

```bash
reproagent inspect https://github.com/user/repository --no-ai
```

Run the bounded audit:

```bash
reproagent audit https://github.com/user/repository --goal auto --no-ai
```

The command reports the run ID, objective status, verification level, attempts,
repairs, report path, and clean-room package path when available. Use a private
runs directory if reports may contain project-specific information:

```bash
reproagent audit https://github.com/user/repository --runs-dir ./local-runs
reproagent runs --runs-dir ./local-runs
reproagent status <run-id> --runs-dir ./local-runs
reproagent report <run-id> --runs-dir ./local-runs
```

Other public commands are `doctor`, `config`, `cleanup`, `version`, and the
compatibility `run` intake-only command. `cleanup` removes only containers
labelled as ReproAgent-managed and can be restricted to one run ID. There is no
arbitrary shell command or arbitrary host-path command in the CLI.

## LLM providers

The default analysis path is deterministic and offline. `--no-ai` explicitly
disables optional LLM interpretation and diagnosis. If AI is enabled, provider
selection and credentials come only from environment variables:

```text
LLM_PROVIDER=mock|gemini|groq
LLM_MODEL=<provider model when required>
GEMINI_API_KEY=<secret, never committed>
GROQ_API_KEY=<secret, never committed>
```

Use `.env.example` as a names-only template. Keys are never printed, persisted,
returned by the API, placed in reports/events/commands, or bundled into the
dashboard. Normal tests use `MockLLMProvider` and do not consume provider quota.

## Local API and dashboard

Start the local API on loopback:

```bash
reproagent serve
```

It exposes `/api/v1/health`, `/version`, audit submission, run listing/detail,
events, reports, and persisted-plan clean-room replay. The API is explicitly a
local development/control API, not a hardened multi-tenant public execution
service. See [`docs/API.md`](docs/API.md).

The dashboard is not part of the Python wheel. From a source checkout:

```bash
cd frontend
npm install
npm run dev
```

It serves on `127.0.0.1:5173` and proxies to the local API on port 8000. It
provides new-audit, runs, run-detail, timeline, evidence, and report views. See
[`docs/DASHBOARD.md`](docs/DASHBOARD.md).

## Architecture

```text
repository URL
    ↓
intake → analysis → planning → Docker sandbox → execution
                                      ↓
                         diagnostics / bounded reasoning
                                      ↓
                   objective verification → clean-room rerun
                                      ↓
                              status → report
```

The control plane persists SQLite state and append-only events. The central
separation is:

```text
LLM = reasoning       Tools = facts + execution
State = control       Verifier = truth
Docker = isolation
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and the focused documents in
[`docs/`](docs/).

## Example result

```text
Reproducibility audit complete.

Run ID: 3e3d...
Status: REPRODUCED
Verification: L2
Attempts: 2
Repairs: 0
Report: runs/3e3d.../report.md
Reproduction package: runs/3e3d.../clean-room-runs/clean-room-.../
```

`REPRODUCED` requires objective target evidence and a successful clean-room
rerun. `PARTIAL`, `BLOCKED`, `FAILED`, and `UNSAFE` are not success states.

## Security model and limitations

Target repository code is untrusted. ReproAgent does not execute it on the
host, does not mount host credentials or the Docker socket, drops Linux
capabilities, enables `no-new-privileges`, applies resource/workspace bounds,
and denies network access unless a plan explicitly requires it. Git intake is
noninteractive and avoids recursive submodules and LFS smudge.

Docker is defense in depth, not a perfect hostile-code boundary. Do not run the
tool against highly sensitive material, do not expose the Docker daemon socket,
and do not expose the local API publicly. Public GitHub HTTPS repositories and
primarily CPU-runnable Python projects are the supported V1 scope; private
repositories, arbitrary operating systems, multi-GPU training, giant datasets,
and paper-result reproduction are outside this release.

## Development and testing

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
```

Docker integration tests are marked separately:

```bash
pytest -m docker
```

Frontend validation is run from `frontend/` with `npm run lint`, `npm test`,
and `npm run build`. The CI workflow runs ordinary Python and frontend checks;
Docker integration remains an explicit local/controlled operation.

## Project status and license

Phases 0–23 are implemented in the repository roadmap. Phase 24 activities
(publication, deployment, and production infrastructure) have not started.

No license has been selected in this repository. Contributors should not infer
permission to redistribute or deploy the project until the maintainers make and
document that legal decision.

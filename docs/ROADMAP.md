# ReproAgent Implementation Roadmap

## Working Rule

Build one phase at a time.

Do not begin a later phase merely because it seems convenient.

Statuses:

```text
NOT STARTED
IN PROGRESS
DONE
BLOCKED
```

---

# Current Phase

## Phase 9 — Controlled Repair Tools

**Status: DONE**

---

# Phase 0 — Project Foundation

## Goal

Create a clean Python repository that can be safely extended phase by phase.

## Build

* `AGENTS.md`
* `README.md`
* `pyproject.toml`
* `.gitignore`
* `.env.example`
* `docs/PROJECT_SPEC.md`
* `docs/ROADMAP.md`
* Python `src/` package
* CLI entrypoint
* configuration placeholder
* pytest setup
* Ruff setup
* initial tests

Expected initial project structure:

```text
ReproAgent/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── docs/
│   ├── PROJECT_SPEC.md
│   └── ROADMAP.md
│
├── src/
│   └── reproagent/
│       ├── __init__.py
│       ├── cli.py
│       └── config.py
│
├── tests/
│   ├── __init__.py
│   └── test_cli.py
│
└── runs/
    └── .gitkeep
```

## Acceptance Criteria

Phase 0 is DONE only when:

* package installs successfully,
* `pytest` passes,
* Ruff passes,
* `reproagent --help` works,
* `reproagent version` works,
* `.env` is ignored,
* `runs/` generated files are ignored,
* project documentation exists,
* no future-phase functionality was prematurely added.

---

# Phase 1 — Repository Intake & Manifest

**Status: DONE**

## Goal

Given a public Git repository URL, clone it and deterministically inspect its structure.

No LLM should be required.

## Build

* repository URL validation,
* clone repository,
* capture exact commit SHA,
* working directory management,
* repository manifest,
* important-file detection,
* basic repository metadata.

Detect files including:

```text
README*
INSTALL*
requirements*.txt
pyproject.toml
setup.py
setup.cfg
environment.yml
Dockerfile*
Makefile
tox.ini
pytest.ini
.github/workflows/*
tests/
examples/
demo/
scripts/
configs/
```

## Output Example

```json
{
  "repository": "owner/project",
  "commit_sha": "abc123",
  "important_files": [
    "README.md",
    "requirements.txt"
  ],
  "has_tests": true
}
```

## Tests

Use controlled fixture repositories when possible.

Test:

* valid repository,
* invalid URL,
* clone failure,
* README detection,
* dependency-file detection,
* nested file detection.

## Acceptance Criteria

A supported repository produces a deterministic manifest without an LLM.

---

# Phase 2 — Docker Sandbox

**Status: DONE**

## Goal

Execute commands in a disposable isolated environment.

## Build

Conceptual API:

```text
Sandbox
DockerSandbox
create()
execute()
destroy()
```

Execution result should capture:

```text
command
stdout
stderr
exit_code
duration
timed_out
```

## Requirements

* target code must not execute on the host,
* timeout support,
* resource limits,
* container cleanup,
* controlled workspace mounting.

## Tests

Verify:

* normal command execution,
* stdout capture,
* stderr capture,
* exit code,
* timeout,
* cleanup,
* workspace behavior.

## Acceptance Criteria

A fixture project executes inside Docker and returns a structured execution result.

---

# Phase 3 — State, Actions & Event Log

**Status: DONE**

## Goal

Create the control plane before adding autonomous reasoning.

## Build

Typed concepts such as:

```text
RunState
Stage
AgentAction
ToolCall
ToolResult
Attempt
Event
RunOutcome
```

State flow:

```text
INTAKE
ANALYZE
PLAN
SETUP
EXECUTE
DEBUG
VERIFY
REPORT
DONE
```

Add persistence.

SQLite is preferred initially.

Add append-only event logging.

## Acceptance Criteria

A mock run can:

* transition between states,
* persist important state,
* reload after application restart,
* retain its event history.

---

# Phase 4 — LLM Provider Layer

**Status: DONE**

## Goal

Add hosted LLM reasoning without coupling ReproAgent to a vendor.

## Build

```text
LLMProvider interface
Provider implementation
Structured AgentDecision
API retry/error handling
Configuration
```

Possible environment configuration:

```text
LLM_PROVIDER
LLM_MODEL
GEMINI_API_KEY
GROQ_API_KEY
```

## Important

No autonomous execution yet.

First prove:

```text
structured application context
       ↓
LLM provider
       ↓
valid typed AgentDecision
```

## Testing

Mock API calls in unit tests.

Normal tests must not consume free API quota.

## Acceptance Criteria

Core application logic can consume provider-independent structured decisions.

---

# Phase 5 — Repository Analysis

**Status: DONE**

## Goal

Turn a repository manifest into a structured understanding of how the project should run.

## Relevant Context

Feed only likely-important content such as:

```text
README
INSTALL
requirements
pyproject
setup.py
Dockerfile
Makefile
CI workflows
examples
```

## Produce

```text
RepositoryAnalysis
```

Attempt to determine:

* runtime,
* Python version,
* framework,
* dependency installation,
* test command,
* demo command,
* GPU requirement,
* required assets,
* environment variables.

## Acceptance Criteria

A small controlled repository set produces sensible structured analyses.

No execution repair loop yet.

---

# Phase 6 — Reproduction Planner

**Status: DONE**

## Goal

Turn repository analysis into a finite, inspectable reproduction plan.

The planner does not execute commands.

Flow:

```text
RepositoryAnalysis
       ↓
ReproductionPlanner
       ↓
ReproductionPlan
```

## Build

* ordered typed plan steps,
* documented-first evidence priority,
* evidence provenance,
* command and working-directory safety checks,
* step, command, and timeout bounds,
* explicit risk classification.

## Acceptance Criteria

Controlled analyses produce deterministic, bounded plans without executing them.

---

# Phase 7 — Initial Execution Engine

**Status: DONE**

## Goal

Execute a finite `ReproductionPlan` inside the Phase 2 Docker sandbox and
persist objective evidence through the Phase 3 state/event control plane.

Core loop:

```text
ReproductionPlan
       ↓
Docker sandbox
       ↓
Attempt / ToolCall / ToolResult
       ↓
bounded logs and ordered events
```

## Build

* Docker-only sequential plan execution with no host fallback,
* exact owned-container lifecycle and cleanup,
* per-step and overall timeout enforcement,
* deterministic failure classification,
* bounded and redacted state, command, event, and log artifacts,
* first-failure stop policy with no automatic repair.

## Acceptance Criteria

Controlled successful, failing, and timing-out fixture repositories complete the
manifest-to-analysis-to-plan-to-Docker pipeline. Execution order, output,
errors, exit codes, timeouts, state events, and exact container cleanup are
verified. A workflow success remains distinct from a final reproducibility
verdict.

---

# Phase 7.5 — Diagnostic & Verification Foundation

**Status: DONE**

## Goal

Convert raw execution failure into compact deterministic evidence before any
LLM diagnosis.

## Build

* typed failure taxonomy and bounded traceback/build/test/network extraction,
* PEP-aware requirement, version, marker, pip report, inspect, and check parsing,
* Docker-only environment fingerprint and pip diagnostic commands,
* AST import/dependency comparison with explicit heuristic mappings,
* bounded evidence builder and stable repeated-failure signatures,
* repository-local checkpoint, dataset, URL, LFS, submodule, and DVC indicators,
* typed objective verification contracts without final status classification.

## Acceptance Criteria

Major failure families, unknown failures, evidence bounds, secret redaction,
dependency formats, environment facts, import mappings, asset indicators, and
verification contracts have deterministic fixture coverage.

---

# Phase 8 — Autonomous Diagnosis

**Status: DONE**

## Goal

Turn compact deterministic evidence into a bounded structured diagnosis and a
permitted next action.

## Build

* deterministic-first diagnosis,
* strict structured hypotheses and evidence references,
* bounded LLM calls and diagnosis attempts,
* repeated-signature and repeated-diagnosis stopping,
* risk and action-policy enforcement,
* persistence through the Phase 3 event infrastructure.

## Acceptance Criteria

Mock-provider fixtures prove valid diagnosis, malformed-output rejection,
unsupported-action rejection, provenance, confidence/risk handling, repetition
stopping, call limits, and secret exclusion.

---

# Phase 9 — Controlled Repair Tools

**Status: DONE**

## Goal

Convert an accepted diagnosis into one finite policy-checked repair experiment.

## Build

* finite repair vocabulary,
* evidence, risk, reversibility, and expected-effect requirements,
* deterministic policy validation,
* bounded Python/dependency/asset experiment contracts,
* before/after signatures and objective evidence-improvement records,
* pure plan transformations with rollback,
* append-only repair events with no host execution or global Docker management.

## Acceptance Criteria

Each repair action and policy rejection has fixture coverage, including limits,
repetition blocking, persistence, unsafe inputs, and rollback metadata.

---

# Phase 10 — Controlled File Editing & Rollback

**Status: NOT STARTED**

## Goal

Allow minimal auditable workspace edits, exact diffs, and rollback, then wire the
controlled intake-to-retry pipeline for end-to-end fixtures.

## Build

* workspace-confined read, replacement, patch, diff, and rollback tools,
* path, symlink, file-size, patch-size, and changed-file limits,
* original/new hashes and `patches.diff` audit artifact,
* controlled CLI pipeline wiring,
* working, repaired, and policy-stopped Docker fixtures.

## Acceptance Criteria

Edits cannot escape the target workspace, exact changes are auditable and
reversible, retries remain Docker-only, and controlled end-to-end fixtures cover
success, repair, and clean stopping. Formal final verification remains later.

---

# Phase 11 — Safety Hardening

**Status: NOT STARTED**

## Goal

Treat repository code as potentially hostile.

## Review / Implement

* no host execution,
* no secret mounts,
* no Docker socket,
* capability dropping,
* no-new-privileges,
* memory limits,
* CPU limits,
* process limits,
* command timeout,
* download limits,
* network policy,
* workspace restrictions,
* unsafe-command handling.

Add terminal outcome:

```text
UNSAFE
```

## Acceptance Criteria

Safety tests demonstrate that prohibited host access and dangerous operations are rejected or isolated.

---

# Phase 12 — Evaluation Benchmark

**Status: NOT STARTED**

## Goal

Prove ReproAgent works beyond hand-picked demos.

## Dataset

Start with approximately:

```text
20 repositories
```

Later:

```text
50+
```

Include:

* healthy projects,
* old dependency projects,
* missing dependencies,
* incorrect README instructions,
* missing assets,
* runtime incompatibilities.

## Metrics

Track:

```text
intake success
analysis success
environment setup success
execution success
test success
full reproduction
partial reproduction
blocked
failed
repair success
human intervention
LLM calls
agent steps
runtime
```

## Later Comparisons

Potential experiments:

```text
LLM A vs LLM B
agent vs README-only baseline
repair loop vs no repair loop
```

## Acceptance Criteria

A reproducible evaluation command generates aggregate benchmark metrics.

---

# Phase 13 — API and Dashboard

**Status: NOT STARTED**

## Goal

Turn the proven engine into a usable product.

Do not begin before core evaluation works.

Potential API:

```text
POST /runs
GET /runs/{id}
GET /runs/{id}/events
GET /runs/{id}/report
```

Potential UI:

```text
repository
current stage
events
commands
errors
repairs
Git diff
verification
report
```

## Acceptance Criteria

A user can submit a repository and inspect the run without using the CLI.

---

# Phase 14 — Portfolio Polish

**Status: NOT STARTED**

## Goal

Make the project interview-ready.

Add:

* architecture diagram,
* demo video/GIF,
* benchmark results,
* failure taxonomy,
* example reports,
* security explanation,
* design tradeoffs,
* polished README.

README should explain:

```text
problem
why an agent is appropriate
architecture
safety
evaluation
results
limitations
example run
```

---

# Future Phase — Research Paper Reproduction

**Status: OUT OF V1 SCOPE**

Input:

```text
paper
+
repository
```

Additional workflow:

```text
extract reported experiment
↓
identify matching configuration/code
↓
run experiment
↓
compare reproduced metric
↓
analyze discrepancy
↓
generate claim-level report
```

Do not work on this until repository-level reproduction is reliable.

---

# Current Next Action

Phase 9 acceptance criteria have passed.

```text
Phase 9 → DONE
Phase 10 → NOT STARTED
```

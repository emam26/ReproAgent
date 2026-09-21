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

## Phase 16 — Observability

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

**Status: DONE**

## Goal

Allow minimal auditable workspace edits, exact diffs, and rollback, then wire the
controlled intake-to-retry pipeline for end-to-end fixtures.

## Build

* workspace-confined read, replacement, patch, diff, and rollback tools,
* path, symlink, file-size, patch-size, and changed-file limits,
* original/new hashes and `patches.diff` audit artifact,
* controlled execution-to-diagnosis-to-retry pipeline wiring,
* working, repaired, and policy-stopped Docker-backed fixtures.

## Acceptance Criteria

Edits cannot escape the target workspace, exact changes are auditable and
reversible, retries remain Docker-only, and controlled end-to-end fixtures cover
success, repair, and clean stopping. Formal final verification remains later.

---

# Phase 11 — Objective Verification Engine

**Status: DONE**

## Goal

Evaluate a finite verification contract using objective execution, environment,
output, and artifact evidence.

## Build

* strict verification level, check, evidence, and result models,
* deterministic installation, command, test, output, environment, and artifact checks,
* file type, size, and SHA-256 checks with workspace containment,
* explicit execution-failed, verification-failed, unavailable, and unspecified outcomes,
* no target command execution or LLM-derived proof.

## Acceptance Criteria

Fixture tests prove objective pass, execution failure, failed verification,
unavailable evidence, unspecified contracts, level handling, path containment,
file facts, and secret-safe bounded evidence.

---

# Phase 12 — Final Reproducibility Status

**Status: DONE**

## Goal

Compute a deterministic final reproduction status from objective evidence and
policy.

## Build

* separate `REPRODUCED`, `PARTIAL`, `BLOCKED`, `FAILED`, and `UNSAFE` models,
* deterministic rules over workflow, verification, safety, and clean-room facts,
* machine-readable reason and evidence references,
* no LLM-derived status authority.

## Acceptance Criteria

Status rules are exhaustively fixture-tested, including the distinction between
workflow success and reproduction, unavailable verification, unsafe findings,
and clean-room requirements.

---

# Phase 13 — Reporting + Run Artifacts

**Status: DONE**

## Goal

Produce useful schema-versioned run artifacts and an evidence-backed report.

## Build

* `run.json`, `report.md`, and real-data-only optional artifacts,
* documented versus agent-assisted reproduction sections,
* events, commands, environment, patches, and recipe serialization,
* secret-safe bounded report generation.

## Acceptance Criteria

Reports explain repository, commit, goal, documented setup, attempts, failures,
diagnosis, repairs, verification, final status, blockers, and documentation
gaps without fabricating facts or persisting secrets.

---

# Phase 14 — Clean-room Reproduction

**Status: DONE**

## Goal

Require successful repaired workflows to reproduce from a completely fresh
workspace and Docker sandbox.

## Build

* bounded derived clean-room recipes,
* fresh workspace copy with symlink/file/byte limits,
* fresh state/run artifacts and Docker sandbox,
* reapplication of real patches only,
* clean-room verification and status evidence,
* portable recipe artifacts when evidence permits.

## Acceptance Criteria

Clean-room success and failure fixtures prove that prior workspace/container
state is not reused and that only a verified clean rerun can satisfy the
clean-room requirement for `REPRODUCED`.

---

# Phase 15 — Security Hardening

**Status: DONE**

## Goal

Treat repository code as potentially hostile.

## Build

* no host execution, secret mounts, Docker socket, or privileged containers,
* capability dropping, no-new-privileges, resource and workspace limits,
* network-denied default with explicit plan opt-in,
* SSRF and redirect revalidation,
* sterile noninteractive Git intake with no recursive submodules/LFS smudge,
* unsafe-command handling and deterministic `UNSAFE` evidence.

## Acceptance Criteria

Safety tests demonstrate that prohibited host access and dangerous operations
are rejected or isolated, including network denial, workspace bounds,
URL/redirect policy, Git hardening, credential exclusion, and process limits.

---

# Phase 16 — Observability

**Status: DONE**

## Goal

Integrate useful run metrics into the existing append-only state/events without
introducing a second logging architecture.

## Build

* run and stage durations,
* attempts, repairs, LLM calls, token usage, failure categories,
* verification level, final status, Docker identity, and network mode,
* stable queryable run timeline.

## Acceptance Criteria

Observability metrics are derived from real persisted events and bounded facts,
remain secret-free, and have fixture coverage for normal and failed runs.

---

# Phase 17 — Evaluation Set

**Status: DONE**

## Goal

Create a versioned, reproducible benchmark contract before measuring system
performance.

## Build

* 20 bounded controlled fixture contracts,
* explicit provenance, strata, expected statuses, and verification levels,
* deterministic coverage summaries and path validation,
* no execution or fabricated observed results.

## Acceptance Criteria

The evaluation set loads offline, has stable sequential IDs, covers positive and
negative regimes, rejects unsafe or duplicate fixture paths, and keeps expected
labels separate from future observed outcomes.

---

# Phase 18 — System Evaluation

**Status: DONE**

## Goal

Measure the system against the controlled contracts without confusing expected
labels with observed evidence.

## Build

* one bounded adapter call per evaluation case,
* deterministic status/verification accuracy and confusion matrices,
* failure strata, repair success, intervention, stage, runtime, and usage metrics,
* explicit mismatch reporting and no LLM-derived verification authority.

## Acceptance Criteria

Evaluation reports are reproducible, reject missing/duplicate/foreign cases,
preserve stable case order, and keep observed facts separate from the benchmark
contracts.

---

# Phase 19 — Baselines + Ablations

**Status: NOT STARTED**

Phase 19 is the next implementation phase.

---

# Current Next Action

Phase 18 acceptance criteria have passed; Phase 19 is not started.

```text
Phase 14 → DONE
Phase 15 → DONE
Phase 16 → DONE
Phase 17 → DONE
Phase 18 → DONE
Phase 19 → NOT STARTED
```

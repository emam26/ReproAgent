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

## Phase 0 — Project Foundation

**Status: IN PROGRESS**

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

**Status: NOT STARTED**

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

**Status: NOT STARTED**

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

**Status: NOT STARTED**

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

**Status: NOT STARTED**

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

# Phase 5 — Repository Analysis & Planning

**Status: NOT STARTED**

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
ReproductionPlan
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

A small controlled repository set produces sensible structured plans.

No execution repair loop yet.

---

# Phase 6 — Initial Execution Engine

**Status: NOT STARTED**

## Goal

Execute a generated reproduction plan.

No autonomous repair yet.

Flow:

```text
plan
 ↓
sandbox
 ↓
environment setup
 ↓
target execution
 ↓
evidence
```

## Build

* plan executor,
* command records,
* log capture,
* output truncation,
* error fingerprinting,
* attempt recording.

## Acceptance Criteria

Known-good fixture repositories can reach successful execution using their generated plans.

---

# Phase 7 — Autonomous Debug & Repair Loop

**Status: NOT STARTED**

## Goal

Turn failures into bounded AI-assisted debugging actions.

Core loop:

```text
EXECUTE
   ↓
FAILURE
   ↓
COLLECT RELEVANT CONTEXT
   ↓
LLM DIAGNOSIS
   ↓
STRUCTURED ACTION
   ↓
POLICY VALIDATION
   ↓
TOOL EXECUTION
   ↓
NEW EVIDENCE
   ↓
RETRY OR STOP
```

## Initial Allowed Repair Actions

Start conservatively:

```text
inspect_file
search_repo
change_command
change_runtime_version
install_dependency
change_dependency_version
```

Do not immediately give the model unrestricted source editing.

## Safeguards

* maximum attempts,
* repeated-failure detection,
* no useless duplicate action,
* timeout,
* bounded LLM calls.

## Acceptance Criteria

Intentionally broken fixture repositories demonstrate automatic repair of several controlled failure types.

Examples:

* missing package,
* wrong dependency version,
* wrong invocation,
* undocumented setup step.

---

# Phase 8 — Controlled File Editing & Git Tracking

**Status: NOT STARTED**

## Goal

Permit minimal configuration/source changes while preserving provenance.

## Build

* patch application,
* Git diff capture,
* rollback,
* pre-change snapshots,
* allowed-path policy.

## Rules

Prefer:

```text
environment fix
configuration fix
dependency fix
```

before:

```text
source-code change
```

## Acceptance Criteria

The agent can:

1. make a small patch,
2. verify it,
3. record the diff,
4. roll it back if unsuccessful.

---

# Phase 9 — Verification Engine

**Status: NOT STARTED**

## Goal

Separate objective success from LLM judgment.

## Build

Verification rules for:

```text
installation
command success
test execution
test results
expected files
expected text patterns
custom goal
```

Determine verification level:

```text
L0
L1
L2
L3
```

## Acceptance Criteria

Identical execution evidence always produces the same verification result regardless of model output.

---

# Phase 10 — Reproduction Report & Artifacts

**Status: NOT STARTED**

## Goal

Produce useful evidence even when reproduction fails.

## Generate

```text
report.md
run.json
events.jsonl
commands.jsonl
patches.diff
environment.json
reproduce.sh
logs/
```

## Report Should Include

```text
summary
repository
commit SHA
goal
status
verification level
environment
documented procedure
actual procedure
failures
repairs
modifications
test results
remaining blockers
exact reproduction instructions
```

## Acceptance Criteria

A human can understand what happened without reading internal implementation details.

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

Complete **Phase 0 only**.

After Phase 0 acceptance criteria pass:

```text
Phase 0 → DONE
Phase 1 → IN PROGRESS
```

Then begin repository intake.

# ReproAgent

ReproAgent is a Python project for auditing whether open-source software can be
reproduced from a clean environment. The long-term project will inspect a
repository, execute its documented workflow in isolation, and produce
evidence-backed results.

## Development status

Phases 0–17 are complete. The current CLI accepts supported public GitHub URLs,
clones them into an isolated run workspace, and generates a deterministic
structural manifest. The programmatic pipeline can analyze a manifest, create a
finite plan, and execute that plan in Docker with persisted evidence. Full CLI
pipeline integration, controlled file editing, and formal reproducibility
verification are not implemented yet.

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

## Repository analysis

Phase 5 adds deterministic-first extraction of package, runtime, CI,
documentation, environment, asset, and hardware evidence with explicit
provenance and bounded optional LLM interpretation. See
[`docs/REPOSITORY_ANALYSIS.md`](docs/REPOSITORY_ANALYSIS.md).

## Reproduction planning

Phase 6 converts repository analysis into a bounded, documented-first sequence
of typed steps with evidence, expected outcomes, risk labels, and deterministic
command-safety checks. Planning performs no execution. See
[`docs/REPRODUCTION_PLANNING.md`](docs/REPRODUCTION_PLANNING.md).

## Initial execution engine

Phase 7 executes finite plans sequentially through the Docker sandbox and
records bounded command results, state events, and run logs. It has no host
fallback and stops at the first deterministic failure without modifying the
target repository. A successful workflow outcome is not a final reproducibility
verdict. See [`docs/EXECUTION_ENGINE.md`](docs/EXECUTION_ENGINE.md).

## Diagnostic evidence foundation

Phase 7.5 adds deterministic failure classification, bounded log extraction,
PEP-aware dependency intelligence, Docker-only pip/environment inspection,
import analysis, repeated-failure signatures, asset indicators, and typed
verification contracts. No autonomous diagnosis or repair occurs in this
layer. See [`docs/DIAGNOSTICS.md`](docs/DIAGNOSTICS.md).

## Bounded autonomous diagnosis

Phase 8 adds deterministic-first diagnosis over compact evidence, strict typed
hypotheses and future repair actions, bounded provider calls, repetition limits,
policy checks, prompt-injection separation, and append-only diagnosis events.
Diagnosis never executes commands or edits repositories. See
[`docs/DIAGNOSIS.md`](docs/DIAGNOSIS.md).

## Controlled repair experiments

Phase 9 converts accepted diagnoses into finite, policy-checked repair
experiments. It provides typed invocation, dependency, Python-version,
environment, asset, path, patch, evidence-gathering, and stop actions; bounded
risk and repetition limits; objective before/after observations; rollback
metadata; and append-only repair events. It performs no host execution,
repository mutation, download, or global Docker management. See
[`docs/REPAIRS.md`](docs/REPAIRS.md).

## Controlled workspace repairs and rollback

Phase 10 adds workspace-confined UTF-8 reads, exact replacements, unified
patches, SHA-256 before/after evidence, size/path/symlink limits, exact
`patches.diff` artifacts, conflict-aware rollback, and a Docker-only repair
retry boundary. A successful retry remains an experiment until formal
verification and clean-room reproduction. See
[`docs/WORKSPACE_REPAIRS.md`](docs/WORKSPACE_REPAIRS.md).

## Untrusted repository security

Phase 15 hardens Docker execution and Git intake with network-denied defaults,
resource and workspace bounds, SSRF-safe public URL handling, redirect and
download limits, sterile noninteractive Git configuration, disabled recursive
submodules/LFS smudge, and malicious-fixture coverage. See
[`docs/SECURITY.md`](docs/SECURITY.md).

## Objective verification

Phase 11 evaluates recorded execution evidence and bounded workspace facts with
deterministic installation, command, test, expected-output, environment, and
artifact checks. It reports explicit verification levels and distinguishes
execution failure, failed conditions, unavailable evidence, and unspecified
contracts. It never executes a target command for verification and never treats
LLM output as proof. See [`docs/VERIFICATION.md`](docs/VERIFICATION.md).

## Final reproducibility status

Phase 12 computes `REPRODUCED`, `PARTIAL`, `BLOCKED`, `FAILED`, or `UNSAFE` from
machine-readable verification, workflow, clean-room, and safety evidence. The
status is separate from `RunOutcome`; a successful workflow alone cannot claim
reproduction. See [`docs/STATUS.md`](docs/STATUS.md).

## Reports and run artifacts

Phase 13 writes schema-versioned `run.json` and `report.md` artifacts, clearly
separating official documented reproduction from agent-assisted attempts. When
real data exists it also writes events, commands, environment, exact patches,
and a validated reproduction recipe without fabricating empty artifacts or
secrets. See [`docs/REPORTING.md`](docs/REPORTING.md).

## Clean-room reproduction

Phase 14 derives a final recipe, copies the source into a new bounded workspace,
reapplies only the real patch, creates a new Docker sandbox, verifies the run,
and requires clean-room evidence before `REPRODUCED`. It emits portable recipe
artifacts when their inputs are real and does not fabricate environment locks or
Dockerfiles. See [`docs/CLEAN_ROOM.md`](docs/CLEAN_ROOM.md).

## Run observability

Phase 16 derives bounded run metrics and a stable timeline from the existing
append-only event stream. It captures durations, attempts, repairs, LLM usage,
failure categories, verification/status, Docker identities, and network modes
without introducing a second logging backend or copying raw event payloads. See
[`docs/OBSERVABILITY.md`](docs/OBSERVABILITY.md).

## Evaluation set

Phase 17 adds a versioned offline set of 20 controlled evaluation contracts
covering success, repair, dependency/runtime, asset/network, configuration,
test/output, resource, safety, documentation, and clean-room cases. The labels
are benchmark expectations, not observed reproduction results; execution and
scoring remain separate evaluation work. See
[`docs/EVALUATION_SET.md`](docs/EVALUATION_SET.md).

## System evaluation

Phase 18 compares one typed observed result per case with the evaluation
contracts and reports status/verification accuracy, confusion matrices, failure
strata, repair and intervention rates, stage success, runtime, agent steps, and
LLM calls. It does not execute repositories or infer success from LLM prose. See
[`docs/SYSTEM_EVALUATION.md`](docs/SYSTEM_EVALUATION.md).

## Baselines and ablations

Phase 19 predeclares documented-only, deterministic-only, and bounded-agent
baselines, plus paired no-LLM, no-repair, and no-clean-room ablations. Comparison
results are descriptive and paired by case; the system does not claim causal or
statistical conclusions from one controlled evaluation set. See
[`docs/BASELINES_ABLATIONS.md`](docs/BASELINES_ABLATIONS.md).

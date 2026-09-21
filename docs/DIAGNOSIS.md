# Bounded Autonomous Diagnosis

Phase 8 converts a compact Phase 7.5 diagnostic context into a typed diagnosis
proposal. It is a reasoning boundary, not an executor or verifier.

## Architecture

`DiagnosisSession` accepts a `DiagnosticContext`, the existing provider
abstraction, and finite `DiagnosisLimits`. It first applies deterministic
diagnoses for obvious timeout, authentication, and missing-module cases. Only
unresolved interpretation reaches `LLMProvider` through a bounded
`LLMRequest`.

Provider output must be an `AgentDecision` with action `diagnose`. Its arguments
are converted into strict `Diagnosis`, `DiagnosisHypothesis`, typed action, and
risk models. Pydantic validation is authoritative. A diagnosis proposes a
future action; Phase 8 never executes that action, edits a workspace, controls
Docker, changes lifecycle state, or claims reproduction success.

## Action boundary

The diagnosis vocabulary is finite:

```text
CHANGE_INVOCATION
CHANGE_PYTHON_VERSION
ADD_DEPENDENCY
CHANGE_DEPENDENCY_VERSION
SET_SAFE_ENVIRONMENT_VARIABLE
ADJUST_CONFIG_PATH
FETCH_DOCUMENTED_ASSET
APPLY_MINIMAL_PATCH
GATHER_MORE_EVIDENCE
STOP_UNREPAIRABLE
```

Arbitrary shell fields, shell metacharacters, host/Docker management actions,
credential-shaped names, high-risk recommendations, and unknown evidence
references are rejected by deterministic policy. Actual repair execution begins
in Phase 9.

## Bounds and repetition control

Each session limits LLM calls, diagnosis attempts, context size, hypotheses,
repeated failure signatures, and repeated recommendations. The session stops
when a bound is reached or a valid recommendation repeats beyond policy. Provider
errors and malformed diagnoses become typed bounded results; they do not trigger
unbounded retries.

## Prompt-injection protection

The request labels system/policy instructions separately from an
`untrusted_evidence` JSON value. Repository text is data only. README, source,
configuration, and log content cannot override action vocabulary, safety policy,
state control, or the prohibition on execution. The compact evidence builder
already bounds and redacts the context before this prompt is built.

## Persistence

When a run ID is supplied, the session uses the existing Phase 3 store to append
typed `Attempt` and `AgentAction` events for diagnosis start and result. Events
retain failure signature, provider/model identity, evidence counts, diagnosis,
selected action, risk, usage metadata, policy rejection, or stop reason. API
keys and authorization headers never enter these records.

## Current limitation

Diagnosis is intentionally not connected to a retry or repair loop yet. This
keeps the separation explicit: LLM reasoning proposes; Phase 9 tools execute;
the state machine controls; later verification establishes truth.

# Controlled Repair Actions

Phase 9 adds a typed repair proposal and experiment boundary. A diagnosis can
recommend a finite `RepairAction`, but the diagnosis layer does not execute it
and the action is not evidence of success.

## Action boundary

The supported vocabulary is deliberately small:

* invocation and dependency changes,
* bounded Python-version candidates,
* non-sensitive environment variables,
* workspace-relative directories and configuration paths,
* HTTPS assets explicitly present in trusted evidence,
* bounded minimal patches with explicit rollback metadata,
* gathering more evidence or stopping as unrecoverable.

Every proposal carries supporting evidence references, an expected effect,
risk, reversibility, and typed arguments. High-risk actions are rejected by the
default policy. Commands are checked by the existing plan safety rules; shell
scripts, multiline commands, credentials, host paths, Docker management, and
other prohibited operations never become repair tools.

Direct URL/VCS dependencies, private or loopback asset destinations, embedded
URL credentials, undocumented assets, path traversal, sensitive environment
variables, and unbounded patches are rejected before an experiment can start.

## Experiment semantics

`RepairExperimentEngine` enforces finite repair and repeated-failure limits. A
backend applies only an accepted typed action, an objective observer returns a
`RepairObservation`, and the engine records before/after failure signatures.
Improvement means verified workflow success or a changed failure signature; an
LLM statement is never used as the verifier. Applied plan transformations are
pure and retain the exact pre-repair plan for rollback. Unsupported actions are
reported as deferred until a later controlled tool exists.

Each proposal, application, rejection, deferral, stop, and observation is
persisted through the existing append-only state event infrastructure when a
run ID is supplied. No host execution, repository mutation, asset download, or
global Docker operation is performed in Phase 9; workspace editing and exact
file rollback are Phase 10 work.

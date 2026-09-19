# Reproduction Planning

Phase 6 turns a `RepositoryAnalysis` into a finite, inspectable
`ReproductionPlan`. Planning is deterministic and does not execute commands,
create containers, install dependencies, or modify a target repository.

## Plan schema

Each ordered `PlanStep` records:

```text
step ID
action type
optional command
workspace-relative working directory
purpose
analysis evidence
timeout
network requirement
expected outcome
risk level
```

Supported action types cover environment and asset prerequisites, dependency
installation, setup, demo execution, tests, and basic-execution target
selection. Commandless steps make unresolved prerequisites visible instead of
inventing executable behavior.

## Documented-first baseline

The first plan preserves what a newcomer would attempt from official README or
INSTALL instructions. Command ordering is:

```text
documented instructions
structured package metadata
CI configuration
explicit inference
```

Documented commands are not silently repaired before the first attempt.
Conflicting evidence remains attached to the analysis and each step carries its
supporting provenance. Package entrypoints may become explicit run steps, but
the original metadata evidence is retained.

## Bounds

`PlannerLimits` defaults to at most 20 steps, 1,000 characters per command,
300 seconds per step, and a 1,800-second overall budget. Step IDs are
deterministic and sequential. The sum of step timeouts cannot exceed the
overall budget.

## Safety

Before a plan is accepted, deterministic checks reject multiline or excessive
commands, absolute/parent-relative working directories, privilege escalation,
privileged Docker, Docker socket access, global/container cleanup, broad
filesystem deletion, host system paths, credential paths, host package-manager
modification, and system-destructive commands.

The planner does not rely on Docker isolation to make an unsafe request
acceptable. Safety validation happens before the execution layer receives the
plan.

## Limitations

Phase 6 does not execute or repair a plan. It does not download external assets,
provision GPUs, choose targets when evidence is absent, or claim that an
expected outcome occurred. A commandless medium/high-risk step communicates
such prerequisites to the later execution layer. Objective verification and
autonomous repair remain future work.

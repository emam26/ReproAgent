# Phase 17 — Evaluation Set

ReproAgent now ships a versioned offline evaluation set with 20 controlled
fixture contracts. The set is loaded by `load_evaluation_set()` and validated by
strict Pydantic models before a later evaluator can use it.

## Design

Each case records:

* stable case identity and normalized fixture path,
* provenance (`CONTROLLED_FIXTURE` in this version),
* user goal and bounded description,
* evaluation stratum,
* expected final status and verification level,
* expected failure class where applicable,
* whether network access or a bounded repair is part of the contract,
* unique tags for stratified analysis.

The cases cover positive controls and failure regimes: successful demos and
tests, dependency and Python-runtime failures, missing assets, network and
credential blockers, configuration and test/output failures, timeouts, unsafe
commands, repair success and policy stops, documentation gaps, and clean-room
state leakage.

## Scientific and operational boundaries

The JSON file contains contracts, not observed results. It does not claim that
any case has been reproduced, and it does not execute fixture code when loaded.
This prevents label leakage into a future evaluator and keeps ordinary tests
offline. Phase 18 can run the cases through the same controlled pipeline and
record observed outcomes separately from these expected labels.

The controlled set is deliberately deterministic and inspectable. It is not a
substitute for a later public-repository evaluation: external repositories need
pinned commits, access and license checks, resource budgets, and a predeclared
protocol before they can support generalization claims.

# Phase 19 — Baselines and Ablations

Phase 19 defines the comparison protocol before observing results. The default
protocol contains three baselines:

* documented-only: official workflow, no LLM diagnosis, no repairs;
* deterministic-only: deterministic analysis and bounded repairs, no LLM;
* bounded-agent: provider-independent diagnosis and policy-bounded repairs.

All baselines require the same clean-room policy. Three paired ablations remove
one capability from the bounded-agent configuration: LLM diagnosis, controlled
repairs, or clean-room verification.

`compare_evaluation_reports` requires the same evaluation set and exactly the
same case order. It reports descriptive status/verification accuracy deltas,
repair/intervention/runtime deltas where available, and case-level status
changes. It performs no hyperparameter tuning, case reordering, label editing,
or causal inference. A single controlled set cannot establish significance or
generalization; those limitations must remain visible in any later report.

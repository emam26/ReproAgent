# Deterministic Reproduction Status

Phase 12 adds `compute_reproduction_status`, a policy function separate from
the control-plane `RunOutcome`. A successful workflow is only one input; it is
not itself a reproduction claim.

The status rules are:

* `UNSAFE` when deterministic safety findings exist,
* `FAILED` when recorded execution fails or an objective verification condition
  fails,
* `BLOCKED` when required verification evidence is unavailable or unspecified,
* `PARTIAL` when workflow success is not confirmed, verification is below target
  execution level, or a required clean-room rerun is not complete,
* `REPRODUCED` only when required objective verification passes at L2/L3,
  workflow success is confirmed, and any required clean-room evidence passes.

Every result contains sequential machine-readable reason records and evidence
references. The final status function does not call an LLM, inspect prose, or
mutate run state. `RunOutcome.SUCCEEDED` remains a workflow/control-plane fact;
`ReproductionStatus.REPRODUCED` is the stronger evidence-backed product claim.

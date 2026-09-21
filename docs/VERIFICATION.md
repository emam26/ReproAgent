# Objective Verification Engine

Phase 12 evaluates a finite `VerificationContract` using deterministic facts.
It does not run a new target command and it never accepts an LLM statement as
verification evidence.

## Checks and levels

The verifier consumes recorded Docker execution results for installation,
command, test, and expected-output checks. It can also inspect a supplied
workspace for an artifact's existence, type, exact size, and SHA-256 hash, and
it can verify that an environment fingerprint is present.

Verification levels are explicit:

* `L0`: repository inspection only,
* `L1`: environment setup evidence,
* `L2`: installation, target command, output, or artifact evidence,
* `L3`: test execution evidence.

Every check contains a required/optional flag, objective status, reason, and
bounded evidence. A result is `PASSED` only when every required check passes.
`EXECUTION_FAILED` means the recorded command itself failed; `FAILED` means
execution evidence exists but a verification condition was not met;
`UNAVAILABLE` means required evidence was not supplied or could not be safely
inspected; and `UNSPECIFIED` means the contract had no required checks.

The result remains separate from both workflow `RunOutcome` and the later
final reproducibility status. In particular, a successful workflow does not
automatically imply a reproduced repository.

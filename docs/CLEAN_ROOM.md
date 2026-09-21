# Clean-room Reproduction

Phase 14 derives a `CleanRoomRecipe` from a real reproduction plan and optional
real repair diff. `CleanRoomRunner` creates a new run ID, a new workspace, and
new Docker sandbox. It copies only regular files under bounded file-count and
byte limits, rejects symlinks, reapplies only the supplied diff, writes a
portable command recipe, and executes the plan through the existing Docker
engine.

The original workspace is not reused as mutable state and the prior sandbox is
not reused. The clean run receives a fresh state history and its own artifacts.
The runner verifies the new execution and computes final status with
`clean_room_required=True`; a successful repaired attempt alone cannot satisfy
that condition.

When evidence permits, the clean run contains `reproduce.sh`,
`REPRODUCTION.md`, and `patches.diff`. It does not fabricate an environment
lock or Dockerfile when the exact image/environment evidence was not supplied.
The success fixture proves fresh-workspace repair and reproduction; the failure
fixture proves a clean-room failure is not claimed as `REPRODUCED`.

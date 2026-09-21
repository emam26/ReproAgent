# Reproducibility Reports and Run Artifacts

Phase 13 writes a schema-versioned `run.json` and human-readable `report.md`
from supplied run facts. The report keeps two signatures distinct:

* Official documented reproduction: the initial attempt and documented setup.
* Agent-assisted reproduction: diagnosis, bounded repairs, and retries.

When real data is supplied, the writer can also emit `events.jsonl`,
`commands.jsonl`, `environment.json`, `patches.diff`, and `reproduce.sh` under
the exact run directory. It does not invent empty logs, fabricate environment
facts, or create a recipe without commands. Existing execution logs remain
owned by the execution artifact layer.

The JSON and Markdown serializers apply the shared secret guards. Recipe
commands are validated against plan command safety; credential-like content is
rejected rather than silently persisted. Report generation consumes diagnosis,
repair, verification, and final-status objects but does not infer a status or
execute a recipe. A report can therefore truthfully say that verification or a
clean-room rerun was not supplied.

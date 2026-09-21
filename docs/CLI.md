# Phase 20 — CLI Polish

The CLI now has a small, explicit command surface:

```text
reproagent --help
reproagent --version
reproagent version
reproagent run <github-url> [--goal auto|install|tests|demo] [--runs-dir PATH]
reproagent runs [--runs-dir PATH]
reproagent report <run-id> [--runs-dir PATH]
```

`run` still performs intake and structural manifest generation only. The goal is
validated and recorded in the machine-readable output, but it does not cause
target code to execute. `report` only reads an existing report artifact, and
`runs` lists only run directories containing `report.md`.

The commands use stable exit behavior: successful operations return zero,
invalid options return Typer’s usage error, and intake/artifact failures return
one with a concise message. Run IDs are constrained before filesystem access,
and all machine-readable output is JSON without provider credentials or raw
exceptions.

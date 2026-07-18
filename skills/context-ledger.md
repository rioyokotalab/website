# Skill: context ledger — cross-session working memory

No task may depend on chat context to survive. A fresh Codex session
reconstructs all in-flight work from the ledger.

## File map and routing

| File | Holds | Budget (bytes) |
| --- | --- | --- |
| `TODO.md` | Active / blocked / recently completed tasks | 8000 |
| `tools/state/session.md` | Current task, last/next step, working set, asks | 4000 |
| `tools/state/facts.md` | Current verified facts | 10000 |
| `tools/state/decisions.md` | Durable choices and rationale | 10000 |
| `tools/codex-log.md` | Delegation/driver log | — |
| `tools/out/` | Transient deliverables and scratch | — |

Procedures belong in `skills/`; tasks in `TODO.md`; current state in
`session.md`; facts and decisions in their named files. Prune stale material
when a budget is approached; Git keeps history.

## Session start

1. Read `TODO.md` and `tools/state/session.md`.
2. If another driver owns a recently updated in-flight task, ask before
   takeover. Otherwise continue from `Next` after checking the working set
   against Git status.
3. Read facts/decisions only as the task needs them.

## Checkpoints

Update `session.md` at task start, after each completed step/discovery/failure,
before risky or long work, and at session end. When finished, set task/status
to `idle` and move one compact completion entry to `TODO.md`.

Keep these headings exactly:

```text
driver: codex | claude
updated: <ISO local time>
task: T-<n> <title> | idle
status: in-progress | blocked | awaiting-user | idle
## Now
## Working set
## Open questions
## Awaiting user
```

`TODO.md` uses stable `T-<n>` IDs and records the next free ID. Ledger files
commit with the task; never create a ledger-only commit merely for persistence.

## Delegation and handoff

The root DRIVER owns `session.md`. Workers receive on-disk pointers and never
edit it. Worker deliverables live under `tools/out/`; prompts cite paths rather
than copying file payloads. Native delegation follows
`skills/codex-delegation.md`.

## Driver report and metrics

Every driver session ends with
`tools/out/driver-report-<YYYYMMDD-HHMM>.md`, containing model/effort when
exposed, start/end times, per-task outcome/files/checks, available runtime
telemetry, escalations, network operations, rule exceptions, and self-noted
gaps.

Instrumented work uses schema v2 and validates with
`python3 tools/task-metrics.py validate`; unknown telemetry is null. Drivers
append one legacy-compatible row per uninstrumented task with
`tools/task-metrics.py append-driver --agent CLIENT --task-ids ... --report
...`. The driver log line is:

```text
date | CLIENT-driver (<model>) | tasks | report path | n/a | outcome
```

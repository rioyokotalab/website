driver: codex
updated: 2026-07-13T09:30+0900
task: T-117
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-125. Quiet-server analytics/runtime-health smoke passed 5/5 in 39.3 seconds with about 200 output tokens and no access lines; the prior full suite passed 37/37.
- Next: write final benchmark/recommendation and driver reports, close the ledger/metrics, commit, pull/rebase, and push deploy-excluded changes.

## Working set
- `tools/todo.md`
- `tools/state/session.md`
- `tools/out/t109-benchmark-comparison.md`
- `tools/out/t109-coding-benchmarks.md`
- `tools/out/t110-suite-spec.md`
- `tools/out/t110-task-capsules.md`
- `tools/agent-benchmark/`
- `tools/out/agent-benchmark/` (raw run artifacts)
- `tools/out/t112-baseline.md`
- `tools/task-metrics.py`
- `tools/task-metrics.schema.json`

## Open questions
- Whether any repository-wide check exposes an integration regression in the benchmark, logging, or standards tooling before push.

## Awaiting user
- None.

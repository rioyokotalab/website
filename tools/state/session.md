driver: codex
updated: 2026-07-13T07:51+0900
task: T-115
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: WBD-002 failed identically on Spark/low, Terra/low, Terra/medium, and Sol/high because exact label/type requirements were hidden; after making them owner-visible, Spark satisfied all semantic assertions but exposed an order-dependent false failure in `standards-check.py`. The checker now has order-independent PDF-link parsing and focused tests.
- Next: commit the task/checker calibration, rerun WBD-002 v2 on Spark/low, then probe Terra/low on WBD-003/004 and freeze routing/escalation rules from passing evidence.

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
- Whether Terra/low or Terra/medium is the cheapest route that reliably satisfies WBD-002's independent name/media/security semantics.

## Awaiting user
- None.

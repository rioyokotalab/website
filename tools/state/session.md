driver: codex
updated: 2026-07-13T07:57+0900
task: T-116
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-115. The selected WBD portfolio is 4/4 at 115,236 effective tokens (-12.7% vs original baseline); WBD-003/004 pass Terra/low and WBD-002 v2 passes Spark/low after explicit criteria and semantic checker repair.
- Next: quantify output-first/codex-log/worker-test overhead, introduce a compact machine-readable handoff that preserves evidence without duplicated prose or exhaustive worker-side tests, rerun representative tasks, and include root-review cost rather than shifting work invisibly.

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
- Whether removing duplicated worker-side exhaustive browser output and Markdown handoff prose reduces total tokens without increasing grader/root repair.

## Awaiting user
- None.

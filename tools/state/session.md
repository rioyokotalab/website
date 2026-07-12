driver: codex
updated: 2026-07-13T08:07+0900
task: T-118
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-116. Runner-lite kept WBD-001/003 at 100/100 and reduced matched effective tokens 15.2%, tool output 12.6%, and worker duration 56.7%; redundant schema enforcement increased effective tokens 47.8% and was rejected.
- Next: repeat representative Spark/low and Terra/low runner-lite tasks, quantify run-to-run variation, and define an evidence threshold so route/process changes are not promoted from a lucky cache result.

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
- How many matched repeats are needed to distinguish a real process improvement from prompt-cache variance without spending more on benchmarking than the optimization can save.

## Awaiting user
- None.

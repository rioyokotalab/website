driver: codex
updated: 2026-07-13T08:30+0900
task: T-120
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-119. Refined focused inspection passed 6/6 tasks at 100 and cut portfolio median effective tokens 21.7% and output 59.2%; a naive bounded variant failed CRLF scope and remains negative evidence.
- Next: add a safe baseline/candidate comparison command that exposes matched-task coverage, routes/modes, capability failures, token distributions, tool output, durations, and missing evidence without manual arithmetic.

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
- How strict the comparison command should be when labels contain unequal task counts, task versions, routes, or missing token telemetry.

## Awaiting user
- None.

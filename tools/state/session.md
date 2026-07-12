driver: codex
updated: 2026-07-13T07:27+0900
task: T-114
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-113. Four baseline rows are imported as valid schema-v2 metrics; raw-event recomputation reports 31 successful and 7 failed commands producing 228,423 tool-output characters, with token/gate/failure provenance and artifact pointers.
- Next: commit the calibrated baseline/logging checkpoint, then slim auto-loaded instructions, remove redundant AGENTS/ledger reads from self-contained work, precreate handoff output, use compact task capsules, and rerun the visible suite.

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
- Whether progressive disclosure materially reduces effective tokens and tool-output size while WBD-001/003 retain full scores.

## Awaiting user
- None.

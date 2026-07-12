driver: codex
updated: 2026-07-13T08:55+0900
task: T-117
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: final-visible-v3 passed all four tasks at 100 with 39,736 effective tokens. Held-out v1 then passed all five browser behaviors but exposed three capsule defects: its glob rejected required root language pages, the static JS grader rejected an equivalent named zero-motion object, and standards-check hard-coded the old helper query while the task required a new uniform version. The failed run remains logged.
- Next: checkpoint held-out v2 with complete HTML authorization, representation-invariant JS grading, dynamic uniform helper-version validation, and root-index cache synchronization. Run the corrected held-out capsule once without changing the selected Sol/high route or behavioral prompt.

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
- Whether the frozen candidate passes the untouched multi-file reduced-motion held-out task without route escalation or prompt/grader changes.

## Awaiting user
- None.

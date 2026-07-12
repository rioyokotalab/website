driver: codex
updated: 2026-07-13T08:42+0900
task: T-117
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: frozen visible run v1 passed WBD-001/002/003 at 100 but failed WBD-004 at 86 because focused inspection on reference-driven CSS guessed 24px instead of the pristine 16px. The run is retained in metrics; focused inspection is now explicitly limited to textual edits with exact acceptance.
- Next: checkpoint the corrected process rule, rerun the entire visible suite as v2 using default inspection for WBD-003/004 and focused only for WBD-001/002, then proceed to held-out only if all four pass.

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

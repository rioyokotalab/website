driver: codex
updated: 2026-07-13T08:45+0900
task: T-117
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: visible v2 again passed WBD-001/002/003 at 100 but WBD-004 independently guessed 24px under default inspection. Two routes/modes missed the same hidden 16px assertion while P2P passed, so the contract was audited rather than escalating. WBD-004 is versioned to v2 with exact 16px/50% acceptance; prior runs remain raw evidence.
- Next: checkpoint the corrected WBD-004 contract, restart the full visible suite from the cheapest selected routes as final-visible-v3, and proceed to held-out only if all four task versions pass.

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

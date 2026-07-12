driver: codex
updated: 2026-07-13T08:40+0900
task: T-117
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-120. Strict comparison now checks task identity/count/version, reports route/mode/gate/cost/failure evidence, and refuses older rows whose append-only telemetry cannot prove equivalence.
- Next: freeze runner-lite + focused local inspection + selected low-cost routes; run WBD-001–004 once with full P2P, then evaluate held-out WBD-005 exactly once and complete repository/session verification.

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

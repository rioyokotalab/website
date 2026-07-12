driver: codex
updated: 2026-07-13T07:31+0900
task: T-114
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: T-114 candidate reduces auto-loaded `AGENTS.md` from 9,654 to 6,394 bytes while preserving authority/security/site invariants; self-contained tasks no longer request AGENTS/global-ledger rereads and fresh fixtures precreate the ignored handoff directory.
- Next: commit the context candidate, run WBD-001 through WBD-004 with compact capsules and unchanged default routes, import schema-v2 metrics, and retain/reject based on matched scores and cost.

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

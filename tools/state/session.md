driver: codex
updated: 2026-07-13T07:38+0900
task: T-115
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-114 and retained progressive disclosure. Context-v1 is 3/4 passing at mean 92.5 and 121,257 effective tokens; WBD-001/003 remain 100 with lower cost and WBD-004 now exactly matches the visual target.
- Next: route WBD-002 through the lowest plausible stronger route, probe cheaper routes for WBD-003/004 only where task inputs permit, define deterministic escalation triggers, and produce a fully passing visible-suite candidate.

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

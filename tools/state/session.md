driver: codex
updated: 2026-07-13T08:15+0900
task: T-119
status: in_progress

## Now
- Goal: spend the three-hour window ending about 2026-07-13T09:44+0900 establishing a defensible web-development regression suite, then iteratively reduce Codex token use without degrading capability and improve logging so future routing decisions are evidence-based.
- Last done: completed T-118. Three matched runner-lite/durable portfolios all passed at 100; effective-token ranges did not overlap (29,098–30,046 versus 42,958–57,936), so a repeated-portfolio promotion rule is now canonical.
- Next: test whether locate-first, bounded-range source inspection lowers cost on WBD-002's large bilingual HTML files without losing exact secure-link semantics.

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
- Whether explicit bounded inspection guidance changes actual command output/context behavior or merely adds prompt tokens.

## Awaiting user
- None.

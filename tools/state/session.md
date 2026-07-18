driver: claude
updated: 2026-07-18T21:35+0900
task: idle
status: idle

## Now
- T-199 complete. Claude benchmark support merged (PR #20, `58f5e7b`) and the
  full study ran: 75 singletons (claude-full-20260718) + 14 WBD-003 adaptive
  repeats (claude-repeat-20260718) in results.jsonl. Result: 72/75 singletons
  full-quality; the 3 WBD-003 higher-effort misses did NOT reproduce (14/14
  repeats pass) — variance, not capability. Low effort best default; Fable 5
  only clean 25/25 sweep + most token-efficient; Sonnet fastest; Opus slowest.
- Deliverables: tools/agent-benchmark/claude-full-20260718.summary.md +
  README "Claude benchmark results" section. Landing via PR (admin-merge only
  on CONFIRMED CI pass).
- Note: the long-lived background repeat orchestrator was killed twice by host
  pressure; the essential repeats were finished in reliable foreground batches.
- Skills applied: research-engineering-validation, plan-interview-execute,
  context-ledger.

## Working set
- results.jsonl (+89 claude rows), summary, README — in the T-199 results PR.

## Open questions
- None.

## Awaiting user
- None.

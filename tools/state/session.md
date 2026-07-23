driver: codex
updated: 2026-07-24T05:46+0900
task: T-205 nightly Codex/Claude benchmark refresh
status: complete

## Now
- Exact current matrices validate: GPT 86/90 strict and 90/90
  browser-functional; Claude 71/75 strict and 74/75 browser-functional.
- Previous matched results were GPT 85/90 strict and 89/90 functional, and
  Claude 72/75 strict and 74/75 functional.
- Focused inspection recovered Opus/xhigh WBD-003 and the genuine Sonnet/low
  WBD-005 browser failure. Sonnet/xhigh WBD-003 remained a browser-correct
  static-grader miss. Focused cells remain outside singleton denominators.
- README tables, machine summaries/comparisons, and
  `docs/audits/agent-benchmark-nightly-2026-07-24.md` hold the final analysis.
- The receipt-backed cowork session
  `tools/state/cowork/t205-nightly-20260723/` validates as complete.
- Benchmark selftest, capsule audit, matrix tests, metrics schema, receipts,
  security suite, 38/38 locked browser tests, and `git diff --check` pass.

## Working set
- None after T-205 publishes through protected `main`.

## Open questions
- None.

## Awaiting user
- None.

## Next action
- Await the next task. The next free ID is T-206.

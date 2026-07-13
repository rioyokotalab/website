driver: codex
updated: 2026-07-13T17:59+0900
task: T-143 Remove Claude benchmark machinery and retained data
status: in-progress

## Now
- T-142 complete: removed 20 tracked active integration/config/MCP/registry
  paths (74,489 bytes) and one untracked project-local settings file. Replaced
  AGENTS, README, delegation, ledger, config, lookup, publish, and skill-index
  text with Codex-only contracts.
- `benchmark.py` now reads model/effort from each task instead of the deleted
  registry. Selftest, all five capsule audits, compile, metrics validation,
  Markdown budgets, reference checks, and diff checks pass.
- Next: remove provider-specific benchmark implementation/results and the
  completed comparison record set, clear associated metrics/pointers, delete
  both raw artifact trees and local evaluation branches, then rerun the
  provider-neutral suite checks.

## Working set
- `skills/claude-benchmark.md`, `tools/state/ab-round4.md`
- `tools/agent-benchmark/` provider-specific and completed result/round files
- `tools/task-metrics.jsonl`, `tools/codex-log.md`
- `tools/out/agent-benchmark/`, `tools/out/claude-benchmark/`
- Local `eval/r1-*` and `eval/r2-*` branches; remote remains main-only
- Verify: runner selftest/audit with empty history, metrics validation, zero
  stale artifact pointers, branch inventory, exact file/byte removal counts.

## Open questions
- None blocking. Provider-neutral task definitions, grader, runner, and failure
  taxonomy are retained for future Codex regression use.

## Awaiting user
- None.

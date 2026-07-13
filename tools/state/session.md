driver: codex
updated: 2026-07-13T18:04+0900
task: T-144 Remove residual references and prove a zero-trace current tree
status: in-progress

## Now
- T-143 complete: removed provider-specific benchmark code/data and the
  completed comparison record set, 106 metrics rows, 27 log lines, 547 raw
  artifact files (12,705,133 bytes), and eight local evaluation tags.
- Retained Codex task definitions, grader, runner, coverage, and failure
  taxonomy have empty result/artifact history. Runner selftest, five-capsule
  audit, zero-artifact audit, metrics selftest/validation (440 legacy rows),
  schema parse, compile, Markdown budgets, and diff checks pass.
- Ten tracked files still contain decommissioned provider/model wording. Next:
  neutralize shared benchmark/preview code, filter remaining ledger/log/metrics
  traces, remove temporary inventories, compact the task board to an idle
  zero-trace state, scan tracked and ignored trees, then run full regressions.

## Working set
- `tools/agent-benchmark/benchmark.py`, `coverage.md`, `task_ops.py`
- `tools/preview-server.sh`, `tools/test-preview-server.sh`
- `tools/task-metrics.jsonl`, `tools/codex-log.md`
- `tools/todo.md`, `tools/state/session.md`, `tools/state/decisions.md`
- Current `tools/out/t141-*` inventories (delete after facts move to report)
- Verify: case-insensitive path/content scans excluding `.git`, ignored-tree
  scan, preview/benchmark/metrics/security tests, Markdown budgets, Git refs,
  status/diff, required rebase, push, and remote verification.

## Open questions
- None. Git history and owner-scope settings remain explicitly outside scope.

## Awaiting user
- None.

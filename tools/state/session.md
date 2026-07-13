driver: claude
updated: 2026-07-13T15:27+0900
task: T-139
status: complete

## Now
- Claude fable/max driver session started; ledger + skill + both T-139 files
  read. Zero-token gate re-run and PASSED at 15:01 (preflight pass, five
  capsules, fresh label, corrected-ref override, fable/max advertised, dynamic
  coordinator fable/max; regenerated plan diff-identical to frozen plan).
- Start checkpoint appended to `tools/out/t139-claude-dynamic-rerun.md`.
- Progress: WBD-001 PASS 100 ($0.6590, 22,470 eff tok, run 150307-…-69c3a1);
  WBD-002 FAIL generator error_max_budget_usd ($0.8352, 19,454 eff tok, run
  150651-…-2ab65d, no rerun per frozen rule); WBD-003 FAIL generator
  error_max_budget_usd ($0.8561, 25,515 eff tok, run 151103-…-5665b9, no
  rerun); WBD-004 FAIL generator error_max_budget_usd ($0.7044, 16,769 eff
  tok, run 151431-…-3af07c, no rerun). Spend so far $3.05 of $18.
- WBD-005 FAIL generator error_max_budget_usd ($1.0506, 23,805 eff tok, run
  151821-…-7df0a2, held-out never exposed, no rerun). All 5 planned attempts
  done: 1/5 PASS (WBD-001 100), 4 generator failures. Measured spend $4.11 of
  $18. No stop condition hit (identity clean, telemetry complete every run).
- CLOSEOUT done: summarize pass; import 5/5 rows (dry-run first); validate
  pass (545 rows incl. driver row); artifact audit pass (23 dirs); round
  addendum appended (T-137 tables untouched, standalone/unmatched stated);
  T-139 report finalized with structured block last; `.claude/settings.json`
  restored to site-coordinator/low; codex-log line + driver metrics row
  appended; driver report `tools/out/driver-report-20260713-1526.md`.
- Prevention (driver): never `pkill -f` with a substring that can match the
  Bash wrapper's own command line (killed one wrapper pre-launch; verified no
  run started before relaunching WBD-001 once). Measured prevention: dynamic
  generator at Fable/max exhausts its budget slice 4/5 — harden generator
  before any further dynamic cohort.
- Next: final gates (selftest/artifacts/py-compile/md-size) then commit and
  push; T-139 closes. No publish/deploy in this experiment.
- Measured runs launched detached (setsid nohup + poll) so tool timeouts cannot
  kill a measured subprocess; command strings stay exactly as planned.
- T-138's uncommitted analysis bookkeeping remains in the working tree and must
  be preserved.

## Working set
- `.claude/agents/claude-benchmark-driver.md`, `.claude/settings.json`
- `skills/claude-benchmark.md`
- `tools/agent-benchmark/claude_benchmark.py`, `tools/task-metrics.py`,
  `tools/task-metrics.schema.json`
- `tools/out/t139-claude-dynamic-rerun.md` and generated plan
- `tools/todo.md`, `tools/state/session.md`, `tools/task-metrics.jsonl`,
  `tools/codex-log.md`
- Existing dirty T-138 bookkeeping: preserve, do not discard or rewrite.

## Open questions
- None. The T-137 vs T-139 provenance caveat (distinct refs and measured-layer
  identities; no matched cross-cohort comparison) is recorded durably in
  `tools/agent-benchmark/rounds/2026-07-13-claude.md` (T-139 addendum).

## Awaiting user
- None.

driver: codex
updated: 2026-07-15T06:31+0900
task: T-179 Consolidate post-incident recovery ledgers | idle
status: idle

## Now
- Harness and website recovery facts are consolidated into their `TODO.md`
  boards; superseded chronology was pruned from website facts/decisions.
- T-180 and harness T-172 are the first recovery-priority items and require an
  exhaustive read-only Git-history audit before other work.
- The old harness recovery handoff and exact T-179 driver report were removed
  after their unique facts were preserved. No pre-incident report was removed.
- Consolidation is complete. T-180 is now the next website task; its harness
  counterpart is T-172.

## Working set
- No public-site file. The intended ledger changes travel in one local website
  commit and one local harness commit; neither is pushed by this task.

## Open questions
- `tools/test-deploy-policy.sh` could not start its local file-transport check:
  line 31 reports `lftp: command not found`. No public file changed, and no
  network/deployment ran. Treat the missing normal-PATH tool as T-180 recovery
  evidence; do not install or improvise it during this ledger cleanup.

## Awaiting user
- None.

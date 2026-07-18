driver: claude
updated: 2026-07-19T00:30+0900
task: T-203 housekeeping
status: idle

## Now
- Housekeeping pass:
  1. Pruned 8 stale remote-tracking refs (`git remote prune origin`:
     board-refresh, docs/t190-stale-hook, feat/claude-takeover,
     harness-readonly-rule, t188-*, t190-*).
  2. Deleted the superseded local branch `t187-ruleset-closeout` (content in
     main). Left `t187-ruleset-validation` (has unmerged pre-existing
     checkpoint commits — not force-deleting others' work).
  3. Guarded-deleted 92 disposable Claude benchmark artifact dirs (~37 MB)
     via `tools/guarded-delete` plan/apply. VERIFIED protected_anchors=
     unchanged, targets=absent; artifacts 265→173. The 173 GPT artifacts and
     all tracked summaries + results.jsonl are intact. Manifest (scratch):
     gd2.manifest; retry-safe (targets already absent). Decision is durable
     in the committed Claude summary/README/results.jsonl.
- No tracked-file change except this ledger note. Board clear. Next ID: T-204.
- Skills applied: guarded-bulk-delete (mandatory for the artifact deletion),
  context-ledger.

## Working set
- None.

## Open questions
- None.

## Awaiting user
- None. (Optional: `t187-ruleset-validation` stale branch removal — say the
  word and I'll force-delete it.)

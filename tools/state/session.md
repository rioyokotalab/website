driver: codex
updated: 2026-07-13T00:12+0900
task: idle
status: idle

## Now
- Goal: idle after T-24 stale artifact cleanup.
- Last done: removed all approved current-tree targets and references; tracked `tools/` fell from 261 MiB to about 371 KiB. Ignored `.playwright/`, `node_modules/`, and Python caches are absent.
- Next: await a new owner task. A Git-history purge of old PDF blobs would require separate explicit destructive/force-push authorization.

## Working set
- Deleted tracked: `tools/judge/`, `skills/model-eval.md`, 41 `tools/papers/*.pdf`, `tools/researchmap-sync.md`.
- Deleted ignored caches: `.playwright/`, `node_modules/`, `tools/__pycache__/`; corrected `skills/settings-scope.md`, skill index, facts, and ledger.

## Open questions
- Historical PDF blobs remain in existing Git history; removing them from all commits is intentionally out of scope because it requires history rewrite and force-push.

## Awaiting user
- None.

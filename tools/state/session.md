driver: codex
updated: 2026-07-23T19:53+0900
task: T-204 relocate the Local website checkout
status: in-progress

## Now
- Preflight passed: source was clean at `f249ae8`, origin was current, and the
  move is cross-filesystem. The first clone's checkout was interrupted; its
  stale zero-owner-open index lock was exact-unlinked, then the index and
  worktree were restored from `HEAD` and verified clean.
- `.dont-remove-me` is a regular tracked public file; no content was read.
- All six ignored state roots were copied and matched by file count, symlink
  count, and bytes. `t187-ruleset-validation` is backed by an up-to-date
  remote branch.
- The destination clone is on `t204-relocate-website`; the remote-backed
  `t187-ruleset-validation` branch and canonical pre-commit hook are present.
- NFS made browser runtime state too slow, so the original `.playwright` state
  was moved intact to `~/.cache/website-playwright`; both checkouts expose it
  through an ignored symlink and its registration points only at the new
  physical checkout.
- Destination validation passed: `tools/test-security.sh`, task-metrics
  validation, hook doctor, and all 38 browser tests. Guarded-delete the old
  checkout, then close the ledger and publish through protected `main`.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `README.md`
- `tools/state/decisions.md`
- source `~/website`
- destination `~/projects/website`

## Open questions
- None.

## Awaiting user
- None.

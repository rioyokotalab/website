driver: claude
updated: 2026-07-18T15:45+0900
task: idle
status: idle

## Now
- T-190 complete. PR #7 merged as `e6faf3b` after required CI passed; owner
  applied the hook via `tools/hook-doctor.sh apply`. Doctor reports `ok`,
  live hook matches canonical byte-for-byte, pre-apply backup preserved, and
  the closing ledger commit passed the hook without bypass.
- Owner relaxed the live main ruleset (no required non-author review) and
  granted the standing authorization recorded in `tools/state/decisions.md`.
- Next task on the board: T-191 — reconcile the tracked ruleset payload and
  `tools/test-github-ruleset.sh` with the relaxed live rules (read-only
  against GitHub settings).

## Working set
- None.

## Open questions
- None.

## Awaiting user
- None.

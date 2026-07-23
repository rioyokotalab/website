driver: codex
updated: 2026-07-23T19:09+0900
task: T-204 relocate the Local website checkout
status: in-progress

## Now
- Preflight passed: source is clean at `f249ae8`, origin is current,
  destination is absent, and the move is cross-filesystem.
- `.dont-remove-me` is a regular tracked public file; no content was read.
- No visible untracked files or stashes exist. Six ignored state roots require
  preservation. `t187-ruleset-validation` is backed by an up-to-date remote
  branch.
- Clone the public origin into `~/projects/website`, preserve ignored state,
  repair Playwright's old absolute registration, and validate before deleting
  the source.

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

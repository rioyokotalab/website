driver: codex
updated: 2026-07-23T19:56+0900
task: idle
status: idle

## Now
- T-204 is complete locally. The repository now lives at
  `~/projects/website`; `~/website` and all guarded-delete transaction state
  are absent.
- All ignored state was preserved. `.playwright` is an ignored symlink to
  local `~/.cache/website-playwright`, avoiding NFS runtime timeouts while
  keeping the project checkout on backed-up storage.
- The public tracked sentinel was recreated by Git without content inspection.
  The canonical hook and remote-backed `t187-ruleset-validation` branch are
  present.
- Offline checks, task-metrics validation, hook doctor, and all 38 browser
  tests pass. Publish the closeout commit and merge its protected PR.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `tools/codex-log.md`
- `tools/task-metrics.jsonl`
- `tools/out/driver-report-20260723-1956.md`

## Open questions
- None.

## Awaiting user
- None.

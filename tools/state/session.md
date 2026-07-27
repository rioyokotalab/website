driver: codex
updated: 2026-07-27T12:20+0900
task: T-210 update checkout and reconcile live protection
status: in-progress

## Now

- T-209 is complete: PR #35 merged at `141a79e`.
- T-210 updates the immutable `actions/checkout` pin from v7.0.0 SHA
  `9c091bb` to publisher-verified v7.0.1 SHA `3d3c42e`.
- Live ruleset `19127356` currently has zero required approvals and an
  always-bypass RepositoryRole actor, while the durable T-198 decision says
  one approval plus admin bypass. Record the drift without changing settings.

## Working set

- `.github/workflows/ci.yml`
- `tools/hook-doctor.sh`
- `tools/test-hook-doctor.sh`
- `TODO.md`
- `tools/state/session.md`
- `tools/out/driver-report-20260727-1220.md`
- `tools/task-metrics.jsonl`
- `tools/codex-log.md`

## Open questions

- None.

## Awaiting user

- None.

## Next action

- Run focused and offline security checks, checkpoint the public report and
  metrics, commit/push, open a protected PR, and merge only after current
  `Offline checks` passes. Do not deploy or alter the live ruleset.

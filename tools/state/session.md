driver: codex
updated: 2026-07-16T08:50+0900
task: T-184 Reconcile global PIE and node-onboarding skill work
status: awaiting-user

## Now
- Harness T-189 created and validated the shared PIE skill. T-190 used it to
  write the complete onboarding plan. D1 is frozen as explicit `onboard HOST`
  without SSH-config inspection. D2 retains one owner-only Restic password
  checkpoint and never inspects credential content. D3 freezes full first-run
  parity, including storage and verified encrypted backup while excluding
  scheduling and unreviewed deletion. T-190 is `ready-for-go`; no onboarding
  implementation has started.
- Website work is ledger-only housekeeping. No public tree, deployment,
  credential, SSH configuration, package, remote, or push is in scope.

## Working set
- `TODO.md`
- `tools/state/session.md`
- final driver report, metrics row, and driver log entry

## Open questions
- None.

## Awaiting user
- T-190 awaits the owner's explicit `go` for the frozen execution plan.

driver: claude
updated: 2026-07-18T15:20+0900
task: T-190 Repair the stale local pre-commit hook safely
status: awaiting-user

## Now
- Tracked T-190 work is complete: canonical `tools/hooks/pre-commit`,
  `tools/hook-doctor.sh` (doctor/apply/rollback, tests never touch real .git),
  `tools/test-hook-doctor.sh` (8 checks) wired into `tools/test-security.sh`,
  README section 4 installs via the doctor. Full offline suite passed.
- Doctor confirms the live hook is stale; no `.git` edit, no `--no-verify`,
  removed checker not restored. TODO pruned completed T-180 detail to stay
  within budget (Git keeps the full text).
- Next: land the PR through the protected main route, then owner runs
  `tools/out/t190-hook-apply-handoff.md` (apply + ordinary commit). After
  owner confirmation, mark T-190 complete in TODO.md.

## Working set
- Branch t190-hook-doctor: tools/hooks/pre-commit, tools/hook-doctor.sh,
  tools/test-hook-doctor.sh, tools/test-security.sh, README.md, TODO.md,
  session.md, driver report, metrics, codex-log.

## Open questions
- None.

## Awaiting user
- Run `tools/hook-doctor.sh apply` per tools/out/t190-hook-apply-handoff.md,
  verify doctor `ok` and one ordinary commit without bypass, then confirm.
- Approve/merge the T-190 PR (non-author review required by the main ruleset).

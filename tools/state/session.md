driver: codex
updated: 2026-08-03T17:51+0900
task: Web-219
status: in-progress

## Now

- Web-219 removes the tracked zero-byte local `.dont-remove-me` placeholder
  while preserving the remote deployment sentinel, mirror exclusion, positive
  deployment allowlist, live exclusion check, and preview refusal.
- Focused deployment-policy, complete offline, and 38/38 browser checks pass.

## Working set

- `.dont-remove-me`
- `AGENTS.md`
- `README.md`
- `skills/html-editing.md`
- `skills/publish-and-verify.md`
- `tools/test-deploy-policy.sh`
- `TODO.md`
- `docs/tasks/Web-219.md`
- `tools/state/session.md`

## Open questions

- None.

## Awaiting user

- None.

## Next action

- Publish without deploying. Guarded-delete the three obsolete unregistered
  Website directories only after the protected change lands.

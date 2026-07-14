driver: codex
updated: 2026-07-14T15:28+0900
task: T-178 Align repository housekeeping paths | idle
status: idle

## Now
- T-178 is complete. The website board is root `TODO.md`, and every current
  website instruction, README, playbook, size check, achievement tracker, and
  benchmark-protection reference uses that path.
- Harness client sources are `.codex/` and `.claude/`; documentation, global
  guidance, allowlist, internal guidance link, and installer paths are aligned.
- Live Codex/Claude discovery links resolve through the new paths. The installer
  migrates only exact legacy targets and remains idempotent and fail-closed for
  unrelated paths.
- Website security/metadata checks and harness isolated migration, live-link,
  stale-reference, and clean-clone restore checks pass.

## Working set
- None.

## Open questions
- None; the requested naming and scope are explicit.

## Awaiting user
- None.

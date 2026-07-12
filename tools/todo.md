# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-21.

## Active

### T-17 — add real-browser consent regression coverage
Add a reproducible headless-browser check for the bilingual GA banner,
keyboard/mobile behavior, accept/reject persistence and revocation, and zero
Google requests before consent. Keep it repo-only and runnable without account
credentials.

### T-20 — make the Claude preview hook account-portable
Replace the absolute `/home/rioyokota/website` path in the committed Claude
SessionStart/SessionEnd hook with a project-root-aware form, under explicit
project-config scope, then verify concurrent clones do not control each other's
preview process.

## Blocked / awaiting user

### T-18 — confirm GA Admin privacy settings
In the GA4 property, set event-data retention to 2 months and confirm Google
Signals/advertising features remain disabled. This is owner-account work; never
request or automate credentials. Record only the confirmed settings afterward.

## Recently completed

- 2026-07-12 T-16 hardened `publish.sh`: main/rebase/placeholder/dry-run gates, commit+push before deploy, clean-worktree push, phase-specific failure states, and seven isolated regression scenarios.
- 2026-07-12 T-15 aligned README, Claude/Codex role instructions, context ledger, publish playbook, and durable decision on standing direct-DRIVER authority versus dispatched/MCP worker prohibition.
- 2026-07-12 T-19 restored the README cluster quickstart with exact verified install/auth/clone/config/MCP/hook/check/launch commands; account-portability of the Claude preview hook remains T-20.

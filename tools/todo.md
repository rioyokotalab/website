# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-21.

## Active

### T-15 — align DRIVER publish documentation
Make `README.md`, `CLAUDE.md`, `AGENTS.md`, `skills/context-ledger.md`, and
`skills/publish-and-verify.md` agree with standing direct-DRIVER authority,
while keeping dispatched/MCP workers prohibited. Verify no stale approval-only
or ownership wording remains.

### T-16 — harden the publish pipeline
Update and test `publish.sh` so it pushes already-committed ahead-of-origin
changes even with a clean worktree, performs/enforces the required rebase
preflight, refuses known placeholders, and reports partial deploy/push failure
states clearly without touching credentials.

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

- 2026-07-12 T-19 restored the README cluster quickstart with exact verified install/auth/clone/config/MCP/hook/check/launch commands; account-portability of the Claude preview hook remains T-20.

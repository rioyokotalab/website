# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-23.

## Active

### T-20 — make the Claude preview hook account-portable
Replace the absolute `/home/rioyokota/website` path in the committed Claude
SessionStart/SessionEnd hook with a project-root-aware form, under explicit
project-config scope, then verify concurrent clones do not control each other's
preview process.

### T-21 — allow Codex to use agents without capability loss
Design and apply a direct Codex DRIVER delegation policy that permits agents for
bounded, independent work while minimizing root-context/token usage. Preserve
full task quality through explicit context pointers, tier/model selection,
output-file-first handoffs, non-overlapping write scopes, root review, and
proportional verification; benchmark representative solo versus delegated tasks
before replacing the current work-solo rule.

## Blocked / awaiting user

### T-22 — audit website/CV/researchmap/ORCID field mirroring
Audit and safe local fixes are complete: postal code 152-8550 is consistent,
the Keio RA role is removed everywhere, and the CV PDF is rebuilt. Automatic
external writes are unavailable without adding a credential-bearing researchmap
WebAPI client; ORCID is manual-only. Owner uploads remain for the approved
29-line `tools/out/researchmap-import.jsonl` and nine-work
`tools/out/orcid-works-selection.bib`; the owner or Claude site-publisher must
deploy the pushed CV/profile changes. Never automate either account login.

### T-18 — confirm GA Admin privacy settings
In the GA4 property, set event-data retention to 2 months and confirm Google
Signals/advertising features remain disabled. This is owner-account work; never
request or automate credentials. Record only the confirmed settings afterward.

## Recently completed

- 2026-07-12 T-17 added pinned real-Chromium consent regression coverage for EN/JP desktop/mobile, keyboard use, persistence, revocation, and the zero-request-before-consent boundary; browser tooling and artifacts are deploy-excluded.
- 2026-07-12 T-16 hardened `publish.sh`: main/rebase/placeholder/dry-run gates, commit+push before deploy, clean-worktree push, phase-specific failure states, and seven isolated regression scenarios.
- 2026-07-12 T-15 aligned README, Claude/Codex role instructions, context ledger, publish playbook, and durable decision on standing direct-DRIVER authority versus dispatched/MCP worker prohibition.
- 2026-07-12 T-19 restored the README cluster quickstart with exact verified install/auth/clone/config/MCP/hook/check/launch commands; account-portability of the Claude preview hook remains T-20.

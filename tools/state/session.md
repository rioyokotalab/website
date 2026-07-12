driver: codex
updated: 2026-07-12T20:40+0900
task: idle
status: idle

## Now
- Goal: idle after T-14; T-12 remains blocked.
- Last done: completed and verified the direct Codex DRIVER standing publish/push policy with mandatory fail-closed preflight; dispatched/MCP workers remain prohibited.
- Next: commit and push T-14 plus ledger bookkeeping after pull/rebase; do not deploy T-12's placeholder. Then await owner direction on T-12.

## Working set
- T-14 policy: `AGENTS.md`, `skills/publish-and-verify.md`.
- Ledger: `tools/todo.md`, `tools/state/session.md`, `tools/state/decisions.md`.
- Evidence: `tools/out/t14-direct-publish-policy.md`; `tools/out/driver-report-20260712-2040.md`.
- Verification passed: targeted stale-policy `rg`, markdown/CLAUDE size checks, `git diff --check`, full diff review.

## Open questions
- Optional future task: shell-level defense-in-depth in `publish.sh`; not required for T-14.

## Awaiting user
- T-12: real GA4 `G-...` measurement ID and privacy/consent decision; never publish `G-XXXXXXXXXX`.

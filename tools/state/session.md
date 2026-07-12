driver: codex
updated: 2026-07-12T22:02+0900
task: idle
status: idle

## Now
- Goal: idle after T-16 publish-pipeline hardening.
- Last done: `publish.sh` now enforces main/rebase/placeholder/dry-run gates, commits and pushes before deploy, pushes clean ahead commits, and reports safe partial states; seven isolated tests pass.
- Next: start T-17 unless the owner explicitly authorizes T-20 project-config work.

## Working set
- T-16 files: `publish.sh`, `tools/test-publish.sh`, `skills/publish-and-verify.md`.
- Verification passed: Bash syntax; executable modes; clean-ahead push; nonconflicting rebase; conflicting rebase abort; included/excluded placeholder behavior; push failure prevents deploy; deploy failure reports pushed/possibly-partial state; markdown/diff/empty-output checks.

## Open questions
- None for T-16; T-20 remains separately scoped.

## Awaiting user
- T-18 requires owner access to GA Admin; no credentials should be shared.

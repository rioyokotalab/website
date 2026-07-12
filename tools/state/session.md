driver: codex
updated: 2026-07-13T00:20+0900
task: T-25 purge archived PDF blobs from Git history
status: in-progress

## Now
- Goal: remove all historical `tools/papers/` blobs from every GitHub-visible ref and local reachable history.
- Last done: owner explicitly authorized destructive history removal. Inventory: clean main, one remote branch, eight remote evaluation tags, all eight tags affected, 2 commits/41 path objects, no `git-filter-repo` installed.
- Next: commit this checkpoint, create a temporary all-ref rollback bundle outside the repository, rewrite all refs with `git filter-branch` index filtering, remove backup refs, verify locally, then force-update main and affected tags with exact expected-old-value leases.

## Working set
- Original remote main: `78fe51a5b3c57f3af4df1ce44aeab6a634e5a375`; affected tags: `eval/r1-{fable,opus,sol,terra}`, `eval/r2-{fable,opus,sol,terra}`.
- Safety: temporary `/tmp/website-pre-pdf-purge.bundle`; do not retain or push any pre-rewrite backup ref after verification.

## Open questions
- Every existing clone will refer to obsolete commit IDs after the rewrite; communicate reclone/reset requirement in final handoff.

## Awaiting user
- None.

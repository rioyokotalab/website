driver: codex
updated: 2026-07-13T01:43+0900
task: T-28 minimize deploy and web-server exposure
status: in-progress

## Now
- Goal: publish and live-verify T-28 fail-closed deployment and server exposure controls.
- Last done: commit `747cdc0` deployed the allowlist and removed stale remote `tools/`, but immediate validation found HTTP 500 on all paths because this Apache host rejects one or more new `.htaccess` access-control directives. Clean deploy dry-run confirms the staging policy itself converges.
- Next: roll `.htaccess` back to the previously working header-only form via commit-before-deploy, verify public 200s immediately, then retain server-layer denial as unresolved and rely on positive staging plus existing server directory controls.

## Working set
- T-28 public roots: `.htaccess`, `index.html`, `style.css`, `en/`, `jp/`, `images/`, `js/`, and only `cv/cv.pdf`.
- Publish scope: `.htaccess` plus repository-only deploy/publish scripts, manifest, tests, docs, and ledger. Expected remote deletion: stale empty `tools/` directory only.

## Open questions
- Rollback condition triggered and is being applied; do not claim T-28 complete until public HTTP is restored.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

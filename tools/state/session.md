driver: codex
updated: 2026-07-13T01:36+0900
task: T-28 minimize deploy and web-server exposure
status: in-progress

## Now
- Goal: publish and live-verify T-28 fail-closed deployment and server exposure controls.
- Last done: staging contains exactly 149 manifest files; isolated tests prove unexpected files cannot stage, rogue/stale remote files delete, sentinel survives, symlinks fail closed, and all seven publish regressions pass. Real dry-run shows only `.htaccess` upload plus deletion of the stale empty remote `tools/` directory.
- Next: run publish transaction; immediately verify public pages remain 200, `.dont-remove-me` changes from 200 to denied, directory listing/source paths are denied/absent, remote `tools/` is gone, and a clean dry-run has no changes.

## Working set
- T-28 public roots: `.htaccess`, `index.html`, `style.css`, `en/`, `jp/`, `images/`, `js/`, and only `cv/cv.pdf`.
- Publish scope: `.htaccess` plus repository-only deploy/publish scripts, manifest, tests, docs, and ledger. Expected remote deletion: stale empty `tools/` directory only.

## Open questions
- Apache directive compatibility cannot be proven locally because Apache is not installed; immediate live 200/403 checks are mandatory, with rollback on HTTP 500.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

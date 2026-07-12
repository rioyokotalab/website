driver: codex
updated: 2026-07-13T00:46+0900
task: T-41 improve back-to-top semantics and reduced-motion behavior
status: in-progress

## Now
- Goal: make the arrow-only back-to-top control semantically clear and motion-preference aware without visual change.
- Last done: T-41 implementation is complete across all 26 pages: stable `body#top`, localized accessible names, explicit `#top` targets, reduced-motion-aware CSS/JS, cache bump, and a permanent standards invariant. The full deterministic suite and live-browser EN/JP normal/reduced-motion checks pass.
- Next: rebase, inspect the deployment dry-run, publish T-41, verify the live EN/JP controls and headers, then close T-41 and start T-42.

## Working set
- All 26 EN/JP pages, `js/pagetop.js`, shared CSS/cache bump, browser/standards tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

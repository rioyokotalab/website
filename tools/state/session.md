driver: codex
updated: 2026-07-13T00:46+0900
task: T-55 migrate obsolete nowrap table attributes
status: in-progress

## Now
- Goal: replace all obsolete nowrap attributes with a shared class while preserving exact News date-cell wrapping and table geometry.
- Last done: T-55 migrates all 152 News nowrap attributes (98 EN, 54 JP) to `.no-wrap`, cache-busts shared CSS, and permanently enforces zero legacy attributes/exact class counts. Full suite passes; recent/middle/old cells retain nowrap, cell dimensions, and row heights within 1px in both languages at desktop/mobile.
- Next: rebase, inspect the two-News/CSS/cache deployment preview, publish T-55, verify live computed nowrap, then close T-55 and start T-56 in bounded News/non-News batches.

## Working set
- EN/JP News table cells, shared `.no-wrap` CSS/cache bump, exact standards counts, representative desktop/mobile row geometry, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

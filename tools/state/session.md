driver: codex
updated: 2026-07-13T05:00+0900
task: T-74 modernize print presentation
status: in-progress

## Now
- Goal: make printed/PDF pages content-first and legible by removing interactive chrome and fixed overlays while retaining useful content, tables, maps, and link destinations.
- Last done: T-73 verified all 26 pages have zero page-level horizontal overflow at 640/320px, consent and open menus fit EN/JP, maps fit, table overflow remains keyboard-local, and Lightbox image/close controls fit after its documented transition; no reflow CSS was needed.
- Next: emulate print media on representative home/news/research/contact/profile/gallery pages, inventory visible navigation/fixed overlays/clipping/page widths and link destination behavior, then add the smallest print-only stylesheet rules supported by the audit.

## Working set
- Representative EN/JP print rendering at A4-like viewport; visible regions, fixed controls, table/image/map widths and link annotations; print-only CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

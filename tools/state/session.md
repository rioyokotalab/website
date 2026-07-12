driver: codex
updated: 2026-07-13T03:31+0900
task: T-68 improve data-table header semantics
status: in-progress

## Now
- Goal: give genuine data tables explicit header relationships while leaving layout tables and all rendered geometry untouched.
- Last done: T-67 corrected four mismatched titles, made all 26 bilingual title/description pairs unique and page-local, mirrored descriptions into Open Graph, enforced exact route titles plus description length/uniqueness, and preserved all landmark geometry at 390/1200px.
- Next: inventory all 38 tables by page, dimensions, cell tags/content and nesting; classify data versus layout; render candidate `td` to `th scope` changes against the current commit before accepting any edit.

## Working set
- All 38 public tables, nested-table structure, current computed cell geometry/styles, any scoped semantic markup/CSS and standards enforcement; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

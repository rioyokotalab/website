driver: codex
updated: 2026-07-13T04:37+0900
task: T-99 name full news-archive tables
status: in-progress

## Now
- Goal: expose useful names for every EN/JP full news-archive table without adding visible content or changing dimensions.
- Last done: T-98 added native localized visually-hidden captions to both home-news tables, preserved clipped 1×1 caption geometry and 48 total row headers, and passed exact static, five layout/name browser, fast, and staging checks.
- Next: map 11 yearly tables per language to existing `Y20xx` headings, name the one nested seminar-details table per language, enforce all 24 names, and compare accessibility/layout trees.

## Working set
- EN/JP news archive tables, year headings/IDs, nested seminar table, accessible names, layout/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T04:39+0900
task: T-100 name cluster hardware tables
status: in-progress

## Now
- Goal: expose a concise localized name for each mirrored Hinadori hardware table without changing specifications or pixels.
- Last done: T-99 associated 22 yearly tables with their existing `Y20xx` headings, named two nested seminar-details tables, and passed exact static, five layout/name browser, fast, and staging checks.
- Next: confirm the two Computers tables have identical purpose/headers, add native visually-hidden localized captions, enforce exact placement, and compare names/geometry.

## Working set
- EN/JP Computers hardware tables, native captions, column headers/specifications, accessible names and geometry.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T04:35+0900
task: T-98 name home-news data tables
status: in-progress

## Now
- Goal: expose concise localized names for the home-news data tables without adding visible text or changing geometry.
- Last done: T-97 removed two unused empty gallery hooks and five exclusive dead CSS selector families, retained live `img.frame` styling, synchronized root/route CSS cache versions, and passed CSS-source, six layout/no-JS, fast, and staging checks.
- Next: inspect rendered table names, add native visually-hidden EN/JP captions to the two home-news tables, enforce exact placement/text, and compare table geometry/accessibility trees.

## Working set
- EN/JP home-news tables, native captions, accessible names, row structure and geometry, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

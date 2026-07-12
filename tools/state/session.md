driver: codex
updated: 2026-07-13T04:08+0900
task: T-88 audit meaningful image alternatives
status: in-progress

## Now
- Goal: ensure image alternatives communicate purpose without repeating nearby text or exposing decorative filenames.
- Last done: T-87 replaced CSS-hidden institutional headings with non-heading metadata and added exactly one localized native visually-hidden `h1` per page; static gates and seven route/layout/no-JS browser contracts pass without visible layout changes.
- Next: inventory every rendered image's element role, link context, alternative, caption, and EN/JP pairing; reproduce accessibility-tree problems before making narrow corrections.

## Working set
- Public image elements, links/captions, accessible names/descriptions, EN/JP pairing, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

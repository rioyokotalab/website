driver: codex
updated: 2026-07-13T04:16+0900
task: T-90 identify alternate-language navigation links
status: in-progress

## Now
- Goal: expose destination language on every visible EN↔JP route switch while keeping link text and layout untouched.
- Last done: T-89 traversed all focusable elements on every route at 390/1200px, reproduced the header logo link's 0×0 focus box, added a containing inline-block anchor, and passed exhaustive forward/reverse keyboard, layout, forced-color, fast, and staging checks.
- Next: inventory language-switch href/text/hreflang across all mirrored pages, then add and enforce exact localized destination hints if absent.

## Working set
- EN/JP header language-switch links, mirrored routes, `hreflang`, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

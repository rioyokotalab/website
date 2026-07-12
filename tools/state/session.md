driver: codex
updated: 2026-07-13T03:14+0900
task: T-79 audit CSS redundancy after modernization
status: in-progress

## Now
- Goal: remove only proven-redundant CSS while preserving the established visual design and every modernized state.
- Last done: T-78 audited all 26 routes at 320/1200px plus the root entry without JavaScript; the only confirmed loss was an inert mobile hamburger, now progressively exposed by an early `html.js` hook while navigation stays expanded without scripts. Two permanent tests cover all routes and all 12 browser tests pass.
- Next: inventory duplicate declarations and selectors absent from source/runtime; exercise all page families plus mobile/desktop, dark, print, forced-colors, consent, open-menu, table, and gallery states before removing only independently proven redundancy.

## Working set
- `style.css`; all public markup and runtime-generated component DOM; CSS coverage/static selector inventory; screen/print/dark/forced-color geometry and appearance contracts; standards/test bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

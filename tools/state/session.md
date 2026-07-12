driver: codex
updated: 2026-07-13T03:24+0900
task: T-80 replace obsolete member-table column sizing
status: in-progress

## Now
- Goal: replace the final mirrored obsolete `<col width>` attributes without moving or resizing the member biography tables.
- Last done: T-79 removed rules whose nine class tokens and one ID token were absent from every public HTML/runtime script, added a gate over all remaining selectors, and matched baseline/working geometry plus 27 computed properties exactly in 60 route/state pairs spanning desktop/mobile, light/dark, print, and forced colors.
- Next: capture both member-table column geometries at 320/390/1200px and print; replace the two `width="72"` attributes with one shared class rule, enforce the migration, and compare exact rendered columns before/after.

## Working set
- `en/member/index.html`, `jp/member/index.html`, `style.css`, standards checks; mirrored member biography columns at screen/print responsive states; cache/ledger bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

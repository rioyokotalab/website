driver: codex
updated: 2026-07-13T04:16+0900
task: T-71 audit oversized image delivery
status: in-progress

## Now
- Goal: identify material image transfer waste relative to rendered dimensions and choose only lossless or visually verified reductions that retain every original and preserve appearance.
- Last done: T-70 confirmed forced colors preserved content/consent/tables but erased current-page distinction and exposed a 22px dot-like menu icon; added normal/forced current state, forced focus, and a 42x42 three-bar button, then passed forced screenshots and EN/JP 320/390/900/901 operation.
- Next: collect encoded bytes, intrinsic dimensions, MIME, alpha/animation metadata, and maximum rendered sizes for all images across 390/1200px pages; rank byte/pixel oversupply and distinguish shared hero/gallery/content assets before proposing edits.

## Working set
- All public raster assets plus rendered usage at 390/1200px; file type/dimensions/bytes/alpha and duplicate hashes; candidate optimization report or verified variants; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

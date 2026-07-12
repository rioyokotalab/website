driver: codex
updated: 2026-07-13T04:48+0900
task: T-73 verify high-zoom reflow
status: in-progress

## Now
- Goal: preserve content and operation at browser-equivalent 200%/400% zoom without two-dimensional page scrolling, clipping, or fixed-overlay obstruction.
- Last done: T-72 measured 1,920 visible targets at 320/390px; all 946 sub-24px text links passed the 24px center-spacing exception, open mobile nav items were 55.5px, consent buttons 48px, settings 35px, and hamburger 42px, so no density-changing CSS was justified.
- Next: emulate 200% (640px effective) and 400% (320px effective) reflow across representative EN/JP long/short/table/map/gallery pages, inspect document overflow and fixed overlays with menus/consent open, and isolate true clipping from intentional table scroll regions.

## Working set
- Representative page families at 640/320px effective widths with menu/consent/table/gallery states; overflow/occlusion geometry and screenshots; any scoped reflow CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

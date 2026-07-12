driver: codex
updated: 2026-07-13T04:36+0900
task: T-72 audit mobile touch targets
status: in-progress

## Now
- Goal: make standalone mobile controls comfortably operable while respecting WCAG inline-text exceptions and preserving content density and desktop geometry.
- Last done: T-71 isolated seven gallery originals totaling 39.66MiB, retained them for Lightbox, added 720/1200px display variants totaling 0.92/2.21MiB, preserved ICC profiles, visually inspected difficult pairs, enforced dimensions/450KiB budgets, and verified EN/JP 1x/2x/3x source selection plus original zoom.
- Next: render every page at 320/390px, inventory visible anchor/button bounding boxes and center-to-center spacing by structural context, exclude inline prose links, and rank standalone targets below 24/44px before any CSS change.

## Working set
- All 26 pages at 320/390px with mobile menus open and consent states; target geometry/context/spacing; any tightly scoped mobile CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

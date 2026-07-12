driver: codex
updated: 2026-07-13T02:46+0900
task: T-65 audit text and control color contrast
status: in-progress

## Now
- Goal: identify and correct only confirmed persistent text/control contrast failures while retaining the current palette, typography, geometry, and content.
- Last done: T-64 traversed 2,131 keyboard stops across all pages at 390/1200px, confirmed every stop had an indicator, replaced the single blue ring with a white-plus-existing-blue two-tone ring, and passed representative light/dark/control checks.
- Next: inventory computed visible text foreground/background pairs in light and dark modes, calculate WCAG ratios by font size/weight and control-boundary requirements, then isolate confirmed failures before editing.

## Working set
- All page families plus generated analytics controls in light/dark modes; computed color/background/font metrics; any palette-only CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

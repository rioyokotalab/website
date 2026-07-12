driver: codex
updated: 2026-07-13T05:18+0900
task: T-75 audit gallery dialog accessibility
status: in-progress

## Now
- Goal: ensure the pinned Lightbox gallery behaves as a properly labeled, keyboard-operable modal with focus containment and reliable focus return in EN/JP without replacing the library.
- Last done: T-74 found print ignored all CSS due media=screen, changed it to media=all, added an isolated content-first print layer with plain page title, constrained images/tables, hid interactive/fixed chrome, eliminated overflow on all 26 pages, visually inspected output, and matched exact screen geometry at 390/1200px.
- Next: open first/middle gallery items by keyboard on EN/JP picture/research/computers, inspect accessibility roles/names/control focusability, Tab/Shift+Tab containment, arrows/Escape, background inertness, and trigger focus return; classify library gaps before adding local JS/CSS.

## Working set
- Six EN/JP Lightbox pages and first/middle/last items; accessibility tree, keyboard sequence, modal/background focus behavior, focus return; any local compatibility JS/CSS/cache/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

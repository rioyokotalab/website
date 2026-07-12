driver: codex
updated: 2026-07-13T00:46+0900
task: T-54 unify responsive navigation breakpoint
status: in-progress

## Now
- Goal: eliminate the 801–900px gap where mobile CSS is active but the hamburger script returns without wiring the control.
- Last done: T-54 replaces the 800px JS cutoff with the CSS-equivalent 900px media query and removes the exact-900 overlap by moving desktop CSS to min-width 901px. Script/style references are cache-busted and enforced. Full suite passes; EN/JP controls open/close correctly at 800/801/850/900 and remain desktop-hidden at 901, while <=800 geometry is exact against live.
- Next: rebase, inspect the JS/CSS/cache deployment preview, publish T-54, verify live 850/900/901 behavior, then close T-54 and start T-55.

## Working set
- `js/responsive-menu.js`, its 26 cache-busted references, exact standards check, EN/JP boundary browser behavior/geometry, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

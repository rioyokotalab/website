driver: codex
updated: 2026-07-13T01:35+0900
task: T-40 simplify the legacy menu JavaScript
status: in-progress

## Now
- Goal: replace legacy global/polyfill menu code with one small scoped modern script and unchanged behavior.
- Last done: folded menu initialization/toggling into scoped modern `responsive-menu.js`, removed 26 loaders and obsolete `openclose.js`. Regression caught native button visibility on desktop from T-39; added explicit default hide plus mobile override and cache bump. EN/JP mobile keyboard/pointer state and desktop visibility now pass 2/2; all offline gates pass.
- Next: run consent/publish regressions, preview deletion-bearing T-40 scope, publish, verify removed asset 404 and live desktop/mobile behavior, then advance to T-41.

## Working set
- All 26 EN/JP pages, `js/openclose.js`, `js/responsive-menu.js`, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

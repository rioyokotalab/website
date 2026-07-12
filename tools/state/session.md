driver: codex
updated: 2026-07-13T00:43+0900
task: T-34 add accessibility landmarks and skip navigation
status: in-progress

## Now
- Goal: add modern semantic landmarks and a keyboard-visible skip link without changing normal visual layout.
- Last done: all 26 pages now have semantic header/main/footer, distinct desktop/mobile navigation labels, and localized focus-visible skip links. Shared CSS bumped to 20260713. Landmark counts/security/publish suites pass; desktop/mobile geometry matches live baseline within 1px and returning-visitor skip focus works (browser 3/3).
- Next: inspect the deploy preview, publish T-34, verify live layout/focus/landmarks in EN/JP, then advance to T-35.

## Working set
- All 26 EN/JP HTML pages, `style.css` and cache-bust references, browser/accessibility tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

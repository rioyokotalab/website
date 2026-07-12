driver: codex
updated: 2026-07-13T00:59+0900
task: T-38 eliminate duplicate document identifiers
status: in-progress

## Now
- Goal: make every HTML `id` unique without changing navigation layout or historical content.
- Last done: converted both menus on all 26 pages from duplicated IDs to shared `topnav` class, updated CSS/cache version, and aligned EN `ev190903_2/_1` anchors with JP. All page IDs are unique; security suite passes; desktop/mobile menu geometry stays within 1px and distinct fragments resolve (browser 3/3).
- Next: remove temporary test, run full publish/size checks, preview/publish T-38, verify live IDs/fragments/layout, then implement T-37 permanent standards checks.

## Working set
- All 26 EN/JP pages, EN news anchors, `style.css` and cache-bust references, browser/fragment tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

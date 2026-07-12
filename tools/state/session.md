driver: codex
updated: 2026-07-13T00:46+0900
task: T-45 improve embedded map semantics and responsiveness
status: in-progress

## Now
- Goal: give both map embeds localized accessible names and shared responsive presentation while preserving their exact rendered geometry.
- Last done: T-44 was published as `227fef0` and representative live pages have exact two/one/zero current markers. T-45 moved the percentage width, fixed height, and border to `.location-map`, added localized titles, and permanently enforces the embed contract. Full suite passes; EN pre/post geometry is exact at 1280px and 390px, and JP matches the same width/height.
- Next: rebase, inspect the contact/CSS/cache-bump deployment preview, publish T-45, verify both live embeds, then close T-45 and start T-46.

## Working set
- EN/JP Contact embeds, shared CSS and site-wide cache version, iframe standards checks, desktop/mobile geometry verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

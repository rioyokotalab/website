driver: codex
updated: 2026-07-13T00:46+0900
task: T-50 prioritize the above-the-fold hero image
status: in-progress

## Now
- Goal: explicitly prioritize the single above-the-fold hero banner on every mirrored page without changing image loading classes or presentation.
- Last done: T-50 adds exactly one high fetch priority to the hero banner on every page and permanently rejects missing/extra/non-hero priority hints. Full suite passes; EN/JP home/subpage banners load naturally and preserve live dimensions within 1px at 1280px and 390px.
- Next: rebase, inspect the hero-markup-only deployment preview, publish T-50, verify representative live attributes, then close T-50 and start T-51 in a small anchor-family batch.

## Working set
- All 26 banner-top/sub image elements, exact fetch-priority standards checks, representative geometry/load browser verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

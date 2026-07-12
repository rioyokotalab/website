driver: codex
updated: 2026-07-13T06:04+0900
task: T-78 audit no-JavaScript resilience
status: in-progress

## Now
- Goal: verify every public route remains navigable and content-complete without JavaScript, with explicit fallbacks only for confirmed essential losses.
- Last done: T-77 added tolerant contracts over 14 EN/JP page-family routes at five responsive boundaries (70 rendered states), requiring ordered visible/contained major regions and exact page width; added 1x/2x/3x responsive-source and 320px local table-scroll checks; all four layout tests pass.
- Next: launch JavaScript-disabled contexts across all 26 pages plus root entry, verify primary/utility/navigation links, content text/images/local URLs, gallery-original destinations, contact data and metadata; inspect mobile menu discoverability and classify enhancements versus essential fallback gaps.

## Working set
- Root plus all 26 routes in JavaScript-disabled 320/1200px contexts; navigation/content/gallery/contact/canonical metadata and overflow; any semantic noscript/fallback markup with parity/checker/tests; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:46+0900
task: T-51 modernize legacy named section anchors
status: in-progress

## Now
- Goal: replace obsolete empty named anchors with IDs on semantic target elements while preserving every fragment and scroll destination in reviewable batches.
- Last done: T-51 second batch converts all 152 equal News name/id anchors (81 EN, 71 JP) to same-position span IDs; 48 mismatches remain and exact-equality anchors are permanently rejected. Full suite passes, and representative EN/JP recent/old event fragments preserve scrollY, target, and date-cell positions exactly at desktop/mobile.
- Next: rebase, inspect and publish the two-News-page checkpoint, verify live event fragments, then audit the 48 mismatched aliases for collision-safe resolution before the final T-51 batch.

## Working set
- EN/JP News exact event anchors and 48 ambiguous aliases, fragment-target/unique-ID standards checks, representative live/local scroll-position comparisons, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

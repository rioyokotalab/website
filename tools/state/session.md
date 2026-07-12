driver: codex
updated: 2026-07-13T00:46+0900
task: T-51 modernize legacy named section anchors
status: in-progress

## Now
- Goal: replace obsolete empty named anchors with IDs on semantic target elements while preserving every fragment and scroll destination in reviewable batches.
- Last done: T-51 first batch migrated the verified 100 heading-start targets (47 EN, 53 JP) to semantic H3 IDs; only 200 News event anchors remain. Permanent checks enforce location/count and fragment/ID validity. A scoped -10px scroll margin exactly preserves historical `scrollY` and visible heading position on tested EN/JP About and Contact targets at desktop/mobile; the full suite passes.
- Next: rebase, inspect and publish the heading-anchor/CSS-cache checkpoint, verify live fragments, then migrate the remaining News event anchors as a separate T-51 batch.

## Working set
- 100 heading-start named anchors across EN/JP, fragment-target and unique-ID standards checks, representative live/local scroll-position comparisons, ledger/bookkeeping. The 200 News event anchors remain a separate T-51 batch.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

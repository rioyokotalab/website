driver: codex
updated: 2026-07-13T00:46+0900
task: T-51 modernize legacy named section anchors
status: in-progress

## Now
- Goal: replace obsolete empty named anchors with IDs on semantic target elements while preserving every fragment and scroll destination in reviewable batches.
- Last done: T-51 final batch preserves 33 unique mismatched names as adjacent ID aliases, retains the 48 current IDs, and removes 15 colliding names whose fragments already resolve to existing IDs. Zero named anchors remain and the full suite passes. Ten representative alias/current/collision fragments preserve exact URL scroll and date-cell positions at both desktop and mobile.
- Next: rebase, inspect and publish the two-News-page final T-51 checkpoint, verify live aliases, then close T-51 and start T-52 crawler discovery files.

## Working set
- EN/JP News exact event anchors and 48 ambiguous aliases, fragment-target/unique-ID standards checks, representative live/local scroll-position comparisons, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:46+0900
task: T-46 reserve intrinsic logo width
status: in-progress

## Now
- Goal: reserve each header logo's verified intrinsic aspect ratio before decode without changing its rendered size.
- Last done: T-46 added verified 450x65 EN and 436x65 JP intrinsic logo dimensions to all 26 pages and permanently enforces them. Full suite passes, natural images load correctly, desktop geometry is exact, and mobile EN/JP geometry differs from live by at most 0.0625px (within the established 1px tolerance).
- Next: rebase, inspect the logo-markup-only deployment preview, publish T-46, verify live dimensions, then close T-46 and start T-47.

## Working set
- All 26 header-logo elements, exact intrinsic-dimension standards checks, desktop/mobile geometry and load verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

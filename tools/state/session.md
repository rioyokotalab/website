driver: codex
updated: 2026-07-13T00:46+0900
task: T-47 add asynchronous decoding to noncritical images
status: in-progress

## Now
- Goal: let 155 already-lazy content images decode asynchronously without changing loading priority, dimensions, order, or presentation.
- Last done: T-47 paired all 155 lazy images (69 EN, 86 JP) with `decoding="async"` and permanently enforces the pairing. Full suite passes; browser decode/load checks pass for EN/JP news, profile portraits, research, gallery, and computer imagery with natural dimensions intact.
- Next: rebase, inspect the content-page-only deployment preview, publish T-47, verify representative live hints/images, then close T-47 and begin the more carefully staged T-48 inline-style/CSP migration.

## Working set
- 155 lazy images across mirrored pages, loading/decoding standards checks, representative load/geometry browser verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

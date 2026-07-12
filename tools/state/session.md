driver: codex
updated: 2026-07-13T00:46+0900
task: T-49 reserve dimensions for all content images
status: in-progress

## Now
- Goal: eliminate missing intrinsic dimensions from all content images using verified local image headers while preserving responsive rendering.
- Last done: T-49 resolved 104 incomplete occurrences (60 unique local assets) through verified file headers, stores exact natural dimensions, and preserves former 220px/638px/70%/95%/98% presentation through five shared classes. Permanent checks reject invalid dimensions and malformed class placement. Full suite passes; four representative image families match live loaded geometry within 1px at desktop/mobile, and an aborted-image test proves space is reserved before load.
- Next: rebase, inspect the CSS/cache/content deployment preview, publish T-49, verify representative live dimensions and strict CSP, then close T-49 and start T-50.

## Working set
- Dimensionless content-image occurrences across EN/JP computers/research/picture and other pages, local image headers, exact standards enforcement, representative geometry/gallery checks, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

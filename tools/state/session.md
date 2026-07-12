driver: codex
updated: 2026-07-13T00:46+0900
task: T-61 make repeated gallery link names distinguishable
status: in-progress

## Now
- Goal: make every repeated Lightbox link distinguishable to assistive technology without changing visible captions or image alternatives.
- Last done: T-61 gives all 143 Lightbox links page-local localized ordinal names and permanently enforces their exact order/count. Full suite passes; all six galleries have unique role names, first/middle/last links focus correctly, and uniquely named keyboard/pointer activation opens Lightbox without geometry changes.
- Next: rebase, inspect the six-page markup-only deployment preview, publish T-61, verify representative live unique names, then close T-61 and start T-62 mobile table containment audit.

## Working set
- Six EN/JP computers/picture/research pages, exact localized ordinal accessible names, keyboard/Lightbox/geometry verification, standards enforcement, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

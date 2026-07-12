driver: codex
updated: 2026-07-13T00:46+0900
task: T-59 defer remaining external scripts
status: in-progress

## Now
- Goal: prevent external scripts from blocking HTML parsing while preserving dependency order and runtime behavior.
- Last done: T-59 defers all 64 remaining external script references and permanently rejects non-deferred external scripts. Full suite and all four privacy-first consent tests pass; EN/JP menu/pagetop, jQuery-before-Lightbox behavior on Picture/Research, CSP, and page-error checks pass.
- Next: rebase, inspect the changed-HTML-only deployment preview, publish T-59, verify representative live defer attributes/runtime, then close T-59 and start T-60.

## Working set
- All 27 HTML documents' external scripts, exact defer standards enforcement, consent/menu/pagetop/Lightbox/CSP browser tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

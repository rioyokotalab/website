driver: codex
updated: 2026-07-13T00:46+0900
task: T-44 identify the current page in navigation
status: in-progress

## Now
- Goal: expose exact current-page state to assistive technology in both navigation variants without changing links, labels, or presentation.
- Last done: T-44 exact current-page markers and permanent page-specific count checks pass the full deterministic suite. Browser checks cover paired desktop/mobile destinations, mobile-only Contact, and deliberately unmarked News/profile pages while preserving 112px desktop header geometry.
- Next: rebase, inspect the navigation-markup-only deployment preview, publish T-44, verify representative live markers, then close T-44 and start T-45.

## Working set
- All 26 mirrored EN/JP navigation copies, page-specific current-state standards checks, representative assistive DOM/layout verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

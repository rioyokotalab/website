driver: codex
updated: 2026-07-13T00:46+0900
task: T-42 modernize root redirect metadata and fallback
status: in-progress

## Now
- Goal: modernize the root redirect document and provide a usable bilingual fallback when JavaScript is disabled, without changing locale routing or normal presentation.
- Last done: T-42 implementation and permanent standards coverage pass the full deterministic suite. Browser checks prove English routing, Japanese routing, non-English default-to-Japanese routing, and a visible bilingual fallback with JavaScript disabled.
- Next: rebase, inspect the root-only deployment dry-run, publish T-42, verify the live redirect/fallback document, then close T-42 and start T-43.

## Working set
- Root `index.html`, redirect/no-JavaScript browser tests, security regression coverage, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

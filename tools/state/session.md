driver: codex
updated: 2026-07-13T00:12+0900
task: T-31 make language switching resilient without JavaScript
status: in-progress

## Now
- Goal: modernize the language switcher without altering labels, placement, style, or bilingual paths.
- Last done: all 26 language controls now use direct mirrored links and work with JavaScript blocked; 26 loaders and unused `js/chglang.js` are removed. Path/parity/security/publish suites pass and browser tests pass 6/6. Secret scanning was made deletion-safe after this batch exposed the edge case.
- Next: inspect the deletion-bearing deploy preview, publish T-31, verify representative live EN/JP navigation and removed asset 404, then advance to T-32.

## Working set
- All 26 EN/JP HTML pages, `js/chglang.js`, ledger/bookkeeping; use a temporary CRLF-safe edit script under `tools/out/`.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

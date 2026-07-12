driver: codex
updated: 2026-07-13T02:18+0900
task: T-63 audit document and asset compression hints
status: in-progress

## Now
- Goal: verify live compression and caching behavior for representative HTML, CSS, JS, and image assets; change server policy only if compatibility and update semantics are safe.
- Last done: T-62 scoped mobile table containment to five affected pages, adds keyboard focus only while a table actually overflows, preserves exact 1200px geometry, and passes full plus 320/390px scroll checks.
- Next: commit/push T-62 after a deployment dry run, then fetch representative live response headers with compressed requests and record the server's actual behavior before deciding whether any safe repository change exists.

## Working set
- Representative live HTML/CSS/JS/image response headers; current .htaccess and known server compatibility constraints; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

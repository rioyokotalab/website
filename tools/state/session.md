driver: codex
updated: 2026-07-13T00:46+0900
task: T-60 remove obsolete and empty head metadata
status: in-progress

## Now
- Goal: remove empty/obsolete head markup while retaining all meaningful resource and structured-data semantics.
- Last done: T-60 removes exactly 26 empty keywords elements, 26 text/javascript attributes, and 27 text/css attributes while retaining JSON-LD types. Permanent checks reject regressions. Full suite passes; styles/scripts load without request failures, structured data parses, representative layout is intact, and pagetop behavior passes deterministically in reduced-motion mode (the initial smooth-scroll assertion sampled mid-animation).
- Next: rebase, inspect the 27-HTML head-only deployment preview, publish T-60, verify representative live heads/resources, then close T-60 and start T-61.

## Working set
- All 27 HTML heads, empty-keywords and redundant MIME-type standards checks, resource/JSON-LD/browser geometry verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

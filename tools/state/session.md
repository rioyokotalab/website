driver: codex
updated: 2026-07-13T04:28+0900
task: T-95 remove empty table-section artifacts
status: in-progress

## Now
- Goal: remove redundant empty table-section markup without altering any rows, grouping, or rendered geometry.
- Last done: T-94 marked 96 EN and 100 JP single-day archive dates with valid ISO/native time semantics, preserved four styled separators and four ranges, and passed exact static, five layout/browser, fast, and staging checks.
- Next: distinguish 20 empty `tbody` pairs from 13 nonempty table sections, remove only the empty pairs, enforce absence, and compare news tables across viewports/print.

## Working set
- EN/JP news table sections, row/group counts and order, screen/print geometry, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

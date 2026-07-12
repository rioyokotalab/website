driver: codex
updated: 2026-07-13T04:24+0900
task: T-94 add machine-readable archive dates
status: in-progress

## Now
- Goal: expose all exact full-archive event dates to machines while preserving visible strings, ordering, and table layout.
- Last done: T-93 marked 32 rendered EN and 14 rendered JP home-news dates with valid ISO/native time semantics, excluded 18 commented Japanese historical rows, and passed exact static, five browser/layout, fast, and staging checks.
- Next: distinguish single-day archive dates from ranges and non-date row headings, convert both zero-padded and legacy unpadded visible forms, validate each ISO calendar value, and compare archive geometry.

## Working set
- EN/JP news archives, exact/ranged dates, `time`/ISO validity, table geometry, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

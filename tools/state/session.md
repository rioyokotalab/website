driver: codex
updated: 2026-07-13T04:21+0900
task: T-93 add machine-readable home-news dates
status: in-progress

## Now
- Goal: expose exact home-news dates to machines while preserving visible date strings and table layout.
- Last done: T-92 added `type=application/pdf` to the only two local document-download links, retained labels/target security, enforced exact EN/JP parity, and passed static, browser, fast, and staging checks.
- Next: inventory exact versus ranged/ambiguous home-news dates, add ISO `datetime` only to exact dates, validate calendar values and EN/JP sequence parity, then compare table geometry.

## Working set
- EN/JP home news date cells, `time`/ISO dates, ordering/parity, table geometry, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:06+0900
task: idle
status: idle

## Now
- Goal: no task in flight.
- Last done: T-30 supply-chain verification passed offline/online, npm audit found zero vulnerabilities, all publish regressions passed, staging excludes every dependency/cache path, and the repository-only scope is ready to push.
- Next: no active ledger items; T-25 and T-28 remain externally blocked.

## Working set
- None.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

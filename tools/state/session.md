driver: codex
updated: 2026-07-13T00:01+0900
task: idle
status: idle

## Now
- Goal: no task in flight.
- Last done: T-26 report-only phase `a23a08e` and enforcement `3c9ef09` are live; representative status/header/browser tests and consent 4/4 passed. Temporary browser dependencies were removed.
- Next: continue with T-30 supply-chain audit.

## Working set
- None.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

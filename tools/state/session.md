driver: codex
updated: 2026-07-13T05:03+0900
task: idle
status: idle

## Now
- Goal: idle; the continuous modernization window is release-ready.
- Last done: T-107 corrected cross-origin iframe-internal Tab modeling in the exhaustive keyboard contract; all 26 routes at 390/1200px pass in 51.3 seconds. T-106 semantic containment and T-105 release sweep pass.
- Next: user or Claude site-publisher may live-publish and verify the pushed post–T-60 commits; Codex must not run the live publication.

## Working set
- Clean main branch, final driver report `tools/out/driver-report-20260713-0453.md`, live publication pending user/Claude.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

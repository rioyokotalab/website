driver: codex
updated: 2026-07-13T03:40+0900
task: T-84 audit sticky-header anchor positioning
status: in-progress

## Now
- Goal: prevent sticky navigation from obscuring headings reached through page-local section links while preserving ordinary layout.
- Last done: T-83 now loads all 26 routes at 320/1200px, cycles every mobile menu, opens/closes every gallery family, and fails on browser exceptions, error-console output, failed same-origin requests or local HTTP errors; all 52 route states passed cleanly.
- Next: enumerate all same-document hash links to heading targets, follow them at 320/900/901/1200px, compare target top/bottom against sticky navigation and viewport bounds, then replace the legacy `scroll-margin-top: -10px` only if clipping is reproduced and add a contract.

## Working set
- all same-document hash links and heading targets; `h3.heading[id]` scroll margin; responsive sticky-nav geometry; Playwright/style/cache/ledger bookkeeping as findings require.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:51+0900
task: T-35 complete image accessibility and loading hints
status: in-progress

## Now
- Goal: complete image alternatives and retain optimal eager/lazy loading without changing rendering.
- Last done: added empty alternatives to the redundantly captioned gallery pair and localized informative alternatives to both professor portraits. Zero images lack alt; exactly 26 logos and 26 heroes remain eager while all content images stay lazy. Security/publish suites pass; profile/gallery browser tests pass 2/2.
- Next: preview/publish the four-page T-35 scope, verify live accessibility/gallery behavior, then advance to T-36.

## Working set
- EN/JP picture and Yokota profile pages, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

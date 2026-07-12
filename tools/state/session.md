driver: codex
updated: 2026-07-13T04:46+0900
task: T-104 enforce rendered interactive names
status: in-progress

## Now
- Goal: verify every rendered interactive has a nonempty accessible name after dynamic controls initialize.
- Last done: T-103 permanently covers all routes at 390/1200px for one banner/main/contentinfo, localized desktop navigation, hidden collapsed mobile navigation, and localized mobile navigation after opening.
- Next: enumerate browser-exposed links/buttons/iframes with privacy-first settings initialized, inspect each accessibility snapshot for a nonempty name, include generated consent settings and maps, and retain the route-wide contract.

## Working set
- All routes' rendered links/buttons/iframes, generated settings controls, accessible names, permanent browser coverage.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

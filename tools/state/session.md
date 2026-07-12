driver: codex
updated: 2026-07-13T04:44+0900
task: T-103 enforce rendered landmark structure
status: in-progress

## Now
- Goal: verify browser parsing preserves one localized, navigable landmark structure on every route.
- Last done: T-102 audited all 26 accessibility trees and permanently enforces the exact route inventory, nonempty route-unique names for all 30 rendered data tables, and presentation-table exclusion.
- Next: enumerate banner/main/contentinfo/navigation landmarks in the rendered tree, assert exact localized primary/secondary navigation names and one of each structural landmark, then retain the route-wide contract.

## Working set
- All routes' rendered landmarks, localized navigation names, browser parsing, permanent accessibility coverage.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

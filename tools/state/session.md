driver: codex
updated: 2026-07-13T04:11+0900
task: T-89 audit keyboard focus order and reachability
status: in-progress

## Now
- Goal: ensure the rendered keyboard sequence contains every visible interactive once, excludes hidden controls, and cannot strand keyboard users.
- Last done: T-88 classified all 207 image elements, confirmed purposeful localized exposure for both logos and portraits plus localized names for linked galleries, removed one Japanese machine-generated placeholder from an English decorative event image, and passed fast plus route-wide browser checks.
- Next: measure focusable DOM elements against actual Tab traversal on representative desktop/mobile routes, then expand to all routes and fix only reproduced omissions, duplicates, or traps.

## Working set
- Public links/buttons/iframes, responsive hidden states, Tab and reverse-Tab sequences, accessible names, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

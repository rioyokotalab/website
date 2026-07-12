driver: codex
updated: 2026-07-13T00:46+0900
task: T-48 remove remaining inline presentation styles
status: in-progress

## Now
- Goal: migrate the remaining five inline style blocks and eleven style attributes to scoped shared classes with computed-style parity, then safely remove style `'unsafe-inline'` through a report-only gate.
- Last done: T-48 markup/CSS migration was published as `4fa5652` and live pages have no inline presentation. Runtime menu/pagetop inline mutations are now class-driven with cache-busted JS and permanent enforcement; normal/reduced-motion behavior passes. A strict no-unsafe-inline style policy is prepared as report-only alongside the existing enforced policy.
- Next: rebase, dry-run, publish the runtime-class/report-only checkpoint; verify both headers and collect browser `securitypolicyviolation` events across representative EN/JP, consent, gallery, map, menu, and scroll interactions before enforcing.

## Working set
- EN/JP home/research/news markup, shared CSS/cache bump, inline-style standards enforcement, computed-style/geometry browser comparisons, then `.htaccess` report-only/enforcement gates.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:46+0900
task: T-48 remove remaining inline presentation styles
status: in-progress

## Now
- Goal: migrate the remaining five inline style blocks and eleven style attributes to scoped shared classes with computed-style parity, then safely remove style `'unsafe-inline'` through a report-only gate.
- Last done: T-48 runtime-class/report-only checkpoint was published as `c8bccd3`. Live dual headers are exact, and the strict policy produced zero violations across EN/JP loads, consent accept/reject/settings, mobile menu, scroll/back-to-top, Lightbox, and map behavior. The strict policy is now prepared for enforcement with permanent source checks rejecting unsafe-inline/report-only fallback.
- Next: run the full suite, rebase, inspect the `.htaccess`-only dry-run, enforce the strict style CSP, then repeat live header and representative interaction checks before closing T-48.

## Working set
- EN/JP home/research/news markup, shared CSS/cache bump, inline-style standards enforcement, computed-style/geometry browser comparisons, then `.htaccess` report-only/enforcement gates.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

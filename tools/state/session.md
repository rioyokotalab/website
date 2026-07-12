driver: codex
updated: 2026-07-13T00:46+0900
task: T-48 remove remaining inline presentation styles
status: in-progress

## Now
- Goal: migrate the remaining five inline style blocks and eleven style attributes to scoped shared classes with computed-style parity, then safely remove style `'unsafe-inline'` through a report-only gate.
- Last done: T-48 migration removes all five style blocks and eleven style attributes, replaces every live rule with scoped shared CSS/classes, drops zero-consumer research-card/topgrid overrides, and permanently rejects inline presentation. Full suite passes; computed parity is exact for EN/JP home news tables, EN slogan, oral callouts, speaker images, and EN news superscript.
- Next: rebase, inspect and publish the markup/CSS/cache migration checkpoint under the existing CSP; verify live parity, then add the strict style policy as a simultaneous report-only header for browser validation before enforcement.

## Working set
- EN/JP home/research/news markup, shared CSS/cache bump, inline-style standards enforcement, computed-style/geometry browser comparisons, then `.htaccess` report-only/enforcement gates.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

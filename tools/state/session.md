driver: codex
updated: 2026-07-13T04:33+0900
task: T-97 retire empty gallery hooks and dead CSS
status: in-progress

## Now
- Goal: remove the final empty gallery hooks and only the CSS that cannot match afterward, without changing live frame/image styling.
- Last done: T-96 retained three deliberate spacing paragraphs and two CSS-referenced gallery hooks, removed only two zero-purpose JP profile articles, and passed exact static, five layout/runtime, fast, and staging checks.
- Next: prove `#gallery` has no JS/link/fragment consumers, split combined live/dead selectors, remove two hooks and exclusive rules, update cache/version and source-reference gates, then compare geometry.

## Working set
- EN/JP research `#gallery` hooks, five CSS selector families, source references, screen/print/runtime tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

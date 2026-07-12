driver: codex
updated: 2026-07-13T01:14+0900
task: T-36 reduce obsolete presentational markup safely
status: in-progress

## Now
- Goal: migrate only repeated high-confidence presentational markup to CSS while preserving computed layout and content.
- Last done: T-37 pushed as `822d7bd`. T-36 inventory selected the only uniform high-confidence pattern: all 145 exact `<p align="center">` instances. They now use `class="text-center"`, CSS/cache version is updated, standards/security pass, and four representative pages preserve centered computed style and wrapper geometry within 1px (browser 4/4).
- Next: remove temporary browser test, run full regressions, preview/publish T-36, verify representative live pages, then seed the next modernization tasks from remaining evidence rather than rewriting heterogeneous table attributes.

## Working set
- Selected EN/JP HTML pattern, shared CSS/cache bump only if needed, browser geometry/computed-style tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

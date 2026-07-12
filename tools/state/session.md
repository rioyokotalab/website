driver: codex
updated: 2026-07-13T01:09+0900
task: T-36 reduce obsolete presentational markup safely
status: in-progress

## Now
- Goal: migrate only repeated high-confidence presentational markup to CSS while preserving computed layout and content.
- Last done: T-37 standards checker passes and is integrated into every pre-publish security run; live T-38 ID uniqueness and event fragment were browser-verified. README documents enforced invariants.
- Next: commit/push the repository-only T-37 tooling, inventory obsolete attributes by tag/pattern, choose the smallest repeated pattern with exact computed-style equivalence, and handle it as an isolated browser-compared batch.

## Working set
- Selected EN/JP HTML pattern, shared CSS/cache bump only if needed, browser geometry/computed-style tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

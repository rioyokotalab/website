driver: codex
updated: 2026-07-13T05:51+0900
task: T-77 add automated rendered-layout smoke coverage
status: in-progress

## Now
- Goal: permanently catch page-level overflow, missing major regions, or gross responsive geometry regressions across representative EN/JP page families without brittle screenshot baselines.
- Last done: T-76 added conventional npm test and test:browser/install commands, retained consent aliases, enforced the exact reviewed script surface, added 900/901px EN/JP menu and six-family print contracts, and passed all 8 browser plus fast security tests.
- Next: select representative home/news/research/computers/contact/picture/profile paths, measure invariant region presence/order/viewport containment at 320/390/900/901/1200px, encode tolerant semantic geometry assertions, and rerun the full suite.

## Working set
- tests/layout-contracts.spec.js, representative EN/JP region/document geometry across five boundaries, tolerant invariants only, full browser/security verification; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

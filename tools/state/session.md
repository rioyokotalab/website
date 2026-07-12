driver: codex
updated: 2026-07-13T04:48+0900
task: T-105 full modernization release-readiness sweep
status: in-progress

## Now
- Goal: verify the accumulated modernization series as one clean, deployable, regression-free release candidate.
- Last done: T-104 audited every exposed link/button and embedded frame on all 26 routes after dynamic privacy controls initialize, and permanently rejects empty names/titles.
- Next: run all fast and browser contracts, dry-run the positive-allowlist deploy, inspect status/diff/cache/generated artifacts, clean test debris, then checkpoint final release readiness and pending live-publication boundary.

## Working set
- Full static/browser suites, staging allowlist, repository/test artifacts, final status/report/publish boundary.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

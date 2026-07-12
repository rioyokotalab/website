driver: codex
updated: 2026-07-13T03:37+0900
task: T-83 audit browser runtime health on every route
status: in-progress

## Now
- Goal: make uncaught client-side errors and failed local runtime resources impossible to introduce unnoticed on any public route.
- Last done: T-82 found the current-page forced-color outline out-specificed the keyboard ring and Lightbox's programmatically focused close control did not match `:focus-visible`; two scoped Highlight outlines now preserve both states and two permanent EN/JP component tests pass within the 16-test suite.
- Next: attach pageerror/console/requestfailed listeners before loading all 26 routes at 320/1200px, reject analytics to isolate local behavior, exercise mobile menus and representative galleries, classify external cancellations separately, fix only local failures, and retain the contract.

## Working set
- all 26 public routes at mobile/desktop; local scripts/styles/images and component interactions; new Playwright runtime-health contract; ledger/test bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

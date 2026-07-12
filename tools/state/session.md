driver: codex
updated: 2026-07-13T00:18+0900
task: T-32 remove unused eval-based menu script
status: in-progress

## Now
- Goal: eliminate obsolete packed/eval JavaScript and tighten CSP without changing current navigation behavior.
- Last done: removed 26 dead loaders and `js/ddmenu_min.js`; zero eval/new-Function/ddmenu references remain. Added a simultaneous no-unsafe-eval report-only policy while keeping current enforcement. Security/publish suites and consent browser tests pass 4/4.
- Next: preview and publish the report-only phase; inspect live CSP console/navigation/gallery/map/consent behavior, then remove `'unsafe-eval'` from enforcement and the temporary report-only header.

## Working set
- All 26 EN/JP HTML pages, `js/ddmenu_min.js`, `.htaccess`, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

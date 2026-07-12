driver: codex
updated: 2026-07-13T00:29+0900
task: T-33 externalize repeated executable inline scripts
status: in-progress

## Now
- Goal: eliminate executable inline JavaScript and test removal of CSP `'unsafe-inline'` without changing page behavior.
- Last done: externalized all 26 responsive bootstraps and the root language redirect; only two JSON-LD blocks remain inline. Security suite passes and browser tests pass 7/7 for consent, EN/JP redirects, and mobile menu behavior. Added a simultaneous report-only `script-src` without unsafe-inline while current enforcement remains.
- Next: preview/publish the externalization/report-only phase, inspect live CSP reports (especially JSON-LD), then either hash JSON-LD or enforce no-unsafe-inline if clean.

## Working set
- All 26 EN/JP HTML pages, root `index.html`, new shared JS, `.htaccess`, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

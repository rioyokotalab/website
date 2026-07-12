driver: codex
updated: 2026-07-13T00:34+0900
task: T-33 externalize repeated executable inline scripts
status: in-progress

## Now
- Goal: eliminate executable inline JavaScript and test removal of CSP `'unsafe-inline'` without changing page behavior.
- Last done: externalization/report-only phase published as `557d795`; root redirect, EN/JP home JSON-LD, analytics acceptance, gallery, and map paths produced zero report-only violations or page errors. Enforcement is prepared without script `'unsafe-inline'`; style unsafe-inline remains for later markup/CSS work.
- Next: publish the `.htaccess`-only enforcement change, repeat live browser/header checks, then close T-33 and advance to T-34.

## Working set
- All 26 EN/JP HTML pages, root `index.html`, new shared JS, `.htaccess`, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

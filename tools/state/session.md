driver: codex
updated: 2026-07-13T00:22+0900
task: T-32 remove unused eval-based menu script
status: in-progress

## Now
- Goal: eliminate obsolete packed/eval JavaScript and tighten CSP without changing current navigation behavior.
- Last done: report-only phase published as `d305d03`; dead script is live 404 and representative home/gallery/research/map/consent paths produced no CSP reports or page errors. Enforcement is now prepared without `'unsafe-eval'` and the temporary report-only header is removed.
- Next: verify and publish the `.htaccess`-only enforcement change, repeat live browser/header checks, then close T-32 and advance to T-33.

## Working set
- All 26 EN/JP HTML pages, `js/ddmenu_min.js`, `.htaccess`, browser/security tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

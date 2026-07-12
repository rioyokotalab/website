driver: codex
updated: 2026-07-13T00:59+0900
task: T-26 harden HTTP response headers and CSP
status: in-progress

## Now
- Goal: deploy a compatible CSP, Permissions Policy, and cautious HSTS policy without breaking the static site or consent flow.
- Last done: inventoried 27 documents: no forms/network APIs; two Google Maps frames; six cdnjs gallery pages; consent-gated GTM; 26 inline handlers, five style blocks, 13 style attributes, and one legacy menu `eval`. Drafted report-only origin restrictions plus Permissions Policy and one-day HSTS without subdomains/preload.
- Next: extend deterministic header checks, validate offline, deploy report-only cautiously, and inspect live headers/browser violations before enforcement.

## Working set
- `.htaccess`, public HTML/JS/CSS inventory, security test harness, README/playbook, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

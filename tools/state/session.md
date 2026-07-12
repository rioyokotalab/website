driver: codex
updated: 2026-07-13T01:04+0900
task: T-26 harden HTTP response headers and CSP
status: in-progress

## Now
- Goal: deploy a compatible CSP, Permissions Policy, and cautious HSTS policy without breaking the static site or consent flow.
- Last done: report-only policy deployed in `a23a08e`; six representative live pages/PDF return 200 with exact headers, representative EN/JP home/gallery/research/map/consent-accept browser paths produced no actionable policy errors, and consent tests passed 4/4.
- Next: enforce the unchanged CSP, verify all headers/browser paths live, document the durable policy, then close T-26.

## Working set
- `.htaccess`, public HTML/JS/CSS inventory, security test harness, README/playbook, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T00:46+0900
task: T-52 add crawler discovery files
status: in-progress

## Now
- Goal: expose only the canonical public page inventory through minimal crawler discovery files and keep it synchronized automatically.
- Last done: T-52 generates 27 unique canonical URLs (root + 26 pages), each with EN/JA/x-default alternates, plus minimal robots.txt. Both are required by the positive deploy allowlist/staging fixture and public security inventory; the pre-publish suite rejects stale output. XML/MIME checks and all 27 local URLs pass with no repository-only paths.
- Next: rebase, inspect the expected two-file upload with no deletions, publish T-52, verify live MIME/content and all sitemap URLs, then close T-52 and start T-53.

## Working set
- `robots.txt`, `sitemap.xml`, deterministic generator, deploy allowlist/staging requirements, public security inventory, exact URL/alternate validation, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

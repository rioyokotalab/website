driver: codex
updated: 2026-07-13T03:14+0900
task: T-67 normalize page titles and descriptions
status: in-progress

## Now
- Goal: make page titles and descriptions clear, unique, and restrained across mirrored EN/JP routes without rewriting sound content or changing visible pages.
- Last done: T-66 added a deploy-manifest-aware gate for 1,676 local public URLs/fragments and CSS assets, integrated it into the full suite, and proved directory/same-origin/fragment success plus missing file/fragment/CSS failures with fixtures.
- Next: parse all titles and description metadata, report missing/duplicate/overlong/route-mismatched pairs and EN/JP asymmetries, then change only confirmed ambiguous metadata and add structural enforcement.

## Working set
- All 26 bilingual heads plus root redirect metadata; title/description lengths and uniqueness; any CRLF-safe page-local corrections and standards enforcement; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

driver: codex
updated: 2026-07-13T04:20+0900
task: T-92 identify linked document media types
status: in-progress

## Now
- Goal: identify locally linked documents by media type without altering link labels, targets, or pixels.
- Last done: T-91 wrapped unchanged contact details in native EN/JP address elements, kept maps outside, neutralized browser-default italics, and passed exact static, five browser/layout, fast, and staging checks.
- Next: inventory local non-HTML link formats and existing user-facing format labels; add exact media-type hints only where unambiguous and mirrored.

## Working set
- Local document links, MIME types, labels/targets, EN/JP parity, standards/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

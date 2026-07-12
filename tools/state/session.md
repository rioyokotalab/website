driver: codex
updated: 2026-07-13T04:18+0900
task: T-91 expose contact details with native semantics
status: in-progress

## Now
- Goal: identify the existing EN/JP contact details as address information without changing content or visual layout.
- Last done: T-90 added `hreflang=ja/en` to all 26 exact mirrored language switches, enforced href/text/language triples, and passed route-wide link/name, fast, and staging checks.
- Next: isolate postal/phone/email content from the map, add native address semantics in both languages, neutralize browser-default italics, and compare geometry/landmarks.

## Working set
- EN/JP contact blocks, native address semantics, shared CSS, standards/layout/browser tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

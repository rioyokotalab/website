driver: codex
updated: 2026-07-13T00:46+0900
task: T-58 audit heading hierarchy and accessible names
status: in-progress

## Now
- Goal: eliminate empty/skipped headings and unnamed interactive elements without changing visible wording or layout.
- Last done: T-58 fixes the EN home heading sequence with a visually identical h2, replaces one empty JP h4 with an aria-hidden separator of exact geometry, labels all 143 Lightbox links locally, and removes/unwraps three empty links. Permanent checks reject empty/skipped headings and unnamed static links/buttons. Full suite, desktop/mobile geometry parity, keyboard focus, and Lightbox behavior pass.
- Next: rebase, inspect the HTML/CSS/cache deployment preview, publish T-58, verify live accessible names/headings, then close T-58 and seed the next modernization queue.

## Working set
- EN home, JP research, EN/JP computers/picture/research Lightbox links, three empty links, shared CSS/cache, heading/name standards enforcement, representative geometry and keyboard/Lightbox checks.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

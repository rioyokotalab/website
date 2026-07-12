driver: codex
updated: 2026-07-13T03:00+0900
task: T-66 make local-link integrity a permanent gate
status: in-progress

## Now
- Goal: make resolution of every public local URL and same-page/cross-page fragment a deterministic commit gate without network dependence.
- Last done: T-65 scanned all 52 page/mode combinations, changed only the dark-mode oral-highlight red (3.12:1 to 6.61:1), removed one stray near-invisible EN hero character, and ended with zero computed text-contrast failures.
- Next: inventory all public href/src/srcset/action/poster/data URLs, normalize directory-index and query/fragment resolution, classify intentional nonpublic/external schemes, and compare the result with the staged public manifest before writing the gate.

## Working set
- All public HTML and staged public files; deterministic URL/fragment parser; integration into tools/test-security.sh and supply-chain/deploy exclusions; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

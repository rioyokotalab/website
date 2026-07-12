driver: codex
updated: 2026-07-13T00:46+0900
task: T-43 add canonical and alternate-language metadata
status: in-progress

## Now
- Goal: give all mirrored pages exact self-canonical and reciprocal EN/JP/x-default discovery metadata without changing visible content or layout.
- Last done: T-43 exact canonical/EN/JA/x-default mappings pass permanent standards checks on all 26 pages; the full deterministic suite and representative EN/JP root/profile browser DOM and unchanged header geometry checks pass.
- Next: rebase, inspect the metadata-only deployment preview, publish T-43, verify live discovery links, then close T-43 and seed the next modernization tasks.

## Working set
- All 26 mirrored EN/JP pages, exact metadata standards checks, representative layout/browser verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

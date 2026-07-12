driver: codex
updated: 2026-07-13T06:07+0900
task: idle
status: idle

## Now
- Goal: idle; the approved modernization tree is live and verified.
- Last done: T-108 published approved public commit `bd662c7` under the already-tracked direct Codex DRIVER exception; 29 modified plus 16 new files deployed, all 45 live bytes match, representative routes/assets return 200, and enforced headers remain present.
- Next: no publication action remains; T-28 and T-25 retain their existing blocked/external states.

## Working set
- Production matches approved `bd662c7`; deploy-excluded publication bookkeeping only; report `tools/out/driver-report-20260713-0607.md`.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.

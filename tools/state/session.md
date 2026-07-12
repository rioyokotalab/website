driver: codex
updated: 2026-07-13T00:43+0900
task: T-25 purge archived PDF blobs from Git history
status: blocked

## Now
- Goal: remove all historical `tools/papers/` blobs from every reachable repository ref and, when GitHub permits, physical server storage.
- Last done: rewrote main and eight local tags, lease-force-updated GitHub main from `78fe51a` to `f967f47`, removed local backup refs/reflogs/bundle, garbage-collected, and verified fresh clones expose zero paper paths. Remote tags never existed and were not introduced.
- Next: security backlog T-26 through T-30 is authorized only as task-board scope; await owner direction before implementation. T-25 remains pending automatic GitHub server GC.

## Working set
- Rewritten main before final ledger commit: `f967f475887f27ae41a507dee1e24831abe5414d`; fresh mirror: zero `tools/papers/` paths, about 72 MiB.
- Local: zero paper paths across all refs, zero `refs/original`, zero unreachable objects after GC, rollback bundle deleted.

## Open questions
- Physical GitHub deletion timing is outside repository control; old SHA remains fetchable even though no advertised ref or fresh clone reaches it.
- Security ordering recommendation: T-27 public-secret exposure first, then T-28 deploy exposure, T-29 regression harness, T-26 CSP/header enforcement, and T-30 supply chain.

## Awaiting user
- None.

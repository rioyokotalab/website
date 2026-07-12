# Model evaluation results

Judge-only cumulative ledger. This file lives on `main` only and is never
mirrored into contestant branches or their shared scaffold.

## Round 1 (4-way), judged 2026-07-12

Judge: gpt-5.6-sol (`sol` was a contestant; bias disclosed). Decisive claims
were independently spot-checked against branch blobs and read-only Git evidence.

| Branch | Score | Tasks done | Key failures | Times (base span / metrics / session) |
| --- | ---: | --- | --- | --- |
| terra | 96 | T-6–T-9 | Minor bundled enum fix | 01:13:36 / 00:20:00 / 11:11 |
| sol | 87 | T-6–T-8 | T-9 unattempted; minor process extras | 00:39:12 / 00:42:01.108 / 10:22 |
| fable | 65 | T-6–T-9 nominally | DOI gate/convention errors; policy scope creep | 03:25:40 / 00:41:47.484 / 13:11 |
| opus | 57 | T-7–T-9; T-6 failed | False T-6 clean claim; policy corruption | 04:25:28 / 00:05:56.707 / 14:27 |

Winner: **terra**, merged into `main` as `4a15349`.

Round-1 branch tips are preserved as `eval/r1-sol`, `eval/r1-terra`,
`eval/r1-fable`, and `eval/r1-opus`.

Timing caveat: commit spans included idle/review/bookkeeping time and contestant
runs started sequentially. Metric sums were self-reported and sometimes
estimated or overlapping; session values are endpoint timestamps, not durations.

```text
2026-07-12 | Round 2 | judge gpt-5.6-sol (also sol contestant; evidence-cited review)
Board: T-10..T-13 + proposal-quality bonus; 110-point total
Scores: sol 110, opus 104, fable 102, terra 96
Ranking: sol > opus > fable > terra; winner sol b8a2b6d
Owner times: sol 40m30s; terra 40m48s raw / ~30m48s if stall included; fable 33m03s; opus 32m11s
Terra's ~10m approval stall credited; inclusion in raw time remains ambiguous; no wait-log penalty
External-file alert resolved as owner/runtime effects; no contestant penalty
All four: judge=0, hand-edit-only=0, deploy=0; GA core coverage identical
Nobody committed gitignored tools/out deliverables; shared protocol gap, no differential penalty
Decisive: Sol's exact validated T-11 overlay plus best GA/T-13 quality beat Opus's broader apply script
T11 owner base: sol, optionally borrowing Opus's structural Codex rollback/update pattern
```


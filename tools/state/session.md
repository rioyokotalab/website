driver: codex
updated: 2026-07-13T23:13+0900
task: T-147 Run all documented model/effort/task cells
status: in-progress

## Now
- User authorized an eight-hour adaptive campaign ending
  2026-07-14T05:08+0900. Execute T-147--T-153 continuously, dynamically
  checkpointing task blocks, selection decisions, and routing evidence.
- Frozen round: baseline `c4b0720`, run label `gpt56-full-20260713`, full
  prompt/default inspection/runner-lite/P2P, deterministic task-blocked order.
- Resumable single-writer orchestrator committed as `579d66f`; dry runs prove
  75 documented and 12 remaining ultra cells with automatic switching.
- WBD-003 documented block complete: 15/15 capability passes; 14 scored 100,
  Sol/xhigh scored 89 from failed `denied-default`. Provisional Pareto routes:
  Terra/low fastest at 25,045 ms total; Sol/low lowest effective tokens at
  8,298. Do not select until ultra and matched repeats are available.
- WBD-001 is complete across all 18 arms: 18/18 scored 100. Initial Pareto
  frontier is Terra/medium fastest at 39,270 ms total and 10,671 effective
  tokens versus Luna/low lowest-token at 43,941 ms and 8,117 tokens. All other
  arms are dominated on score/runtime/tokens; both leaders require repeats.
- WBD-005 documented block complete: 10/15 capability passes. Provisional
  passing Pareto frontier is Luna/low fastest at 110,069 ms and 29,551
  effective tokens, Terra/low balanced at 123,509 ms and 24,022 tokens, and
  Sol/low lowest-token at 140,525 ms and 18,826 tokens. Terra medium/high/max
  and Luna/medium failed `js-reduced-zero`; Terra/xhigh passed all static
  assertions but failed the lightbox focus-return P2P assertion. These are
  genuine capability results, not infrastructure failures, and remain recorded.
- WBD-002 documented block complete: 15/15 capability passes at score 100.
  Luna/low leads latency at 76,818 ms total and 12,141 effective tokens;
  Sol/low is the only other Pareto arm at 93,096 ms and 11,174 tokens. Every
  higher-effort arm is dominated. Repeat both low-effort contenders.
- Integrity checkpoint: 63 runs, artifact directories, and metric pointers,
  no errors; metrics contain 63 v2 rows. T-147 is 60/75. Next frozen block:
  WBD-004 documented.

## Working set
- `tools/agent-benchmark/gpt56-full-20260713.freeze.json`
- `tools/agent-benchmark/results.jsonl`
- `tools/out/agent-benchmark/` (three complete ignored probe artifacts)
- `tools/agent-benchmark/` matrix orchestrator and routing evidence
- Deadline: 2026-07-14T05:08+0900; T-147 in progress.

## Open questions
- None.

## Awaiting user
- None.

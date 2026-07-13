driver: codex
updated: 2026-07-13T21:08+0900
task: T-147 Run all documented model/effort/task cells
status: in-progress

## Now
- User authorized an eight-hour adaptive campaign ending
  2026-07-14T05:08+0900. Execute T-147--T-153 continuously, dynamically
  checkpointing task blocks, selection decisions, and routing evidence.
- Frozen round: baseline `c4b0720`, run label `gpt56-full-20260713`, full
  prompt/default inspection/runner-lite/P2P, deterministic task-blocked order.
- Runner and v2 metrics now support low/medium/high/xhigh/max/ultra. Luna,
  Terra, and Sol each passed the WBD-001 ultra cell at 100/100 with full P2P and
  exact scope. Three artifacts and three v2 metric rows validate.
- Next: add a resumable single-writer matrix orchestrator without changing the
  frozen benchmark runner, verify its dry-run order/counts, then execute the
  documented cells in frozen task blocks and import metrics after every run.

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

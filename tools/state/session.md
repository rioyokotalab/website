driver: codex
updated: 2026-07-14T01:37+0900
task: T-151 Allocate adaptive matched repeats
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
- WBD-004 documented block complete: 15/15 capability passes at score 100.
  Luna/low is jointly best for latency and tokens at 46,892 ms total and 9,669
  effective tokens; every other documented arm is dominated.
- T-147 complete: all 75 documented cells are present (70 capability passes,
  five genuine WBD-005 failures). Including the three completed WBD-001 ultra
  probes, 78 runs, artifact directories, and metric pointers reconcile with
  78 v2 metrics. The documented dry-run reports zero pending cells.
- T-148 in progress: run the 12 remaining ultra cells in task blocks, then
  audit the exact 90-cell matrix. WBD-003 ultra is complete: all three models
  passed score 100, but Terra/ultra at 68,045 ms and Sol/ultra at 12,251 tokens
  are still dominated by the documented low-effort leaders. Ultra progress is
  3/12 new rows; 81 runs/artifacts/metric pointers reconcile with 81 v2 rows.
  Next frozen block: WBD-005 ultra.
- Infrastructure checkpoint: the first Sol/ultra WBD-005 attempt stopped before
  grading/result creation with `ENOSPC` while opening the artifact worker log.
  `/home` is globally full (space and inodes), while `/tmp` has 342 GB free.
  The pushed `7a54508` repository, all 81 valid artifacts, and reproducible
  dependencies were transferred to `/tmp/yokota-campaign-local`; the lone
  result-less partial artifact was inspected and removed. Local artifact and
  metrics audits pass 81/81. Retry the identical cell once from the local clone;
  continue committing and pushing canonical tools-only state from there.
- WBD-005 ultra complete: Terra, Luna, and Sol all passed score 100 with full
  P2P and exact scope, but all are dominated by the documented low-effort
  frontier. The first local Sol grade failed all P2P tests in 3,723 ms because
  the ignored Chromium cache had not transferred; that uncommitted result,
  metric, and artifact were transactionally removed, Chromium was restored,
  and the identical stable id reran successfully with a 64,557 ms grade.
  Ultra progress is 6/12 new rows; 84 runs/artifacts/metric pointers reconcile
  with 84 v2 rows. Next frozen block: WBD-002 ultra.
- WBD-002 ultra complete: all three models passed score 100, but all are
  dominated. Luna/ultra was best among them at 132,830 ms and 27,819 effective
  tokens versus Luna/low at 76,818 ms and 12,141 tokens. Ultra progress is
  9/12 new rows; 87 runs/artifacts/metric pointers reconcile with 87 v2 rows.
  Next frozen block: WBD-004 ultra.
- WBD-004 ultra complete: all three models passed score 100 and are dominated
  by Luna/low. T-148 is complete with all 15 ultra cells passing.
- Exact matrix audit passes: 90 unique cells = 75 documented + 15 ultra, 30 per
  model, 15 per effort, and 18 per task; 85 capability passes and five genuine
  WBD-005 failures. There are no duplicate cells. All rows share baseline
  `c4b0720`, frozen modes, worker, and task versions. Ninety artifacts and 90
  v2 metric pointers reconcile; both matrix dry runs have zero pending cells,
  and all five task mutation/pristine audits pass. T-149 is now in progress.
- T-149 complete: deterministic JSON/Markdown summaries validate both frozen
  runner identity groups (87 matrix + three WBD-001 probe cells), aggregate
  by task-normalized model/effort metrics, and report 11 full-quality Pareto
  arms with break-even slopes. The summaries reproduce byte-for-byte. Low is
  the only 15/15 full-quality effort and is best in aggregate; ultra is never
  Pareto. Monetary cost is unknown because no price table was frozen.
- T-151 stage 1 allocation: run two additional interleaved observations for
  every low-effort task/model route plus WBD-001 Terra/medium (16 routes × two
  repeats = 32 runs). This brings all low controls and the only non-low matrix
  frontier arm to `n=3` before elimination. Next, repeat the five WBD-005
  failures and WBD-003 Sol/xhigh twice each if the stage-1 audit remains clean.
- The resumable repeat orchestrator and plan dry-run at exactly 32 stage-1 and
  12 original stage-2 cells with unique stable ids. Repeat-runner SHA-256 is
  `0c33d1161a87fd980f23f68479e8556a39d360b5ee84409f53a4a617560a7691`;
  the original plan SHA-256 was
  `9414ff807edb91648b0d538b1a6f4fbce043e6633140b273067212064644bf61`.
- T-151 stage 1 complete: 32/32 planned repeats, 28 capability passes, and
  four genuine WBD-005 quality failures. The 122 result rows, artifacts, and
  metric pointers reconcile; all metric and artifact audits pass. The repeat
  summary reproduces byte-for-byte and gates on reliability before medians.
- Stage-1 medians select WBD-001 Terra/low at 41,703 ms and 7,493 effective
  tokens. WBD-002 retains Luna/low for speed (84,682 ms) versus Sol/low for
  tokens (12,368). WBD-003 is a near-tie: Terra/low 34,685 ms versus Sol/low
  10,664 tokens. WBD-004 retains a three-route runtime/token frontier. WBD-005
  Sol/low passed 3/3 at 140,525 ms and 18,936 tokens; Luna/low and Terra/low
  each passed only 1/3 and are excluded from default routing.
- Adaptive allocation revision 2 supersedes the unrun anomaly stage. Next run
  three additional WBD-005 Sol/low observations (`n=6`), two WBD-005
  Sol/medium observations (`n=3`) as a fallback screen, and two more WBD-003
  Terra/low and Sol/low observations each (`n=5`). Recompute before any further
  allocation. Revision-2 plan SHA-256 is
  `c563b025a508d26f3a6ff2eb1d300d25b410e3240aa755e7b901a7bf98de3b6a`.
  Reserve final campaign time for the durable routing policy and closeout
  before 2026-07-14T05:08+0900.

## Working set
- `tools/agent-benchmark/gpt56-full-20260713.freeze.json`
- `tools/agent-benchmark/results.jsonl`
- `tools/out/agent-benchmark/` (three complete ignored probe artifacts)
- `tools/agent-benchmark/` matrix orchestrator and routing evidence
- Deadline: 2026-07-14T05:08+0900; T-151 in progress.

## Open questions
- None.

## Awaiting user
- None.

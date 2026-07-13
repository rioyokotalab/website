driver: codex
updated: 2026-07-14T03:48+0900
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
- Adaptive stage 2 complete: all nine planned rows, artifacts, and v2 metrics
  reconcile. WBD-005 Sol/low failed repeats 4 and 5 on `css-zero-motion`, then
  passed repeat 6, for 4/6 full-quality capability. Sol/medium passed both
  repeats and is 3/3 overall; its reliability-first median is 153,655 ms and
  42,681 effective tokens versus Sol/low's passing-only medians of 147,208.5 ms
  and 20,229 tokens. Prefer medium provisionally; low requires validation and
  escalation. The Wilson intervals still overlap, so add confidence evidence.
- WBD-003 tie-break complete: both Terra/low and Sol/low passed 5/5. Sol/low
  now dominates with medians of 33,493 ms and 10,664 effective tokens versus
  Terra/low at 34,685 ms and 11,875 tokens. Select Sol/low unless later evidence
  changes the result.
- Cumulative audit at 01:52 passes with 131 result/artifact/metric pointers and
  131 v2 benchmark metrics. The repeat set has 41 runs, 35 capability passes,
  3,500,446 ms summed end-to-end time, and 878,601 effective tokens. Repeat
  summary regeneration remains byte-identical.
- Adaptive plan revision 3 allocates 17 next observations: WBD-005 Sol/medium
  repeats 4--6, WBD-005 Sol/high repeats 2--3, WBD-004 Luna/Terra/Sol low
  repeats 4--5, WBD-002 Luna/Sol low repeats 4--5, and WBD-001 Terra/low
  repeats 4--5. Run as separate resumable substages and recompute between
  them; WBD-003 is resolved and receives no further allocation. Revision-3
  plan SHA-256 is
  `dc5fe7a451405e9c5d05894762676f6a3285814f03bfaa41d5bf22968f6846b0`.
- WBD-005 Sol/medium confidence stage complete at 5/6 full-quality. Repeats 4
  and 5 passed; repeat 6 scored 87 after the dialog remained visible on Escape
  in the lightbox accessibility P2P suite. This is a substantive capability
  failure, not infrastructure. Medium is stronger than low's 4/6 but does not
  reach the intended high-confidence gate.
- WBD-005 Sol/high screen passed both repeats and is 3/3 overall. Apply the
  predeclared adaptive rule: revision 4 adds high repeats 4--5, then stop this
  arm and recompute. Revision-4 plan SHA-256 is
  `497f0bb4a742285880e66a4c66db563cd5d9d5996876ca62c6908550b724efe5`.
  Continue with WBD-001/002/004 stages afterward.
- Adaptive Stage 3 complete. WBD-005 Sol/high passed confirmations 4--5 and is
  5/5, making it the only qualified reliability fallback under the planned
  `n>=5`/Wilson-lower-bound gate. Sol/medium is 5/6 and Sol/low 4/6. Stop all
  three arms pending retry-adjusted analysis.
- WBD-001 Terra/low passed 5/5. Updated medians are 52,465 ms and 12,146
  effective tokens. It remains the runtime leader, but Luna/low's `n=3` token
  median of 11,469 reopens a small tradeoff; consider Luna repeats 4--5 after
  the current analysis checkpoint.
- WBD-002 Luna/low and Sol/low both passed 5/5. Luna is the runtime route at
  79,082 ms median; Sol is the token alternate at 12,368 effective tokens,
  saving 829 tokens for 14,014 ms additional median time.
- WBD-004 Luna/Terra/Sol low all passed 5/5. Luna is the runtime route at
  50,092 ms median and 18,696 tokens; Sol is the token route at 68,144 ms and
  12,832 tokens. Terra at 61,400 ms and 23,336 tokens is dominated by Luna.
- Cumulative audit at 02:35 passes: 150 unique result/artifact/metric pointers,
  150 v2 benchmark metrics, 60 matched repeat rows, and 53 repeat full-quality
  passes. Correct the repeat analyzer before further route selection: gate on
  completed planned sampling, use full-quality Wilson bounds consistently,
  add smoothed success probability and all-attempt expected time/tokens per
  success, and do not permanently exclude a route after one failure.
- Repeat analyzer corrected and deterministic regeneration passes. Confidence
  now waits for planned sampling and uses full-quality Wilson bounds:
  high-confidence is `n>=6`/lower `>=0.60`, qualified is `n>=5`/lower `>=0.55`,
  provisional is `n>=3`/lower `>=0.40`. Route estimates use Beta(1,1)-smoothed
  success probability and all-attempt mean time/tokens per expected success;
  observed medians and ranges remain available. This keeps failed-attempt cost
  and uncertainty visible. Intervals are descriptive, not selection-adjusted.
- Corrected expected-cost frontiers: WBD-001 Terra/low dominates its sampled
  alternatives; WBD-002 Luna/low is runtime versus Sol/low tokens; WBD-003
  Terra/low is runtime versus Sol/low tokens; WBD-004 Luna/low is runtime versus
  Sol/low tokens; WBD-005 Sol/high is the sole qualified route. Do not add
  WBD-001 Luna repeats from the median-only signal.
- Adaptive plan revision 5 adds a single sixth observation for those eight
  selected primary/alternate routes. A 6/6 result crosses the predeclared
  high-confidence threshold; any failure demotes the route and is therefore
  high-information. Revision-5 plan SHA-256 is
  `2ea10d37cd7dde0a3e59d3d30969591e58179d9f3e2cd7c7e328745bed2bd635`.
  Recompute before allocating Stage 5.
- Stage 4 complete: seven selected WBD-001--004 routes passed and are 6/6
  high-confidence. Runtime primaries are Terra/low WBD-001, Luna/low WBD-002,
  Terra/low WBD-003, and Luna/low WBD-004; Sol/low is the high-confidence token
  alternate for WBD-002--004. WBD-005 Sol/high repeat 6 failed
  `js-reduced-zero`, leaving high and medium each 5/6 provisional and low 4/6
  insufficient. No WBD-005 route qualifies standalone.
- Analyzer review fixes complete: Wilson thresholds use unrounded values;
  attained confidence survives later adaptive extensions; integrity now
  distinguishes analysis completeness from row validity. Deterministic
  regeneration passes with 68 repeat rows and 60 full-quality passes.
- Adaptive plan revision 6 screens WBD-005 Luna/high and Luna/xhigh at repeats
  2--3. These were the fastest and lower-token Luna higher-effort singleton
  passes in the matrix. Expand only an arm that remains clean and competitive;
  model-diverse fallback evidence is more valuable than further Sol sampling.
  Revision-6 plan SHA-256 is
  `1b84578fa89e6b0c338d02189764adcb604ab7f1f6bf65ab161d947678fbd62c`.
- WBD-005 model-diverse screen complete. Luna/high repeats 2 and 3 both failed
  `js-reduced-zero`, leaving the arm 1/3; stop it. Luna/xhigh passed both
  repeats and is 3/3 provisional. Its observed repeats were expensive
  (190,752--282,721 ms and 57,393--71,213 effective tokens), but it is the only
  clean model-diverse candidate and advances under the predeclared rule.
- Adaptive plan revision 7 adds Luna/xhigh repeats 4--5. If both pass, 5/5
  crosses the qualified fallback gate; any failure stops the arm. No other
  WBD-005 route is scheduled before recomputation. Revision-7 plan SHA-256 is
  `be70923a71b9e06ce09207261918df041b2e7797cdd092cad09c9084d9cffb99`.
- Luna/xhigh qualification stopped: repeats 4 and 5 failed reduced-motion
  contracts (`css-zero-motion` + `js-reduced-zero`, then `js-reduced-zero`),
  leaving the arm 3/5 and insufficient. The fifth cell was already in flight
  when repeat 4 completed, so it finished safely; no further xhigh allocation.
- Cumulative audit passes at 164 rows/artifacts/v2 metric pointers and 74 repeat
  rows. No WBD-005 arm is qualified; a validation-dependent route chain is now
  a required policy property rather than an optional fallback.
- Adaptive plan revision 8 uses the remaining experiment window to screen the
  two unreplicated `max` singleton passes: Luna/max for matrix speed and Sol/max
  for matrix token cost, repeats 2--3 each. Recompute without automatic
  expansion, leaving time for policy installation and closeout. Revision-8
  plan SHA-256 is
  `4c55f5ade6c930833e80c17ac25e1bc2bb25e2114015e488d4948ec87bf4f215`.
- Stage 6 complete: Luna/max and Sol/max both passed repeats 2--3 and are 3/3
  provisional. Luna/max expected cost is 411,730 ms/92,408 effective tokens per
  success; Sol/max is 358,397 ms/64,677. Both are slower and more token-heavy
  than the six-observation Sol medium/high candidates, so do not select them as
  primaries or expand them now.
- T-152 initial policy installed in `tools/agent-benchmark/routing-policy.json`
  with a strict query/validation CLI, all task-class validation commands,
  confidence/evidence, objective-specific selection, and fallback chains.
  `skills/codex-delegation.md` now requires policy lookup for analogous tasks.
  Policy validation and all 15 task/objective lookups pass; evidence hash is
  pinned to the complete 168-row summary.
- Residual campaign allocation: Sol/medium and Sol/high WBD-005 are each 5/6
  provisional. Run repeat 7 for both, recompute, and continue one repeat at a
  time only while an arm remains capable of reaching 8/9 (Wilson lower 0.565)
  qualification before the closeout reserve.
- Adaptive plan revision 9 adds exactly repeat 7 for Sol/medium and Sol/high.
  Run both, checkpoint, and add repeat 8 only for arms that pass. The complete
  policy remains pinned to the 168-row summary until new results are analyzed.
  Revision-9 plan SHA-256 is
  `444b9ee23727ba4cf0979c7ec4d10fa35dfde38536f7b385c95f2df2378e681d`.

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

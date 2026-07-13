# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. `T-109` through `T-117` form the original three-hour
experiment; later iterations are inserted before final T-117 closure. Next free
id: T-126.

## Active

None.

## Blocked / awaiting user

None.

## Recently completed

- **T-117 — Final regression complete:** visible 4/4 and held-out 1/1 score 100; visible effective tokens fell 69.9% and tool output 80.7% versus baseline, with a conservative same-version three-task saving of 60.5% (`tools/out/t117-final.md`).
- **T-125 — Browser-test access logs suppressed:** Playwright uses a quiet local handler so routine asset requests do not consume driver context; fatal server errors, test failures, traces, and reporter summaries remain visible.
- **T-124 — Compact artifact query added:** `benchmark.py show RUN_ID` returns the decision view from raw artifacts/results without injecting full grader tails; `--verbose-result` remains available.
- **T-123 — Compact run responses retained:** decision stdout is 82–86% smaller on final artifacts while complete browser/grader evidence remains available by pointer and `--verbose-result` (`tools/out/t123-compact-run-output.md`).
- **T-122 — Zero-token capsule audit added:** all five clean fixtures prove pristine and broken static gates plus authorization coverage before model spend; semantic/value-invariant checks prevent the held-out false negatives (`tools/out/t122-capsule-audit.md`).
- **T-121 — Experiment budget/stop rule added:** per-label logging exposes 1.187M setup tokens and 24.6% failed-run spend; future tuning uses one-probe, threshold, repeat-cap, preflight, and break-even gates (`tools/out/t121-experiment-budget.md`).
- **T-120 — Decision logging completed:** future rows retain task/repo/runtime/mode identity, and strict comparisons report repeated distributions, gates, failures, and tradeoffs while rejecting unsafe matches (`tools/out/t120-decision-logging.md`).
- **T-119 — Focused inspection retained:** six focused trials across two bilingual HTML tasks scored 100; median effective tokens fell 21.7% and tool output 59.2%. A simpler bounded variant failed CRLF scope and was rejected (`tools/out/t119-focused-inspection.md`).
- **T-118 — Repeatability rule established:** three matched runner-lite and durable portfolios all scored 100; token ranges did not overlap (29,098–30,046 versus 42,958–57,936), and future process promotions require repeated portfolio medians/ranges (`tools/out/t118-repeatability.md`).
- **T-116 — Runner-lite handoff retained:** matched WBD-001/003 stayed 100/100 while effective tokens fell 15.2%, tool output 12.6%, and worker duration 56.7%; redundant schema enforcement increased tokens 47.8% and was rejected (`tools/out/t116-handoff-iteration.md`).
- **T-115 — Routing/escalation optimized:** selected portfolio is 4/4 at
  115,236 effective tokens (-12.7% vs baseline); bounded JS/visual work passes
  Terra/low, and identical two-route failures now trigger contract/grader audit
  before more escalation (`tools/out/t115-routing-iteration.md`).
- **T-114 — Progressive disclosure retained:** capability 2/4→3/4, mean
  90.25→92.5, effective tokens -8.2%, input -25.5%, worker time -21.8%, tool
  output -36.7%; matched passing tasks remain 100 (`tools/out/t114-context-iteration.md`).
- **T-113 — Diagnostic logging upgraded:** backward-compatible schema v2,
  append-only validation/import/summaries, completed-event command counts,
  token/context/tool/duration/gate/failure fields, and raw artifact pointers are
  canonical; four baseline rows validate (`tools/task-metrics.py`).
- **T-112 — Full-context baseline measured:** WBD-001/003 pass and WBD-002/004
  fail; mean 90.25, 132,062 effective tokens, with raw attributable telemetry
  and calibration exclusions retained (`tools/out/t112-baseline.md`).
- **T-111 — Benchmark harness implemented and calibrated:** guarded mutators,
  hidden/static graders, local pinned Playwright P2P, isolated Codex runner, raw
  JSONL/stderr capture, usage parsing, visual reference comparison, and result
  aggregation distinguish WBD-002 broken (42/100) from pristine (100/100).
- **T-110 — Capability suite frozen:** five isolated task capsules cover
  bilingual CRLF HTML, named/secure links, privacy JS, responsive visual CSS,
  and held-out multi-file reduced motion; scoring and no-regression gates are
  fixed (`tools/out/t110-suite-spec.md`).
- **T-109 — Benchmark architecture selected:** compared SWE-bench Multimodal,
  Vision2Web, WebGen-Bench, and WebDev Arena; chose frozen local repo tasks with
  deterministic F2P/P2P plus browser grading and measured Codex telemetry
  (`tools/out/t109-benchmark-comparison.md`).

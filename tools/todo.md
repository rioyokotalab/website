# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-109.

## Active

- **T-115 — Iteration 2: optimize model/effort routing and escalation**
  - Calibrate the cheapest passing route by task class, with explicit automatic escalation on deterministic failure signals.
  - Re-run the fixed suite and compare cost, capability, latency, and review burden with baseline.
- **T-116 — Iteration 3: optimize handoff, review, and logging overhead**
  - Reduce duplicated narrative in worker outputs while preserving commands, evidence, failures, and machine-readable results.
  - Test whether compact handoffs lower total tokens without shifting hidden work to the driver.
- **T-117 — Final regression and recommendations**
  - Run the final suite, summarize retained/rejected experiments, document remaining uncertainty, and update the canonical process files.
  - Produce a driver report with reproducible evidence and recommendations for the next benchmark expansion.

## Blocked / awaiting user

None.

## Recently completed

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

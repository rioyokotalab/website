# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-154.

## Active

- **T-149 — Audit and summarize the complete matrix:** require exactly 75
  documented scored cells plus 15 scored `ultra` cells. Check run identity,
  task version, settings, artifacts, scope, P2P, and metrics integrity; report
  per-task and aggregate model/effort quality, token cost, latency, failures,
  Pareto routes, and break-even. Treat single-run cells as estimates rather
  than medians, and clean obsolete raw artifacts/results together after the
  decision is durable.
- **T-151 — Allocate adaptive matched repeats:** after T-149, identify each
  task's passing cost/latency/quality Pareto frontier and use the remaining
  campaign time for matched repeats of plausible dispatch winners. Target at
  least three observations per contender, eliminate dominated routes only from
  comparable evidence, and checkpoint every allocation decision and result.
- **T-152 — Install the evidence-backed dispatch policy:** write a versioned
  per-task/capability model-effort routing policy with fallback and confidence
  fields, reference it from the Codex delegation workflow, and validate that
  future dispatch can select a route without relying on chat history.
- **T-153 — Close the eight-hour campaign:** stop new runs by
  2026-07-14T05:08+0900, finish in-flight evidence safely, audit artifacts and
  metrics, report spend/runtime/failures/uncertainty, checkpoint the ledger,
  commit and push tools-only results, and do not publish the website.

## Blocked / awaiting user

None.

## Recently completed

- **T-148 — Complete the `ultra` rows:** completed all 15 ultra cells (the
  three WBD-001 probes plus 12 new rows). All ultra cells passed score 100 with
  exact scope and P2P, but every ultra route is dominated by a documented-effort
  route on its task. The exact 90-cell dry runs report zero pending cells.
- **T-147 — Run all documented model/effort/task cells:** completed the frozen
  75-cell grid with automatic routing and fixed task-specific timeouts. All 75
  rows, artifacts, and v2 metrics reconcile: 70 capability passes and five
  genuine WBD-005 failures. WBD-004 passed 15/15, with Luna/low jointly best
  for latency and tokens at 46,892 ms and 9,669 effective tokens.
- **T-146 — Freeze, extend, and preflight the GPT-5.6 round:** extended and
  selftested xhigh/max, froze baseline/settings/task/runner/grader identities,
  restored ignored lockfile/browser dependencies, and passed the five-capsule
  audit. Luna/Terra/Sol all accepted `ultra` and passed WBD-001 at 100/100 with
  P2P and exact scope (3 runs, 421,864 ms total, 94,152 effective tokens), so
  `ultra` was promoted to the benchmark and v2 metrics schemas. Paused before
  T-147 at the user's request.
- **T-150 — Expand the GPT-5.6 matrix:** replaced the gated finalist design
  with all five WBD tasks across the full requested model/effort grid; 75 cells
  use documented efforts and `ultra` is capability-gated because it is absent
  from both the official model catalog and current local schemas.
- **T-145 — Plan GPT-5.6 benchmark matrix:** selected a gated 3-model ×
  3-effort screen using Luna, Terra, and Sol at low/medium/high, followed by
  matched visible-suite repeats and held-out confirmation; superseded by T-150
  before any paid run started.
- **T-144 — Normalize the current tree:** renamed shared preview state,
  restarted stale metric and delegation logs, removed residual references and
  reproducible dependency caches, and verified current content, paths, and refs.
- **T-143 — Remove obsolete comparison machinery:** removed the retired runner,
  result and round data, exclusions, raw artifact trees, and local evaluation
  tags while retaining an empty reusable regression suite.
- **T-142 — Remove the inactive project integration:** removed runtime,
  project configuration, registries, dispatch helpers, and obsolete checks;
  consolidated the retained instructions into a Codex-native workflow.
- **T-141 — Inventory and compact:** classified the removal scope, cleared
  completed scratch reports, and reduced the task, fact, decision, session,
  metric, and delegation ledgers to durable current state.

Historical Git commits remain intact; owner-scope settings were not changed.

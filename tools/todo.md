# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-151.

## Active

- **T-146 — Freeze, extend, and preflight the exhaustive GPT-5.6 round:** run
  benchmark selftest/audit, freeze task/runner/grader identities and matched
  settings, and extend the runner for documented `xhigh`/`max` plus schema and
  selftests. Use full prompts, default inspection, `runner-lite`, P2P, run label
  `gpt56-full-20260713`, and a blocked/randomized execution order. After the
  deterministic gates pass, use WBD-001 as one `ultra` capability probe per
  model; keep a successful probe as its matrix cell. Do not add `ultra` to the
  result schema unless the runtime actually accepts it.
- **T-147 — Run all documented model/effort/task cells:** run WBD-001 through
  WBD-005 once for every `gpt-5.6-{luna,terra,sol}` ×
  `{low,medium,high,xhigh,max}` arm (75 scored runs), using
  `--include-held-out` for WBD-005. WBD-005 is a fifth measured task in this
  round, not an unseen selection gate. Never reroute a failed cell to a
  different model or effort. Record score, critical assertions, effective and
  reasoning tokens, duration, scope, cost, and failure class for every attempt.
- **T-148 — Complete or close the `ultra` rows:** for each model whose T-146
  WBD-001 `ultra` probe succeeds, run WBD-002 through WBD-005 at `ultra`, giving
  the requested 90-cell matrix. If a probe is rejected, record its exact
  capability failure once and mark that model's remaining four `ultra` cells
  unsupported/N/A; do not substitute `max` or spend calls repeating a known
  invalid configuration.
- **T-149 — Audit and summarize the complete matrix:** require exactly 75
  documented scored cells plus either 15 scored `ultra` cells or explicit
  unsupported evidence for every `ultra` row. Check run identity, task version,
  settings, artifacts, scope, P2P, and metrics integrity; report per-task and
  aggregate model/effort quality, token cost, latency, failures, Pareto routes,
  and break-even. Treat single-run cells as estimates rather than medians, and
  clean obsolete raw artifacts/results together after the decision is durable.

## Blocked / awaiting user

None.

## Recently completed

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

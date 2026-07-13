# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-150.

## Active

- **T-146 — Freeze and preflight the GPT-5.6 round:** commit the planning
  baseline, run benchmark selftest/audit, and freeze task versions, runner and
  grader identity, full prompt/default inspection, `runner-lite` handoff, P2P,
  and run label `gpt56-20260713`. No model call before both gates pass.
- **T-147 — Screen nine GPT-5.6 arms:** run WBD-001 and WBD-003 once for each
  of `gpt-5.6-{luna,terra,sol}` at `{low,medium,high}` (18 matched runs).
  Stop an arm on a capability/critical-assertion failure; classify failures
  before rerouting. Record score, effective/reasoning tokens, duration, scope,
  and cost for every attempted run.
- **T-148 — Repeat the visible-suite finalists:** select at most three distinct
  Pareto-relevant passing arms (lowest cost, highest quality, and best
  cost/quality tradeoff; collapse duplicates). Give WBD-001/WBD-003 two more
  repeats and WBD-002/WBD-004 three repeats per finalist, so each visible task
  has three matched observations. Compare medians and ranges; do not select on
  an isolated minimum.
- **T-149 — Held-out confirmation and decision:** freeze the finalists, run
  WBD-005 three times for at most two nondominated arms with
  `--include-held-out`, verify the no-regression and 85/100/critical gates, and
  record the recommended default route plus break-even. Clean obsolete raw
  artifacts/results together after the decision is durable.

## Blocked / awaiting user

None.

## Recently completed

- **T-145 — Plan GPT-5.6 benchmark matrix:** selected a gated 3-model ×
  3-effort screen using Luna, Terra, and Sol at low/medium/high, followed by
  matched visible-suite repeats and held-out confirmation; no paid run started.
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

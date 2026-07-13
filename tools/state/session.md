driver: claude (claude-benchmark-driver role; settings.json restored)
updated: 2026-07-13T13:58+0900
task: T-137 Compare Claude agentic-harness strategies
status: complete

## Now
- Goal: DONE. Three-arm frozen Claude configuration screen complete, including
  the user-requested dynamic WBD-005 measurement.
- Outcome: visible WBD-001–004 12/12 PASS @100 across all arms. Held-out
  WBD-005: dynamic PASS 100 (sole passer); autonomous 87, current-harness 78
  (P2P standards-check). Dynamic is the only 5/5 arm (mean 100.0) — clears the
  capability gate over current-harness (cost inconclusive: current Codex MCP
  telemetry incomplete) and beats autonomous on WBD-005 but at +186% eff
  tokens (no-decision-grade-token-gain). Not adopted (per-task generation
  strategy, stochastic generator defect 3/8 calls, single screen);
  current-harness stays canonical pending generator hardening + confirmatory
  phase. Autonomous = efficiency signal (−74% tokens). Aggregate $8.5249/$54.
- Root cause of prior gap: generator is stochastic (2-turn successes vs 6-turn
  failures exceeding schema maxLength). WBD-005 measured via 3rd unchanged
  retry; NO invariant changed.

## Closeout status
- Round record, driver report, decisions.md, todo.md updated with the completed
  dynamic arm and corrected 3/8 generator-failure count. exclusions.json c2eacd
  reason updated (stochastic, resolved). settings.json already at
  site-coordinator/low. Compares regenerated incl.
  t137-compare-autonomous-vs-dynamic.json.
- Next: re-run closeout gates (metrics/selftest/artifacts/preflight/md/py/json),
  commit, rebase, push. No publish/deploy.

## Follow-ups (not blocking)
- Harden the dynamic config generator (retry/backoff, bounded output, or a
  simpler re-validated structured schema) before treating dynamic as adoptable.
- Confirmatory repeat phase (matched portfolios) before any canonical change;
  weigh dynamic's capability win against its +186% token cost vs autonomous.

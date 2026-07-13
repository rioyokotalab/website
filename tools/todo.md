# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-141.

## Active

None.

## Blocked / awaiting user

None.

## Recently completed

- **T-140 — Verify Fable evaluation handoff:** `7140f44` confirmed on
  `origin/main`; five unique Fable/max artifacts and rows reconcile at 1/5,
  108,013 effective tokens, $4.10524, and 937,726 ms; all validators pass.
  Clarified that WBD-005 reached the task-specific generator but no executor or
  grader, identified four derived metrics rows with wrong worker-vs-generator
  phase labels (totals unaffected), and removed one redundant/noncompliant
  post-commit closeout row after preserving it verbatim in the audit. Evidence:
  `tools/out/t140-independent-artifact-audit.md`; driver report:
  `tools/out/driver-report-20260713-1714.md`.
- **T-139 — Corrected Claude dynamic rerun:** COMPLETE. All five frozen
  Fable/max dynamic commands ran once each at corrected ref `b23416b` under
  label `claude-dynamic-b23416b-fable-max-v1`: **1/5 pass** (WBD-001 100;
  WBD-002–005 generator `error_max_budget_usd`; WBD-005's request reached the
  task-specific generator, but no executor or grader ran).
  $4.1052 of $18; 108,013 effective tokens; telemetry complete; 5 rows
  imported + validated; artifact audit pass. Standalone cohort — old-arm
  comparisons remain unmatched; current-harness stays canonical; dynamic needs
  generator hardening. Results: `tools/out/t139-claude-dynamic-rerun.md`;
  round addendum: `tools/agent-benchmark/rounds/2026-07-13-claude.md`.
- **T-138 — Audit benchmark logging and compare Claude/Codex models:** all 79
  retained results, 68 measured metrics, 11 exclusions, and artifact pointers
  reconcile, but the T-137 held-out ranking is not decision-grade: Claude
  WBD-005@2 used pre-fix ref `3364e2c`, so stale P2P and representation-specific
  F2P checks created the dynamic-only win. Clean WBD-001–004 is a four-way
  capability tie; efficiency ranks Codex, Claude autonomous, dynamic, then
  current-harness. Dynamic's true retrying total is 304,755 effective tokens.
  Analysis: `tools/out/t138-model-comparison.md`; audit:
  `tools/out/t138-log-audit.md`.
- **T-137 — Compare Claude agentic-harness strategies:** ran the frozen
  WBD-001–005 suite across current-harness / autonomous / dynamic arms
  (15 measured runs, 3 excluded stochastic generator-setup failures,
  $8.52/$54). Visible WBD-001–004: 12/12 PASS at 100 across all arms. Held-out
  WBD-005: **dynamic PASS 100 — sole passer**; autonomous 87 and
  current-harness 78 failed (P2P `standards-check.py`). Dynamic is the only arm
  at 5/5 and clears the capability gate over current-harness; vs autonomous it
  passes the gate but at +186% tokens. Not adopted (per-task generation
  strategy, stochastic generator defect 3/8 calls, single screen);
  current-harness stays canonical pending a generator-hardened confirmatory
  phase; autonomous is the efficiency signal (−74% tokens). Round record:
  `tools/agent-benchmark/rounds/2026-07-13-claude.md`; driver report:
  `tools/out/t137-claude-benchmark.md`.
- **T-136 — Benchmark-round cleanup and handoff:** promoted the compact round
  record to `tools/agent-benchmark/rounds/2026-07-13.md`; removed 28 integrated
  transient reports, four redundant screenshot pairs, and Python bytecode;
  retained 61 complete pointer-backed run directories plus baseline/failure/
  final visual anchors; documented retention and next-round gates.
- **T-109–T-135 — Agent web-development benchmark and token optimization:**
  established the local five-task suite, achieved 5/5 at 100, reduced effective
  tokens 60.5% on the conservative same-version comparison, improved diagnostic
  logging and compact outputs, and froze the decision workflow. Canonical
  outcome: `tools/agent-benchmark/rounds/2026-07-13.md`.

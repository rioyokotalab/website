# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-138.

## Active

None.

## Blocked / awaiting user

None.

## Recently completed

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

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
  (14 measured runs, 3 excluded generator-setup failures, $7.34/$54). Visible
  WBD-001–004: 12/12 PASS at 100 across all arms. Held-out WBD-005: all
  executed arms missed (autonomous 87, current-harness 78 on P2P
  `standards-check.py`; dynamic unmeasured — systematic structured-output
  generator failure). No arm passed 5/5, so no capability-gated winner and no
  config change adopted; current-harness stays canonical. Autonomous flagged
  as an efficiency candidate (−74% Claude-side tokens) and the dynamic
  generator flagged with a reliability defect. Round record:
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

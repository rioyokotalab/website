driver: claude (claude-benchmark-driver → restored site-coordinator)
updated: 2026-07-13T13:40+0900
task: T-137 Compare Claude agentic-harness strategies
status: complete

## Now
- Goal: DONE. Three-arm frozen Claude configuration screen executed and closed
  out.
- Outcome: visible WBD-001–004 12/12 PASS @100 across all arms; held-out
  WBD-005 all executed arms missed (autonomous 87, current-harness 78, both on
  P2P standards-check; dynamic unmeasured — systematic generator
  structured-output failure ×2). No arm passed 5/5 → no capability-gated
  winner, no config change adopted; current-harness stays canonical.
  Autonomous flagged as efficiency candidate; dynamic generator flagged with a
  reliability defect. Aggregate spend $7.3385/$54.
- Closeout done: round record tools/agent-benchmark/rounds/2026-07-13-claude.md;
  decisions.md + todo.md updated; .claude/settings.json restored to
  site-coordinator/low; gates pass (metrics validate 536, selftest, artifacts
  17, preflight, md-size, claude-size, py_compile, json). Launcher scratch
  removed; driver report + plan + compares + artifact dirs retained (gitignored
  local evidence, pointer-backed by claude-results.jsonl).

## Next
- Commit tracked changes (ledger trio + benchmark bookkeeping committed
  silently), rebase, push after gates. No publish/deploy (no public change).

## Follow-ups (not blocking)
- If a future phase pursues the autonomous efficiency signal, target a full
  5/5 pass, not a screen. Harden the dynamic config generator
  (retry/backoff or simpler schema) before treating it as a viable arm.

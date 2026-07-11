# Durable decisions (newest first; one-line rationale each)

- 2026-07-12 Context ledger adopted: all cross-session context lives in
  tools/todo.md + tools/state/{session,facts,decisions}.md with size
  budgets (tools/check-md-size.py, pre-commit), because session restarts
  and claude<->codex handoffs must lose nothing. Protocol:
  skills/context-ledger.md.
- 2026-07-12 Driver symmetry: codex can drive the repo (AGENTS.md
  "Driving this repo"); handoff in either direction happens only through
  the ledger. Publish stays user/Claude-executed; codex-driver git push
  needs explicit in-conversation user approval.
- 2026-07-12 Ledger lives under tools/state/ to inherit the tools/ deploy
  exclusion (no deploy.sh change needed).
- 2026-07-12 Dispatch prompts point at on-disk state instead of restating
  context (skills/codex-dispatch.md); workers never edit session.md.
- 2026-07-12 researchmap grant rows 2,3,5,6,7,13,19 deliberately left
  without grant numbers (user decision).
- 2026-07-11 Per-call codex model/effort pins are mandatory; startup pins
  in .mcp.json are a safety net only (commit 56669c5).

# Durable decisions (newest first; one-line rationale each)

- 2026-07-12 T-16 publish transaction order: rebase and dry-run first, then
  commit+push before live deployment, so push failure cannot change production
  and any partial deploy is traceable to an existing GitHub commit.
- 2026-07-12 T-12 GA4 policy: use measurement ID `G-DVRGG7FDLX` with
  privacy-first basic consent—no Google tag/request before explicit acceptance;
  persist accept/reject locally and keep settings reversible—because the owner
  selected privacy-first behavior.
- 2026-07-12 Direct DRIVER publish policy: directly user-started Claude and
  Codex DRIVER sessions have standing authority to publish/push completed
  owner-requested repository changes after mandatory preflight, without a
  separate permission prompt; dispatched/MCP Codex WORKER sessions remain
  prohibited and ambiguity defaults to WORKER.
- 2026-07-12 T-11 zero-interaction configuration applied owner-side: routine
  in-scope work uses Claude bypass and Codex never/full-access after a cold
  restart; credentials, destructive/force operations, and material
  scope-expansion remain prohibited or owner-gated.
- 2026-07-12 Context ledger adopted: all cross-session context lives in
  tools/todo.md + tools/state/{session,facts,decisions}.md with size
  budgets (tools/check-md-size.py, pre-commit), because session restarts
  and claude<->codex handoffs must lose nothing. Protocol:
  skills/context-ledger.md.
- 2026-07-12 Driver symmetry: codex can drive the repo (AGENTS.md
  "Driving this repo"); handoff in either direction happens only through
  the ledger. Publish/push authority follows the current role gates in
  AGENTS.md and skills/publish-and-verify.md.
- 2026-07-12 Ledger lives under tools/state/ to inherit the tools/ deploy
  exclusion (no deploy.sh change needed).
- 2026-07-12 Dispatch prompts point at on-disk state instead of restating
  context (skills/codex-dispatch.md); workers never edit session.md.
- 2026-07-12 researchmap grant rows 2,3,5,6,7,13,19 deliberately left
  without grant numbers (user decision).
- 2026-07-11 Per-call codex model/effort pins are mandatory; startup pins
  in .mcp.json are a safety net only (commit 56669c5).

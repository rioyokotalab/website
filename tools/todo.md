# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending

### Give codex agents web access
- [ ] Enable network access for codex MCP workers (currently sandbox workspace-write blocks network). Determine correct codex-cli config key, add via gen-codex-mcp.py to .mcp.json + user scope, update codex-workers.json _meta + CLAUDE.md/policy note ("codex has no network" becomes false). Deliver as tools/out proposal + apply script.

## Recently completed (durable in git; here only as context)
- RM<->website consolidation Cat 1-4: published live (commit 80a0de8); JP/EN member + achievements + cv.tex.
- media_coverage exporter path added (commit d543652); researchmap-import.jsonl generated and IMPORTED by user to ResearchMap.
- Latency fix: codex model/effort startup pins baked into .mcp.json + gen-codex-mcp.py + codex-workers.json (commit 56669c5); verified live both scopes. Latency guardrails added to tools/task-tier-policy.md.
- Cat 5 (2026-07-12): grant-ID extraction from publication PDFs -> researchmap research_projects linked-papers, DONE. 41 collected PDFs permanently archived in tools/papers/ (named `{FirstAuthorLastName}{Year}.pdf`). Grant->paper links applied manually by user: 10/22 projects populated, 21 papers, 31 confirmed/3 inferred. Fixed researchmap-export.py `fetch_live` empty-but-valid guard bug; `--check-live` import (29 entries) imported by user. Deliberately left open: 7 research projects (rows 2,3,5,6,7,13,19) still lack researchmap grant numbers — user chose to leave unfilled.

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. Codex workers now have network via `-c sandbox_workspace_write.network_access=true` and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- tools/out/ is gitignored transient scratch; nothing there is durable. Delete task scratch once verified/committed; never blind-wipe pending deliverables.

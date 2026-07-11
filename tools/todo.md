# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending

### Give codex agents web access
- [ ] Enable network access for codex MCP workers (currently sandbox workspace-write blocks network). Determine correct codex-cli config key, add via gen-codex-mcp.py to .mcp.json + user scope, update codex-workers.json _meta + CLAUDE.md/policy note ("codex has no network" becomes false). Deliver as tools/out proposal + apply script.

### Cat 5 — subtasks (STASHED — in progress, resume on request)
Goal: parse Acknowledgements of each publication PDF, extract grant IDs (JSPS KAKENHI JPxxxxxxxx, JST/AMED/MEXT programs), match each to a researchmap research_project, populate that project's linked-papers ("List of results of the research project"). Feeds RM export. Incremental, bounded, all deliverables under tools/out/.
- [x] 5a. DONE: 134 publications with accessible-PDF identifiers indexed -> tools/out/cat5-pdf-index.md (NOTE: tools/out was cleared earlier but these were regenerated after; if absent, re-run 5a by parsing en/achievements/index.html data-doi/data-url).
- [x] 5c. DONE: 22 research projects extracted from jp/member/yokota.html 研究課題 -> tools/out/cat5-project-map.md. IMPORTANT: member page has NO grant/課題番号 numbers, so 5d must source grant IDs externally (KAKENHI/researchmap).
- [~] 5b. IN PROGRESS: batch 1 done (pubs #7,#43,#44,#46 -> tools/out/cat5-grants-batch01.md; all had grants). ~130 pubs remain (~33 batches of 4, or ~11 chunks of ~10-12). Fetch via Claude Bash (arxiv/openreview/jstage/crossref), extract grants via codex. BLOCKER: OpenReview-only entries (#6,#72,#82) return app-shell to non-browser clients — need arXiv/DOI fallback. Cached PDFs in tools/out/cat5-pdfs/.
- [ ] 5d. Aggregate 5b grants against 5c projects; resolve unmatched grant IDs via web search -> tools/out/cat5-linked-papers.md
- [ ] 5e. Generate research_projects linked-papers import lines -> tools/out/researchmap-import.jsonl, re-run/verify exporter.

## Recently completed (durable in git; here only as context)
- RM<->website consolidation Cat 1-4: published live (commit 80a0de8); JP/EN member + achievements + cv.tex.
- media_coverage exporter path added (commit d543652); researchmap-import.jsonl generated and IMPORTED by user to ResearchMap.
- Latency fix: codex model/effort startup pins baked into .mcp.json + gen-codex-mcp.py + codex-workers.json (commit 56669c5); verified live both scopes. Latency guardrails added to tools/task-tier-policy.md.

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. Codex workers now have network via `-c sandbox_workspace_write.network_access=true` and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- tools/out/ is gitignored transient scratch; nothing there is durable. Delete task scratch once verified/committed; never blind-wipe pending deliverables.

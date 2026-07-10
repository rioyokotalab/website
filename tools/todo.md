# Claude x codex collaboration and ResearchMap metadata todo

Cross-session source of truth. Keep this file concise, current, and actionable.

## SESSION HANDOFF / current state
>>> COLD-RESTART HANDOFF 2026-07-10 (READ FIRST) <<<
NEXT TASK: read `/home/rioyokota/website/SPARK.md` (untracked, at repo root) — that is the task to work on after this restart. Follow its instructions.
PRIOR WORK STATE (all DONE & LIVE, nothing in progress): ResearchMap metadata Fields 1-5 and the domestic ja/en author split (`data-authors-ja`/`data-authors-en` on sub005+sub007, en+jp) are complete, published, and live; latest related commit a4bdefc. Tooling/todo committed through commit 2cc790f. There is NO active website-metadata task in progress.
RESUME AFTER SPARK.md: the remaining OPTIONAL/open website work is in the sections below — "Future exporter refinements" (incl. extending explicit ja/en split attributes to international sections sub001-004,006, currently covered by exporter fallback) and the "Claude x codex workflow checklist" (C3-C7). Pick these up only when returning from the SPARK.md task.
REMINDERS: MCP approval dialog will NOT reappear (`hasTrustDialogAccepted=true`); every write-capable codex call MUST pass `sandbox:"workspace-write"`; codex sandbox has NO network so metadata lookups run via Bash/site-author/site-checker; pull --rebase before every push (multi-committer repo); after EVERY task append to `tools/task-metrics.jsonl` and refresh `tools/task-tier-policy.md`.
>>> END COLD-RESTART HANDOFF <<<

## Legend
- [~] in progress
- [ ] not started

## Future exporter refinements
- [ ] Optional later: extend explicit split attributes to international sections (sub001-004,006); currently covered by exporter fallback.
- [ ] researchmap update/delete path: `tools/researchmap-export.py` only generates insert lines; update/delete JSONL is hand-built. Future work is adding an automated update path while preserving the stable import grammar in `CLAUDE.md`.
- [ ] ORCID auto-diff / OAuth push: ORCID export is one-way BibTeX, no live diff. Future work is 3-legged OAuth/member-API auto-diff + push while preserving the current no-OAuth/public-API rule.
- [ ] `data-isbn` for books: skipped in Field-5 because ISBNs were not in citation text; future work is adding sourced ISBNs and exporter support.
- [ ] Automatic ResearchMap push: blocked on JST WebAPI key from the URA office; until then upload remains manual via ResearchMap settings/import.
- [ ] 川畑輝 extra author on sub005 #1 (ANLP2025): flagged but never added across the four targets (website EN/JP, `cv.tex` + `cv.pdf`, ORCID bib, ResearchMap). Do only if user requests; detail preserved below.

## Claude x codex workflow checklist
- [~] C3 **Enforce output-file-first**: standing rule in all four codex-enabled agent prompts + `AGENTS.md` that the `tools/out/` file is the deliverable. The Claude agent must confirm the file exists and is non-empty before reporting PASS; chat replies are pointers, not payloads. Re-run the achievements parity sweep after this is fully enforced so its report persists.
- [ ] C4 **Make codex-by-default explicit**: update site-checker/editor/author prompts so any task reading >2 files or >~100 lines goes to codex; the Claude agent reads only codex's output file plus minimal spot-check lines; cap subagent final messages at ~15 lines. `.claude/agents/*.md` are HAND-EDIT only.
- [ ] C5 **Exercise cross-session resumption**: for follow-up work on a logged task, resume via codex-reply with the logged conversationId instead of re-supplying context. Treat conversationIds as optimization; `tools/out/` files + this todo remain the durable truth. Validate once on a real task and note the result here.
- [ ] C6 **AGENTS.md upkeep**: add or verify (a) codex self-logging duty, (b) output-file-first rule, and (c) pointer to `tools/todo.md` and active `tools/out/` task files so codex self-loads ongoing context.
- [ ] C7 **Document + commit**: record the finalized division of labor and the C1-C6 outcomes in `CLAUDE.md` (codex MCP section), commit and push.

## Persistent notes / reference
- Placeholder rules: values that cannot be confirmed follow the no-year-only style rule per field; for dates use the deterministic `-01` placeholder when only year/month logic requires it. Prefer fixing the source citation over guessing.
- Section entry counts (en, 2026-07-08): sub001=42, sub002=2, sub003=2, sub004=115, sub005=32, sub006=45, sub007=62. EN and JP citations are identical for international entries; shared attributes are normally written to both language files.
- Per-field workflow: derive values in small batches and append each result immediately to `tools/out/`; write attributes to both EN/JP with CRLF-safe Python using `open(path, newline='', encoding='utf-8')` for both read and write; verify localhost 200 plus EN/JP parity; preview and get user approval; publish via site-publisher only; update exporters to prefer attributes over heuristics; update this todo after each step.
- GTC talks are internally reviewed by NVIDIA (user confirmed 2026-07-08; submissions can be rejected), so GTC-talk entries correctly belong in sub004 (international peer-reviewed); do not move them to sub006.
- PENDING (2026-07-08): sub005 #1 ANLP2025 paper 「新聞記事からつくる 時事と社会に強い日本語LLM」 official proceedings list an extra author 川畑輝 not present on the website/CV/ResearchMap/ORCID entry. Title was mirrored to all targets 2026-07-08 (website EN/JP, `cv.tex` + `cv.pdf`, ORCID bib, ResearchMap update rm:id 50836989); the 川畑輝 author addition was flagged but NOT done. Add it across all four targets only if the user requests.
- Keep this file and `CLAUDE.md` in sync when the plan changes.

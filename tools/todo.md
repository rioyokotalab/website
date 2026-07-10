# Claude×codex collaboration optimization — persistent todo (added 2026-07-08)

Objective: minimize Claude token use by offloading bulk reading/generation to
codex, while keeping Claude's workflow/permission/verification control and
lossless context transfer (Claude↔codex and across sessions). Do steps in
order; tick and commit after each.

## SESSION HANDOFF (update every time before a restart)
>>> COLD-RESTART HANDOFF 2026-07-10 (READ FIRST) <<<
STATE: ResearchMap metadata Fields 1-5 are fully DONE. Field-5 is PUBLISHED and LIVE at commit c190e48; EN/JP parity PASS.
UNCOMMITTED FILES on disk (persist across restart): tools/todo.md, tools/task-metrics.jsonl, tools/task-tier-policy.md, tools/codex-log.md.
FIRST ACTION AFTER RESTART: no Field-1-5 metadata action remains. Only handle future exporter refinements if explicitly requested.
REMINDERS: MCP approval dialog will NOT reappear (hasTrustDialogAccepted=true) — that is expected, do not worry. Every write-capable codex call MUST pass sandbox:"workspace-write". codex sandbox has NO network (metadata lookups via Bash only). After EVERY task append a line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md (PostToolUse Task hook reminds). Pull --rebase before every push (multi-committer repo).
AFTER FIELD-5 PUBLISHED: DONE 2026-07-10 at commit c190e48; remaining optional work is only future exporter refinements if requested.
>>> END COLD-RESTART HANDOFF <<<

Status 2026-07-10: sub007 Field-2 fully applied (item 6 IPSJ URL added en+jp, NOT yet published). sub005->sub007 move (深層学習における低精度演算…PRMU 2017) verified live in repo (sub005=31, sub007=63). Exporters emit data-doi/data-url. tools/out scratch cleared.
Status 2026-07-10b: Field-3 STARTED. sub001 done (35 entries data-volume/number/pages, matched by data-doi via Crossref) + sub005 done (5 entries), both en+jp, verified parity, NOT yet published/committed. Remaining Field-3: sub004 (115), then exporter emits volume/number/starting_page/ending_page. Derivation files: tools/out/field3-sub001.md, tools/out/field3-sub005.md.
Status 2026-07-09: Field-2 data-doi/data-url LOOKUPS COMPLETE for all sections sub001-sub007. sub006 = 45/45 blank (tools/out/doi-sub006.md). sub007 = 4 doi + 3 url + 55 blank (tools/out/doi-sub007.md). REMAINING Field-2: (a) site-editor writes sub006 (nothing to write) + sub007's 4 data-doi + 3 data-url onto matching <li> in BOTH en+jp achievements pages; (b) update tools/researchmap-export.py + orcid-export.py to emit doi from data-doi / see_also from data-url. Codex config left AS-IS by user decision 2026-07-09 (the ~1h sub007 run was one agent doing 62 serial lookups; no codex effort/trials knob would fix that — future long sections should be fanned out, not a config change).
Status 2026-07-08 (context-reset handoff): TWO threads in flight. (A) Field 2 data-doi sub004 COMPLETE 115/115 (2026-07-09); results in tools/out/doi-sub004.md. Remaining Field-2: sub006, sub007, then the exporter (map data-doi -> DOI identifier, data-url -> see_also). NOTE: several sub004 entries recorded a DOI/arXiv despite website title/venue revisions vs the published version — flagged inline in doi-sub004.md (e.g. Aurora-M, Formula-Driven/Supervised, RePOSE, BiCGStab, EPASA FMM, Task-Parallel FMM, treecode-vs-FMM journal). Do NOT edit any HTML titles unless the user asks. (B) CONFIG-OFFLOAD CHANGE DONE (verified 2026-07-09): the site-coordinator/site-rescue codex-high tier + offload-by-default proposals were already applied in an earlier session; proposal files removed from tools/out/. Live .claude/agents/*.md, AGENTS.md, and CLAUDE.md already contain the codex-tier/offload-first content (verification in tools/out/verify-config-proposals.md). Nothing further to apply. Tier map: site-checker/site-editor->codex-medium; site-author/site-coordinator/site-rescue->codex-high; site-publisher->NO codex tier. Tier map after apply: site-checker/site-editor->codex-medium; site-author/site-coordinator/site-rescue->codex-high; site-publisher->NO codex tier. codex-high/medium/low ARE all in ~/.claude.json user scope (confirmed), so the main session gets codex-high after restart + MCP approval; if main-session codex cannot WRITE tools/out/, add -c sandbox_mode="workspace-write" to user-scope codex-high args (project .mcp.json already has it). AFTER RESET: apply config, restart, then continue sub004 DOI at entry 27.
Status 2026-07-08 (hard-reset handoff): CONFIG/OFFLOAD WORKFLOW NOW LIVE — the aggressive-codex-offload standing directive + config-hand-edit-only rules were applied. CLAUDE.md now carries the '## Standing directive: codex offload and config edits' block (top, before '## Budget rule:'). The 6 .claude/agents/site-*.md files, .claude/agents/codex-offload-policy.md (shared DRY policy; all agents reference it at /home/rioyokota/website/.claude/agents/codex-offload-policy.md), and repo-root AGENTS.md were replaced via tools/out proposals moved into place by the user with tools/out/apply-agent-proposals.sh. .claude/settings.local.json now has an airtight two-layer lock (permissions.deny + PreToolUse hook) so only the human can run apply-agent-proposals.sh. NEW WORKFLOW: CLAUDE.md/.claude/agents/*.md/.mcp.json/AGENTS.md are hand-edit-only; agents write proposed changes to tools/out/<same-filename> for the user to mv. tools/out/CLAUDE-standing-directive-snippet.md is now redundant (its content is in CLAUDE.md) and may be deleted. FIRST ACTION next session: read this file top-to-bottom, then resume Field 2 data-doi sub004 at entry 9 (see below).
Status 2026-07-10c: Field-3 COMPLETE (sub001 35, sub004 48, sub005 5 entries; exporters emit vol/num/pages). All uncommitted, pending publish. NOTE: codex sandbox has NO network — Crossref/metadata lookups must run via Bash (site-author/site-checker), not codex.
Status 2026-07-10d: Field-4 data-authors COMPLETE for all sections sub001-007 (300 entries, en+jp, semicolon-separated, whitespace-normalized; positional-match write with data-doi guard) + exporters emit authors. Verified parity PASS. UNCOMMITTED, pending publish. Extraction scratch tools/out/authors-*.md still present (delete after publish).
Status 2026-07-10e: Field-5 COMPLETE. data-publisher sub002/003 (4), data-event 108 + data-location 2 + data-invited 44 (sole-Yokota) sub006/007, exporters emit all. Verified parity PASS. UNCOMMITTED, pending publish. ALL FIELDS 1-5 now done. Scratch tools/out/field5-*.md present (delete after publish).

Investigations done 2026-07-08:
- sub007 count: 62 is CORRECT (counted inside the <ol>); the "79" was a naive-regex boundary artifact spilling into the <aside id="sub"> sidebar nav. No change needed; keep 62 everywhere.
- NAV FIX DONE & LIVE (2026-07-08, commit 11f890c): the JP mobile `<ul id="topnav">` 連絡先 item was added to all 13 JP pages (jp/index.html href=contact/index.html; jp/contact/index.html href=index.html; other 11 = ../contact/index.html). Published and verified live (site-checker PASS, 0 EN/JP mobile-nav mismatches). Edit script at tools/out/jp-mobile-contact-fix.py.

- [x] C1 **Unblock codex writes** (root blocker, found 2026-07-08: codex sandbox
  rejected writing tools/out/achievements-parity.md, so the append-incrementally
  durability convention is dead). HAND-EDIT .mcp.json (main session/user only —
  subagents refuse config edits): add `-c sandbox_mode="workspace-write"` (and
  pin cwd to the repo if needed) to codex-high/medium/low args. Restart, approve
  servers, then verify: site-checker asks codex-low to write + read back
  tools/out/sandbox-test.md.
  VERIFIED 2026-07-08: codex-medium wrote+read-back tools/out/sandbox-test.md (conversationId 019f41a1-9084-7e93-be3e-2a401742ff5f). PASS.
- [x] C2 **Fix the logging contradiction**: site-checker is read-only yet its
  prompt tells it to append to tools/codex-log.md (result: log empty despite a
  2026-07-08 delegation). New convention: CODEX appends its own log line
  (date | calling agent | task | output file | conversationId | outcome) as the
  last action of every task — add this duty to AGENTS.md; agents only relay the
  conversationId. Backfill the 2026-07-08 parity-sweep line
  (conversationId 019f418a-ea0e-7062-b279-90bc4b4f711e, no output file).
- [~] C3 **Enforce output-file-first**: standing rule in all four codex-enabled
  agent prompts + AGENTS.md — the tools/out/ file IS the deliverable; the Claude
  agent must confirm the file exists and is non-empty before reporting PASS;
  chat replies are pointers, not payloads. Re-run the achievements parity sweep
  after C1 so its report actually persists.
- [ ] C4 **Make codex-by-default explicit**: update site-checker/editor/author
  prompts — any task reading >2 files or >~100 lines goes to codex; the Claude
  agent reads only codex's output file plus minimal spot-check lines; cap
  subagent final messages at ~15 lines. (.claude/agents/*.md are HAND-EDIT only.)
- [ ] C5 **Exercise cross-session resumption**: for follow-up work on a logged
  task, resume via codex-reply with the logged conversationId instead of
  re-supplying context; treat conversationIds as optimization, tools/out/ files
  + this todo as the durable truth. Validate once on a real task and note the
  result here.
- [ ] C6 **AGENTS.md upkeep**: add (a) the codex self-logging duty (C2), (b) the
  output-file-first rule (C3), (c) a pointer to tools/todo.md
  and any active tools/out/ task files so codex self-loads ongoing context.
- [ ] C7 **Document + commit**: record the finalized division of labor and the
  C1–C6 outcomes in CLAUDE.md (codex MCP section), commit and push.

# ResearchMap metadata attributes — persistent project todo

Goal: enrich every Achievements `<li>` with the metadata ResearchMap needs, stored
as invisible `data-*` attributes on the `<li>` (rendered page unchanged). Done
one FIELD at a time, each field rolled across sections sub001..sub007, so each
step is small and independently verifiable. This file is the source of truth for
progress across sessions — read it first, update + commit it after each step.

Rules live in CLAUDE.md: the `data-date` convention + no-year-only derivation
rule (Content conventions), and the failure-driven workflow rules (Delegation to
subagents). Section entry counts (en, 2026-07-08): sub001=42, sub002=2, sub003=2,
sub004=115, sub005=32, sub006=45, sub007=62. EN and JP citations are identical for
international entries, so each attribute is written to BOTH language files.

## Legend
- [x] done & live   - [~] in progress   - [ ] not started

## Per-field workflow (repeat for every field)
1. Derive values — site-author, SMALL batches (<=3-4 entries), authorize hosts
   (Crossref/DBLP/Semantic Scholar/J-STAGE/DOI resolvers), append each result to
   a tools/out/ file IMMEDIATELY (survives mid-run cutoff).
2. Write attribute to BOTH en+jp — site-editor, give unique title substring +
   value per entry, CRLF-safe python3 script; stop if any substring is non-unique.
3. Verify — site-checker: localhost 200 + EN/JP parity (counts & values).
4. User previews at http://localhost:8000/jp/achievements/index.html, approves.
5. Publish — site-publisher runs publish.sh; expect the publickey push to fail,
   then site-editor recovers the push via the /tmp/ssh-* socket. Verify live.
6. Update tools/researchmap-export.py (and orcid-export.py) to PREFER the new
   attribute over heuristic parsing when present.
7. Tick the boxes below, commit+push this file.

## Field order & progress

### Field 1 — data-date (publication_date; REQUIRED)
- [x] sub001 journal (42) — live 2026-07-08, commit 517df17 (4 Jan placeholders: TSIPN, TMLR, 2x JSCES)
- [x] sub002 book series (2)
- [x] sub003 books (2)
- [x] sub004 intl peer-reviewed (115) — conferences: first day of conference
- [x] sub005 domestic peer-reviewed (32)
- [x] sub006 intl non-reviewed (45)
- [x] sub007 domestic non-reviewed (62)
- [x] exporter prefers data-date over heuristic date parsing — live 2026-07-08 (researchmap-export.py + orcid-export.py read <li data-date>, override heuristic; offline dry-run OK)

### Field 2 — data-doi
- [x] sub001 (37 doi + 2 url; 3 blank: JP domestic 計算工学/シミュレーション + JSCES)  - [x] sub002 (0; 数学セミナー magazine, no DOI)  - [x] sub003 (2 doi; MK/Elsevier chapters)  - [x] sub004 (115/115 done 2026-07-09; results in tools/out/doi-sub004.md; mix of DOIs + arXiv/OpenReview URLs + blanks for posters/talks; title/venue-mismatch cases flagged inline)  - [x] sub005 (4 doi + 5 url; rest domestic-only, no identifier; #1 left blank—ANLP title mismatch)  - [x] sub006 (0 doi + 0 url + 45 blank; all talks/keynotes/posters, no identifier — tools/out/doi-sub006.md)  - [x] sub007 (4 doi J-STAGE pjsai/jpsgaiyo + 4 url ANLP2024 anthology + IPSJ item 6 https://ipsj.ixsq.nii.ac.jp/records/235916 + 54 blank — tools/out/doi-sub007.md; JSAI proceedings→pjsai DOIs, JPS annual→jpsgaiyo DOIs)
- [x] exporter emits doi from data-doi / see_also from data-url — live (commit 115c196/f96db57)

### Field 3 — data-volume / data-number / data-pages (journals & proceedings)
- [x] sub001 (35 entries: volume 32 / number 28 / pages 32; en+jp, NOT yet published)  - [x] sub004 (48 entries: pages 48 / volume 4 / number 4; en+jp, NOT yet published)  - [x] sub005 (5 entries have values: 10/23/28/29/30; en+jp, NOT yet published) (others N/A)
- [x] exporter emits volume/number/starting_page/ending_page (researchmap + orcid, offline dry-run OK, NOT yet published)

### Field 4 — data-authors (normalized; later ja/en split)
- [x] sub001 (42)  - [x] sub002 (2)  - [x] sub003 (2)  - [x] sub004 (115)  - [x] sub005 (31)  - [x] sub006 (45)  - [x] sub007 (63) — 300 total, en+jp, NOT yet published
- [x] exporter emits authors from data-authors (researchmap + orcid, prefer over heuristic, offline dry-run OK, NOT yet published)

### Field 5 — books/presentations extras
- [x] data-publisher for sub002 (日本評論社) + sub003 (Morgan Kaufmann); data-isbn skipped (not in citation text, per user 2026-07-10) — NOT yet published
- [x] data-event (108) + data-location (2: Heidelberg, Kobe) + data-invited (44, marked where Rio Yokota is SOLE author per data-authors) for sub006/sub007 — NOT yet published
- [x] exporter emits event/location/invited/publisher (researchmap + orcid, offline dry-run OK) — NOT yet published

## Extracted from CLAUDE.md (2026-07-10)
- [x] Field 1 exporter preference — CLAUDE.md still said "Remaining Field-1 task: update exporter to prefer `data-date`"; this was already completed and live per Field 1 above, so the pending note was removed from CLAUDE.md.
- [x] Field 2 completion/exporter mapping — CLAUDE.md still said "Future Field-2 exporter maps `data-doi` -> DOI identifier and `data-url` -> `see_also`" and that sub006/sub007 plus exporter update remained; this was already completed and live per Field 2 above, so the stale pending note was removed from CLAUDE.md.
- [ ] researchmap update/delete automation — CLAUDE.md noted that `researchmap-export.py` has no update path and update/delete JSONL is hand-built; keep the stable import grammar in CLAUDE.md, but track the automated update/delete exporter work under Future exporter refinements below.
- [ ] Automatic researchmap push — CLAUDE.md noted that automatic push awaits a JST WebAPI key from the URA office; keep the stable sanctioned WebAPI/read-API rule in CLAUDE.md, but track the blocked push work under Future exporter refinements below.
- [ ] ORCID auto-diff / OAuth push — CLAUDE.md noted that future OAuth/member-API or 3-legged OAuth token auto-diff push is possible but not built; keep the stable no-OAuth/public-API rule in CLAUDE.md, but track the push work under Future exporter refinements below.

## Future exporter refinements (optional — added 2026-07-10, moved from CLAUDE.md)
- [~] ja/en author split — APPROVED design: add two attributes `data-authors-ja` / `data-authors-en` on every Achievements `<li>`; exporter maps them to `authors.ja` / `authors.en` with fallback to legacy `data-authors`. Current state: `data-authors` is one normalized semicolon-separated string.
- [ ] researchmap update/delete path — researchmap-export.py only generates insert lines; update/delete JSONL is hand-built; future work is adding an automated update path.
- [ ] ORCID auto-diff / OAuth push — ORCID export is one-way BibTeX, no live diff (public API read-only without OAuth); future work is 3-legged OAuth member-API auto-diff + push.
- [ ] data-isbn for books — skipped in Field-5 (not in citation text); future work is adding data-isbn + exporter field when ISBNs are sourced.
- [ ] Automatic researchmap push — blocked on JST WebAPI key (URA office); until then upload is manual via 設定 > インポート.
- [ ] 川畑輝 extra author on sub005 #1 (ANLP2025) — flagged but never added across the four targets (website EN/JP, cv.tex+cv.pdf, ORCID bib, researchmap); do only if user requests. See existing PENDING note below.

## Notes
- Values that cannot be confirmed follow the no-year-only style rule per field
  (dates -> `-01` placeholder). Prefer fixing the source citation over guessing.
- Keep this file and CLAUDE.md in sync when the plan changes.
- GTC talks ARE internally reviewed by NVIDIA (user confirmed 2026-07-08 — has had submissions rejected), so GTC-talk entries correctly belong in sub004 (intl peer-reviewed); do NOT move them to sub006.
- PENDING (2026-07-08): sub005 #1 ANLP2025 paper 「新聞記事からつくる 時事と社会に強い日本語LLM」 — the official proceedings lists an extra author 川畑輝 not present on the website/CV/researchmap/ORCID entry. Title was mirrored to all targets 2026-07-08 (website EN/JP, cv.tex+cv.pdf, ORCID bib, researchmap update rm:id 50836989); the 川畑輝 author addition was flagged but NOT done — do it across all four targets if the user requests.

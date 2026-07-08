# Claude×codex collaboration optimization — persistent todo (added 2026-07-08)

Objective: minimize Claude token use by offloading bulk reading/generation to
codex, while keeping Claude's workflow/permission/verification control and
lossless context transfer (Claude↔codex and across sessions). Do steps in
order; tick and commit after each.

## SESSION HANDOFF (update every time before a restart)
Status 2026-07-08 (updated): C1 DONE & VERIFIED — codex writes unblocked via .mcp.json workspace-write (conversationId 019f41a1-9084-7e93-be3e-2a401742ff5f). C2 DONE — tools/codex-log.md backfilled; codex self-logging duty added to AGENTS.md. C3 IN PROGRESS — output-file-first rule added to AGENTS.md and the achievements parity sweep was RE-RUN & PERSISTED (tools/out/achievements-parity.md; 317 content <li>/side, 0 data-date/data-doi/data-url mismatches), but the ".claude/agents/*.md prompt" half of C3/C4 is NOT done (hand-edit only). All of the above committed+pushed as b9c13a5. FIRST ACTION next session: read this file top-to-bottom, then continue C4–C7 (all require HAND-EDITing .claude/agents/*.md and a CLAUDE.md update — main-session/manual work).

Investigations done 2026-07-08:
- sub007 count: 62 is CORRECT (counted inside the <ol>); the "79" was a naive-regex boundary artifact spilling into the <aside id="sub"> sidebar nav. No change needed; keep 62 everywhere.
- OPEN NAV BUG (awaiting user go-ahead to fix): the JP mobile <ul id="topnav"> is missing the Contact/連絡先 item that EN mobile has — SITE-WIDE across all 12 JP content pages (every JP page EXCEPT jp/contact/index.html, whose self-page omission mirrors EN's en/contact). Fix = add a `<li><a href="[depth]contact/index.html">連絡先</a></li>` to each JP page's MOBILE topnav block only (not desktop), matching EN's placement; relative depth = `contact/index.html` for jp/index.html, `../contact/index.html` for section pages and jp/member/*. Scope detail in tools/out/jp-mobile-contact-scope.md. Not yet edited — needs preview+approval before publish.

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
  output-file-first rule (C3), (c) a pointer to tools/researchmap-metadata-todo.md
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
- [x] sub001 (37 doi + 2 url; 3 blank: JP domestic 計算工学/シミュレーション + JSCES)  - [x] sub002 (0; 数学セミナー magazine, no DOI)  - [x] sub003 (2 doi; MK/Elsevier chapters)  - [ ] sub004  - [x] sub005 (4 doi + 5 url; rest domestic-only, no identifier; #1 left blank—ANLP title mismatch)  - [ ] sub006  - [ ] sub007
- [ ] exporter emits doi from data-doi

### Field 3 — data-volume / data-number / data-pages (journals & proceedings)
- [ ] sub001  - [ ] sub004  - [ ] sub005 (others N/A)
- [ ] exporter emits volume/number/starting_page/ending_page

### Field 4 — data-authors (normalized; later ja/en split)
- [ ] sub001  - [ ] sub002  - [ ] sub003  - [ ] sub004  - [ ] sub005  - [ ] sub006  - [ ] sub007
- [ ] exporter emits authors from data-authors

### Field 5 — books/presentations extras
- [ ] data-isbn / data-publisher for sub002, sub003
- [ ] data-event / data-location (+ data-invited) for sub006, sub007
- [ ] exporter emits these

## Notes
- Values that cannot be confirmed follow the no-year-only style rule per field
  (dates -> `-01` placeholder). Prefer fixing the source citation over guessing.
- Keep this file and CLAUDE.md in sync when the plan changes.
- PENDING (2026-07-08): sub005 #1 ANLP2025 paper 「新聞記事からつくる 時事と社会に強い日本語LLM」 — the official proceedings lists an extra author 川畑輝 not present on the website/CV/researchmap/ORCID entry. Title was mirrored to all targets 2026-07-08 (website EN/JP, cv.tex+cv.pdf, ORCID bib, researchmap update rm:id 50836989); the 川畑輝 author addition was flagged but NOT done — do it across all four targets if the user requests.

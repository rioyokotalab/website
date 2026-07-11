# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp: hand-built static HTML (originally Adobe Dreamweaver), no build/framework; stored files and folder tree are served one-to-one.

## Standing directive: codex offload and config edits

Codex-enabled agents follow `.claude/agents/codex-offload-policy.md`, resolving workers from `tools/codex-workers.json` and routing from `tools/task-tier-policy.md`. Hand-edit-only config changes are proposals under `tools/out/` and require an exact user apply command.

After results are verified and committed or regenerable, delete only that task's transient `tools/out/` scratch in the same turn; never blind-wipe `tools/out/`, and keep pending deliverables until upload/apply confirmation.

## Dynamic codex effort selection and task metrics

Worker definitions, task routing/pool state, and dispatch/failover rules live in `tools/codex-workers.json`, `tools/task-tier-policy.md`, and `.claude/agents/codex-offload-policy.md`; read them at dispatch time. Regenerate/check MCP proposals with `tools/gen-codex-mcp.py`; use `tools/gen-codex-mcp.py --check` for drift.

The three bookkeeping files tools/task-metrics.jsonl, tools/task-tier-policy.md, and tools/codex-log.md are committed silently alongside whatever other changes are being committed; NEVER prompt the user to commit them separately (a dedicated commit would loop forever).

## Budget rule:

- CLAUDE.md has a size budget enforced by tools/check-claude-size.py (git pre-commit); keep it terse — compress or move detail out rather than appending.

## Structure

`en/` and `jp/` mirror every path; `js/chglang.js` swaps the language prefix, so missing counterparts 404. Nav: `about`, `research`, `achievements`, `member`, `computers`, `teaching`, `picture`; header: `contact`, `links`; unlinked: `news`, `software`. `style.css` is shared; CSS edits require a scripted `?v=YYYYMMDD` bump in all pages/templates. Galleries use pinned cdnjs Lightbox 2.11/jQuery 3.7 with SRI. Site-wide strings also update `Templates/*.dwt`; preserve `.dont-remove-me`.

## Delegation to subagents (save rate limit)

Use `site-coordinator` routing; agent capabilities and boundaries live in `.claude/agents/site-*.md`. Dispatches are self-contained because subagents share no conversation state.

**Failure-driven workflow updates (standing rule):** record a workflow prevention after every failed, incomplete, or mistaken result.

- Follow-up `Agent` starts fresh (no SendMessage tool); resupply ALL context, e.g. index->citation date mapping, never "the list from before".
- Lookup subagents curl only explicitly authorized hosts. Prompts name Crossref `api.crossref.org`, DBLP, Semantic Scholar, J-STAGE `api.jstage.jst.go.jp`, publisher DOI resolvers; OpenReview and researchmap login block non-browser clients.
- Finals may be EMPTY. Important work must be written incrementally under `tools/out/` and printed finally for `Read` recovery. Because agents may cut off after ~15-20 tool calls with a truncated line, append per item and keep lookup dispatches <=3-4 entries.

**codex MCP backend for site-agents:** register all five registry labels at user `~/.claude.json` AND project `/home/rioyokota/website/.mcp.json`; user scope alone cannot reach project agents/coordinator. Enabled-agent frontmatter grants labels in `mcpServers:` plus matching `mcp__<worker>__codex` (e.g. `mcp__codex-medium__codex`) and `codex-reply`; site-publisher has none. The MANDATORY dispatch contract above applies.

`tools/gen-codex-mcp.py` generates project `.mcp.json` proposal plus exact user-scope `claude mcp add-json`/rollback; check with `tools/gen-codex-mcp.py --check`. `.mcp.json` and `.claude/agents/*.md` remain hand-edit-only proposals in `tools/out/` with exact apply command. `.claude/config-edit-approved` and PreToolUse remain hard accidental-edit blocks, never authorization. `.mcp.json` is repo-only/deploy-excluded by `deploy.sh` `-x '^\.mcp\.json$'`, never public.

Project MCP trust prompts once: `~/.claude.json` records `"hasTrustDialogAccepted": true` for `/home/rioyokota/website`, so later `claude` starts load silently; verify via `/mcp` or `claude mcp list`. Every delegation's final action logs date, agent, task, output file, conversationId in `tools/codex-log.md`; committed pages plus this log are durable, while `codex-reply` conversationIds optimize resumption. Safe rerouting follows the handoff and failover rules above.


## Publishing workflow

Publish only after explicit user approval.

1. **Edit:** update mirrored EN/JP pages; grep changed names/links site-wide. Removing a member also prepends them to Alumni on both member pages (JP: `姓 名 (Romaji Name)`); never rewrite historical news/publications for status changes.
2. **Preview:** user checks `http://localhost:8000/jp/index.html`; wait for explicit approval.
3. **Publish:** route the approved publish to `site-publisher` for its documented preflight and command.
4. **Verify:** curl changed live pages.
5. **Document:** after every publish, update project instructions for durable structure/convention/workflow/tooling changes and ensure GitHub reflects both the site and any required instruction update.

ResearchMap/ORCID mirroring remains explicit-only. Keep `cv/cv.tex` content synchronized automatically as specified below; build `cv/cv.pdf` with `./cv/build-cv.sh` only on explicit request, outside `publish.sh`.

## Content conventions

- **HTML editing:** preserve CRLF with Python `open(path, newline='', encoding='utf-8')` for both read and write. Parse tags case-insensitively; legacy uppercase `<LI>` may be unclosed.
- **Institution:** use 東京科学大学 総合研究院 / Institute of Science Tokyo, IIR for current content. Preserve historical names in historical records and live URLs.
- **Achievements** (`achievements/index.html`): sections `sub001`-`sub007` map to journal / book series / books / international peer-reviewed / domestic peer-reviewed / international non-reviewed / domestic non-reviewed. Entries are newest-first inside each `<ol>`. International citations are English on BOTH language pages; domestic citations are Japanese on both.
- **Achievements `data-date`:** every Achievements `<li>` has `data-date="YYYY-MM"` or `YYYY-MM-DD`. Journals use publication date; conferences use the first conference day. Resolve month from citation text, then DOI/Crossref print or online-first, then J-STAGE 発行日; if still unknown, use January of the known year. Never store year-only. Exporters prefer `data-date`; progress lives in `tools/todo.md`.
- **Achievements identifiers:** an Achievements `<li>` may carry bare `data-doi` or, only when no DOI exists, a confirmed same-paper `data-url` (arXiv abs, OpenReview forum, or ANLP anthology). Require title/author/year agreement; otherwise leave both blank. Export `data-doi` as DOI and `data-url` as `see_also`; track lookup progress in `tools/todo.md`.
- **News:** only top-conference acceptances and grants. Add the dated top-page row and anchored news entry in both languages; use announcement date and grade at that date.
- **Computers page:** refresh Hinadori/Computers-page facts via `site-checker` (which may run short `ybatch` probes); never guess. Last refreshed 2026-07-05: 81 GPUs. 2-GPU RTX 6000 Ada CPU (AMD EPYC 9654) was supplied by user; 8-GPU RTX 6000 Ada CPU is unknown ("-" in table, node down).
- **Research:** current topics precede newest-first yearly thesis sections and matching sidebar anchors. Entries use `<h4>Title（Name）</h4>`, abstract, and lightbox figure from `jp/research/images20XX/`. `en/` is English and `jp/` Japanese; translate titles/abstracts, using known kanji names and romaji for international students.
- Site-wide strings must also update `Templates/*.dwt`.
- **Mirroring to researchmap/FIS**: explicit-only. Run `python3 tools/researchmap-export.py --check-live`, review `tools/out/researchmap-import.jsonl`, and never automate the researchmap login UI (403).
- **Mirroring to ORCID / ORCID BibTeX export**: explicit-only. Run `python3 tools/orcid-export.py` (or `python3 tools/orcid-export.py --dry-run`); output is `tools/out/orcid-works.bib`. Import manually through ORCID **Add works > Import BibTeX**.
- **cv.tex content sync:** automatic in both directions. Whenever `achievements/index.html` or the CV sections of `jp/member/yokota.html` (受賞歴/委員歴/研究課題) change, update the matching `cv/cv.tex` section in the same edit; when `cv/cv.tex` supplies a new item, update the matching website pages in that same edit.
- **CV PDF build:** run `./cv/build-cv.sh` only on explicit request; it stays outside `publish.sh`.


## Content sources and figure tooling

Figure-production sources and recipes live with `site-author`.

## Deployment details

`publish.sh` calls `deploy.sh`, which mirrors the deploy-included tree to SFTP `www/` with deletion. Preview deletion-bearing deploys with `./deploy.sh --dry-run`; excluded repo/config/CV-source paths are defined in `deploy.sh`.

- Deployment is SFTP-only to web root `www/`; never expose credentials and never upload/deploy `.git`.

## Known issues (as of 2026-07)

- External links carry `rel="noopener noreferrer"`; keep that on new `target="_blank"` links.
- Page HTML remains Dreamweaver-era (floats, table layouts); `style.css` is written against existing selectors, so keep class/id names stable when editing pages.

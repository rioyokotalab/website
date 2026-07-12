# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp: hand-built static HTML (originally Adobe Dreamweaver), no build/framework; stored files and folder tree are served one-to-one. The public `en/`-`jp/` tree is frozen (URLs serve 1:1): structural optimization happens in config/tooling/skills, never by moving public pages.

## Skills (canonical playbooks)

Repo-root `skills/` holds the single canonical copy of every recurring procedure, shared by Claude agents and codex workers: html-editing, en-jp-parity, achievements, news-and-members, web-lookup, codex-dispatch, publish-and-verify, config-proposals, exporters, figures (index: `skills/README.md`). Agents read the skills a task touches before acting; dispatches cite skill paths instead of restating rules; when a convention changes, update the matching skill in the same change set. `skills/` is git-tracked, deploy-excluded, and NOT hand-edit-only.

## Context ledger (cross-session memory)

All cross-session context lives on disk, never only in chat: `tools/todo.md` (task board), `tools/state/session.md` (in-flight handoff state), `tools/state/facts.md` (current site/cluster/tooling facts), `tools/state/decisions.md` (durable decisions). Protocol, routing, budgets, checkpoint triggers: `skills/context-ledger.md`. Session start: read todo.md + session.md before acting; checkpoint session.md at task start, after each completed step, and at turn end; record pending asks — approvals are conversation-scoped, never carried. codex can DRIVE this repo directly (charter: `AGENTS.md` "Driving this repo", same ledger and skills); Claude↔codex handoff in either direction happens only through these files. Ledger files commit silently like the bookkeeping trio; budgets enforced by `tools/check-md-size.py` (pre-commit).

## Standing directive: codex offload and config edits

Codex-enabled agents follow `.claude/agents/codex-offload-policy.md` (mechanics condensed in `skills/codex-dispatch.md`), resolving workers from `tools/codex-workers.json` and routing from `tools/task-tier-policy.md`. Codex workers have outbound network access (verified codex-cli 0.144.1): web/metadata lookups run inside codex per `skills/web-lookup.md`, with Claude Bash curl as fallback and independent verification. Hand-edit-only config changes are proposals under `tools/out/` and require an exact user apply command (`skills/config-proposals.md`).

After results are verified and committed or regenerable, delete only that task's transient `tools/out/` scratch in the same turn; never blind-wipe `tools/out/`, and keep pending deliverables until upload/apply confirmation.

## Dynamic codex effort selection and task metrics

Worker definitions, task routing/pool state, and dispatch/failover rules live in `tools/codex-workers.json`, `tools/task-tier-policy.md`, and `.claude/agents/codex-offload-policy.md`; read them at dispatch time. Regenerate/check MCP proposals with `tools/gen-codex-mcp.py`; use `--check` for drift.

The bookkeeping files tools/task-metrics.jsonl, tools/task-tier-policy.md, tools/codex-log.md and the context-ledger files tools/todo.md, tools/state/** are committed silently alongside whatever other changes are being committed; NEVER prompt the user to commit them separately (a dedicated commit would loop forever).

## Budget rule

- CLAUDE.md has a size budget enforced by tools/check-claude-size.py (git pre-commit); keep it terse — move detail into `skills/` rather than appending.

## Structure

`en/` and `jp/` mirror every HTML page path (image assets live under `jp/` only and are shared cross-language — see skills/en-jp-parity.md); `js/chglang.js` swaps the language prefix, so missing page counterparts 404. Nav: `about`, `research`, `achievements`, `member`, `computers`, `teaching`, `picture`; header: `contact`, `links`; unlinked: `news`, `software`. Shared `style.css` with scripted `?v=YYYYMMDD` bumps; pinned cdnjs Lightbox 2.11/jQuery 3.7 with SRI; `Templates/*.dwt` kept in sync; preserve `.dont-remove-me`. Editing and parity rules: `skills/html-editing.md`, `skills/en-jp-parity.md`.

## Delegation to subagents (save rate limit)

Use `site-coordinator` routing; agent capabilities and boundaries live in `.claude/agents/site-*.md`. Dispatches are self-contained via pointers (subagents share no conversation state; follow-up `Agent` calls start fresh): cite skill paths and ledger paths (`tools/state/`, `tools/todo.md` task ids) plus the task delta — shared memory lives on disk (`skills/context-ledger.md`), not in prompts.

**Failure-driven workflow updates (standing rule):** record a workflow prevention after every failed, incomplete, or mistaken result.

- Web/metadata lookups run inside network-enabled codex per `skills/web-lookup.md` (Crossref, DBLP, Semantic Scholar, J-STAGE, publisher DOI resolvers, researchmap public read API; OpenReview and researchmap login block non-browser clients).
- Finals may be EMPTY. Important work must be written incrementally under `tools/out/` and printed finally for `Read` recovery. Agents may cut off after ~15-20 tool calls with a truncated line; append per item; codex lookup sessions <=2 items, Claude lookup dispatches <=3-4 entries.

**codex MCP backend for site-agents:** register all five registry labels at user `~/.claude.json` AND project `/home/rioyokota/website/.mcp.json`; user scope alone cannot reach project agents/coordinator. Enabled-agent frontmatter grants labels in `mcpServers:` plus matching `mcp__<worker>__codex` and `codex-reply`; site-publisher has none. The MANDATORY per-call dispatch contract (`skills/codex-dispatch.md`) applies to every call. Generated servers pass `sandbox_workspace_write.network_access=true`.

`tools/gen-codex-mcp.py` generates the project `.mcp.json` proposal plus exact user-scope `claude mcp add-json`/rollback commands; check with `--check`. `.mcp.json` and `.claude/agents/*.md` remain hand-edit-only proposals in `tools/out/` with exact apply command. `.claude/config-edit-approved` and PreToolUse remain hard accidental-edit blocks, never authorization. `.mcp.json` is repo-only/deploy-excluded, never public.

Project MCP trust prompts once: `~/.claude.json` records `"hasTrustDialogAccepted": true` for `/home/rioyokota/website`, so later `claude` starts load silently; verify via `/mcp` or `claude mcp list`. Every delegation's final action logs date, agent, task, output file, conversationId in `tools/codex-log.md`; committed pages plus this log are durable, while `codex-reply` conversationIds optimize resumption.

## Publishing workflow

Publish only after explicit user approval. Full pipeline, pre-publish checks, and deploy/auth facts: `skills/publish-and-verify.md`.

1. **Edit:** mirrored EN/JP pages (skills/html-editing.md, skills/en-jp-parity.md); member/news rules incl. the Alumni prepend: skills/news-and-members.md; grep changed names/links site-wide.
2. **Preview:** user checks `http://localhost:8000/jp/index.html`; wait for explicit approval.
3. **Publish:** route the approved publish to `site-publisher` for its documented preflight and command.
4. **Verify:** curl changed live pages.
5. **Document:** update project instructions/skills for durable structure/convention/workflow/tooling changes and ensure GitHub reflects both the site and any required instruction update.

## Content conventions

Canonical copies live in `skills/`: html-editing (CRLF, case-insensitive tags, templates, css bump, noopener), en-jp-parity (translation, institution naming), achievements (sections sub001–sub007, newest-first, citation language, data-date/data-doi/data-url and other data-* attributes), news-and-members. Lookup/attribute progress: `tools/todo.md`.

- **Computers page:** refresh Hinadori/Computers-page facts via `site-checker` (which may run short `ybatch` probes); never guess. Current numbers: `tools/state/facts.md`.
- **Research pages:** current topics precede newest-first yearly thesis sections and matching sidebar anchors; entries use `<h4>Title（Name）</h4>`, abstract, and lightbox figure from `jp/research/images20XX/`; `en/` is English and `jp/` Japanese. Figure recipes: `skills/figures.md`.
- **Mirroring to researchmap/FIS:** explicit-only. Run `python3 tools/researchmap-export.py --check-live`, review `tools/out/researchmap-import.jsonl`, and never automate the researchmap login UI (403). Details: `skills/exporters.md`.
- **Mirroring to ORCID:** explicit-only. Run `python3 tools/orcid-export.py` (or `--dry-run`); output `tools/out/orcid-works.bib`; import manually via ORCID Add works > Import BibTeX.
- **cv.tex content sync:** automatic and bidirectional with achievements/index.html and the CV sections of jp/member/yokota.html (same edit). **CV PDF build:** `./cv/build-cv.sh` only on explicit request; it stays outside `publish.sh`.

## Deployment details

`publish.sh` calls `deploy.sh`, which mirrors the deploy-included tree to SFTP `www/` with deletion. Preview deletion-bearing deploys with `./deploy.sh --dry-run`; excluded repo/config/CV-source paths (including `skills/` and `tools/`) are defined in `deploy.sh`.

- Deployment is SFTP-only to web root `www/`; never expose credentials and never upload/deploy `.git`.

## Known issues

Live in `tools/state/facts.md` (noopener on `target="_blank"` links; Dreamweaver-era layouts — keep class/id names stable).

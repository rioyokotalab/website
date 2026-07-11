# Instructions for codex agents (YOKOTA Lab website)

You assist Claude agents maintaining a hand-built static HTML site in this
folder (no build step; served as-is). Claude delegates bounded tasks to you;
Claude retains final review, verification, and publishing.

## Hard rules
- NEVER run publish.sh, deploy.sh, lftp, ssh, or git push. Never touch
  credentials, ~/.ssh, .claude/, .mcp.json, .git/, or .dont-remove-me.
- Do not edit website files unless the task explicitly says so. Default mode:
  read, analyze, and produce output files/scripts under tools/out/ for Claude
  to review.
- Hand-edit-only config (.claude/agents/*.md, .mcp.json, AGENTS.md,
  CLAUDE.md): write full proposed copies under tools/out/ and provide an
  EXACT copy-paste apply command; never edit these in place.
- Never enter credentials anywhere; never automate login UIs (researchmap and
  OpenReview block non-browser clients).

## Skills (canonical playbooks — read before the matching work)
The repo-root `skills/` folder is the single source for recurring
procedures, shared by Claude agents and codex. When a task names a skill, or
touches its domain, READ IT FIRST:

- skills/html-editing.md — CRLF-safe editing, tags, templates, css bumps
- skills/en-jp-parity.md — mirrored trees, translation conventions
- skills/achievements.md — sections, ordering, data-* attributes
- skills/news-and-members.md — news criteria, member/alumni rules
- skills/web-lookup.md — network lookups, sources, verification gate
- skills/codex-dispatch.md — dispatch contract, output, logging (canonical)
- skills/publish-and-verify.md — publish pipeline and deploy facts (context
  only: codex never publishes)
- skills/config-proposals.md — hand-edit-only proposals, tools/out lifecycle
- skills/exporters.md — researchmap/ORCID/cv.tex operations
- skills/figures.md — figure production recipes

## Network access
Sessions run with `sandbox_workspace_write.network_access=true` (verified
codex-cli 0.144.1): you CAN fetch sources directly. Follow
skills/web-lookup.md — preferred structured sources (Crossref, DBLP,
Semantic Scholar, arXiv, J-STAGE, publisher DOI resolvers, researchmap
public read API), record a source URL per resolved fact, <=2 lookup items
per session, a DNS/HTTP failure is terminal for that provider in the
session, and factual claims destined for commit/publish require independent
verification.

## Site facts (minimum; details in skills/)
- jp/ and en/ are mirrored trees; EN/JP parity is a standing requirement.
- Page HTML is CRLF with legacy unclosed uppercase <LI>: edit scripts use
  python3 `open(path, newline='', encoding='utf-8')` for BOTH read and write
  and parse tags case-insensitively
  (`re.split(r'<li[^>]*>', text, flags=re.I)`).
- Achievements: sections sub001–sub007, newest-first; international
  citations English on both pages, domestic Japanese on both; entries carry
  data-date and other data-* attributes (skills/achievements.md).
- style.css is shared with ?v=YYYYMMDD cache busting; Templates/*.dwt must
  stay in sync with site-wide strings; new target="_blank" links need
  rel="noopener noreferrer".
- Repo map: en/ and jp/ mirrored sections (about, research, achievements,
  member, computers, teaching, picture; header: contact, links; unlinked:
  news, software); shared style.css, images/, js/; Templates/*.dwt;
  .htaccess; cv/ (cv.pdf served, sources repo-only); tools/ (scripts, state,
tools/out/ deliverables); skills/ (playbooks). tools/, skills/, .claude/,
.mcp.json, AGENTS.md, CLAUDE.md, README.md are deploy-excluded.

## Worker registry and dispatch contract
`tools/codex-workers.json` defines the five logical workers
(codex-spark-low, codex-spark-medium, codex-medium, codex-high, legacy
codex-low); `tools/task-tier-policy.md` maps task types to workers. VERIFIED
on codex-cli 0.144.1: per-call `model=<worker.model>` plus
`config={"model_reasoning_effort":<worker.effort>}` are MANDATORY on every
call (server names are routing labels only; omission runs the account
default); writes also require `sandbox: "workspace-write"` and
`cwd: "/home/rioyokota/website"`. Use exactly the dispatched worker; report
hard failures with evidence instead of changing model or effort yourself.

## Output-file-first, logging, and handoff (canonical: skills/codex-dispatch.md)
- The tools/out/ file IS the deliverable; chat replies are pointers. Append
  results immediately as resolved; for lookup/edit work run
  `tail -1 <output-file>` after each append. Keep lookup batches <=2 items.
- Every deliverable ENDS with the populated `## Structured result` block:
  status / summary / changed_files / commands / verification / evidence
  (confirmed + hypotheses) / remaining. If you append more later, repeat the
  updated block so it stays last.
- LAST action of every delegated task: append one line to tools/codex-log.md:
  `date | calling agent | task | output file | conversationId | outcome`.
- Never run two write-capable workers concurrently on one task; fan-out only
  for independent subtasks with separate output files and non-overlapping
  write scopes. Never auto-revert, overwrite, or discard partial work —
  Claude decides how to reconcile it.
- Self-load `tools/todo.md` and the task's prior tools/out/ file before
  continuing related work; do not rely on chat memory.

## Division of labor
- codex generates, analyzes, parses, looks up, drafts
  translations/content/scripts/figures, and records evidence under
  tools/out/.
- Claude reviews, decides, executes scripts, verifies, publishes, reports.
- codex never publishes, never verifies its own work, and never edits
  website pages unless the task explicitly authorizes that exact scope.

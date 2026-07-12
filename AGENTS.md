# Instructions for codex agents (YOKOTA Lab website)

Codex runs here in one of two roles. WORKER: a Claude agent dispatched you
a bounded task prompt (it names a tools/out/ output file and cites skills)
— Claude retains final review, verification, and publishing. DRIVER: the
user started codex directly with no dispatch prompt — you orchestrate, per
"Driving this repo" below. The site is hand-built static HTML (no build
step; served as-is).

## Hard rules
- Role is the security boundary. A WORKER never runs publish.sh, deploy.sh,
  lftp, ssh, or git push, regardless of its dispatch prompt. A directly
  user-started DRIVER has standing authority to run the repository publish
  pipeline and git push as the normal completion of owner-requested repository
  changes, without asking for separate permission, subject to every preflight
  and stop gate in skills/publish-and-verify.md. If role is ambiguous, act as
  WORKER. Never force-push; never read, print, copy, or modify credentials,
  ~/.ssh, or .dont-remove-me; never edit .git internals. The approved repository
  scripts may use configured authentication without Codex inspecting it. Project
  .claude/ and .mcp.json changes require explicit task scope. Drivers may run
  normal git commands; workers only when the task says so.
- Workers: do not edit website files unless the task explicitly says so —
  default mode is read, analyze, and produce output under tools/out/ for
  Claude to review. Drivers: edit per skills/ conventions (EN/JP parity,
  html-editing) and checkpoint the ledger.
- Project configuration, including .claude/agents/*.md, .mcp.json, AGENTS.md,
  and CLAUDE.md, may be edited directly only when the current task explicitly
  authorizes that exact scope. Owner-scope configuration stays proposal-only
  unless the user explicitly authorizes the exact external write.
- Never enter credentials anywhere; never automate login UIs (researchmap and
  OpenReview block non-browser clients).

## Context ledger (both roles — read first)
Cross-session memory lives on disk; protocol: skills/context-ledger.md.
tools/todo.md = task board; tools/state/session.md = in-flight handoff;
tools/state/facts.md = current facts; tools/state/decisions.md = durable
decisions. Workers: read todo.md, the task's prior tools/out/ file, and
any ledger paths the dispatch cites; NEVER edit session.md (the driver
checkpoints it). Drivers: own session.md.

## Driving this repo (codex as driver)
1. Read tools/todo.md + tools/state/session.md. If session.md holds an
   in-flight task from either driver, continue from its `Next:`; if the
   other driver updated it within ~1 hour, ask the user before taking
   over.
2. Checkpoint session.md per skills/context-ledger.md (task start, each
   completed step, before risky/long ops, session end); set driver: codex.
3. Delegate selectively through native Codex subagents according to
   `skills/codex-delegation.md`. Stay solo for small, serial, context-heavy, or
   security-sensitive work; delegate only bounded independent work when the
   expected root-context savings exceed handoff/review cost. Use minimal context
   forks and on-disk pointers, disjoint scopes, and at most two concurrent
   subagents by default. Subagents never own `session.md`, project/owner config,
   publishing, pushes, credentials, or final decisions. The DRIVER reviews and
   proportionally verifies every result before acting. Durable state remains
   ledger + `tools/out/` + commits, never chat.
4. Follow skills/publish-and-verify.md. A DRIVER normally publishes and pushes
   completed owner-requested repository changes without a separate permission
   prompt. Report the preflight scope while proceeding; stop instead of asking
   for routine approval only when a documented gate fails or the required
   action would expand the user's task scope. Project config follows the
   task-scoped direct-edit rule in skills/config-proposals.md; Claude-side hooks
   do not bind you, so self-enforce.
5. Session-end bookkeeping (commits silently with other work): update
   session.md + todo.md; write the driver session report to
   tools/out/driver-report-<YYYYMMDD-HHMM>.md per skills/context-ledger.md
   "Driver session report" (model/effort used, per-task outcomes +
   verification, escalations and network fetches, self-noted gaps); append
   ONE tools/task-metrics.jsonl line PER task attempted
   {"agent":"codex","tier":"driver-codex","model":"<model>",...} and a
   codex-log.md line `date | codex-driver (<model>) | tasks | report path
   | n/a | outcome`.

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
- skills/context-ledger.md — session/facts/decisions ledger, checkpoints,
  claude<->codex handoff (BOTH roles read this)
- skills/publish-and-verify.md — role-gated publish/push authority, preflight,
  failure stops, and deploy facts
- skills/config-proposals.md — task-scoped project config edits, owner-scope proposals, tools/out lifecycle
- skills/exporters.md — researchmap/ORCID/cv.tex operations
- skills/figures.md — figure production recipes

## Network access
Sessions run with `sandbox_mode="danger-full-access"` and approval policy
`never`: you CAN fetch sources directly without sandbox escalation. Follow
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
default); every call uses `sandbox: "danger-full-access"` and approval
policy `never`, with `cwd: "/home/rioyokota/website"`. Use exactly the
dispatched worker; report
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
- Self-load `tools/todo.md`, the task's prior tools/out/ file, and any
  cited tools/state/ paths before continuing related work; NEVER rely on
  chat memory (skills/context-ledger.md).

## Division of labor
- codex generates, analyzes, parses, looks up, drafts
  translations/content/scripts/figures, and records evidence under
  tools/out/.
- Claude reviews and publishes delegated WORKER output. A direct Codex DRIVER
  may verify and publish only through the role and preflight gates above.
- codex never edits website pages unless the task explicitly authorizes that
  exact scope.

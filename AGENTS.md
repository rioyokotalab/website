# Instructions for codex agents (YOKOTA Lab website)

You are assisting Claude agents maintaining a hand-built static HTML site in
this folder (no build step; served as-is). Claude delegates bounded tasks to
you; Claude retains final review, verification, and publishing.

## Hard rules
- NEVER run publish.sh, deploy.sh, lftp, ssh, or git push. Never touch
  credentials, ~/.ssh, .claude/, .mcp.json, .git/, or .dont-remove-me.
- Do not edit website files unless the task explicitly says so. Default mode:
  read, analyze, and produce output files/scripts for Claude to review.
- When proposing changes to any hand-edit-only config file (.claude/agents/*.md, .mcp.json, AGENTS.md, CLAUDE.md), the agent MUST give the user an EXACT copy-paste shell command (mv/apply) to move the tools/out/ proposals into place. This apply-command duty is itself documented in the config files for high visibility.
- Output convention: write results to the file path given in the task (usually
  tools/out/<task>.md). APPEND incrementally as you work, so partial progress
  survives interruption. Keep your final chat reply to a few lines: outcome +
  output file path.

## Site facts you need
- jp/ and en/ are mirrored trees: every page exists at the same path in both.
  EN/JP parity is a standing requirement.
- Page HTML has CRLF line endings and stray non-breaking spaces. Any edit
  script must use python3 with open(path, newline='', encoding='utf-8') for
  BOTH read and write to preserve CRLF byte-for-byte.
- Parse tags case-insensitively; legacy pages use unclosed uppercase <LI>.
  Split list items with re.split(r'<li[^>]*>', text, flags=re.I).
- Achievements (achievements/index.html): sections sub001–sub007, newest-first
  in each <ol>. International citations in English on BOTH language pages;
  domestic in Japanese on both. <li> tags carry data-date (YYYY-MM), and
  data-doi (bare DOI) or data-url.
- Research pages are monolingual per language (en/ all English, jp/ all
  Japanese). News items: only top-conference acceptances and grants.
- style.css is shared; pages reference it as style.css?v=YYYYMMDD.
- External target="_blank" links need rel="noopener noreferrer".

## Repo map
- index.html: root redirect to jp/ or en/ based on browser language.
- en/ and jp/: mirrored language trees. Header language toggle swaps /en/ and
  /jp/ in the URL, so missing counterparts break navigation.
- Main mirrored sections: about/, research/, achievements/, member/,
  computers/, teaching/, picture/.
- Header-bar pages: contact/ and links/.
- Existing but unlinked sections: news/ and software/.
- style.css: one shared stylesheet. Pages and templates reference it with
  ?v=YYYYMMDD cache busting; CSS edits require bumping that version everywhere.
- images/: shared images, favicon.ico, apple-touch-icon.png, and some
  section-specific image folders below language trees.
- js/: vanilla dropdown/mobile/back-to-top/language-switcher scripts.
- Templates/*.dwt: Dreamweaver templates, inert outside Dreamweaver; keep
  site-wide strings/nav/footer in sync with page copies.
- .htaccess: security headers, deployed to web root.
- cv/: cv/cv.pdf is served; cv/cv.tex, cv/cv.cls, and cv/build-cv.sh are
  repo-only sources excluded from deploy.
- tools/: repo-only scripts, state, task notes, and tools/out/ deliverables.

## CLAUDE.md conventions codex must honor
- CLAUDE.md is the authoritative convention source. Read pointed sections when
  the task touches content conventions, delegation, publishing, deployment,
  researchmap, ORCID, CV, computers, or figure tooling.
- CRLF rule: any edit script for HTML must use python3 and
  open(path, newline='', encoding='utf-8') for BOTH read and write.
- EN/JP parity: page trees mirror each other; content changes normally happen
  in both language pages together.
- Achievements sections are sub001 journal, sub002 book series, sub003 books,
  sub004 international peer-reviewed, sub005 domestic peer-reviewed, sub006
  international non-reviewed, sub007 domestic non-reviewed.
- Achievements entries are newest-first inside each <ol>.
- International Achievements citations are English on both language pages.
  Domestic citations are Japanese on both language pages.
- Achievements data-date is YYYY-MM, or YYYY-MM-DD when day is known.
  Derive journals from published date; conferences from first day of the
  conference. Resolve month from citation text, then DOI/Crossref print or
  online-first, then J-STAGE 発行日. Year-only is never allowed; if month cannot
  be confirmed, default deterministically to January of the known year.
- Achievements data-doi is a bare DOI only, with no https://doi.org/ prefix.
- Achievements data-url is used only when no DOI exists and a canonical
  same-paper URL is confirmed, such as arXiv abs, OpenReview forum, or ANLP
  anthology PDF. If title/author/year do not match, leave both attributes off.
- News items are only for top-conference acceptances and grants. Do not add
  workshop/talk/low-tier venue news unless explicitly approved.
- Research pages are monolingual: en/ all English, jp/ all Japanese. Translate
  titles and abstracts; use kanji names where known and romaji for
  international students.
- Institution naming: use 東京科学大学 総合研究院 / Institute of Science Tokyo, IIR
  for current content. Do not retroactively change historical records, old news,
  CV historical entries, or live URLs that still contain titech/gsic names.
- New target="_blank" links need rel="noopener noreferrer".
- Site-wide string changes must also update Templates/*.dwt.
- style.css edits require bumping style.css?v=YYYYMMDD in all pages and
  templates with a scripted replace.

## Deploy exclusions and safety
- NEVER upload .git to the server.
- Deploy excludes .git, .claude, tools, CLAUDE.md, .mcp.json, scripts, and CV
  source files such as cv/cv.tex, cv/cv.cls, and cv/build-cv.sh.
- publish.sh and deploy.sh are Claude/user responsibilities only. codex never
  runs them, even for dry-runs.
- lftp, ssh, and git push are forbidden to codex.
- Credentials and ~/.ssh are forbidden to codex.

## codex self-logging & output-file-first (added 2026-07-08)
- As the LAST action of every delegated task, codex must append one line to
  `tools/codex-log.md` in the format: `date | calling agent | task | output
  file | conversationId | outcome`. The calling Claude agent only relays the
  conversationId; it does not write the log (site-checker is read-only).
- The `tools/codex-log.md` line and, more importantly, the orchestrator's
  `tools/task-metrics.jsonl` line MUST record `task_type`, `tier`,
  `duration_ms`, and `success` for every codex session. Use the fixed
  task_type enum only: `mechanical-edit`, `content-draft`, `translation`,
  `metadata-lookup`, `verify-parity`, `git-summary`, `deploy-publish`,
  `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`, `other`.
- The `tools/out/` file IS the deliverable, not the chat reply. codex must
  append each result to its output file immediately as it works. The calling
  agent must confirm the output file exists and is non-empty before
  reporting PASS; chat replies are pointers, not payloads.
- Reliability rule for lookup/edit codex sessions: append each resolved result
  to the `tools/out/` file the instant it is resolved and run
  `tail -1 <output-file>` to confirm the write landed BEFORE moving on.
  Batching or end-of-run writes get lost on cutoff. Keep lookup batches to
  <=2 items.
- Shared policy: read `/home/rioyokota/website/.claude/agents/codex-offload-policy.md`
  when delegated work mentions offload-first or codex division of labor.
- Codex tiers: codex-low is available to every codex-enabled agent for
  simple/mechanical bounded work. site-checker/site-editor also keep
  codex-medium for moderate parsing/verification/edit-script drafting;
  site-author/site-coordinator/site-rescue also keep codex-high for judgment;
  site-publisher has NO codex tier in the website workflow.
- OFFLOAD BY DEFAULT, including from site-coordinator directly: any bounded
  task involving more than 2 files, more than about 100 lines, multi-page
  analysis, non-trivial drafting/translation, counting/parsing, citation
  reasoning, or edit-script generation MUST go to the cheapest capable codex
  tier first. Tier selection: codex-low is DEFAULT for simple/mechanical
  bounded work (metadata/DOI/URL lookups, Crossref/J-STAGE/arXiv resolution,
  counting, grepping/parsing, aggregating tools/out files, format/URL
  normalization, and straightforward CRLF-safe edit-script drafting);
  codex-medium is for moderate parsing/verification; codex-high is reserved
  for genuine judgment (house-style content drafting, JP<->EN translation,
  exporter/citation-parser logic, deep failure/root-cause diagnosis). Prefer
  the cheapest tier that can do the task. Reserve codex-high for judgment; do
  NOT use codex-high for lookups, counting, aggregation, or mechanical edits.
  This applies to retries too: if a first attempt is incomplete, narrow or fan
  out codex work instead of doing the bulk work in Claude context. The
  coordinator reads only the `tools/out/` deliverable plus minimal spot-checks
  and keeps its reply short.
- Dynamic-effort tier rule: a subagent MUST use exactly the codex tier the
  orchestrator specifies in its dispatch, and MUST NOT override that tier up
  or down. On hard failure at that tier, the subagent reports the failure and
  evidence back to the orchestrator so the orchestrator can decide whether to
  escalate the tier. A subagent must not silently escalate itself.
- FAN OUT codex: when work decomposes into independent bounded subtasks, the
  Claude agent SHOULD issue multiple `mcp__codex-<tier>__codex` calls in a
  SINGLE turn rather than doing them serially or spawning more Claude
  subagents. Fan out MANY parallel codex-low sessions for simple lookup,
  parse, aggregate, normalize, and mechanical edit-script work. Prefer many
  small parallel codex sessions over many Claude subagents. Each session gets
  pointers not payloads, writes its own `tools/out/` deliverable, appends
  incrementally, verifies writes with `tail -1` for lookup/edit work, and
  self-logs to `tools/codex-log.md`. Keep each codex scope small (lookup
  batches <=2 items; other bounded batches <=2-4 items).
- Claude subagent capacity is a scarce weekly-limited resource; codex capacity
  is not. Prefer bounded work via codex fan-out inside as FEW Claude subagents
  as possible, and prefer coordinator direct codex-low offload for simple
  bounded work whenever the task is codex-eligible. Use codex-high only for
  judgment-heavy work. Do NOT spawn Claude subagents in parallel; DO fan out
  codex in parallel.
- Continuously and frequently improve the configuration to offload as much work
  as possible from Claude to codex. On an ongoing basis, the coordinator should
  look for Claude-side work (reading, parsing, counting, drafting, translating,
  analysis, script-generation) that codex could do instead, and propose config
  updates (to `.claude/agents/*.md`, `AGENTS.md`, `CLAUDE.md`,
  `codex-offload-policy.md`) that push that work down to codex -- always
  delivered as `tools/out/` proposals with an exact copy-paste apply command.

## Division of labor
- codex generates, analyzes, parses, drafts translations, normalizes
  citations, reasons about exporters, and drafts scripts under tools/out/.
- site-coordinator offloads directly to the cheapest capable codex tier before
  spending main-session context on bounded reading/parsing/drafting/analysis
  tasks; use codex-low for simple lookups, counting, aggregation, parsing, and
  mechanical edit-script drafting, and reserve codex-high for judgment,
  drafting, translation, exporter/citation-parser logic, and deep diagnosis.
  Subagents remain the route for edits, independent verification, and
  publishing. For parallel bounded subtasks, prefer codex fan-out in a single
  turn over spawning more Claude subagents.
- Claude reviews, decides, executes scripts, verifies, publishes, and reports.
- codex never edits pages directly unless the task explicitly authorizes
  writing a proposed output file/script under tools/out/.
- codex never publishes and never verifies its own work.
- site-checker or the calling Claude agent performs independent verification.

## Dynamic effort and metrics
- Durable metrics store: `tools/task-metrics.jsonl` is the permanent per-task
  metrics log, one JSON object per line with keys:
  `{"date","task_type","agent","tier","duration_ms","success","note"}`.
  The orchestrator writes the task-metrics line for each dispatched task and
  uses it to tune future tier selection.
- Durable tier policy: `tools/task-tier-policy.md` maps each `task_type` to
  its default tier, rolling median duration, and success rate. Orchestrators
  and codex-enabled agents should consult this file before choosing or
  dispatching a tier, unless the caller explicitly specifies the tier.
- Codex sessions and codex-enabled agents should self-load
  `tools/task-metrics.jsonl`, `tools/task-tier-policy.md`, and
  `tools/todo.md` as durable context for ongoing work
  when relevant to the delegated task.
- Fixed task_type enum: `mechanical-edit`, `content-draft`, `translation`,
  `metadata-lookup`, `verify-parity`, `git-summary`, `deploy-publish`,
  `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`, `other`.

## Persistent task pointers
- Metadata progress tracker: tools/todo.md.
- Active or recent tools/out/ task files:
  - tools/out/doi-sub001.md
  - tools/out/doi-sub002-003.md
  - tools/out/doi-sub005.md
  - tools/out/date-batch2.md
  - tools/out/data-date-exporter-spec.md
  - tools/out/achievements-parity.md
  - tools/out/jp-mobile-contact-fix.py
  - tools/out/jp-mobile-contact-scope.md
- When continuing a task, read the relevant output file and append new results
  immediately; do not rely on chat memory.

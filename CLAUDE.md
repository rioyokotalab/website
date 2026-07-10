# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp -- a hand-built static HTML site
(originally Adobe Dreamweaver). No build step or framework: files are served
exactly as stored, and URL structure mirrors the folder tree one-to-one.

## Standing directive: codex offload and config edits

- OFFLOAD BY DEFAULT. Agents, including `site-coordinator`, must send bounded
  reading, parsing, counting, aggregation, drafting, translation, citation
  reasoning, and script-generation work to the cheapest capable codex tier
  before spending main-session context. Mandatory triggers: more than 2 files,
  more than about 100 lines, multi-page analysis, non-trivial drafting or
  translation, counting/parsing, citation reasoning, or edit-script generation.
- Collaboration pattern (2026-07-08): pass pointers, not payloads: task, acceptance check, file paths, and a
  `tools/out/` output path. codex has repo file access and reads root
  `AGENTS.md` (deploy-excluded). Claude reads only the `tools/out/`
  deliverable plus minimal spot-checks and keeps replies short.
- Seed tier defaults, overridden by the dynamic metrics policy below:
  `codex-low` for simple/mechanical bounded work (metadata/DOI/URL lookups,
  Crossref/J-STAGE/arXiv resolution, counting, grepping/parsing, aggregating
  `tools/out` files, format/URL normalization, straightforward CRLF-safe
  edit-script drafting); `codex-medium` for moderate parsing/verification;
  `codex-high` for genuine judgment (house-style content drafting, JP<->EN
  translation, exporter/citation-parser logic, deep failure/root-cause
  diagnosis). Use the cheapest tier that can succeed; do NOT use `codex-high`
  for lookups, counting, aggregation, or mechanical edits. Retries should be
  smaller or fanned out, not moved back into Claude context.
- FAN OUT codex when independent bounded subtasks exist: issue multiple
  `mcp__codex-<tier>__codex` calls in a SINGLE turn. Prefer many small
  parallel `codex-low` sessions over serial work or Claude subagent budget for
  lookup, parse, aggregate, normalize, and mechanical edit-script work. No
  parallel Claude subagents.
- Every codex session writes its own `tools/out/` deliverable, appends
  incrementally, and self-logs as its last action to `tools/codex-log.md`. For
  lookup/edit codex sessions, append each resolved result immediately and run
  `tail -1 <output-file>` before moving on; batching or end-of-run writes get
  lost on cutoff, so lookup batches stay <=2 items.
- `tools/out/` lifecycle: classify files as TRANSIENT SCRATCH (lookup notes,
  parse/apply helper scripts, investigation/parity notes, batch working files)
  or PENDING DELIVERABLES (files awaiting user action, including
  export/import payloads the user uploads such as `researchmap-import.jsonl`
  or `orcid-works.bib`, and hand-edit-only config proposals such as
  `tools/out/CLAUDE.md`, `tools/out/AGENTS.md`, `.claude/agents/*.md`, and
  `apply-*.sh`). Once a task is fully VERIFIED and its result is committed to
  the pages, or the exporter can regenerate it, the coordinator deletes that
  task's TRANSIENT SCRATCH files in the SAME turn with `rm` of specific files,
  never a blind wipe. PENDING DELIVERABLES stay until the user confirms the
  upload/apply is done, then are removed. `tools/codex-log.md` plus committed
  pages are the durable audit trail, so deleting scratch does not lose
  provenance.
- Division of labor: codex generates drafts, translations, analysis, edit
  scripts, and lookup results; Claude reviews, executes, and verifies. codex
  never edits pages directly, never publishes, and never verifies its own work
  (site-checker remains the independent verifier).
- Proposed config/context rewrites go under `tools/out/` with the SAME filename
  the user can move into place manually, e.g. `tools/out/site-editor.md` or
  `tools/out/AGENTS.md`. `.claude/agents/*.md`, `.mcp.json`, `AGENTS.md`, and
  `CLAUDE.md` are hand-edit-only; subagents refuse direct edits. When proposing
  changes to any hand-edit-only config file (`.claude/agents/*.md`, `.mcp.json`,
  `AGENTS.md`, `CLAUDE.md`), give the user an EXACT copy-paste shell command
  (`mv`/apply) to move the `tools/out/` proposal into place.
- Continuously improve configuration to offload more Claude-side work to codex.
  Propose updates to `.claude/agents/*.md`, `AGENTS.md`, `CLAUDE.md`, and
  `codex-offload-policy.md` as `tools/out/` proposals with exact apply
  commands.

## Dynamic codex effort selection and task metrics

- Codex-using site agents `site-checker`, `site-editor`, `site-author`,
  `site-coordinator`, and `site-rescue` have all three tiers: `codex-low`,
  `codex-medium`, `codex-high`. `site-publisher` has NO codex tier in the
  website workflow. `.mcp.json` already registers all three servers
  (`model_reasoning_effort` low, medium, high).
- The orchestrator (`site-coordinator` / main session) chooses `low`, `medium`,
  or `high` per dispatched task from task type plus metrics-derived policy, and
  states the tier explicitly. Subagents MUST use exactly that tier and MUST NOT
  change it up or down; on hard failure they report back. The orchestrator may
  escalate `low` -> `medium` -> `high`, then the Claude-side ladder `Opus` ->
  `Fable` for persistent Claude-side bugs.
- Permanent metrics store: `tools/task-metrics.jsonl`, repo-tracked, one JSON
  object per line:
  `{"date":"YYYY-MM-DD","task_type":"<enum>","agent":"<agent>","tier":"low|medium|high","duration_ms":<int>,"success":true|false,"note":"<short>"}`.
  The orchestrator appends one line after each task; `duration_ms` and token
  counts come from the subagent task-notification.
- Policy file: `tools/task-tier-policy.md` maps `task_type` to recommended
  default tier, rolling median `duration_ms`, and success rate. The orchestrator
  reads it before choosing a tier, prefers the LOWEST tier meeting the success
  bar while minimizing completion time, and periodically updates it from
  `tools/task-metrics.jsonl`.
- Task-type enum: `mechanical-edit`, `content-draft`, `translation`,
  `metadata-lookup`, `verify-parity`, `git-summary`, `deploy-publish`,
  `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`, `other`.
- Seed policy before data: `mechanical-edit=low`, `metadata-lookup=low`,
  `verify-parity=low`, `git-summary=low`, `deploy-publish=low`,
  `content-draft=high`, `translation=high`, `exporter-logic=high`,
  `diagnosis=high`, `figure-production=high`, `config-edit=high`,
  `other=medium`. Older fixed tier maps are seed defaults only.

## Budget rule:

- No agent for explanation-only answers.
- No Fable/Opus in normal website workflow except debugging escalation: if a
  bug persists after Sonnet-tier attempts, escalate to Opus; if Opus also
  cannot fix it, escalate to Fable.
- Claude subagent capacity is scarce weekly-limited capacity; codex capacity is
  not. Prefer bounded work via codex fan-out inside as few Claude subagents as
  possible. Coordinator should offload directly to `codex-low` for simple
  bounded codex-eligible work and reserve `codex-high` for judgment-heavy work,
  subject to dynamic per-task selection.
- No parallel Claude subagents. No nested subagents. No broad "check
  everything" unless requested.
- Checker returns summaries, not raw outputs. Editor receives exact edits, not
  goals. Author returns final content plus edit specs, not file modifications.
  Publisher runs one documented publish command after explicit approval.

## Structure

- `index.html` -- root page; redirects only to `jp/` or `en/` based on browser
  language.
- `en/` and `jp/` are mirrored language trees. Every page must exist at the
  same path in both because the JAPANESE/ENGLISH header toggle
  (`js/chglang.js`) swaps `/jp/` <-> `/en/` in the URL. Creating or moving a
  page in one language without the counterpart breaks the toggle with a 404.
- Sections: `about`, `research`, `achievements`, `member`, `computers`,
  `teaching`, `picture` (top nav), plus `contact`, `links` (header bar).
  `news` and `software` exist but are unlinked from navigation.
- `style.css` is the single site-wide stylesheet. Pages reference
  `style.css?v=YYYYMMDD`; CSS edits require bumping that version in ALL pages
  and templates with a scripted replace or browsers serve stale CSS.
- `images/` holds shared images; section-specific photos live in paths such as
  `en/member/images/`. `favicon.ico` and `apple-touch-icon.png` live in
  `images/` (moved from repo root 2026-07-08); every page/template references
  them as `images/…` at the correct relative depth.
- `js/` holds dropdown menu, mobile menu, back-to-top, and language switcher
  vanilla JS. There is no local jQuery; gallery pages use only the SRI-pinned
  CDN copy.
- Galleries (research figures, picture page, computers photos) use lightbox2
  2.11 + jQuery 3.7 from cdnjs with SRI hashes pinned in each page head. There
  is no local copy; recompute `integrity` hashes when bumping versions.
- `.htaccess` sets security headers (`nosniff`, `SAMEORIGIN`, referrer policy);
  it is deployed to web root and honored by the server.
- `Templates/*.dwt` are Dreamweaver templates, inert outside Dreamweaver. Every
  HTML page carries its own full header/nav/footer copy. Site-wide changes
  (e.g. nav menu) must be edited in every page, usually by find-and-replace,
  and in templates too.
- `.dont-remove-me` is a hosting marker file; keep it, deploy it, never delete
  it.

## Delegation to subagents (save rate limit)

Six project agents exist in `.claude/agents/`; `.claude/` is gitignored EXCEPT
for a `!.claude/agents` un-ignore rule in `.gitignore`, so agent definitions
ARE tracked while the rest of `.claude/` stays local-only. Route work DOWN to
the cheapest capable agent by default; keep the main session for orchestration,
user-facing decisions, escalation, and final review.

- **site-checker** (Sonnet, read-only): verification/searching, site-wide
  grepping/counting, EN/JP parity, curl checks of localhost:8000 and live site
  (workflow steps 2 and 4), git status summaries, and `sinfo`/`yrun` cluster
  queries.
- **site-editor** (Sonnet): fully specified edits (workflow step 1). Give exact
  strings/entries, target files, insertion points; it knows CRLF/python3/both
  language rules. Publishing is site-publisher's job.
- **site-author** (Opus): judgment work that does not need the main session:
  news/achievements/research content in house style, jp<->en translation,
  researchmap exporter changes, figure production, failure diagnosis. It reads
  this file first.
- **site-publisher** (Haiku): runs `publish.sh` only after explicit user
  approval in the current conversation (workflow step 3); stops and reports on
  ssh/publish failures rather than touching credentials.
- **site-coordinator** (Opus): main orchestration; routes each task to the
  cheapest capable agent, keeps user-facing decisions, escalation, and final
  review. Escalation exception: if a bug persists after Sonnet-tier attempts,
  escalate to Opus, then Fable.
- **site-rescue** (Opus, manual-only): deep root-cause diagnosis for tangled or
  cross-cutting failures; launched explicitly by the user in a separate
  session, read-only unless told otherwise.

Subagents do NOT share conversation state, so every dispatch must be
self-contained: exact content, file paths, and acceptance check. Typical flow:
main decides change -> site-editor/site-author makes it -> site-checker verifies
independently -> user previews -> site-publisher publishes -> site-checker
confirms live. Escalate up a tier when ambiguity/failure is reported; only
credentials/ssh recovery and user decisions stay in the main session.

**Failure-driven workflow updates (standing rule):** every subagent failure,
incomplete result, or mistaken result must change the workflow so it cannot
recur; record the fix here.

- A follow-up `Agent` call does NOT resume a previous agent; it spawns a fresh
  instance with no memory (no SendMessage tool in website session). Every
  dispatch and retry must re-supply ALL context, e.g. full index->citation
  mapping for date lookup; never say "the list from before". (Learned 2026-07-08,
  sub001 `data-date` pilot.)
- Research/lookup subagents decline to curl external hosts unless explicitly
  authorized. Metadata-lookup prompts must name allowed hosts up front:
  Crossref `api.crossref.org`, DBLP, Semantic Scholar, J-STAGE
  `api.jstage.jst.go.jp`, publisher DOI resolvers; note OpenReview and the
  researchmap login block non-browser clients. (Learned 2026-07-08.)
- A subagent can finish with an EMPTY final message. For any output that
  matters, instruct it to WRITE results under `tools/out/` as it works AND
  print them as final message so the main session can `Read` that file to recover the result.
  Especially important for long research/lookup dispatches. (Learned 2026-07-08.)
- Writing only at the end does not survive mid-run cutoff; lookup agents stop
  after ~15-20 tool calls with a truncated final line and no file. Fix:
  append each result immediately after resolving that item and keep lookup
  dispatches small (<=3-4 entries) so they finish. (Learned 2026-07-08.)

**codex MCP backend for site-agents:** site-agents and site-coordinator can
delegate to codex MCP servers. `codex-{high,medium,low}` must be registered at
BOTH user scope (`~/.claude.json`) AND project scope
(`/home/rioyokota/website/.mcp.json`); user scope alone does NOT reach project
agents or project-scoped coordinator tools (confirmed 2026-07-08 when an actual
`mcp__codex-medium__codex` call from site-checker returned only after
`.mcp.json` was added). Each codex-enabled agent frontmatter lists all three
tiers under `mcpServers:` and includes `mcp__codex-<tier>__codex` and
`codex-reply`. Earlier fixed pairings remain seed defaults for dynamic
selection: site-author/site-coordinator/site-rescue ->
codex-low+codex-high; site-checker/site-editor -> codex-low+codex-medium;
site-publisher has no codex tier. On startup Claude prompts to approve project
MCP servers. Editing `.claude/agents/*.md` or `.mcp.json` must be BY HAND:
subagents categorically refuse config edits regardless of
`.claude/config-edit-approved` marker/PreToolUse hook (site-editor refused
twice, 2026-07-08); marker+hook remain a hard block against accidental config
edits, not an authorization channel. `.mcp.json` is repo-only and excluded from
deploy (`deploy.sh` `-x '^\.mcp\.json$'`), so it is never public. Every
delegation logs one line in `tools/codex-log.md` (date, agent, task, output
file, conversationId); `tools/codex-log.md` plus committed pages are durable
cross-session memory, while conversationIds resumable via `codex-reply` are an
optimization. Escalation ladder for stuck tasks: Sonnet -> codex-medium/high
-> Opus -> Fable.

## Publishing workflow

> **NON-NEGOTIABLE RULE -- after EVERY `publish.sh` run, in the same turn:**
> (1) update CLAUDE.md if anything documentable changed, and (2) `git add -A
> && git commit && git push` so BOTH the website change and CLAUDE.md reach
> GitHub. A publish is not complete until GitHub reflects it. `publish.sh`
> already commits+pushes the website change; if that push fails (e.g. GitHub
> key not in the ssh-agent), the publish is UNFINISHED -- surface it to the
> user and resolve before moving on. A PostToolUse hook in
> `.claude/settings.local.json` prints a reminder after every publish.

Standard cycle for every content change (first exercised end-to-end on
2026-07-04, removing a member from the member page):

**Standing workflow rules:**

- Always: preview at `http://localhost:8000/jp/index.html` before publishing;
  update CLAUDE.md immediately after publishing if anything documentable
  changed; commit and push CLAUDE.md to GitHub immediately after updating it.
- Only when explicitly asked: mirror website EN/JP pages to ResearchMap; mirror
  website into `cv/cv.tex`, compile `cv/cv.pdf`, and publish.

1. **Edit** -- make the change and update both `jp/` and `en/` counterparts.
   When Claude edits, grep for other occurrences of changed content (names,
   links) site-wide. When asked to remove someone from member list, also add
   them to the TOP of Alumni on both member pages (jp form: `姓 名 (Romaji Name)`).
   Historical records (news, publication lists) are never edited when
   members leave or change grade.
2. **Preview** -- user checks `http://localhost:8000/jp/index.html`.
   `.claude/settings.local.json` SessionStart/SessionEnd hook starts/stops
   `python3 -m http.server 8000` automatically (PID `.claude/http-server.pid`);
   if down mid-session, start it the same way. Wait
   for user OK before publishing.
3. **Publish** -- `./publish.sh "what changed"`. It shows pending git changes
   and upload list, asks one y/N confirmation, deploys, commits, and pushes.
   When Claude runs it after OK, pipe confirmation:
   `echo y | ./publish.sh "message"`. This no longer triggers ResearchMap
   export automatically. FIRST check `git status` because `git add -A` sweeps
   unrelated pending changes; if any exist, mention them and use a commit
   message covering everything. (Learned 2026-07-06, leftover CSS rode along.)
   Debugging artifacts in repo (e.g. iPhone screenshots `IMG_*.PNG`) get swept
   in AND deployed to public web root; delete them before publishing or remove
   them later from server with `lftp`.
4. **Verify** -- after publishing, curl changed pages on
   https://www.rio.scrc.iir.isct.ac.jp and confirm live.
5. **Document** -- if structure, conventions, workflow, or tooling changed,
   update CLAUDE.md in the same turn and commit/push it. PostToolUse in
   `.claude/settings.local.json` reminds after every `publish.sh`.

## Content conventions

- **File quirks**: HTML files have CRLF line endings and occasional
  non-breaking spaces. Edit with small `python3` scripts using
  `open(path, newline='')` to preserve CRLF; use `newline=''` for read and
  write. Parse tags case-insensitively and do NOT assume closing tags: legacy
  sections used unclosed uppercase `<LI>`, and one such block hid duplicated
  entries on `jp` achievements until 2026-07-06.
- **Institution naming** (renamed 2024): 東京科学大学 総合研究院 / Institute of
  Science Tokyo, IIR. Old names (東京工業大学, Tokyo Tech, 学術国際情報センター,
  GSIC) were replaced site-wide on 2026-07-05 EXCEPT historical records -- CV
  on `member/yokota.html`, old news items -- and live URLs
  (`t4.gsic.titech.ac.jp`, SuperCon links).
- **Achievements** (`achievements/index.html`): sections `sub001`-`sub007`
  map to journal / book series / books / international peer-reviewed /
  domestic peer-reviewed / international non-reviewed / domestic non-reviewed.
  Entries are newest-first inside each `<ol>`. International citations are
  English on BOTH language pages; domestic citations are Japanese on both.
- **Achievements `data-date` (ResearchMap metadata):** every Achievements
  `<li>` carries invisible `data-date` on the opening `<li>`; rendered page
  unchanged. Format `YYYY-MM` or `YYYY-MM-DD` when day known. Derivation for
  all entries and new entries lacking dates: (1) journals -> published date;
  conferences -> first conference day; otherwise ask user. (2) Month priority:
  citation text, else DOI/Crossref confirmed month (print, else online-first),
  else J-STAGE 発行日. (3) YEAR-ONLY IS NEVER ALLOWED; if month cannot be
  confirmed, default deterministically to January (`-01`) of known year.
  Exporter should prefer `data-date` over heuristic parsing when present.
  Progress is tracked in `tools/researchmap-metadata-todo.md` (persistent,
  repo-only); read/update it each step. Field 1 complete across sub001-sub007
  as of 2026-07-08 (pilot sub001, 2026-07-08; sub001 42, sub004 115, sub005
  32, sub006 45, sub007 62, sub002/sub003 4, all en+jp). Remaining Field-1
  task: update exporter to prefer `data-date`.
- **Achievements `data-doi` / `data-url` (Field 2, ResearchMap identifier):**
  each `<li>` may carry invisible `data-doi` (BARE DOI, e.g. `10.1234/...`,
  no `https://doi.org/`) OR, if no DOI, `data-url` for the SAME paper:
  arXiv abs page, OpenReview forum, or 言語処理学会/ANLP anthology PDF.
  Derivation priority: (1) DOI via Crossref/J-STAGE matching title+author+year;
  (2) confirmed same-paper URL (arXiv/OpenReview/anthology); (3) leave BOTH
  blank. Be conservative: differing title means blank. Lookups run in small
  (<=4-6) site-author batches, authorized hosts Crossref/DBLP/Semantic
  Scholar/J-STAGE/arXiv (+anlp.jp for ANLP), appending each result immediately
  to `tools/out/doi-subNNN.md`. Future Field-2 exporter maps `data-doi` -> DOI
  identifier and `data-url` -> `see_also`. Progress (2026-07-09) in
  `tools/researchmap-metadata-todo.md`: sub001 (37 doi + 2 url), sub002 (0),
  sub003 (2 doi), sub004 (48 doi + 25 url; 42 blank posters/talks), sub005
  (4 doi + 5 url) done; sub006/sub007 plus exporter update remain. For 7
  sub004 entries with website title differing from published title, the
  PUBLISHED title was mirrored onto website en+jp on 2026-07-09, e.g. Aurora-M,
  Formula-Supervised, RePOSE, BiCGStab, N-Body Problems with Boundary
  Distributions, Task Parallel Implementation, k-th Eigenvalue.
- **News**: only top-conference acceptances (ICLR/NeurIPS/CVPR/AAAI level) and
  grants get news items, not workshops, GTC talks, or LREC-tier venues. Each
  item appears in four places: dated row in News table on both top pages
  (`en/index.html`, `jp/index.html`) linking to `news/index.html#evYYMMDD`,
  and full anchored entry on both news pages. Dates are announcement dates;
  member grades are as of that date, e.g. "(2nd year PhD)"/"(D2)".
- **Computers page**: Hinadori section is generated from live cluster data;
  this machine IS the Hinadori login node. `sinfo`/`slurm.conf` give node
  layout, `yrun` (no args) lists resources with GPU models, and short `ybatch`
  jobs (`#YBATCH -r <resource>`; output to `$HOME`, not `/tmp` because `/tmp`
  is node-local) give exact CPU/GPU models. Direct `srun` is blocked. Last
  refreshed 2026-07-05: 81 GPUs. 2-GPU RTX 6000 Ada CPU (AMD EPYC 9654) was
  supplied by user; 8-GPU RTX 6000 Ada CPU is unknown ("-" in table, node down).
- **Research page** (`research/index.html`): "Current Research Topics YYYY"
  first (anchor `rYYYY`), then per-year thesis sections newest-first (anchors
  `rYYYYM`/`rYYYYB`), mirrored in sidebar. Entry format: `<h4>Title（Name）
  </h4>` + abstract `<p>` + lightbox figure. Figures for BOTH language pages
  live in `jp/research/images20XX/NNN.jpg` (numbering continues within folder).
  Unlike Achievements, Research pages are monolingual since 2026-07-05:
  English only on `en/`, Japanese only on `jp/`; translate titles/abstracts;
  use kanji names where known (check member/alumni), romaji for international
  students.
- Site-wide strings must also update `Templates/*.dwt`.
- **Mirroring to researchmap/FIS**: `researchmap-export.py` no longer runs from
  `publish.sh`. Run only on explicit sync request:
  `python3 tools/researchmap-export.py --check-live`. It fetches public API
  `https://api.researchmap.jp/rioyokota/{published_papers,books_etc,presentations,misc}`
  and diffs against ALL current Yokota-authored Achievements entries, not only
  local-state additions, because `tools/researchmap-state.json` can drift from
  live (generated but never uploaded, or partially uploaded). It writes missing
  entries to `tools/out/researchmap-import.jsonl`.
  Category mapping (agreed 2026-07-06): peer-reviewed sections
  (sub001/004/005) -> Papers; Book series + Books (sub002/003) -> Books and
  Other Publications; non-peer-reviewed sections (sub006/007) ->
  Presentations when Rio Yokota is SOLE author (invited talks), Misc otherwise.
  Bulk-import grammar supports insert, `update` (+`doc`), and `delete` by
  `rm:id` from public read API; this built the 2026-07-06 recategorization
  migration. Insert/update lines must NOT carry `user_id`: in self-import the
  logged-in account is implied, and `user_id` (even own permalink) means
  "another member's list", fails 403, and blocks the ENTIRE file because
  researchmap validates all lines before applying any. Learned 2026-07-06.
  Verified 2026-07-08 exact UPDATE grammar against researchmap V2 API spec
  (`researchmap-export.py` has NO update path; update/delete hand-built): one
  JSON object per line,
  `{"update": {"type": "<record-type>", "id": "<rm:id>"}, "doc": {<only the changed fields>}}`;
  partial update leaves unlisted fields untouched and carries NO `user_id`.
  `rm:id`s come from public read API, e.g.
  `https://api.researchmap.jp/rioyokota/published_papers?limit=1000`. Example
  used 2026-07-08 for ANLP2025 title:
  `{"update": {"type": "published_papers", "id": "50836989"}, "doc": {"paper_title": {"ja": "..."}}}`.
  ORCID has no such update path: a no-DOI title change adds a new BibTeX work
  on re-import, so stale old-title work must be removed manually in ORCID UI.
  User downloads
  `http://localhost:8000/tools/out/researchmap-import.jsonl` and uploads at
  researchmap 設定 > インポート (permalink: rioyokota); university FIS syncs
  from researchmap automatically. Review printed NEW lines before upload.
  Do NOT script researchmap website: login blocks non-browser clients (403).
  Sanctioned automation is WebAPI; automatic push awaits JST API key (as of
  2026-07-06 user is asking URA office). Public READ needs no key:
  `https://api.researchmap.jp/rioyokota/{type}` (JSON).
  Import error granularity (learned 2026-07-07): `user_id` on any insert line
  403s and blocks the ENTIRE file; per-entry validation errors (e.g.
  `published_papers` missing `publication_date`) return 400 for THAT line only
  while others import. researchmap emails/serves
  `errors_researchmap-import-N.csv` with failing line number, field, message.
  When one row fails, do NOT re-upload whole file; extract corrected failing
  line into a tiny one-line jsonl. Public READ API lags behind imports, so
  `--check-live` will NOT immediately dedupe just-imported entries.
  `published_papers` entries REQUIRE `publication_date` (出版年月); trailing-note
  dates can fail 400 until fixed. Parser hardened 2026-07-07 for author lists
  separated by either 、 or ASCII commas, "LastAuthor. Title" boundary
  (period+space after last author, preserving initials like "David E. Keyes"),
  and trailing parenthetical after date ("Dec. 2022. (Best paper)",
  "(学生奨励賞)") by extracting date and dropping note from `publication_name`.
  Still heuristic: review output.
- **Mirroring to ORCID / ORCID BibTeX export**: `tools/orcid-export.py` mirrors
  website Achievements publications where Rio Yokota is an author to ORCID
  https://orcid.org/0000-0001-7573-7873. ORCID has no researchmap-style JSON
  bulk-import API; sanctioned no-API route is ORCID > Add works > Import BibTeX
  (BibTeXImportWizard). Exporter parses `en/achievements/index.html`, reuses
  `researchmap-export.py` hardened citation parser via importlib (hyphenated
  filename), and writes complete Yokota-authored set to
  `tools/out/orcid-works.bib`, served at
  `http://localhost:8000/tools/out/orcid-works.bib`. Usage:
  `python3 tools/orcid-export.py`; dry run: `tools/orcid-export.py --dry-run`
  prints counts + risky parses, no file. Section -> BibTeX mapping: sub001 ->
  `@article`; sub002 -> `@incollection`; sub003 -> `@book`; sub004/sub005 ->
  `@inproceedings`; sub006/sub007 -> `@misc`. ORCID public API is read-only
  without OAuth, so no live diff; re-import is non-destructive because ORCID
  groups/merges by identifier/title. First run 2026-07-07: 284 entries. Future
  OAuth/member-API or 3-legged OAuth token auto-diff push is possible but not
  built. Same on-demand pattern as researchmap export and CV build; kept OUT of
  `publish.sh`. Review risky parses; parser is only as good as source
  citations. Three malformed achievements entries (colon-separated author,
  全角 ．/「」 delimiters) were normalized in achievements pages 2026-07-07; prefer
  fixing source citation over patching `.bib`. User downloads
  `tools/out/orcid-works.bib` and imports via ORCID Add works > Import BibTeX.
- **cv.tex sync**: `cv/cv.tex` must stay in sync with website both directions.
  Whenever `achievements/index.html` or CV sections of `jp/member/yokota.html`
  (受賞歴/委員歴/研究課題) change, update matching section of `cv/cv.tex` in same
  edit; if `cv/cv.tex` is source of a new item, add it to website pages too.
- **CV PDF build**: `cv/cv.tex` plus custom `cv/cv.cls` in `cv/` compiles to
  `cv/cv.pdf` via `cv/build-cv.sh`, which runs XeTeX-based `tectonic`
  installed at `~/.local/bin/tectonic`. `cv/cv.tex` preamble MUST keep
  `\usepackage{xeCJK}` + `\setCJKmainfont{Noto Sans CJK JP}` because the CV
  contains Japanese names/titles; Noto CJK font is in `~/.local/share/fonts`;
  without it XeTeX silently drops kanji. Run `./cv/build-cv.sh` on demand
  whenever `cv/cv.tex` changes (kept OUT of `publish.sh`); normal `publish.sh`
  then deploys regenerated `cv/cv.pdf`. Single English+Japanese `cv/cv.pdf`
  lives in `cv/` and is linked from BOTH `en/member/yokota.html` and
  `jp/member/yokota.html` as `../../cv/cv.pdf` (`target=_blank`,
  `rel=noopener`). `cv/cv.tex`, `cv/cv.cls`, `cv/build-cv.sh` are repo-only and
  excluded from deploy in `deploy.sh`; only `cv/cv.pdf` is served.
- **CV items on personal page** are mirrored to researchmap. Canonical source:
  `jp/member/yokota.html` sections 受賞歴 / 委員歴 / 研究課題; `en` page mirrors
  Awards / Committee Memberships / Research Projects but is NOT parsed. Exporter
  line formats (em-dash separators, 全角 space after dates):
  `2009年11月　AWARD_NAME` / `2024–2025　ROLE — ASSOCIATION` /
  `2025–2028　TITLE（FUNDING SYSTEM、FUNDER）`. Add items to BOTH language pages
  in that format; run on-demand export. Initial content imported FROM
  researchmap on 2026-07-06, so page contents as of then are baseline.

## Content sources and figure tooling

- **Lab Google Drive**: read-only via rclone:
  `~/.local/bin/rclone lsf --drive-root-folder-id 1MRyEsesRkuZ_eGtUgnPgC9k3rXuo_BLa gdrive:<path>`.
  Layout: `Thesis/YYYY/{master,bachelor}/` (thesis PDFs for Research entries),
  `Posters/YYYY/` (研究室紹介 lab-intro poster; `.pages` files are zip archives
  containing `preview.jpg` and original images under `Data/`),
  `Slides/YYYY発表.../` (defense slides). OAuth token is Drive-read-only and
  revocable at myaccount.google.com/permissions.
- **Swallow material**: https://swallow-llm.github.io/ (`.ja.html` and
  `.en.html` release pages). Charts are ApexCharts SVGs whose legends are NOT
  in SVG; series names are in `seriesName` attributes and colors follow palette
  `#008FFB`, `#00E396`, `#FEB019`, `#FF4560`, `#775DD0` in series order.
  Rebuild legend with PIL when rasterizing.
- **Figure production**: thesis-PDF figures via
  `pdftoppm -jpeg -r 150 -f N -l N` + PIL crop (trim captions; flatten
  transparency onto white). SVG->PNG needs cairosvg in a venv
  (`python3 -m venv`; system pip is PEP-668-locked) and Japanese fonts. Noto
  Sans CJK JP installed in `~/.local/share/fonts` (2026-07-05); patch SVG
  `font-family` to "Noto Sans CJK JP" before converting because cairo does no
  font fallback.

## Deployment details

`publish.sh` calls `./deploy.sh` (preview `./deploy.sh --dry-run`). It mirrors
this folder to `www/` on server via lftp/SFTP, uploading only new/changed files.
It uses `mirror -R --delete`, so local removals are removed remotely next deploy;
server stays exact mirror of deployed set, no more manual `lftp rm`. Excluded
paths (`-x` list: `.git`, `.claude`, `tools`, scripts, `CLAUDE.md`, source
files `cv/cv.tex`/`cv/cv.cls`/`cv/build-cv.sh`, etc.) are never uploaded and
never deleted remotely. Verified 2026-07-08 live mirror had zero remote-only
orphans. Because `--delete` is destructive, always preview with
`./deploy.sh --dry-run` when deploy includes deletions.

- Server: `gsic0017@web-o3.noc.titech.ac.jp`, SFTP only (no shell), web root
  `www/`.
- Auth: password-only via `web` alias in `~/.ssh/config`, multiplexed over
  ControlMaster (`ControlPersist yes`, lives until reboot). If master is down,
  `deploy.sh` re-establishes automatically: password stored in
  `~/.ssh/web-password` (chmod 600, user-created, NEVER printed or read into
  conversation) and supplied by `~/.ssh/web-askpass` via
  `SSH_ASKPASS_REQUIRE=force`.
- If password file missing, ask user to run `ssh -fN web` in separate terminal;
  never ask for password in chat. `!` commands in Claude Code have no tty, so
  interactive password entry does not work there.
- Key-based auth impossible: chrooted SFTP home is root-owned, so no
  `~/.ssh/authorized_keys` can be created on server.
- NEVER upload `.git` to server. Its public copy was removed on 2026-07-04
  after being found downloadable over HTTPS; `deploy.sh` excludes it.
- If `git push` fails with "Permission denied (publickey)", ssh-agent lacks
  passphrase-protected GitHub key `~/.ssh/id_ed25519`. Standard fix: persistent
  agent at fixed socket `~/.ssh/agent.sock`; user runs
  `sh ~/scripts/ssh-agent-setup.sh` once per reboot in real tmux pane (e.g.
  new window via `Ctrl-b c`) to start agent and load key (passphrase once).
  Shells auto-point via `# yokota-ssh-agent` block in user's rc. From any
  session, including Claude's non-login Bash which does NOT source rc, push
  deterministically with `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git push`; no
  hunting `/tmp/ssh-*` sockets. Helper `ssh-agent-setup.sh` (repo-external,
  `~/scripts`) is idempotent and safe to rerun. (Standardized 2026-07-08 after
  repeated ssh-add failures under tmux/remote-control.)

## Known issues (as of 2026-07)

- Fixed 2026-07-05: broken http:// jQuery now loads locally from `js/`, dead
  Google Analytics snippet and IE8 shims removed from every page, and
  `style.css` modernized with same selectors and refreshed look.
- Fixed 2026-07-07: two mobile layout bugs found via iPhone screenshots:
  hamburger menu opened white-on-white because floated 50%-width `li`s
  collapsed `ul#topnav` to zero height (fix: `overflow: hidden` clearfix on
  mobile menu rules); top pages' `.slogan` overlay (absolute inline
  `width:500px`) overflowed shrunken banner and covered header (fix:
  `position: static; width: auto !important` on mobile). Literal
  `background: #002855` fallbacks now precede `var(--navy)` in nav rules.
- External links carry `rel="noopener noreferrer"`; keep that on new
  `target="_blank"` links.
- Page HTML remains Dreamweaver-era (floats, table layouts); `style.css` is
  written against existing selectors, so keep class/id names stable when
  editing pages.

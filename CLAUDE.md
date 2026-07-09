# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp — a hand-built static HTML site
(originally made with Adobe Dreamweaver). No build step, no framework: files are
served exactly as they are here, and the URL structure mirrors the folder
structure one-to-one.

## Standing directive: codex offload and config edits

- Agents aggressively offload bounded reading, parsing, drafting, translation,
  and script-generation work to their codex tier by default. This explicitly
  includes site-coordinator, which offloads directly to codex-high before
  spending main-session context on bounded analysis or drafting. Use pointers,
  not payloads: pass paths, task, acceptance check, and a tools/out/ output path.
- Proposed config/context rewrites are written under `tools/out/` with the
  SAME filename the user can move into place manually, e.g.
  `tools/out/site-editor.md` or `tools/out/AGENTS.md`.
- `.claude/agents/*.md`, `.mcp.json`, `AGENTS.md`, and `CLAUDE.md` are
  hand-edit-only. Subagents refuse direct edits to these files.
- When proposing changes to any hand-edit-only config file (.claude/agents/*.md, .mcp.json, AGENTS.md, CLAUDE.md), the agent MUST give the user an EXACT copy-paste shell command (mv/apply) to move the tools/out/ proposals into place. This apply-command duty is itself documented in the config files for high visibility.
- codex output files are the durable deliverable. codex appends incrementally
  and self-logs as its last action to `tools/codex-log.md`; Claude reviews,
  executes, and verifies.
- Continuously and frequently improve the configuration to offload as much work
  as possible from Claude to codex. On an ongoing basis, the coordinator should
  look for Claude-side work (reading, parsing, counting, drafting, translating,
  analysis, script-generation) that codex could do instead, and propose config
  updates (to `.claude/agents/*.md`, `AGENTS.md`, `CLAUDE.md`,
  `codex-offload-policy.md`) that push that work down to codex -- always
  delivered as `tools/out/` proposals with an exact copy-paste apply command.

## Budget rule:

- No agent for explanation-only answers.
- No Fable/Opus in normal website workflow, EXCEPT for debugging escalation: if a bug persists after Sonnet-tier attempts, escalate to Opus; if Opus also cannot fix it, escalate to Fable.
- No parallel subagents.
- No nested subagents.
- No broad “check everything” unless requested.
- Checker returns summaries, not raw outputs.
- Editor receives exact edits, not goals.
- Author returns final content plus edit specs, not file modifications.
- Publisher runs one documented publish command after explicit approval.

## Structure

- `index.html` — root page; only redirects to `jp/` or `en/` based on browser language.
- `en/` and `jp/` — the two language trees. They are mirrors: every page must
  exist at the same path in both, because the JAPANESE/ENGLISH header toggle
  (`js/chglang.js`) just swaps `/jp/` ↔ `/en/` in the URL. Creating or moving a
  page in one language without the counterpart breaks the toggle with a 404.
- Sections: `about`, `research`, `achievements`, `member`, `computers`,
  `teaching`, `picture` (top nav) plus `contact`, `links` (header bar).
  `news` and `software` exist but are not linked from the navigation.
- `style.css` — the single site-wide stylesheet. Pages reference it with a
  cache-busting query (`style.css?v=YYYYMMDD`); when editing the CSS, bump the
  version in ALL pages and templates (scripted replace) or browsers will keep
  serving the stale sheet.
- `images/` — shared images; section-specific photos live in e.g. `en/member/images/`. The site icons `favicon.ico` and `apple-touch-icon.png` live here too (moved from the repo root 2026-07-08); every page/template references them as `images/…` at the correct relative depth.
- `js/` — dropdown menu, mobile menu, back-to-top (vanilla JS), language
  switcher. No local jQuery; the only jQuery is the SRI-pinned CDN copy on
  gallery pages.
- Galleries (research figures, picture page, computers photos) all use
  lightbox2 2.11 + jQuery 3.7 from cdnjs with SRI hashes pinned in each
  page's head; there is no local copy. When bumping versions, recompute the
  `integrity` hashes.
- `.htaccess` — sets security headers (nosniff, SAMEORIGIN, referrer policy);
  deployed to the web root and honored by the server.
- `Templates/*.dwt` — Dreamweaver templates. Inert outside Dreamweaver; every
  HTML page carries its own full copy of the header/nav/footer. Site-wide
  changes (e.g. the nav menu) must be edited in every page (find-and-replace).
- `.dont-remove-me` — hosting marker file; keep it, deploy it, never delete it.

## Delegation to subagents (save rate limit)

Six custom agents exist in `.claude/agents/` (project-level; `.claude/` is gitignored EXCEPT for a `!.claude/agents` un-ignore rule in `.gitignore`, so the agent definitions ARE tracked in git and versioned with the repo, while the rest of `.claude/` stays local-only), tiered by model. The main session burns tokens fastest, so route work
DOWN to the cheapest capable agent by default and keep the main session for
orchestration, user-facing decisions, and final review:

- **site-checker** (Sonnet, read-only) — all verification and searching:
  grepping/counting occurrences site-wide, EN/JP parity checks, curl checks
  of localhost:8000 and the live site (workflow steps 2 and 4), git status
  summaries, sinfo/yrun cluster queries.
- **site-editor** (Sonnet) — executing fully-specified edits (workflow
  step 1): give it the exact strings/entries, target files, and insertion
  points; it knows the CRLF/python3/both-languages rules. Publishing is no
  longer its job — that is site-publisher's.
- **site-author** (Opus) — judgment work that still doesn't need the main
  session: composing news/achievements/research content in house style,
  jp↔en translation, researchmap exporter changes, figure production,
  failure diagnosis. It reads this file first.
- **site-publisher** (Haiku) — runs the publish command (`publish.sh`) only
  after the user has explicitly approved publishing in the current
  conversation (workflow step 3); stops and reports on ssh/publish failures
  rather than touching credentials.
- **site-coordinator** (Opus) — the main orchestration session: routes each
  task DOWN to the cheapest capable agent, keeps user-facing decisions,
  escalation calls, and final review. Escalation exception to the
  no-Opus/Fable rule: if a bug persists after Sonnet-tier attempts, escalate
  to Opus, then to Fable.
- **site-rescue** (Opus, manual-only) — deep root-cause diagnosis for
  tangled or cross-cutting failures; launched explicitly by the user in a
  separate session, read-only unless the user says otherwise.

Subagents do NOT share the conversation, so every dispatch must be
self-contained: exact content, file paths, and the acceptance check to run.
Typical flow: main session decides what to change → site-editor (or
site-author) makes it → site-checker verifies independently → user previews
→ site-publisher publishes → site-checker confirms live. Escalate up a tier
when an agent reports ambiguity or failure; only credentials/ssh recovery
and anything needing the user stay in the main session.

**Failure-driven workflow updates (standing rule):** every time a subagent
fails or returns an incomplete or mistaken result, change the workflow so the
same mistake cannot recur, and record the fix here so it persists across
sessions. Failures logged so far:

- A follow-up `Agent` call does NOT resume the previous agent — it spawns a
  FRESH instance with no memory of the earlier dispatch (there is no
  SendMessage tool available in the website session). So every dispatch,
  including retries, must re-supply ALL context it needs (e.g. the full
  index→citation mapping for a date-lookup task); never say "the list from
  before". (Learned 2026-07-08, sub001 `data-date` pilot.)
- Research/lookup subagents DECLINE to curl external hosts unless the prompt
  explicitly authorizes them. When dispatching a metadata-lookup task, name
  the allowed hosts up front (Crossref `api.crossref.org`, DBLP, Semantic
  Scholar, J-STAGE `api.jstage.jst.go.jp`, publisher DOI resolvers) and note
  that OpenReview / the researchmap login block non-browser clients.
  (Learned 2026-07-08.)
- A subagent can finish with an EMPTY final message (work done internally but
  nothing returned to the caller). For any task whose output matters, instruct
  the agent to WRITE its result to a file as it works (e.g. under `tools/out/`)
  AND print it as its final message; the main session can then `Read` that file
  to recover the result even when the final message comes back empty. Applies
  especially to long research/lookup dispatches with many tool calls.
  (Learned 2026-07-08.)
- Writing results to a file only "at the end" does not survive a mid-run
  cutoff — these lookup agents repeatedly stop after ~15–20 tool calls with a
  truncated final line and no file. Fix: instruct lookup agents to
  append each result to the output file IMMEDIATELY after resolving that one
  item (not batched at the end), and keep each lookup dispatch small (≤3–4
  entries) so it finishes before being cut off. (Learned 2026-07-08.)

**codex MCP backend for site-agents:** the site-agents and site-coordinator can delegate reasoning to the codex MCP servers. codex-{high,medium,low} must be registered at BOTH user scope (`~/.claude.json`) AND project scope (`/home/rioyokota/website/.mcp.json`) — user scope ALONE does NOT reach project agents or the project-scoped coordinator tools (confirmed 2026-07-08: an actual `mcp__codex-medium__codex` call from site-checker returned only after `.mcp.json` was added). Each codex-enabled agent's frontmatter lists its tier under `mcpServers:` plus the `mcp__codex-<tier>__codex` and `codex-reply` tools: site-author/site-coordinator/site-rescue→codex-high, site-checker/site-editor→codex-medium;
site-publisher has no codex tier in the website workflow. On startup Claude prompts to approve the project MCP servers. Editing `.claude/agents/*.md` or `.mcp.json` must be done BY HAND — subagents categorically refuse config edits regardless of the `.claude/config-edit-approved` marker/PreToolUse hook (site-editor refused twice, 2026-07-08); the marker+hook still serve as a hard block against accidental config edits, not as an authorization channel. `.mcp.json` is repo-only and is excluded from deploy (deploy.sh `-x '^\.mcp\.json$'`), so it is never served publicly.
  Collaboration pattern (2026-07-08): OFFLOAD BY DEFAULT; PASS POINTERS, NOT PAYLOADS — codex has
  its own file access and reads `AGENTS.md` (repo root, deploy-excluded)
  automatically, so delegation prompts carry file paths + task + an output
  path under `tools/out/`, never pasted file contents; codex appends results
  to the output file incrementally and replies in a few lines. site-coordinator
  offloads directly to codex-high for bounded reading, parsing, multi-page
  analysis, substantial drafting/translation, and edit-script drafting, then
  reads only the tools/out deliverable plus minimal spot-checks. site-rescue
  offloads bounded reading/parsing/analysis to codex-high during deep
  root-cause diagnosis while staying read-only unless the user explicitly asks
  otherwise. Division of
  labor: codex generates (drafts, translations, analysis, edit scripts),
  Claude reviews/executes/verifies — codex never edits pages directly, never
  publishes, and never verifies its own work (site-checker stays the
  independent verifier). Every delegation
  is logged as one line in `tools/codex-log.md` (date, agent, task, output
  file, conversationId) — output files are the durable cross-session memory;
  conversationIds (resumable via codex-reply) are an optimization. Escalation
  ladder for stuck tasks: Sonnet → codex-medium/high → Opus → Fable.

## Publishing workflow

> **NON-NEGOTIABLE RULE — after EVERY `publish.sh` run, in the same turn:**
> (1) update CLAUDE.md if anything documentable changed, and (2) `git add -A
> && git commit && git push` so BOTH the website change and CLAUDE.md reach
> GitHub. A publish is not complete until GitHub reflects it. `publish.sh`
> already commits+pushes the website change; if that push fails (e.g. GitHub
> key not in the ssh-agent), the publish is UNFINISHED — surface it to the
> user and resolve before moving on. A PostToolUse hook in
> `.claude/settings.local.json` prints a reminder after every publish, but
> this rule holds even if the hook is absent.

This is the standard cycle for every content change (first exercised
end-to-end on 2026-07-04, removing a member from the member page):

**Standing workflow rules:**

- Always, on every change:
  1. Preview at `http://localhost:8000/jp/index.html` before publishing.
  2. Update CLAUDE.md immediately after publishing if anything documentable changed.
  3. Commit and push CLAUDE.md to GitHub immediately after updating it.
- Only when the user explicitly asks:
  1. Mirror the website EN/JP pages to ResearchMap.
  2. Mirror the website into `cv/cv.tex`, compile `cv/cv.pdf`, and publish.

1. **Edit** — make the change; remember to update both `jp/` and `en/`
   counterparts. When Claude makes the edit, grep for other occurrences of
   the changed content (names, links) across the whole site, not just the
   page the user named.
   - Standing rule: when asked to remove someone from the member list,
     don't just delete them — also add them to the TOP of the Alumni list
     on both member pages (jp form: `姓 名 (Romaji Name)`).
   - Historical records (news items, publication lists) are never edited
     when members leave or change grade.
2. **Preview** — the user checks the result at
   `http://localhost:8000/jp/index.html`. A SessionStart/SessionEnd hook in
   `.claude/settings.local.json` starts and stops `python3 -m http.server
   8000` automatically (PID in `.claude/http-server.pid`); if the server is
   down mid-session, start it the same way. Wait for the user's OK before
   publishing; do not skip this step.
3. **Publish** — `./publish.sh "what changed"`. It shows the pending git
   changes and exactly which files would be uploaded, asks one y/N
   confirmation, then deploys to the web server and commits and pushes to
   GitHub in one step. When Claude runs it after the user's OK, pipe the
   confirmation: `echo y | ./publish.sh "message"`. This no longer triggers
   a ResearchMap export automatically — that is now a separate,
   explicitly-requested step (see the researchmap/FIS bullet above).
   - It commits with `git add -A`, so FIRST check `git status` for pending
     changes unrelated to the current edit (e.g. left over from an earlier
     session); if any exist, mention them to the user and write a commit
     message that covers everything being swept in. (Learned 2026-07-06,
     when a leftover CSS change rode along under an unrelated message.)
     Debugging artifacts dropped into the repo folder (e.g. iPhone
     screenshots like IMG_*.PNG) get swept in AND deployed to the public
     web root — delete them before publishing, or remove them from the
     server afterwards with lftp.
4. **Verify** — after publishing, curl the changed pages on
   https://www.rio.scrc.iir.isct.ac.jp and confirm the change is live.
5. **Document** — if the change added or altered structure, conventions,
   workflow, or tooling described in this file, update CLAUDE.md in the same
   turn and commit and push it (repo-only file, not deployed). A PostToolUse
   hook in `.claude/settings.local.json` injects a reminder after every
   publish.sh run so this step is not forgotten.

## Content conventions

- **File quirks**: the HTML files have CRLF line endings and occasional
  non-breaking spaces, so the Edit tool's exact-match replace often fails.
  Edit them with a small `python3` script (`open(path, newline='')` to
  preserve CRLF) instead. When parsing this Dreamweaver-era HTML with
  scripts, match tags case-insensitively and do NOT assume closing tags
  (legacy sections used unclosed uppercase `<LI>`; one such block hid a
  duplicated run of entries on the jp achievements page until 2026-07-06).
- **Institution naming** (renamed 2024): 東京科学大学 総合研究院 / Institute of
  Science Tokyo, IIR. Old names (東京工業大学, Tokyo Tech, 学術国際情報センター,
  GSIC) were replaced site-wide on 2026-07-05, EXCEPT in historical records —
  the CV on `member/yokota.html`, old news items — and in live URLs
  (`t4.gsic.titech.ac.jp`, SuperCon links), which keep the old names.
- **Achievements** (`achievements/index.html`): sections `sub001`–`sub007`
  (journal / book series / books / international peer-reviewed / domestic
  peer-reviewed / international non-reviewed / domestic non-reviewed), entries
  newest-first inside each `<ol>`. International citations are written in
  English on BOTH language pages; domestic ones in Japanese on both.
- **Achievements `data-date` (ResearchMap metadata):** every Achievements
  `<li>` carries an invisible `data-date` attribute on the opening `<li>` tag
  (the ResearchMap `publication_date`); it does not change the rendered page.
  Format `YYYY-MM` (or `YYYY-MM-DD` when the day is known). Derivation rule,
  applied consistently to every entry AND when auto-filling a newly added entry
  that lacks a date: (1) journals → published date; conferences → first day of
  the conference; if neither applies, ask the user. (2) Resolve the month in
  fixed priority: the date in the citation text, else the confirmed month from
  the DOI/Crossref (print, else online-first), else the J-STAGE 発行日.
  (3) YEAR-ONLY IS NEVER ALLOWED — if the month cannot be confirmed from any
  source, default to `-01` (January of the known year) as the deterministic
  placeholder. This attribute is being filled section by section (pilot:
  sub001, 2026-07-08); the exporter should prefer `data-date` over its
  heuristic date parsing when the attribute is present. Progress across all
  fields/sections is tracked in `tools/researchmap-metadata-todo.md`
  (persistent, repo-only) — read and update it each step.
  Field 1 (data-date) is COMPLETE across sub001–sub007 as of 2026-07-08
  (sub001 42, sub004 115, sub005 32, sub006 45, sub007 62, sub002/sub003 4 —
  all in en+jp); the only remaining Field-1 task is updating the exporter to
  prefer `data-date` over heuristic date parsing.
- **Achievements `data-doi` / `data-url` (Field 2, ResearchMap identifier):** each
  Achievements `<li>` may carry an invisible `data-doi` (BARE DOI, e.g.
  `10.1234/...`, no `https://doi.org/` prefix) OR, when no DOI exists, a `data-url`
  (a canonical URL for the SAME paper — arXiv abs page, OpenReview forum, or the
  言語処理学会/ANLP anthology PDF). Derivation priority: (1) DOI via
  Crossref/J-STAGE, matching title+author+year; else (2) a confirmed same-paper
  URL (arXiv/OpenReview/anthology); else (3) leave BOTH off (blank). Be
  conservative — only record an identifier whose title actually matches; a
  differing title means leave it blank. Lookups run in small (<=4-6) site-author
  batches, authorized hosts Crossref/DBLP/Semantic Scholar/J-STAGE/arXiv (+anlp.jp
  for ANLP), appending each result immediately to `tools/out/doi-subNNN.md`. The
  Field-2 exporter step (not yet built) will map `data-doi`->DOI identifier and
  `data-url`->see_also link. Progress (2026-07-08) in
  `tools/researchmap-metadata-todo.md`: sub001 (37 doi + 2 url), sub002 (0),
  sub003 (2 doi), sub005 (4 doi + 5 url) done; sub004 / sub006 / sub007 + the
  exporter update remain.
- **News**: only top-conference acceptances (ICLR/NeurIPS/CVPR/AAAI level) and
  grants get news items — not workshops, GTC talks, or LREC-tier venues. Each
  item appears in four places: a dated row in the News table on both top pages
  (`en/index.html`, `jp/index.html`) linking to `news/index.html#evYYMMDD`,
  and the full anchored entry on both news pages. Dates = announcement date;
  member grades are written as of that date (e.g. "(2nd year PhD)"/"(D2)").
- **Computers page**: the Hinadori section is generated from live cluster data —
  this machine IS the Hinadori login node. `sinfo`/`slurm.conf` give the node
  layout, `yrun` (no args) lists resources with GPU models, and short `ybatch`
  jobs (`#YBATCH -r <resource>`; write output to `$HOME`, not `/tmp` — `/tmp`
  is node-local) give exact CPU/GPU models. Direct `srun` is blocked. Last
  refreshed 2026-07-05: 81 GPUs. The 2-GPU RTX 6000 Ada node's CPU (AMD EPYC
  9654) was supplied by the user; the 8-GPU RTX 6000 Ada node's CPU is
  unknown ("-" in the table, node was down).
- **Research page** (`research/index.html`): "Current Research Topics YYYY"
  first (anchor `rYYYY`), then per-year thesis sections newest-first (anchors
  `rYYYYM`/`rYYYYB`), mirrored in the sidebar. Entry format: `<h4>Title（Name）
  </h4>` + abstract `<p>` + a lightbox figure. Figures for BOTH language pages
  live in `jp/research/images20XX/NNN.jpg` (numbering continues within the
  folder). Unlike Achievements, the Research pages are fully monolingual
  (since 2026-07-05): everything in English on `en/`, everything in Japanese
  on `jp/` — translate titles and abstracts; use kanji names where known
  (check the member/alumni lists), romaji for international students.
- When changing a site-wide string, also update `Templates/*.dwt` so the
  inert templates stay consistent with the pages.
- **Mirroring to researchmap/FIS**: `researchmap-export.py` no longer runs
  automatically from `publish.sh`. Run it on demand only when the user
  explicitly asks to sync ResearchMap: `python3 tools/researchmap-export.py
  --check-live`. This mode fetches the live public API
  (`https://api.researchmap.jp/rioyokota/{published_papers,books_etc,
  presentations,misc}`) and diffs it against ALL current Yokota-authored
  Achievements entries on the website — not just entries added since the
  last local run — because `tools/researchmap-state.json` can drift from
  what's actually live (an export generated but never uploaded, or
  uploaded partially). It writes the full set of missing entries to
  `tools/out/researchmap-import.jsonl`.
  Category mapping (agreed 2026-07-06): peer-reviewed sections
  (sub001/004/005) → Papers; Book series + Books (sub002/003) → Books and
  Other Publications; non-peer-reviewed sections (sub006/007) →
  Presentations when Rio Yokota is the SOLE author (invited talks), Misc.
  otherwise. The bulk-import grammar also supports `update` (+`doc`) and
  `delete` by `rm:id` (the public read API exposes the ids), which is how
  the 2026-07-06 recategorization migration was built. Insert lines must
  NOT carry `user_id` — in a self-import the logged-in account is implied,
  and a `user_id` (even the own permalink) means "another member's list"
  and fails with 403 forbidden, which blocks the ENTIRE file (researchmap
  validates all lines before applying any). Learned 2026-07-06.
  The exact bulk-import UPDATE grammar (verified 2026-07-08 against the
  researchmap V2 API spec; `researchmap-export.py` has NO update code path,
  so update/delete lines are hand-built): one JSON object per line,
  `{"update": {"type": "<record-type>", "id": "<rm:id>"}, "doc": {<only the
  changed fields>}}` — a PARTIAL update (unlisted fields are left untouched),
  and like inserts it must carry NO `user_id`. The `rm:id`s come from the
  public read API (e.g. `https://api.researchmap.jp/rioyokota/published_papers?
  limit=1000`). Example used 2026-07-08 to fix an ANLP2025 paper title:
  `{"update": {"type": "published_papers", "id": "50836989"}, "doc":
  {"paper_title": {"ja": "..."}}}`. Note ORCID has no such update path — a
  no-DOI title change adds a new BibTeX work on re-import, so the stale
  old-title work must be removed manually in the ORCID UI.
  The user then downloads the file from
  http://localhost:8000/tools/out/researchmap-import.jsonl and uploads it
  at researchmap 設定 > インポート (permalink: rioyokota); the university
  FIS syncs from researchmap automatically. Review the printed NEW lines
  before upload — citation parsing is heuristic. Do NOT script the
  researchmap website itself: its login path actively blocks non-browser
  clients (403), and the sanctioned automation route is the WebAPI —
  fully automatic push awaits a JST API key (as of 2026-07-06, the user
  is asking the URA office). Public READ needs no key:
  `https://api.researchmap.jp/rioyokota/{type}` (JSON).
  - Import error granularity (learned 2026-07-07): a `user_id` on any insert
    line 403s and blocks the ENTIRE file, but a per-entry validation error
    (e.g. a `published_papers` line missing `publication_date`) returns a 400
    for THAT line only while the other lines still import successfully.
    researchmap emails/serves an errors CSV (`errors_researchmap-import-N.csv`)
    listing the failing line number, field, and message. When one row fails,
    do NOT re-upload the whole file (it would duplicate the rows that already
    imported) — extract only the corrected failing line into a tiny one-line
    jsonl and upload just that. The public READ API lags behind imports
    (indexing delay), so `--check-live` will NOT immediately dedupe
    just-imported entries; that lag is another reason to hand-extract the one
    failed line rather than regenerate the full set.
  - `published_papers` entries REQUIRE a `publication_date` (出版年月);
    an entry whose citation buries the date behind a trailing note fails 400
    until fixed.
  - The exporter's citation parser is heuristic and was hardened 2026-07-07
    to handle: author lists separated by either 、 or ASCII commas, the
    "LastAuthor. Title" boundary (a period+space after the last author — the
    fix keeps single-letter initials like "David E. Keyes" intact rather than
    splitting there), and a trailing parenthetical after the date
    ("Dec. 2022. (Best paper)", "(学生奨励賞)") — the date is extracted and the
    note dropped from `publication_name`. Still heuristic: review the output.
- **Mirroring to ORCID**: `tools/orcid-export.py` mirrors the website's
  publication list to the user's ORCID record
  (https://orcid.org/0000-0001-7573-7873). ORCID has no researchmap-style
  JSON grammar; the sanctioned no-API route is ORCID's **Add works > Import
  BibTeX** wizard, so the exporter emits a single BibTeX file at
  `tools/out/orcid-works.bib` (repo-only; served for download at
  http://localhost:8000/tools/out/orcid-works.bib). Run on demand:
  `python3 tools/orcid-export.py`, then the user imports the .bib via ORCID
  Add works > Import BibTeX. It reuses `researchmap-export.py`'s hardened
  citation parser verbatim (loaded via importlib since that filename has a
  hyphen), so both exporters split author/title/venue/date identically —
  fixing a citation for one fixes it for both. Section -> BibTeX type map:
  sub001 -> @article; sub002 -> @incollection; sub003 -> @book;
  sub004/sub005 (peer-reviewed conferences) -> @inproceedings;
  sub006/sub007 (non-reviewed) -> @misc. It generates the FULL Yokota-authored
  set (no live diff — ORCID's public API is read-only without OAuth); ORCID
  de-duplicates by grouping/merge on its side, so re-import is non-destructive.
  First run 2026-07-07: 284 entries. A future OAuth/member-API auto-diff push
  is possible but not built. Same on-demand pattern as the researchmap export
  and cv build — kept OUT of publish.sh. NOTE: the exporter's parser is only as
  good as the source citations; three malformed achievements entries
  (colon-separated author, 全角 ．/「」 delimiters) were normalized in the
  achievements pages 2026-07-07 so they parse — prefer fixing the source
  citation over patching the .bib.
- **cv.tex sync**: `cv/cv.tex` must stay in sync with the website, in both
  directions. Whenever `achievements/index.html` or the CV sections of
  `jp/member/yokota.html` (受賞歴/委員歴/研究課題) change, update the
  matching section of `cv/cv.tex` in the same edit — and vice versa, if
  `cv/cv.tex` is the source of a new item, add it to the website pages too.
- **CV PDF build**: `cv/cv.tex` (+ its custom `cv/cv.cls`, both in the `cv/` folder) is
  compiled to `cv/cv.pdf` by `cv/build-cv.sh`, which runs `tectonic` (XeTeX-based,
  installed at `~/.local/bin/tectonic`). `cv/cv.tex`'s preamble MUST keep
  `\usepackage{xeCJK}` + `\setCJKmainfont{Noto Sans CJK JP}` (the CV contains
  Japanese names/titles; the Noto CJK font is installed under
  `~/.local/share/fonts`) — without it XeTeX silently drops every kanji. Run
  `./cv/build-cv.sh` on demand whenever `cv/cv.tex` changes (kept OUT of `publish.sh`,
  same on-demand pattern as the researchmap export); then a normal `publish.sh`
  deploys the regenerated `cv/cv.pdf`. The single English+Japanese `cv/cv.pdf` lives in the `cv/` folder and is linked from BOTH
  `en/member/yokota.html` and `jp/member/yokota.html` as `../../cv/cv.pdf`
  (target=_blank, rel=noopener). `cv/cv.tex`, `cv/cv.cls`, and `cv/build-cv.sh` are
  repo-only — excluded from deploy in `deploy.sh`; only `cv/cv.pdf` is served.
- **CV items on the personal page** are mirrored to researchmap the same
  way. Canonical source: `jp/member/yokota.html` sections 受賞歴 / 委員歴 /
  研究課題 (the en page mirrors them as Awards / Committee Memberships /
  Research Projects but is NOT parsed). Line formats the exporter expects
  (em-dash separators, 全角 space after dates):
  `2009年11月　AWARD_NAME` / `2024–2025　ROLE — ASSOCIATION` /
  `2025–2028　TITLE（FUNDING SYSTEM、FUNDER）`. When adding an item, add it
  to BOTH language pages in that format; run the on-demand export
  described above to mirror it to researchmap. Initial content was
  imported FROM researchmap on
  2026-07-06, so everything on the page as of then is in the baseline.
- **ORCID BibTeX export**: `tools/orcid-export.py` exports the website's
  Achievements publication list as BibTeX for ORCID import. ORCID has no
  researchmap-style JSON bulk-import API; the sanctioned import path in the UI is
  ORCID > Add works > Import BibTeX (the BibTeXImportWizard). This exporter
  parses `en/achievements/index.html`, keeps only entries where Rio Yokota is an
  author, and reuses the *same* hardened citation parser as `researchmap-export.py`
  (loaded dynamically via importlib) so both exporters split author/title/venue/date
  identically — ensuring consistency across mirrors.
  Section-to-BibTeX mapping: sub001 (journal) → @article, sub002 (book series) →
  @incollection, sub003 (books) → @book, sub004–005 (peer-reviewed) →
  @inproceedings, sub006–007 (non-peer-reviewed) → @misc.
  Usage:
    `tools/orcid-export.py`         write tools/out/orcid-works.bib
    `tools/orcid-export.py --dry-run` print counts + risky parses, no file
  ORCID's public API is read-only without an OAuth token, so unlike the
  researchmap exporter, this tool does NOT diff against live. It always writes
  the complete Yokota-authored set from the website; ORCID de-duplicates on
  import (groups works by identifier/title and lets the user merge). An
  API-diff mode can be added later once a 3-legged OAuth token exists. The user
  then downloads `tools/out/orcid-works.bib` and uploads it at ORCID > Add works >
  Import BibTeX. Review the printed risky parses before import — citation parsing
  is heuristic.

## Content sources and figure tooling

- **Lab Google Drive**: read-only access via rclone —
  `~/.local/bin/rclone lsf --drive-root-folder-id 1MRyEsesRkuZ_eGtUgnPgC9k3rXuo_BLa gdrive:<path>`.
  Layout: `Thesis/YYYY/{master,bachelor}/` (thesis PDFs — source for Research
  page entries), `Posters/YYYY/` (研究室紹介 lab-intro poster; `.pages` files
  are zip archives containing `preview.jpg` and original images under
  `Data/`), `Slides/YYYY発表.../` (defense slides). The OAuth token is
  Drive-read-only and revocable at myaccount.google.com/permissions.
- **Swallow material**: https://swallow-llm.github.io/ (release pages exist
  in `.ja.html` and `.en.html`). Its charts are ApexCharts SVGs whose legends
  are NOT in the SVG — series names are in `seriesName` attributes, colors
  follow the ApexCharts palette (#008FFB, #00E396, #FEB019, #FF4560, #775DD0
  in series order); rebuild the legend with PIL when rasterizing.
- **Figure production**: thesis-PDF figures via `pdftoppm -jpeg -r 150 -f N -l N`
  + PIL crop (trim captions; flatten transparency onto white). SVG→PNG needs
  cairosvg in a venv (`python3 -m venv`; system pip is PEP-668-locked) and
  Japanese fonts — Noto Sans CJK JP is installed in `~/.local/share/fonts`
  (2026-07-05); patch the SVG's `font-family` to "Noto Sans CJK JP" before
  converting, since cairo does no font fallback.

## Deployment details

`publish.sh` calls `./deploy.sh` (preview with `./deploy.sh --dry-run`). It mirrors
this folder to `www/` on the server via lftp/SFTP, uploading only new/changed
files. It uses `mirror -R --delete`, so files removed locally are automatically
removed from the remote on the next deploy — the server stays an exact
mirror of the deployed set (no more manual `lftp rm`). Excluded paths
(`-x` list: `.git`, `.claude`, `tools`, the scripts, `CLAUDE.md`,
the source files `cv/cv.tex`/`cv/cv.cls`/`cv/build-cv.sh`, etc.) are never uploaded and never
deleted remotely. Verified 2026-07-08 the live mirror had zero remote-only
orphans. Because `--delete` is destructive, always preview with
`./deploy.sh --dry-run` when a deploy includes deletions.

- Server: `gsic0017@web-o3.noc.titech.ac.jp`, SFTP only (no shell), web root `www/`.
- Auth: password-only via the `web` alias in `~/.ssh/config`, multiplexed over
  a ControlMaster connection (`ControlPersist yes` — lives until reboot).
  If the master is down, `deploy.sh` re-establishes it automatically: the
  password is stored in `~/.ssh/web-password` (chmod 600, created by the user,
  NEVER printed or read into the conversation) and supplied to ssh by the
  `~/.ssh/web-askpass` helper via `SSH_ASKPASS_REQUIRE=force`.
- If that file is missing, ask the user to run `ssh -fN web` in a separate
  terminal — never ask for the password in chat. Note: `!` commands in the
  Claude Code session have no tty, so interactive password entry does not
  work there.
- Key-based auth is impossible: the chrooted SFTP home is root-owned, so no
  `~/.ssh/authorized_keys` can be created on the server.
- NEVER upload `.git` to the server. Its public copy was removed on 2026-07-04
  after being found downloadable over HTTPS; `deploy.sh` excludes it.
- If `git push` fails with "Permission denied (publickey)": the session's ssh-agent lacks the passphrase-protected GitHub key (`~/.ssh/id_ed25519`). The standardized fix is a single persistent agent at a FIXED socket `~/.ssh/agent.sock`: the user runs `sh ~/scripts/ssh-agent-setup.sh` once per reboot (in a real tmux pane, e.g. a new window via `Ctrl-b c`) to start that agent and load the key (passphrase entered once); shells auto-point at it via a `# yokota-ssh-agent` block in the user's rc. From any session — including Claude's non-login Bash, which does NOT source rc — push deterministically with `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git push`; no more hunting `/tmp/ssh-*` sockets. The helper `ssh-agent-setup.sh` (repo-external, in `~/scripts`) is idempotent and safe to re-run. (Standardized 2026-07-08 after repeated ssh-add failures under tmux/remote-control.)

## Known issues (as of 2026-07)

- (Fixed 2026-07-05: the broken http:// jQuery now loads locally from `js/`,
  the dead Google Analytics snippet and IE8 shims were removed from every
  page, and `style.css` was modernized — same selectors, refreshed look.)
- (Fixed 2026-07-07: two mobile layout bugs found via iPhone screenshots — the
  hamburger menu opened white-on-white because the floated 50%-width `li`s
  collapsed `ul#topnav` to zero height (fix: `overflow: hidden` clearfix on
  the mobile menu rules), and the top pages' `.slogan` overlay (absolute,
  inline `width:500px`) overflowed the shrunken banner and covered the
  header (fix: `position: static; width: auto !important` on mobile).
  Literal `background: #002855` fallbacks now precede `var(--navy)` in the
  nav rules as belt-and-braces.)
- External links carry rel="noopener noreferrer"; keep that on new
  target="_blank" links.
- The page HTML itself is still Dreamweaver-era (floats, table layouts);
  `style.css` is written against those existing selectors, so keep class/id
  names stable when editing pages.

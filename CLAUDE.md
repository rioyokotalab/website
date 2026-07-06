# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp — a hand-built static HTML site
(originally made with Adobe Dreamweaver). No build step, no framework: files are
served exactly as they are here, and the URL structure mirrors the folder
structure one-to-one.

## Budget rule:

- No agent for explanation-only answers.
- No Fable/Opus in normal website workflow.
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
- `images/` — shared images; section-specific photos live in e.g. `en/member/images/`.
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

Three custom agents exist in `.claude/agents/` (project-level; `.claude/` is
gitignored, so they live on this machine only), tiered by model. The main session burns tokens fastest, so route work
DOWN to the cheapest capable agent by default and keep the main session for
orchestration, user-facing decisions, and final review:

- **site-checker** (Haiku, read-only) — all verification and searching:
  grepping/counting occurrences site-wide, EN/JP parity checks, curl checks
  of localhost:8000 and the live site (workflow steps 2 and 4), git status
  summaries, sinfo/yrun cluster queries.
- **site-editor** (Sonnet) — executing fully-specified edits (workflow
  step 1) and the publish run after the user's OK (step 3): give it the
  exact strings/entries, target files, and insertion points; it knows the
  CRLF/python3/both-languages rules. It stops and reports on ssh/publish
  failures rather than touching credentials.
- **site-author** (Opus) — judgment work that still doesn't need the main
  session: composing news/achievements/research content in house style,
  jp↔en translation, researchmap exporter changes, figure production,
  failure diagnosis. It reads this file first.

Subagents do NOT share the conversation, so every dispatch must be
self-contained: exact content, file paths, and the acceptance check to run.
Typical flow: main session decides what to change → site-editor (or
site-author) makes it → site-checker verifies independently → user previews
→ site-editor publishes → site-checker confirms live. Escalate up a tier
when an agent reports ambiguity or failure; only credentials/ssh recovery
and anything needing the user stay in the main session.

## Publishing workflow

This is the standard cycle for every content change (first exercised
end-to-end on 2026-07-04, removing a member from the member page):

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
   confirmation: `echo y | ./publish.sh "message"`.
   - It commits with `git add -A`, so FIRST check `git status` for pending
     changes unrelated to the current edit (e.g. left over from an earlier
     session); if any exist, mention them to the user and write a commit
     message that covers everything being swept in. (Learned 2026-07-06,
     when a leftover CSS change rode along under an unrelated message.)
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
- **Mirroring to researchmap/FIS**: `publish.sh` automatically runs
  `tools/researchmap-export.py` whenever a publish touches the
  Achievements page. The tool diffs the page against
  `tools/researchmap-state.json` (baseline = 2026-07-06, when researchmap
  was made to match the page exactly via a one-off migration import; the
  state update rides in the same commit), keeps only entries with Rio
  Yokota as author, and writes researchmap V2 bulk-import JSON Lines to
  `tools/out/researchmap-import.jsonl`
  (`similar_merge` + `priority: similar_data`, so researchmap dedups).
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
- **CV items on the personal page** are mirrored to researchmap the same
  way. Canonical source: `jp/member/yokota.html` sections 受賞歴 / 委員歴 /
  研究課題 (the en page mirrors them as Awards / Committee Memberships /
  Research Projects but is NOT parsed). Line formats the exporter expects
  (em-dash separators, 全角 space after dates):
  `2009年11月　AWARD_NAME` / `2024–2025　ROLE — ASSOCIATION` /
  `2025–2028　TITLE（FUNDING SYSTEM、FUNDER）`. When adding an item, add it
  to BOTH language pages in that format; publish.sh exports it
  automatically. Initial content was imported FROM researchmap on
  2026-07-06, so everything on the page as of then is in the baseline.

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
files. It does NOT delete remote files removed locally — after deleting
files, remove them from the server with `lftp -e "rm -f www/<path>; bye"
sftp://web` (remote made an exact mirror on 2026-07-05).

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
- If `git push` fails with "Permission denied (publickey)": the GitHub key
  (`~/.ssh/id_ed25519`) is passphrase-protected and the session's ssh-agent
  has lost it. Ask the user to run `ssh-add ~/.ssh/id_ed25519` in a real
  terminal, then find the agent that now holds the key and push through it:
  `for s in /tmp/ssh-*/agent.*; do SSH_AUTH_SOCK=$s ssh-add -l ...; done`,
  then `SSH_AUTH_SOCK=<that socket> git push`.

## Known issues (as of 2026-07)

- (Fixed 2026-07-05: the broken http:// jQuery now loads locally from `js/`,
  the dead Google Analytics snippet and IE8 shims were removed from every
  page, and `style.css` was modernized — same selectors, refreshed look.)
- External links carry rel="noopener noreferrer"; keep that on new
  target="_blank" links.
- The page HTML itself is still Dreamweaver-era (floats, table layouts);
  `style.css` is written against those existing selectors, so keep class/id
  names stable when editing pages.

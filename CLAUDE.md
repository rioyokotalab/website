# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp — a hand-built static HTML site
(originally made with Adobe Dreamweaver). No build step, no framework: files are
served exactly as they are here, and the URL structure mirrors the folder
structure one-to-one.

## Structure

- `index.html` — root page; only redirects to `jp/` or `en/` based on browser language.
- `en/` and `jp/` — the two language trees. They are mirrors: every page must
  exist at the same path in both, because the JAPANESE/ENGLISH header toggle
  (`js/chglang.js`) just swaps `/jp/` ↔ `/en/` in the URL. Creating or moving a
  page in one language without the counterpart breaks the toggle with a 404.
- Sections: `about`, `research`, `achievements`, `member`, `computers`,
  `teaching`, `picture` (top nav) plus `contact`, `links` (header bar).
  `news` and `software` exist but are not linked from the navigation.
- `style.css` — the single site-wide stylesheet.
- `images/` — shared images; section-specific photos live in e.g. `en/member/images/`.
- `js/` — dropdown menu, mobile menu, back-to-top, language switcher, and a
  local jQuery 1.7.2 (pages load it from here; never from a CDN).
- `lightbox/`, `lightbox2/` — image-popup library for the photo gallery.
- `Templates/*.dwt` — Dreamweaver templates. Inert outside Dreamweaver; every
  HTML page carries its own full copy of the header/nav/footer. Site-wide
  changes (e.g. the nav menu) must be edited in every page (find-and-replace).
- `.dont-remove-me` — hosting marker file; keep it, deploy it, never delete it.

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
4. **Verify** — after publishing, curl the changed pages on
   https://www.rio.scrc.iir.isct.ac.jp and confirm the change is live.

## Content conventions

- **File quirks**: the HTML files have CRLF line endings and occasional
  non-breaking spaces, so the Edit tool's exact-match replace often fails.
  Edit them with a small `python3` script (`open(path, newline='')` to
  preserve CRLF) instead.
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
  refreshed 2026-07-05: 81 GPUs; the two RTX 6000 Ada nodes' CPU models are
  still unverified ("-" in the table).
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
files. It does NOT delete remote files removed locally.

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

## Known issues (as of 2026-07)

- (Fixed 2026-07-05: the broken http:// jQuery now loads locally from `js/`,
  the dead Google Analytics snippet and IE8 shims were removed from every
  page, and `style.css` was modernized — same selectors, refreshed look.)
- The research pages additionally load lightbox2 2.7.1 + jQuery 1.12.4 from
  HTTPS CDNs for the figure pop-ups; these work and are left as-is.
- The page HTML itself is still Dreamweaver-era (floats, table layouts);
  `style.css` is written against those existing selectors, so keep class/id
  names stable when editing pages.

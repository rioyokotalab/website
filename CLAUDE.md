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
- `js/` — dropdown menu, mobile menu, back-to-top, language switcher, IE shims.
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
2. **Preview** — the user checks the result on their local server
   (`python3 -m http.server 8000` in this folder →
   `http://localhost:8000/jp/index.html`). Wait for the user's OK before
   publishing; do not skip this step.
3. **Publish** — `./publish.sh "what changed"`. It shows the pending git
   changes and exactly which files would be uploaded, asks one y/N
   confirmation, then deploys to the web server and commits and pushes to
   GitHub in one step. When Claude runs it after the user's OK, pipe the
   confirmation: `echo y | ./publish.sh "message"`.
4. **Verify** — after publishing, curl the changed pages on
   https://www.rio.scrc.iir.isct.ac.jp and confirm the change is live.

## Deployment details

`publish.sh` calls `./deploy.sh` (preview with `./deploy.sh --dry-run`). It mirrors
this folder to `www/` on the server via lftp/SFTP, uploading only new/changed
files. It does NOT delete remote files removed locally.

- Server: `gsic0017@web-o3.noc.titech.ac.jp`, SFTP only (no shell), web root `www/`.
- Auth: password-only via the `web` alias in `~/.ssh/config`, which multiplexes
  over an authenticated ControlMaster connection (persists 8h). If the master
  has expired (`ssh -O check web` fails), ask the user to run `! ssh -fN web`
  and enter the password themselves — never ask for the password in chat.
- Key-based auth is impossible: the chrooted SFTP home is root-owned, so no
  `~/.ssh/authorized_keys` can be created on the server.
- NEVER upload `.git` to the server. Its public copy was removed on 2026-07-04
  after being found downloadable over HTTPS; `deploy.sh` excludes it.

## Known issues (as of 2026-07)

- Pages load jQuery 1.7.2 from `http://code.jquery.com/...` — plain HTTP is
  blocked on the HTTPS site, so anything depending on jQuery may be broken.
- Every page embeds a dead Google Analytics snippet (Universal Analytics
  `UA-82924932-1`, shut down in 2023).
- Old-IE shims (`html5.js`, `css3-mediaqueries.js`) are obsolete.

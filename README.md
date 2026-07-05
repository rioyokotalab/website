# YOKOTA Laboratory website

Source for https://www.rio.scrc.iir.isct.ac.jp — a hand-built static HTML site
with no build step. The `jp/` and `en/` trees are mirrors of each other, and
the URL structure matches the folder structure one-to-one. See `CLAUDE.md` for
the full structure and content conventions.

The intended workflow is: **ask Claude Code to make the change, check the
result locally, say "OK" — and the live site and the GitHub repo are updated
automatically.**

## One-time setup

### 1. Clone and install tools

```
git clone https://github.com/rioyokotalab/website
```

You need `python3` (local preview), `lftp` (deploy), and
[Claude Code](https://claude.com/claude-code).

### 2. SSH config for the SFTP connection

The site is hosted at `gsic0017@web-o3.noc.titech.ac.jp` (web root `www/`).
The server is **SFTP-only** (no shell) and **password-only** — key-based auth
is impossible because the chrooted SFTP home is root-owned, so no
`authorized_keys` can be installed. Instead, deploys ride on a multiplexed SSH
connection that is authenticated once and reused.

Add this to `~/.ssh/config`:

```
Host web
	HostName web-o3.noc.titech.ac.jp
	User gsic0017
	ControlMaster auto
	ControlPath ~/.ssh/cm-%r@%h-%p
	ControlPersist yes
```

Then store the account password (get it from the lab admin) so the connection
can re-establish itself unattended. Run this in a normal terminal — it prompts
without echoing and writes `~/.ssh/web-password` readable only by you:

```
bash -c 'umask 077; read -rsp "web server password: " p; printf "%s\n" "$p" > ~/.ssh/web-password; echo'
```

Create the askpass helper `~/.ssh/web-askpass` (this is how ssh reads the
password file):

```
#!/bin/sh
cat "$HOME/.ssh/web-password"
```

and make it executable: `chmod 700 ~/.ssh/web-askpass`.

That's it — `deploy.sh` checks the connection before every deploy and silently
re-authenticates from the password file when needed. If you skip the password
file, you must run `ssh -fN web` (and type the password) whenever the
connection has expired.

### 3. Optional: auto-start the preview server

To have Claude Code start `python3 -m http.server 8000` when a session opens
and stop it when the session ends, create `.claude/settings.local.json` in
this folder (it is gitignored) with:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "timeout": 10,
      "command": "f=$PWD/.claude/http-server.pid; if ! { [ -f \"$f\" ] && kill -0 \"$(cat \"$f\")\" 2>/dev/null; }; then { nohup python3 -m http.server 8000 >/dev/null 2>&1 & echo $! > \"$f\"; }; fi" }] }],
    "SessionEnd": [{ "hooks": [{ "type": "command", "timeout": 10,
      "command": "f=$PWD/.claude/http-server.pid; if [ -f \"$f\" ]; then p=$(cat \"$f\"); if [ -n \"$p\" ] && grep -qa http.server \"/proc/$p/cmdline\" 2>/dev/null; then kill \"$p\" 2>/dev/null; fi; rm -f \"$f\"; fi" }] }]
  }
}
```

Otherwise just run `python3 -m http.server 8000` in this folder yourself.

## Updating the website

1. Start Claude Code in this folder: `claude` (or `claude --continue`).
2. Describe the change in plain language, e.g. *"Remove Taro Yamada from the
   member page"* or *"Add this paper to the Achievements page: …"*.
   `CLAUDE.md` teaches Claude the house rules automatically: edit both the
   Japanese and English pages, move removed members to the top of Alumni,
   never rewrite historical news or publication entries, etc.
3. Check the result in your browser at
   [http://localhost:8000/jp/index.html](http://localhost:8000/jp/index.html)
   (and the `/en/` counterpart).
4. If it looks right, reply **"OK"**. Claude then runs `./publish.sh`, which
   uploads the changed files to the web server **and commits and pushes to
   GitHub in one step**, and finally verifies the change on the live site.

Nothing goes live before your "OK", and every published change lands in the
GitHub history automatically.

## Publishing manually (without Claude)

```
./deploy.sh --dry-run     # preview what would be uploaded
./publish.sh "message"    # deploy + git commit + git push, with confirmation
```

`deploy.sh` mirrors this folder to `www/` on the server, uploading only
new/changed files. It excludes repo-only files (`.git`, `.claude/`,
`deploy.sh`, `publish.sh`, `CLAUDE.md`, `README.md`, `.gitignore`) so they
never reach the public site. It does not delete remote files removed locally.

## Rules that keep the site healthy

- Every page must exist in **both** `jp/` and `en/` at the same path — the
  language toggle just swaps `/jp/` ↔ `/en/` in the URL.
- Never upload `.git` to the server (it was once publicly downloadable).
- Keep `.dont-remove-me` — it is a hosting marker file.

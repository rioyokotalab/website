#!/bin/bash
# Deploy the website to www/ on web-o3.noc.titech.ac.jp over SFTP.
#
# Uses the "web" host alias from ~/.ssh/config, which multiplexes over an
# authenticated master connection. If the master has expired, re-open it
# first with:  ssh -fN web   (you will be asked for the password)
#
# Pass --dry-run to preview what would be uploaded without changing anything.
set -euo pipefail
cd "$(dirname "$0")"

DRY_RUN=""
if [ "${1:-}" = "--dry-run" ]; then
	DRY_RUN="--dry-run"
fi

# Make sure the SSH master connection is alive; re-establish it from the
# stored password file if possible, otherwise ask the user to log in.
if ! ssh -O check web >/dev/null 2>&1; then
	if [ -r "$HOME/.ssh/web-password" ]; then
		echo "Re-establishing connection to the web server..."
		SSH_ASKPASS="$HOME/.ssh/web-askpass" SSH_ASKPASS_REQUIRE=force ssh -fN web </dev/null
	else
		echo "No active connection to the web server."
		echo "Run:  ssh -fN web   (enter the password), then re-run this script."
		exit 1
	fi
fi

# mirror -R: local -> remote; uploads new/changed files only.
# Never uploads .git or repo-only files (this script, CLAUDE.md, .gitignore,
# cv.tex/cv.cls/build-cv.sh — only the built cv.pdf is served).
# --delete: files removed locally are also removed from the remote, so the
# server stays an exact mirror of the deployed set. Excluded paths (-x below)
# are never uploaded AND never deleted remotely.
lftp -e "mirror -R --delete --verbose $DRY_RUN -x '^\.git/' -x '^\.claude/' -x '^tools/' -x '^deploy\.sh$' -x '^publish\.sh$' -x '^CLAUDE\.md$' -x '^README\.md$' -x '^\.gitignore$' -x '^\.mcp\.json$' -x '^cv/cv\.tex$' -x '^cv/cv\.cls$' -x '^cv/build-cv\.sh$' . www; bye" sftp://web

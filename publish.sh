#!/bin/bash
# Publish the website: deploy to the web server, then commit and push to GitHub.
#
# Workflow:
#   1. Edit files, preview locally:
#        python3 -m http.server 8000   ->  http://localhost:8000/jp/index.html
#   2. When it looks good:
#        ./publish.sh "what you changed"
#      (the message is optional; a generic one is used if omitted)
#
# The script shows what changed, asks once for confirmation, then uploads
# and pushes. Nothing happens without the confirmation.
set -euo pipefail
cd "$(dirname "$0")"

# The web server allows password auth only; deploys ride on a pre-authenticated
# SSH master connection. deploy.sh re-establishes it automatically from
# ~/.ssh/web-password if it has expired, so no check is needed here.

echo "== Uncommitted changes =="
if git status --porcelain | grep -q .; then
	git status --short
else
	echo "(none)"
fi

echo
echo "== Files that would be uploaded =="
./deploy.sh --dry-run

echo
read -r -p "Deploy to the web server and push to GitHub? [y/N] " answer
[ "$answer" = "y" ] || { echo "Aborted — nothing was changed."; exit 0; }

echo
echo "== Deploying =="
./deploy.sh

echo
echo "== Committing and pushing =="
if git status --porcelain | grep -q .; then
	git add -A
	git commit -m "${1:-Update website content}"
	git push
else
	echo "Nothing new to commit."
fi

echo
echo "Published. Check https://www.rio.scrc.iir.isct.ac.jp/"

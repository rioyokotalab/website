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

# If this publish touches the Achievements page or the personal CV page,
# export any new Rio Yokota items for researchmap. Runs before the commit
# so the updated tools/researchmap-state.json rides in the same commit.
RESEARCHMAP_NEW=0
if git status --porcelain | grep -qE "achievements/index.html|member/yokota.html"; then
	echo
	echo "== researchmap mirror =="
	rm -f tools/out/researchmap-import.jsonl
	python3 tools/researchmap-export.py
	[ -s tools/out/researchmap-import.jsonl ] && RESEARCHMAP_NEW=1
fi

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
if [ "$RESEARCHMAP_NEW" = "1" ]; then
	echo
	echo "New publications were exported for researchmap:"
	echo "  1. Download: http://localhost:8000/tools/out/researchmap-import.jsonl"
	echo "  2. Upload at: https://researchmap.jp/  設定 > インポート"
	echo "(FIS syncs from researchmap automatically.)"
fi

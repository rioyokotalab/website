#!/bin/bash
# Publish the website: preflight, commit/push to GitHub, then deploy.
#
# Workflow:
#   1. Edit files, preview locally:
#        python3 -m http.server 8000   ->  http://localhost:8000/jp/index.html
#   2. When it looks good:
#        ./publish.sh "what you changed"
#      (the message is optional; a generic one is used if omitted)
#
# The script rebases on origin/main, rejects known placeholders, shows the
# deletion-bearing deploy preview, asks once, then commits/pushes before upload.
set -euo pipefail
cd "$(dirname "$0")"

phase="startup"

on_error() {
	local status="$1"
	trap - ERR
	echo >&2
	case "$phase" in
		"GitHub push")
			echo "FAILED during GitHub push. No live deployment was attempted." >&2
			;;
		"live deployment")
			echo "FAILED during live deployment after GitHub push completed." >&2
			echo "The live site may be partially updated; diagnose and rerun publish.sh." >&2
			;;
		*)
			echo "FAILED during $phase. No live deployment was attempted." >&2
			;;
	esac
	exit "$status"
}
trap 'on_error $?' ERR

die_preflight() {
	echo "Preflight refused: $*" >&2
	exit 1
}

is_deploy_included() {
	case "$1" in
		.htaccess|index.html|style.css|en/*|jp/*|images/*|js/*|cv/cv.pdf)
			return 0
			;;
		*)
			return 1
			;;
	esac
}

check_placeholders() {
	local file
	local found=0
	while IFS= read -r file; do
		if is_deploy_included "$file" && [ -f "$file" ] && grep -Iq . "$file" && grep -qF 'G-XXXXXXXXXX' "$file"; then
			echo "  $file" >&2
			found=1
		fi
	done < <(git ls-files --cached --others --exclude-standard)
	[ "$found" -eq 0 ] || die_preflight "deploy-included files contain G-XXXXXXXXXX"
}

phase="branch check"
branch=$(git symbolic-ref --quiet --short HEAD) || die_preflight "detached HEAD"
[ "$branch" = "main" ] || die_preflight "publish must run from main (current: $branch)"
git remote get-url origin >/dev/null || die_preflight "origin remote is missing"

echo "== Rebasing on origin/main =="
phase="preflight rebase"
if ! SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-$HOME/.ssh/agent.sock}" git pull --rebase --autostash origin main; then
	git rebase --abort >/dev/null 2>&1 || true
	echo "FAILED during preflight rebase. Rebase was aborted; no deploy was attempted." >&2
	exit 1
fi

echo
echo "== Placeholder check =="
phase="placeholder check"
check_placeholders
echo "No known deploy-included placeholders found."

echo
echo "== Security regression check =="
phase="security regression check"
tools/test-security.sh

echo
echo "== Uncommitted changes =="
if git status --porcelain | grep -q .; then
	git status --short
else
	echo "(none)"
fi

echo
echo "== Files that would be uploaded =="
phase="deploy dry-run"
./deploy.sh --dry-run

echo
read -r -p "Commit/push to GitHub, then deploy to the web server? [y/N] " answer
[ "$answer" = "y" ] || { echo "Aborted — no commit, push, or live deployment was attempted."; exit 0; }

echo
echo "== Committing =="
phase="commit"
if git status --porcelain | grep -q .; then
	git add -A
	if ! git diff --cached --quiet; then
		git commit -m "${1:-Update website content}"
	fi
else
	echo "Working tree is clean; existing commits will still be pushed."
fi

echo
echo "== Pushing to GitHub =="
phase="GitHub push"
SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-$HOME/.ssh/agent.sock}" git push origin main

echo
echo "== Deploying =="
phase="live deployment"
./deploy.sh

phase="completion"
echo
echo "Published and pushed. Check https://www.rio.scrc.iir.isct.ac.jp/"

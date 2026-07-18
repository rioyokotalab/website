#!/bin/bash
# Isolated positive-allowlist and deletion tests. No network or live deploy.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP_ROOT=${TMPDIR:-/tmp}
TMP=$(mktemp -d "$TMP_ROOT/website-deploy-test.XXXXXX")
cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	if [ -d "$TMP" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$TMP_ROOT" "$TMP" "$TMP_ROOT" \
			>/dev/null || cleanup_failed=1
	fi
	if [ "$status" -eq 0 ] && [ "$cleanup_failed" -ne 0 ]; then
		status=1
	fi
	exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
SRC="$TMP/source"
STAGE="$TMP/stage"
REMOTE="$TMP/remote"

mkdir -p "$SRC"/{en,jp,images,js,cv,tools} "$STAGE" "$REMOTE/en"
cp "$ROOT/.htaccess" "$SRC/.htaccess"
touch "$SRC/index.html" "$SRC/robots.txt" "$SRC/sitemap.xml" "$SRC/style.css" "$SRC/en/index.html" \
	"$SRC/jp/index.html" "$SRC/images/public.png" "$SRC/js/public.js" \
	"$SRC/cv/cv.pdf" "$SRC/README.md" "$SRC/package.json" \
	"$SRC/tools/private.txt" "$SRC/unexpected-root.html"

"$ROOT/tools/stage-public-site.sh" "$STAGE" "$SRC"

for allowed in .htaccess index.html robots.txt sitemap.xml style.css en/index.html jp/index.html \
	images/public.png js/public.js cv/cv.pdf; do
	test -e "$STAGE/$allowed"
done
for blocked in README.md package.json tools/private.txt unexpected-root.html; do
	test ! -e "$STAGE/$blocked"
done

touch "$REMOTE/.dont-remove-me" "$REMOTE/rogue-root.html" \
	"$REMOTE/en/obsolete.html"
"$ROOT/tools/validated-lftp-mirror.sh" "$STAGE" "$REMOTE" file:/// >/dev/null

test -e "$REMOTE/.dont-remove-me"
test ! -e "$REMOTE/rogue-root.html"
test ! -e "$REMOTE/en/obsolete.html"
test -e "$REMOTE/en/index.html"

mkdir -p "$REMOTE/recursive-old"
touch "$REMOTE/recursive-old/hidden"
if "$ROOT/tools/validated-lftp-mirror.sh" --dry-run "$STAGE" "$REMOTE" file:/// \
	>"$TMP/recursive-delete.out" 2>&1; then
	echo "recursive directory deletion was not refused" >&2
	exit 1
fi
test -e "$REMOTE/recursive-old/hidden"

if "$ROOT/tools/guarded-tree-cleanup.sh" /home "$HOME" "${TMPDIR:-/tmp}" \
	>"$TMP/home-cleanup.out" 2>&1; then
	echo "guarded cleanup accepted the account home" >&2
	exit 1
fi
test -d "$HOME"

# SFTP preview format: lftp narrates an in-place update as
# "Removing old file X" + "Transferring file X" (no rm command line), which the
# earlier command-count check mis-read as an unmatched deletion. Cover both the
# update format and true deletions directly against the validator.
VP="$ROOT/tools/validate-lftp-preview.py"
expect_deletions() {  # expected_count preview_file
	got=$(python3 "$VP" preview "$2") || { echo "validator failed on $2" >&2; exit 1; }
	[ "$got" = "deletions=$1 max=250" ] || { echo "expected deletions=$1, got '$got'" >&2; exit 1; }
}
expect_refused() {  # marker preview_file
	if python3 "$VP" preview "$2" >"$TMP/vp.out" 2>&1; then
		echo "validator did not refuse $2" >&2; exit 1
	fi
	grep -qF "$1" "$TMP/vp.out" || { echo "missing refusal '$1' for $2" >&2; exit 1; }
}
# Update-only (remove + retransfer, same paths) => 0 net deletions.
printf 'Removing old file `.htaccess'\''\nTransferring file `.htaccess'\''\nRemoving old file `style.css'\''\nTransferring file `style.css'\''\n' \
	>"$TMP/upd.txt"
expect_deletions 0 "$TMP/upd.txt"
# Mixed: one update, one true deletion => 1 deletion.
printf 'Removing old file `en/index.html'\''\nTransferring file `en/index.html'\''\nRemoving old file `rogue.html'\''\n' \
	>"$TMP/mixed.txt"
expect_deletions 1 "$TMP/mixed.txt"
# True deletions (no matching transfer) are counted.
printf 'Removing old file `a.html'\''\nRemoving old file `b/c.html'\''\n' >"$TMP/del.txt"
expect_deletions 2 "$TMP/del.txt"
# Sentinel, recursive directory, and traversal deletions are refused.
printf 'Removing old file `.dont-remove-me'\''\n' >"$TMP/sent.txt"
expect_refused "sentinel" "$TMP/sent.txt"
printf 'Removing old directory `stale'\''\n' >"$TMP/dir.txt"
expect_refused "directory deletion is forbidden" "$TMP/dir.txt"
printf 'Removing old file `../escape'\''\n' >"$TMP/trav.txt"
expect_refused "unsafe remote deletion path" "$TMP/trav.txt"

echo "PASS: deploy staging is allowlisted; remote sentinel is preserved; rogue files are removed"

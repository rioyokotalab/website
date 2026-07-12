#!/bin/bash
# Isolated positive-allowlist and deletion tests. No network or live deploy.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
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
lftp -e "mirror -R --delete --verbose -x '^\.dont-remove-me$' '$STAGE' '$REMOTE'; bye" file:/// >/dev/null

test -e "$REMOTE/.dont-remove-me"
test ! -e "$REMOTE/rogue-root.html"
test ! -e "$REMOTE/en/obsolete.html"
test -e "$REMOTE/en/index.html"
echo "PASS: deploy staging is allowlisted; remote sentinel is preserved; rogue files are removed"

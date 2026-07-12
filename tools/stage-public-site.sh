#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST=${1:?Usage: stage-public-site.sh DEST [SOURCE_ROOT]}
SOURCE=${2:-$ROOT}

mkdir -p "$DEST"
[ -z "$(find "$DEST" -mindepth 1 -print -quit)" ] || {
	echo "Staging destination is not empty: $DEST" >&2
	exit 1
}

rsync -a --delete --filter="merge $ROOT/tools/deploy-files.filter" "$SOURCE/" "$DEST/"

if find "$DEST" -type l -print -quit | grep -q .; then
	echo "Public staging tree contains a symlink; refusing deployment." >&2
	exit 1
fi

for required in .htaccess index.html style.css en jp images js cv/cv.pdf; do
	[ -e "$DEST/$required" ] || {
		echo "Required public path is missing from staging: $required" >&2
		exit 1
	}
done

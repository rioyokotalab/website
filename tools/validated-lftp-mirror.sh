#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then
	DRY_RUN=1
	shift
fi
[ "$#" -eq 3 ] || { echo "Usage: validated-lftp-mirror.sh [--dry-run] SOURCE DEST ENDPOINT" >&2; exit 2; }
SOURCE=$1
DEST=$2
ENDPOINT=$3

SOURCE=$(realpath -e -- "$SOURCE")
[ -d "$SOURCE" ] && [ ! -L "$SOURCE" ] || { echo "Mirror source is not a real directory" >&2; exit 2; }
case "$SOURCE:$DEST:$ENDPOINT" in *"'"*|*$'\n'*|*$'\r'*)
	echo "Mirror arguments contain unsafe quoting or control characters" >&2
	exit 2
esac
case "$ENDPOINT" in sftp://web|file:///) ;;
	*) echo "Unsupported mirror endpoint: $ENDPOINT" >&2; exit 2 ;;
esac
if [ "$ENDPOINT" = sftp://web ]; then
	[ "$DEST" = www ] || { echo "Live mirror destination must be www" >&2; exit 2; }
else
	case "$DEST" in /*) ;;
		*) echo "File mirror destination must be absolute" >&2; exit 2 ;;
	esac
	DEST=$(realpath -e -- "$DEST")
	[ -d "$DEST" ] && [ ! -L "$DEST" ] || { echo "File mirror destination is not a real directory" >&2; exit 2; }
fi

TMP_ROOT=${TMPDIR:-/tmp}
STATE=$(mktemp -d "$TMP_ROOT/website-lftp-state.XXXXXX")
cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	if [ -d "$STATE" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$TMP_ROOT" "$STATE" "$TMP_ROOT" \
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

snapshot_before=$(python3 "$ROOT/tools/validate-lftp-preview.py" snapshot "$SOURCE")
for pass in 1 2; do
	preview=$STATE/preview-$pass.txt
	lftp -e "mirror -R --delete --verbose --dry-run -x '^\.dont-remove-me$' '$SOURCE' '$DEST'; bye" \
		"$ENDPOINT" >"$preview"
	python3 "$ROOT/tools/validate-lftp-preview.py" preview "$preview" >"$STATE/validation-$pass.txt"
	[ "$(python3 "$ROOT/tools/validate-lftp-preview.py" snapshot "$SOURCE")" = "$snapshot_before" ] || {
		echo "Mirror source changed during validation" >&2
		exit 1
	}
done
cmp -s "$STATE/preview-1.txt" "$STATE/preview-2.txt" || {
	echo "Mirror previews changed between validation passes" >&2
	exit 1
}
cmp -s "$STATE/validation-1.txt" "$STATE/validation-2.txt" || {
	echo "Mirror deletion validations disagree" >&2
	exit 1
}
preview_hash=$(sha256sum "$STATE/preview-1.txt" | awk '{print $1}')
echo "VALIDATED mirror source=($snapshot_before) $(cat "$STATE/validation-1.txt") preview_sha256=$preview_hash passes=2"
cat "$STATE/preview-1.txt"

if [ "$DRY_RUN" -eq 0 ]; then
	[ "$(python3 "$ROOT/tools/validate-lftp-preview.py" snapshot "$SOURCE")" = "$snapshot_before" ] || {
		echo "Mirror source changed before apply" >&2
		exit 1
	}
	lftp -e "mirror -R --delete --verbose -x '^\.dont-remove-me$' '$SOURCE' '$DEST'; bye" \
		"$ENDPOINT"
fi

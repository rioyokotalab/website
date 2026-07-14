#!/bin/sh
set -eu

usage() {
	echo "Usage: guarded-tree-cleanup.sh WITHIN TARGET STATE_DIR" >&2
	exit 2
}

[ "$#" -eq 3 ] || usage
WITHIN=$1
TARGET=$2
STATE_DIR=$3
HARNESS=${HARNESS_BIN:-$HOME/harness/bin/harness}

case "$HARNESS:$WITHIN:$TARGET:$STATE_DIR" in
	/*:/*:/*:/*) ;;
	*) usage ;;
esac
[ -x "$HARNESS" ] || { echo "Guarded-delete harness is unavailable: $HARNESS" >&2; exit 2; }
for directory in "$WITHIN" "$TARGET" "$STATE_DIR"; do
	[ -d "$directory" ] && [ ! -L "$directory" ] || {
		echo "Cleanup path is not a real directory: $directory" >&2
		exit 2
	}
done

WITHIN=$(realpath -e -- "$WITHIN")
TARGET=$(realpath -e -- "$TARGET")
STATE_DIR=$(realpath -e -- "$STATE_DIR")
prefix=$STATE_DIR/.website-guarded-cleanup.$$
manifest=$prefix.manifest
plan_output=$prefix.plan
umask 077

remove_exact_state() {
	path=$1
	[ -e "$path" ] || [ -L "$path" ] || return 0
	[ -f "$path" ] && [ ! -L "$path" ] || return 1
	[ "$(realpath -e -- "$path")" = "$path" ] || return 1
	[ "$(stat -c '%u' -- "$path")" = "$(id -u)" ] || return 1
	unlink "$path"
}

cleanup_state() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	remove_exact_state "$plan_output" || cleanup_failed=1
	remove_exact_state "$manifest" || cleanup_failed=1
	if [ "$status" -eq 0 ] && [ "$cleanup_failed" -ne 0 ]; then
		status=1
	fi
	exit "$status"
}

trap cleanup_state EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

[ ! -e "$manifest" ] && [ ! -L "$manifest" ] || {
	echo "Cleanup manifest path already exists: $manifest" >&2
	exit 2
}
[ ! -e "$plan_output" ] && [ ! -L "$plan_output" ] || {
	echo "Cleanup plan path already exists: $plan_output" >&2
	exit 2
}

"$HARNESS" guarded-delete plan --within "$WITHIN" \
	--manifest "$manifest" -- "$TARGET" >"$plan_output"
token=$(sed -n 's/^TOKEN sha256=//p' "$plan_output")
[ -n "$token" ] || { echo "Cleanup plan emitted no token" >&2; exit 2; }
"$HARNESS" guarded-delete apply --manifest "$manifest" --token "$token"
[ ! -e "$TARGET" ] && [ ! -L "$TARGET" ] || {
	echo "Cleanup target remains: $TARGET" >&2
	exit 2
}
echo "Guarded cleanup verified: $TARGET"

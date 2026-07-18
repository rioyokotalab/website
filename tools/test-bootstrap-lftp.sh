#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
BOOTSTRAP=$ROOT/tools/bootstrap-lftp.sh
TMP_ROOT=${TMPDIR:-/tmp}
TEST_ROOT=$(mktemp -d "$TMP_ROOT/website-lftp-bootstrap-test.XXXXXX")

cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	if [ -d "$TEST_ROOT" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$TMP_ROOT" "$TEST_ROOT" \
			"$TMP_ROOT" >/dev/null || cleanup_failed=1
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

sh -n "$BOOTSTRAP"
"$BOOTSTRAP" doctor >"$TEST_ROOT/doctor.out"
grep -F 'LFTP_DOCTOR status=pass' "$TEST_ROOT/doctor.out" >/dev/null
env PATH=/usr/bin:/bin WEBSITE_LFTP_PREFIX="$TEST_ROOT/prefix" \
	"$BOOTSTRAP" plan >"$TEST_ROOT/plan.out"
grep -F 'action=install' "$TEST_ROOT/plan.out" >/dev/null
grep -F 'sha256=60140fcd971e86f0be1cea9d206a4cdf9baead70cb65adcc09403c6294290b72' \
	"$TEST_ROOT/plan.out" >/dev/null
grep -F 'member=./usr/bin/lftp' "$TEST_ROOT/plan.out" >/dev/null
[ ! -e "$TEST_ROOT/prefix" ] || {
	echo 'FAIL: read-only lftp plan changed its prefix' >&2
	exit 1
}
echo 'PASS: lftp doctor and rootless pinned plan'

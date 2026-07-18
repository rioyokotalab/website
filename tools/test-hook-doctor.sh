#!/bin/sh
# Offline coverage for tools/hook-doctor.sh and the canonical pre-commit hook.
# All writes go to a temporary hooks directory; the real .git is never touched.
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
DOCTOR=$ROOT/tools/hook-doctor.sh
CANONICAL=$ROOT/tools/hooks/pre-commit
TMP_ROOT=${TMPDIR:-/tmp}
TEST_ROOT=$(mktemp -d "$TMP_ROOT/website-hook-doctor-test.XXXXXX")
HOOKS_DIR=$TEST_ROOT/hooks
LIVE=$HOOKS_DIR/pre-commit
OUT=$TEST_ROOT/out.txt

fail() {
	echo "FAIL: $*" >&2
	exit 1
}

cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	if [ -d "$TEST_ROOT" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$TMP_ROOT" "$TEST_ROOT" \
			"$TMP_ROOT" >/dev/null || cleanup_failed=1
	fi
	if [ "$status" -eq 0 ] && [ "$cleanup_failed" -ne 0 ]; then
		echo "FAIL: hook-doctor suite cleanup" >&2
		status=1
	fi
	exit "$status"
}
trap cleanup EXIT HUP INT TERM

expect_doctor() {
	expected_exit=$1
	expected_text=$2
	rc=0
	HOOK_DOCTOR_HOOKS_DIR=$HOOKS_DIR "$DOCTOR" doctor >"$OUT" 2>&1 || rc=$?
	[ "$rc" -eq "$expected_exit" ] ||
		fail "doctor exit $rc, expected $expected_exit ($expected_text)"
	grep -F -- "$expected_text" "$OUT" >/dev/null ||
		fail "doctor output missing '$expected_text'"
}

# 1. The canonical hook is tracked, executable, and passes from the repo root.
[ -f "$CANONICAL" ] || fail "canonical hook missing"
[ -x "$CANONICAL" ] || fail "canonical hook not executable"
grep -F 'check-claude-size' "$CANONICAL" >/dev/null &&
	fail "canonical hook must not reference the removed checker"
(cd "$ROOT" && sh "$CANONICAL" >"$OUT" 2>&1) ||
	fail "canonical hook failed in repository: $(cat "$OUT")"
grep -F 'check-md-size: OK' "$OUT" >/dev/null ||
	fail "canonical hook did not run the size gate"

# 2. Missing live hook: doctor reports and fails without writing.
mkdir -p "$HOOKS_DIR"
expect_doctor 1 "missing"
[ ! -e "$LIVE" ] || fail "doctor wrote to the hooks directory"

# 3. Stale live hook (the pre-T-190 form): doctor detects it.
printf '%s\n' '#!/bin/sh' \
	'python3 tools/check-claude-size.py || exit 1' \
	'python3 tools/check-md-size.py || exit 1' 'exit 0' >"$LIVE"
chmod 755 "$LIVE"
expect_doctor 1 "stale"

# 4. Apply: backs up the stale hook, installs an executable exact copy.
HOOK_DOCTOR_HOOKS_DIR=$HOOKS_DIR "$DOCTOR" apply >"$OUT" 2>&1 ||
	fail "apply failed: $(cat "$OUT")"
cmp -s "$CANONICAL" "$LIVE" || fail "applied hook differs from canonical"
[ -x "$LIVE" ] || fail "applied hook not executable"
[ -f "$LIVE.pre-apply-backup" ] || fail "apply did not keep a backup"
grep -F 'check-claude-size' "$LIVE.pre-apply-backup" >/dev/null ||
	fail "backup does not preserve the previous hook"
expect_doctor 0 "ok"

# 5. Re-apply is a no-op on a healthy hook.
HOOK_DOCTOR_HOOKS_DIR=$HOOKS_DIR "$DOCTOR" apply >"$OUT" 2>&1 ||
	fail "re-apply failed"
grep -F 'nothing to do' "$OUT" >/dev/null || fail "re-apply was not a no-op"

# 6. Matching content without the executable bit is rejected.
chmod 644 "$LIVE"
expect_doctor 1 "not-executable"
chmod 755 "$LIVE"

# 7. Rollback restores the pre-apply hook exactly.
HOOK_DOCTOR_HOOKS_DIR=$HOOKS_DIR "$DOCTOR" rollback >"$OUT" 2>&1 ||
	fail "rollback failed: $(cat "$OUT")"
grep -F 'check-claude-size' "$LIVE" >/dev/null ||
	fail "rollback did not restore the previous hook"
expect_doctor 1 "stale"

# 8. Rollback without a recorded backup fails closed.
rm -f "$LIVE.pre-apply-backup"
rc=0
HOOK_DOCTOR_HOOKS_DIR=$HOOKS_DIR "$DOCTOR" rollback >"$OUT" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "rollback without backup unexpectedly succeeded"
grep -F 'no backup' "$OUT" >/dev/null || fail "missing no-backup evidence"

echo "test-hook-doctor: OK (8 checks)"

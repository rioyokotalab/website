#!/bin/sh
# Verify, install, or roll back the local pre-commit hook against the tracked
# canonical copy at tools/hooks/pre-commit.
#
#   tools/hook-doctor.sh [doctor]   read-only status check (default)
#   tools/hook-doctor.sh apply      back up any existing hook, install canonical
#   tools/hook-doctor.sh rollback   restore the pre-apply backup
#
# `doctor` never writes. `apply` and `rollback` write inside .git/hooks and are
# owner-run commands; agents report doctor output and hand off the exact apply
# command instead. HOOK_DOCTOR_HOOKS_DIR overrides the hooks directory so tests
# never touch the real repository hooks.
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
CANONICAL=$ROOT/tools/hooks/pre-commit
HOOKS_DIR=${HOOK_DOCTOR_HOOKS_DIR:-$ROOT/.git/hooks}
LIVE=$HOOKS_DIR/pre-commit
BACKUP=$LIVE.pre-apply-backup

fail() {
	echo "hook-doctor: $*" >&2
	exit 1
}

[ -f "$CANONICAL" ] || fail "canonical hook missing: $CANONICAL"

live_status() {
	if [ ! -e "$LIVE" ]; then
		echo missing
	elif ! cmp -s "$CANONICAL" "$LIVE"; then
		echo stale
	elif [ ! -x "$LIVE" ]; then
		echo not-executable
	else
		echo ok
	fi
}

doctor() {
	status=$(live_status)
	echo "hook-doctor: live pre-commit hook is $status ($LIVE)"
	[ "$status" = ok ] && return 0
	echo "hook-doctor: install with:   tools/hook-doctor.sh apply"
	echo "hook-doctor: roll back with: tools/hook-doctor.sh rollback"
	return 1
}

apply() {
	if [ "$(live_status)" = ok ]; then
		echo "hook-doctor: live hook already matches canonical; nothing to do"
		return 0
	fi
	mkdir -p "$HOOKS_DIR"
	if [ -e "$LIVE" ]; then
		cp -p "$LIVE" "$BACKUP"
		echo "hook-doctor: backed up previous hook to $BACKUP"
	fi
	cp "$CANONICAL" "$LIVE"
	chmod 755 "$LIVE"
	doctor
}

rollback() {
	[ -f "$BACKUP" ] ||
		fail "no backup at $BACKUP; nothing recorded to restore"
	cp -p "$BACKUP" "$LIVE"
	echo "hook-doctor: restored previous hook from $BACKUP"
	doctor || true
}

case "${1:-doctor}" in
	doctor) doctor ;;
	apply) apply ;;
	rollback) rollback ;;
	*)
		echo "Usage: tools/hook-doctor.sh [doctor|apply|rollback]" >&2
		exit 2
		;;
esac

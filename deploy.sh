#!/bin/bash
# Deploy the website to www/ on web-o3.noc.titech.ac.jp over SFTP.
#
# Uses the "web" host alias from ~/.ssh/config, which multiplexes over an
# authenticated master connection. If the master has expired, re-open it
# first with:  ssh -fN web   (you will be asked for the password)
#
# Pass --dry-run to preview what would be uploaded without changing anything.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT"

DRY_RUN=""
if [ "${1:-}" = "--dry-run" ]; then
	DRY_RUN="--dry-run"
fi

# Build a fresh positive-allowlist staging tree. Anything not selected by
# tools/deploy-files.filter cannot be uploaded, even if it is untracked or a
# future repository file that nobody remembered to exclude.
TMP_ROOT=${TMPDIR:-/tmp}
STAGE=$(mktemp -d "$TMP_ROOT/website-deploy.XXXXXX")
cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	if [ -d "$STAGE" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$TMP_ROOT" "$STAGE" "$TMP_ROOT" \
			>/dev/null || cleanup_failed=1
	fi
	if [ "$status" -eq 0 ] && [ "$cleanup_failed" -ne 0 ]; then
		echo "FAILED: guarded deployment staging cleanup" >&2
		status=1
	fi
	exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
tools/stage-public-site.sh "$STAGE" "$ROOT"

# Make sure the SSH master connection is alive; re-establish it from the
# stored password file if possible, otherwise ask the user to log in.
if ! ssh -O check web >/dev/null 2>&1; then
	if [ -r "$HOME/.ssh/web-password" ]; then
		echo "Re-establishing connection to the web server..."
		SSH_ASKPASS="$HOME/.ssh/web-askpass" SSH_ASKPASS_REQUIRE=force ssh -fN web </dev/null
	else
		echo "No active connection to the web server."
		echo "Run:  ssh -fN web   (enter the password), then re-run this script."
		exit 1
	fi
fi

# The wrapper snapshots the allowlisted source, validates two identical dry
# runs, bounds file deletion, rejects recursive directory deletion, and then
# applies without an approval prompt. The server sentinel remains excluded.
if [ -n "$DRY_RUN" ]; then
	tools/validated-lftp-mirror.sh --dry-run "$STAGE" www sftp://web
else
	tools/validated-lftp-mirror.sh "$STAGE" www sftp://web
fi

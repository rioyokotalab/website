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
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
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

# mirror -R: allowlisted staging tree -> remote. --delete removes anything
# outside the public manifest from www, except the required server sentinel.
lftp -e "mirror -R --delete --verbose $DRY_RUN -x '^\.dont-remove-me$' '$STAGE' www; bye" sftp://web

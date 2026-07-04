#!/bin/bash
# Deploy the website to www/ on web-o3.noc.titech.ac.jp over SFTP.
#
# Uses the "web" host alias from ~/.ssh/config, which multiplexes over an
# authenticated master connection. If the master has expired, re-open it
# first with:  ssh -fN web   (you will be asked for the password)
#
# Pass --dry-run to preview what would be uploaded without changing anything.
set -euo pipefail
cd "$(dirname "$0")"

DRY_RUN=""
if [ "${1:-}" = "--dry-run" ]; then
	DRY_RUN="--dry-run"
fi

# mirror -R: local -> remote; uploads new/changed files only.
# Never uploads .git or this script. Does NOT delete remote files
# that were removed locally — add --delete below if you want that.
lftp -e "mirror -R --verbose $DRY_RUN -x '^\.git/' -x '^deploy\.sh$' . www; bye" sftp://web

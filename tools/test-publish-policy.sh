#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() {
	printf 'FAIL: %s\n' "$*" >&2
	exit 1
}

POLICY=skills/publish-and-verify.md

for token in \
	'current process `SSH_AUTH_SOCK`' \
	'current-user-owned' \
	'Unix socket' \
	'git pull --rebase --autostash origin main' \
	"tmux's" \
	'anything under `~/.ssh`'
do
	grep -F "$token" "$POLICY" >/dev/null ||
		fail "missing process-scoped SSH-agent contract: $token"
done

if grep -F '$HOME/.ssh/agent.sock' "$POLICY" >/dev/null; then
	fail 'publication policy still hardcodes the obsolete SSH-agent socket'
fi

printf '%s\n' 'PASS: website process-scoped SSH-agent policy'

#!/bin/bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
tmp=$(mktemp -d)
cleanup() {
	for clone in a b; do
		CLAUDE_PROJECT_DIR="$tmp/$clone" "$root/tools/preview-server.sh" stop 2>/dev/null || true
	done
	rm -rf "$tmp"
}
trap cleanup EXIT

for clone in a b; do
	mkdir -p "$tmp/$clone/.claude"
done

CLAUDE_PROJECT_DIR="$tmp/a" YOKOTA_PREVIEW_PORT=18761 "$root/tools/preview-server.sh" start
CLAUDE_PROJECT_DIR="$tmp/b" YOKOTA_PREVIEW_PORT=18762 "$root/tools/preview-server.sh" start
pid_a=$(cat "$tmp/a/.claude/http-server.pid")
pid_b=$(cat "$tmp/b/.claude/http-server.pid")
test "$pid_a" != "$pid_b"
kill -0 "$pid_a"
kill -0 "$pid_b"

# A stale/corrupt PID file in clone A must not control clone B's server.
printf '%s\n' "$pid_b" > "$tmp/a/.claude/http-server.pid"
CLAUDE_PROJECT_DIR="$tmp/a" "$root/tools/preview-server.sh" stop
kill -0 "$pid_a"
kill -0 "$pid_b"
test -f "$tmp/b/.claude/http-server.pid"

printf '%s\n' "$pid_a" > "$tmp/a/.claude/http-server.pid"
CLAUDE_PROJECT_DIR="$tmp/a" "$root/tools/preview-server.sh" stop
! kill -0 "$pid_a" 2>/dev/null

CLAUDE_PROJECT_DIR="$tmp/b" "$root/tools/preview-server.sh" stop
! kill -0 "$pid_b" 2>/dev/null
echo "PASS: concurrent clone preview processes are isolated"

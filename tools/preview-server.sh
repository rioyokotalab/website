#!/bin/bash
set -euo pipefail

action=${1:-}
root=${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}
state_dir="$root/.claude"
pid_file="$state_dir/http-server.pid"
port_file="$state_dir/http-server.port"
port=${YOKOTA_PREVIEW_PORT:-8000}

owned_preview() {
	local pid=$1
	[ -n "$pid" ] &&
		grep -qa "http.server" "/proc/$pid/cmdline" 2>/dev/null &&
		[ "$(readlink -f "/proc/$pid/cwd" 2>/dev/null || true)" = "$(readlink -f "$root")" ]
}

case "$action" in
	start)
		mkdir -p "$state_dir"
		if [ -f "$pid_file" ] && owned_preview "$(cat "$pid_file")"; then
			exit 0
		fi
		cd "$root"
		nohup python3 -m http.server "$port" --bind 127.0.0.1 >/dev/null 2>&1 &
		pid=$!
		sleep 0.2
		if ! kill -0 "$pid" 2>/dev/null; then
			wait "$pid" || true
			echo "Could not start preview server on 127.0.0.1:$port" >&2
			exit 1
		fi
		printf '%s\n' "$pid" > "$pid_file"
		printf '%s\n' "$port" > "$port_file"
		;;
	stop)
		if [ -f "$pid_file" ]; then
			pid=$(cat "$pid_file")
			if owned_preview "$pid"; then
				kill "$pid" 2>/dev/null || true
			fi
			rm -f "$pid_file" "$port_file"
		fi
		;;
	*)
		echo "Usage: $0 start|stop" >&2
		exit 2
		;;
esac

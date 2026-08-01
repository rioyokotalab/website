#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
CHECK=$ROOT/tools/ci-browser-scope.py
WORKFLOW=$ROOT/.github/workflows/ci.yml

assert_scope() {
	expected=$1
	shift
	actual=$(printf '%s\0' "$@" | python3 "$CHECK" | sed -n 's/^browser=//p')
	[ "$actual" = "$expected" ] || {
		echo "FAIL: browser scope expected=$expected actual=$actual" >&2
		exit 1
	}
}

assert_scope false TODO.md docs/audit.md tools/state/session.md
assert_scope false README.md AGENTS.md tools/task-metrics.jsonl
assert_scope true en/index.html
assert_scope true tools/test-browser.mjs
assert_scope true .github/workflows/ci.yml
assert_scope true ../outside
actual=$(python3 "$CHECK" </dev/null | sed -n 's/^browser=//p')
[ "$actual" = true ] || {
	echo "FAIL: empty browser scope did not fail closed" >&2
	exit 1
}
grep -F 'git diff --no-renames --name-only -z' "$WORKFLOW" >/dev/null || {
	echo "FAIL: workflow browser scope does not expose rename source paths" >&2
	exit 1
}
[ "$(grep -Fc "if: steps.scope.outputs.browser == 'true'" "$WORKFLOW")" -eq 2 ] || {
	echo "FAIL: workflow browser steps are not both scoped" >&2
	exit 1
}

echo "test-ci-browser-scope: OK (9 checks)"

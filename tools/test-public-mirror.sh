#!/bin/sh
# Offline coverage for tools/build-public-mirror.sh (T-192). Builds a real
# mirror in a temporary directory and verifies sanitization, single-commit
# history, audit gating, and refusal behavior. Local only; no remote.
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
BUILD=$ROOT/tools/build-public-mirror.sh
TMP_ROOT=${TMPDIR:-/tmp}
TEST_ROOT=$(mktemp -d "$TMP_ROOT/website-public-mirror-test.XXXXXX")
MIRROR=$TEST_ROOT/mirror
AUDIT=$TEST_ROOT/audit.json
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
		echo "FAIL: public-mirror suite cleanup" >&2
		status=1
	fi
	exit "$status"
}
trap cleanup EXIT HUP INT TERM

# 1. Relative DEST is refused before any staging.
rc=0
"$BUILD" relative-dest >"$OUT" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "relative DEST unexpectedly accepted"
grep -F 'absolute path' "$OUT" >/dev/null || fail "missing absolute-path error"

# 2. A full build succeeds and reports a clean audit.
"$BUILD" "$MIRROR" "$AUDIT" >"$OUT" 2>&1 ||
	fail "mirror build failed: $(cat "$OUT")"
grep -F 'mirror audit clean' "$OUT" >/dev/null || fail "audit not clean"
grep -F 'publication is a separate owner action' "$OUT" >/dev/null ||
	fail "missing publication boundary notice"

# 3. Exactly one commit, no remotes, provenance README present.
[ "$(git -C "$MIRROR" rev-list --count HEAD)" = 1 ] ||
	fail "mirror history is not a single commit"
[ -z "$(git -C "$MIRROR" remote)" ] || fail "mirror has a configured remote"
grep -F 'no source history' "$MIRROR/README.md" >/dev/null ||
	fail "provenance README missing or wrong"

# 4. Sanitization: server config, tooling, ledger, and CV sources are absent.
for forbidden in .htaccess tools skills docs .github AGENTS.md CLAUDE.md \
	TODO.md publish.sh deploy.sh package.json cv/cv.tex; do
	[ ! -e "$MIRROR/$forbidden" ] || fail "forbidden path in mirror: $forbidden"
done

# 5. Required public content is present.
for required in index.html robots.txt sitemap.xml style.css en jp images js \
	cv/cv.pdf; do
	[ -e "$MIRROR/$required" ] || fail "required path missing: $required"
done

# 6. Audit report is value-free with no credential-category finding.
python3 - "$AUDIT" <<'PY'
import json
import sys

report = json.loads(open(sys.argv[1], encoding="utf-8").read())
assert not report.get("value_exposed"), "audit exposed values"
counts = report.get("finding_counts", {})
bad = {r: c for r, c in counts.items() if c and r != "large-blob"}
assert not bad, f"credential-category findings: {bad}"
PY

# 7. Refusals: non-empty DEST and existing audit output fail closed.
rc=0
"$BUILD" "$MIRROR" "$TEST_ROOT/audit2.json" >"$OUT" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "non-empty DEST unexpectedly accepted"
rc=0
"$BUILD" "$TEST_ROOT/mirror2" "$AUDIT" >"$OUT" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "existing audit output unexpectedly accepted"
grep -F 'Audit output exists' "$OUT" >/dev/null ||
	fail "missing audit-overwrite refusal evidence"

echo "test-public-mirror: OK (7 checks)"

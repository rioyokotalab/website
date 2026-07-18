#!/bin/sh
# Offline coverage for tools/workflow-security-check.py. Verifies the real
# workflows pass and that each hardening invariant is actually enforced against
# a deliberately unsafe fixture. Fixture lives in a temp dir; real .github is
# never touched.
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
CHECK=$ROOT/tools/workflow-security-check.py
TMP_ROOT=${TMPDIR:-/tmp}
TEST_ROOT=$(mktemp -d "$TMP_ROOT/website-workflow-security-test.XXXXXX")
WF=$TEST_ROOT/.github/workflows
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
		echo "FAIL: workflow-security suite cleanup" >&2
		status=1
	fi
	exit "$status"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$WF"

# 1. The real repository workflows pass.
python3 "$CHECK" >"$OUT" 2>&1 || fail "real workflows failed: $(cat "$OUT")"
grep -F 'PASS: workflow security' "$OUT" >/dev/null || fail "no PASS line"

# 2. An unsafe fixture triggers every invariant.
cat > "$WF/bad.yml" <<'EOF'
on:
  pull_request_target:
permissions:
  contents: write
jobs:
  x:
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
EOF
rc=0
WORKFLOW_SECURITY_DIR="$WF" python3 "$CHECK" >"$OUT" 2>&1 || rc=$?
[ "$rc" -eq 1 ] || fail "unsafe fixture did not fail (rc=$rc)"
for needle in \
	"pull_request_target" \
	"permissions are not minimal" \
	"not pinned to a 40-char SHA" \
	"without --ignore-scripts" \
	"persist-credentials: false"; do
	grep -F -- "$needle" "$OUT" >/dev/null || fail "missing finding: $needle"
done

# 3. A hardened fixture passes.
cat > "$WF/bad.yml" <<'EOF'
on:
  pull_request:
permissions: {}
jobs:
  x:
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd
        with:
          persist-credentials: false
      - run: npm ci --ignore-scripts
EOF
WORKFLOW_SECURITY_DIR="$WF" python3 "$CHECK" >"$OUT" 2>&1 ||
	fail "hardened fixture failed: $(cat "$OUT")"
grep -F 'PASS: workflow security' "$OUT" >/dev/null || fail "hardened fixture no PASS"

echo "test-workflow-security: OK (3 checks)"

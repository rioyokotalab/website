#!/bin/bash
# Isolated regression tests for publish.sh. No network, SSH, lftp, or live deploy.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

fail() {
	echo "FAIL: $*" >&2
	exit 1
}

new_case() {
	local name="$1"
	CASE_DIR="$TMP/$name"
	REMOTE="$CASE_DIR/remote.git"
	WORK="$CASE_DIR/work"
	LOG="$CASE_DIR/deploy.log"
	OUTPUT="$CASE_DIR/output.log"
	mkdir -p "$CASE_DIR"
	git init --bare --initial-branch=main "$REMOTE" >/dev/null
	git init --initial-branch=main "$CASE_DIR/seed" >/dev/null
	git -C "$CASE_DIR/seed" config user.name "Publish Test"
	git -C "$CASE_DIR/seed" config user.email "publish-test@example.invalid"
	echo "baseline" > "$CASE_DIR/seed/index.html"
	git -C "$CASE_DIR/seed" add index.html
	git -C "$CASE_DIR/seed" commit -m baseline >/dev/null
	git -C "$CASE_DIR/seed" remote add origin "$REMOTE"
	git -C "$CASE_DIR/seed" push -u origin main >/dev/null
	git clone "$REMOTE" "$WORK" >/dev/null 2>&1
	git -C "$WORK" config user.name "Publish Test"
	git -C "$WORK" config user.email "publish-test@example.invalid"
	cp "$ROOT/publish.sh" "$WORK/publish.sh"
	cat > "$WORK/deploy.sh" <<'EOF'
#!/bin/bash
set -euo pipefail
if [ "${1:-}" = "--dry-run" ]; then
	echo dry-run >> "$PUBLISH_TEST_LOG"
	exit 0
fi
echo deploy >> "$PUBLISH_TEST_LOG"
[ "${PUBLISH_TEST_DEPLOY_FAIL:-0}" != "1" ]
EOF
	chmod +x "$WORK/publish.sh" "$WORK/deploy.sh"
	git -C "$WORK" add publish.sh deploy.sh
	git -C "$WORK" commit -m "install publish test fixture" >/dev/null
}

run_yes() {
	(
		cd "$WORK"
		printf 'y\n' | PUBLISH_TEST_LOG="$LOG" PUBLISH_TEST_DEPLOY_FAIL="${PUBLISH_TEST_DEPLOY_FAIL:-0}" ./publish.sh "test publish"
	) >"$OUTPUT" 2>&1
}

run_no() {
	(
		cd "$WORK"
		printf 'n\n' | PUBLISH_TEST_LOG="$LOG" ./publish.sh "test publish"
	) >"$OUTPUT" 2>&1
}

new_case clean-ahead
echo "ahead" > "$WORK/ahead.txt"
git -C "$WORK" add ahead.txt
git -C "$WORK" commit -m ahead >/dev/null
run_yes
[ "$(git -C "$WORK" rev-parse HEAD)" = "$(git --git-dir="$REMOTE" rev-parse main)" ] || fail "clean ahead commit was not pushed"
[ "$(tr '\n' ' ' < "$LOG")" = "dry-run deploy " ] || fail "clean ahead deploy phases"
grep -q "Working tree is clean; existing commits will still be pushed" "$OUTPUT" || fail "clean ahead message"
echo "PASS: clean worktree still pushes ahead commit and deploys"

new_case rebase-before-confirm
echo "local" > "$WORK/local.txt"
git -C "$WORK" add local.txt
git -C "$WORK" commit -m local >/dev/null
git clone "$REMOTE" "$CASE_DIR/other" >/dev/null 2>&1
git -C "$CASE_DIR/other" config user.name "Publish Test"
git -C "$CASE_DIR/other" config user.email "publish-test@example.invalid"
echo "remote" > "$CASE_DIR/other/remote.txt"
git -C "$CASE_DIR/other" add remote.txt
git -C "$CASE_DIR/other" commit -m remote >/dev/null
git -C "$CASE_DIR/other" push origin main >/dev/null
run_no
git -C "$WORK" merge-base --is-ancestor origin/main HEAD || fail "remote commit was not rebased before confirmation"
[ -f "$WORK/local.txt" ] && [ -f "$WORK/remote.txt" ] || fail "rebase did not retain both changes"
[ "$(tr '\n' ' ' < "$LOG")" = "dry-run " ] || fail "abort should not deploy"
echo "PASS: origin/main rebase occurs before confirmation and abort does not deploy"

new_case rebase-conflict
printf '%s\n' 'local conflict' > "$WORK/index.html"
git -C "$WORK" add index.html
git -C "$WORK" commit -m "local conflict" >/dev/null
git clone "$REMOTE" "$CASE_DIR/other" >/dev/null 2>&1
git -C "$CASE_DIR/other" config user.name "Publish Test"
git -C "$CASE_DIR/other" config user.email "publish-test@example.invalid"
printf '%s\n' 'remote conflict' > "$CASE_DIR/other/index.html"
git -C "$CASE_DIR/other" add index.html
git -C "$CASE_DIR/other" commit -m "remote conflict" >/dev/null
git -C "$CASE_DIR/other" push origin main >/dev/null
if run_no; then
	fail "conflicting rebase unexpectedly succeeded"
fi
grep -q "FAILED during preflight rebase. Rebase was aborted" "$OUTPUT" || fail "rebase conflict message"
[ ! -e "$WORK/.git/rebase-merge" ] && [ ! -e "$WORK/.git/rebase-apply" ] || fail "rebase conflict was left in progress"
[ ! -e "$LOG" ] || fail "rebase conflict reached deploy dry-run"
echo "PASS: conflicting rebase aborts and stops before dry-run"

new_case placeholder
printf '%s\n' 'G-XXXXXXXXXX' >> "$WORK/index.html"
if run_yes; then
	fail "placeholder publish unexpectedly succeeded"
fi
grep -q "deploy-included files contain G-XXXXXXXXXX" "$OUTPUT" || fail "placeholder refusal message"
[ ! -e "$LOG" ] || fail "placeholder refusal reached deploy dry-run"
echo "PASS: deploy-included placeholder is refused before dry-run"

new_case excluded-placeholder
mkdir -p "$WORK/tools"
printf '%s\n' 'G-XXXXXXXXXX' > "$WORK/tools/repo-only-note.txt"
run_no
[ "$(tr '\n' ' ' < "$LOG")" = "dry-run " ] || fail "repo-only placeholder should reach dry-run"
grep -q "Aborted — no commit, push, or live deployment was attempted." "$OUTPUT" || fail "repo-only placeholder was not accepted"
echo "PASS: placeholder in deploy-excluded tools/ does not block preflight"

new_case push-failure
echo "change" > "$WORK/change.txt"
cat > "$REMOTE/hooks/pre-receive" <<'EOF'
#!/bin/sh
exit 1
EOF
chmod +x "$REMOTE/hooks/pre-receive"
if run_yes; then
	fail "rejected push unexpectedly succeeded"
fi
grep -q "FAILED during GitHub push. No live deployment was attempted." "$OUTPUT" || fail "push failure state message"
[ "$(tr '\n' ' ' < "$LOG")" = "dry-run " ] || fail "push failure reached live deploy"
echo "PASS: push failure stops before deploy and reports state"

new_case deploy-failure
echo "change" > "$WORK/change.txt"
PUBLISH_TEST_DEPLOY_FAIL=1
if run_yes; then
	fail "failed deploy unexpectedly succeeded"
fi
unset PUBLISH_TEST_DEPLOY_FAIL
[ "$(git -C "$WORK" rev-parse HEAD)" = "$(git --git-dir="$REMOTE" rev-parse main)" ] || fail "commit was not pushed before deploy failure"
grep -q "FAILED during live deployment after GitHub push completed." "$OUTPUT" || fail "deploy failure state message"
grep -q "live site may be partially updated" "$OUTPUT" || fail "partial live warning"
[ "$(tr '\n' ' ' < "$LOG")" = "dry-run deploy " ] || fail "deploy failure phases"
echo "PASS: deploy failure reports pushed/possibly-partial state"

echo "PASS: publish.sh regression suite"

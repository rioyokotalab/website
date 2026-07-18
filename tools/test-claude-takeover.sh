#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() {
	printf 'FAIL: %s\n' "$*" >&2
	exit 1
}

[ -f CLAUDE.md ] && [ ! -L CLAUDE.md ] ||
	fail 'root Claude guidance must be a regular repository-owned file'
[ "$(sed -n '1p' CLAUDE.md)" = '@AGENTS.md' ] ||
	fail 'Claude guidance does not import root project policy first'
[ "$(grep -Fxc '@AGENTS.md' CLAUDE.md)" -eq 1 ] ||
	fail 'Claude guidance must import root project policy exactly once'

for token in \
	'# Claude client compatibility' \
	'`driver: claude`' \
	'`--agent claude`' \
	'A bounded Claude dispatch is a WORKER' \
	'Do not import or invoke a sibling control repository'
do
	grep -F "$token" CLAUDE.md >/dev/null ||
		fail "missing Claude takeover contract: $token"
done

for token in \
	'Codex and Claude share two roles' \
	'Claude imports it through root `CLAUDE.md`' \
	'`codex` or `claude`'
do
	grep -F "$token" AGENTS.md >/dev/null ||
		fail "missing shared project contract: $token"
done

grep -F 'A WORKER never runs `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.' \
	skills/publish-and-verify.md >/dev/null ||
	fail 'publication playbook does not apply the worker prohibition to both clients'

grep -F '"CLAUDE.md": 4000' tools/check-md-size.py >/dev/null ||
	fail 'Claude guidance lacks a size budget'
grep -F 'AGENTS.md CLAUDE.md README.md' \
	tools/test-repository-independence.sh >/dev/null ||
	fail 'independence test does not scan Claude guidance'
[ "$(grep -Fxc 'tools/test-claude-takeover.sh' tools/test-security.sh)" -eq 1 ] ||
	fail 'complete offline suite does not run Claude takeover test exactly once'

python3 tools/task-metrics.py selftest >/dev/null ||
	fail 'task metrics selftest rejected Claude driver support'
python3 - <<'PY' || fail 'task metrics JSON schema rejected client allowlist'
import json

schema = json.load(open("tools/task-metrics.schema.json", encoding="utf-8"))
for branch in schema["oneOf"]:
    assert branch["properties"]["agent"] == {"enum": ["codex", "claude"]}
PY
python3 tools/check-md-size.py >/dev/null ||
	fail 'instruction or ledger size budget'

printf '%s\n' 'PASS: website Claude takeover contract'

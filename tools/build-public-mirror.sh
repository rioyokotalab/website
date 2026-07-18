#!/bin/bash
# Build a sanitized single-commit public mirror of the website (T-192).
#
#   tools/build-public-mirror.sh DEST [AUDIT_OUT]
#
# Stages only the deploy allowlist via stage-public-site.sh, removes the
# .htaccess server configuration, adds a provenance README, and initializes a
# fresh Git repository at DEST with exactly one commit and no source history.
# The value-free audit (tools/public-repo-audit.py) then scans the mirror and
# this script fails on any credential-category finding. Everything is local:
# no remote, push, or account operation happens here.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST=${1:?Usage: build-public-mirror.sh DEST [AUDIT_OUT]}
AUDIT_OUT=${2:-$DEST.audit.json}

case "$DEST" in
	/*) ;;
	*) echo "DEST must be an absolute path: $DEST" >&2; exit 2 ;;
esac
[ ! -e "$AUDIT_OUT" ] || { echo "Audit output exists: $AUDIT_OUT" >&2; exit 2; }

"$ROOT/tools/stage-public-site.sh" "$DEST"

# Server configuration is deployed but never served; keep it out of the mirror.
rm "$DEST/.htaccess"

SOURCE_COMMIT=$(git -C "$ROOT" rev-parse --short HEAD)
BUILD_DATE=$(date -u +%Y-%m-%d)
cat > "$DEST/README.md" <<EOF
# YOKOTA Lab website — public mirror

Sanitized single-commit mirror of the lab website's public tree, generated
on $BUILD_DATE from private source commit $SOURCE_COMMIT. It contains only
content already served publicly (HTML, CSS, JS, images, one CV PDF) and
carries no source history, tooling, or server configuration. Regenerated
mirrors replace this repository; do not send pull requests here.
EOF

for forbidden in tools skills docs .github .git AGENTS.md CLAUDE.md TODO.md \
	README-source publish.sh deploy.sh package.json .htaccess \
	cv/cv.tex cv/cv.cls cv/build-cv.sh; do
	[ ! -e "$DEST/$forbidden" ] || {
		echo "Forbidden path staged into mirror: $forbidden" >&2
		exit 1
	}
done

git -C "$DEST" init --quiet --initial-branch=main
git -C "$DEST" add --all
git -C "$DEST" commit --quiet \
	-m "Public mirror of the YOKOTA Lab website (source $SOURCE_COMMIT)"

COMMITS=$(git -C "$DEST" rev-list --count HEAD)
[ "$COMMITS" -eq 1 ] || {
	echo "Mirror must contain exactly one commit, found $COMMITS" >&2
	exit 1
}

python3 "$ROOT/tools/public-repo-audit.py" --repo "$DEST" \
	--name website-public-mirror --output "$AUDIT_OUT" >/dev/null

python3 - "$AUDIT_OUT" <<'PY'
import json
import sys

report = json.loads(open(sys.argv[1], encoding="utf-8").read())
counts = report.get("finding_counts", {})
blocking = {
    rule: count
    for rule, count in counts.items()
    if count and rule not in ("large-blob",)
}
if report.get("value_exposed"):
    print("Audit unexpectedly exposed values; refusing mirror", file=sys.stderr)
    raise SystemExit(1)
if blocking:
    print(f"Blocking audit findings in mirror: {blocking}", file=sys.stderr)
    print("Review the audit metadata before any publication", file=sys.stderr)
    raise SystemExit(1)
print(f"mirror audit clean (finding_counts={counts})")
PY

echo "Public mirror built at $DEST (source $SOURCE_COMMIT, audit $AUDIT_OUT)"
echo "No remote configured; publication is a separate owner action."

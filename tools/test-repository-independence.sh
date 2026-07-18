#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

scan_files=$(
	{
		printf '%s\n' AGENTS.md README.md deploy.sh publish.sh package.json
		find .github docs skills tools -type f -print
	} |
		LC_ALL=C sort -u |
		sed -e '/^docs\/audits\//d' \
			-e '/^tools\/agent-benchmark\//d' \
			-e '/^tools\/out\//d' \
			-e '/^tools\/state\//d' \
			-e '/^tools\/codex-log\.md$/d' \
			-e '/^tools\/task-metrics\.jsonl$/d' \
			-e '/^tools\/test-repository-independence\.sh$/d'
)

forbidden=$(printf '%s' 'harn''ess')
if printf '%s\n' "$scan_files" | xargs rg -n -i \
	"HARNESS_BIN|/home/[^/]+/$forbidden|\$HOME/$forbidden|github\\.com/[^/]+/$forbidden|$forbidden/bin/$forbidden|$forbidden guarded-delete"; then
	echo 'FAIL: website has an operational dependency on the external control repository' >&2
	exit 1
fi

if rg -n 'git init .*RUNNER_TEMP|git -C .* fetch' .github/workflows; then
	echo 'FAIL: website CI fetches a second source repository' >&2
	exit 1
fi

[ ! -e .gitmodules ] || {
	echo 'FAIL: website must not declare a Git submodule' >&2
	exit 1
}
git ls-files -s | awk '$1 == 120000 { print $4 }' |
while IFS= read -r link; do
	target=$(readlink "$link")
	case "$target" in /*)
		echo "FAIL: tracked symlink leaves the repository: $link" >&2
		exit 1
		;; esac
	resolved=$(realpath -m -- "${link%/*}/$target")
	case "$resolved" in "$ROOT"/*) ;;
		*) echo "FAIL: tracked symlink leaves the repository: $link" >&2; exit 1 ;;
	esac
done

echo 'PASS: website operational surfaces are repository-independent'

#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

python3 tools/security-check.py "$@"
python3 tools/link-check.py
python3 tools/test-link-check.py
tools/test-guarded-delete.sh
tools/test-public-repo-audit.sh
tools/test-github-ruleset.sh
tools/test-bootstrap-lftp.sh
tools/test-repository-independence.sh
tools/test-deploy-policy.sh
python3 tools/supply-chain-check.py
python3 tools/generate-sitemap.py --check
python3 tools/standards-check.py
python3 tools/css-selector-check.py
python3 tools/test-researchmap-export.py
python3 tools/test-researchmap-retry-errors.py
python3 tools/test-orcid-export.py
python3 tools/populate-achievement-metadata.py --check
python3 tools/normalize-achievement-format.py --check

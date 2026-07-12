#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

python3 tools/security-check.py "$@"
tools/test-deploy-policy.sh
python3 tools/supply-chain-check.py
python3 tools/standards-check.py

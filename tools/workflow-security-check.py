#!/usr/bin/env python3
"""Enforce least-privilege, pinned, fork-safe GitHub Actions workflows.

Regex-based (no YAML dependency) so it runs anywhere the offline suite runs.
Locks in the hardening from T-195/T-196 as a regression test.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# WORKFLOW_SECURITY_DIR overrides the scanned directory so tests can point at a
# fixture tree without touching the real workflows.
WORKFLOW_DIR = Path(os.environ.get("WORKFLOW_SECURITY_DIR", ROOT / ".github" / "workflows"))
BASE = WORKFLOW_DIR.parent.parent if "WORKFLOW_SECURITY_DIR" in os.environ else ROOT

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*(?P<ref>\S+)", re.M)
SHA_REF = re.compile(r"^[^@]+@[0-9a-f]{40}$")
LOCAL_REF = re.compile(r"^\./")
NPM_CI = re.compile(r"\bnpm ci\b")


def check_workflow(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        rel = path.relative_to(BASE).as_posix()
    except ValueError:
        rel = path.name
    problems: list[str] = []

    # 1. No pull_request_target — it runs with a privileged token on fork code.
    if re.search(r"^\s*pull_request_target\s*:", text, re.M):
        problems.append(f"{rel}: uses pull_request_target (unsafe on a public repo)")

    # 2. A top-level permissions block must exist and be minimal.
    top = re.search(r"^permissions:\s*(.*)$", text, re.M)
    if not top:
        problems.append(f"{rel}: missing top-level permissions block")
    else:
        value = top.group(1).strip()
        if value not in ("{}", "read-all") and "write" in value:
            problems.append(f"{rel}: top-level permissions are not minimal ({value})")

    # 3. Every third-party action is pinned to a full commit SHA.
    for match in USES.finditer(text):
        ref = match.group("ref").strip("\"'")
        if LOCAL_REF.match(ref):
            continue
        if not SHA_REF.match(ref):
            problems.append(f"{rel}: action not pinned to a 40-char SHA: {ref}")

    # 4. npm ci must not run lifecycle scripts (fork-PR defense in depth).
    for line in text.splitlines():
        if NPM_CI.search(line) and "--ignore-scripts" not in line:
            problems.append(f"{rel}: 'npm ci' without --ignore-scripts")

    # 5. checkout must not persist credentials.
    if "actions/checkout@" in text and "persist-credentials: false" not in text:
        problems.append(f"{rel}: actions/checkout without persist-credentials: false")

    return problems


def main() -> int:
    if not WORKFLOW_DIR.is_dir():
        print("workflow-security: no .github/workflows directory")
        return 0
    workflows = sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))
    if not workflows:
        print("workflow-security: no workflow files found")
        return 0
    problems: list[str] = []
    for path in workflows:
        problems.extend(check_workflow(path))
    if problems:
        print("workflow-security: findings:\n  " + "\n  ".join(problems))
        return 1
    print(f"PASS: workflow security ({len(workflows)} workflow file(s) checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

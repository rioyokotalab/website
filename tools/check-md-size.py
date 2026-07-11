#!/usr/bin/env python3
"""Enforce size budgets on context-ledger and instruction .md files (pre-commit)."""

import os
import sys

BUDGETS = {  # repo-root-relative path -> max bytes
    "tools/todo.md": 8000,
    "tools/state/session.md": 4000,
    "tools/state/facts.md": 10000,
    "tools/state/decisions.md": 10000,
    "skills/context-ledger.md": 8000,
    "AGENTS.md": 10000,
}


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = []
    for rel, cap in BUDGETS.items():
        path = os.path.join(root, rel)
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > cap:
                bad.append(
                    f"{rel}: {size} > {cap} bytes — prune per "
                    "skills/context-ledger.md (git keeps history)"
                )
    if bad:
        print("check-md-size: over budget:\n  " + "\n  ".join(bad))
        return 1
    print(f"check-md-size: OK ({len(BUDGETS)} budgets checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

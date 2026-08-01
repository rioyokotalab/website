#!/usr/bin/env python3
"""Fail-closed browser-test scope for pull-request path lists."""

from __future__ import annotations

import sys


SAFE_FILES = {
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "TODO.md",
    "tools/codex-log.md",
    "tools/task-metrics.jsonl",
}
SAFE_PREFIXES = ("docs/", "tools/out/", "tools/state/")


def browser_required(paths: list[str]) -> bool:
    if not paths:
        return True
    for path in paths:
        if (
            not path
            or path.startswith("/")
            or any(ord(character) < 32 or ord(character) == 127 for character in path)
            or any(part in {"", ".", ".."} for part in path.split("/"))
        ):
            return True
        if path not in SAFE_FILES and not path.startswith(SAFE_PREFIXES):
            return True
    return False


def main() -> int:
    try:
        paths = [
            value.decode("utf-8")
            for value in sys.stdin.buffer.read().split(b"\0")
            if value
        ]
    except UnicodeDecodeError:
        paths = []
    required = browser_required(paths)
    print(f"browser={'true' if required else 'false'}")
    print(f"classified_paths={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

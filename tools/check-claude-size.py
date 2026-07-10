#!/usr/bin/env python3
"""Enforce the repository CLAUDE.md file-size budget."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


MAX_BYTES = 35000
WARN_BYTES = 33000
TARGET_FILE = "CLAUDE.md"


def repository_root() -> Path:
    """Return the Git worktree root, with the script's repository as fallback."""
    script_dir = Path(__file__).resolve().parent
    try:
        result = subprocess.run(
            ["git", "-C", str(script_dir), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return script_dir.parent
    return Path(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file",
        metavar="PATH",
        help="file to check; relative paths are resolved from the repository root",
    )
    args = parser.parse_args()

    root = repository_root()
    target = Path(args.file) if args.file else root / TARGET_FILE
    if not target.is_absolute():
        target = root / target

    try:
        size = target.stat().st_size
    except OSError as error:
        print(f"ERROR: cannot measure {target}: {error}", file=sys.stderr)
        return 2

    headroom = MAX_BYTES - size
    try:
        label = str(target.relative_to(root))
    except ValueError:
        label = str(target)
    print(f"{label}: {size} bytes; budget: {MAX_BYTES}; headroom: {headroom} bytes")

    if size > MAX_BYTES:
        print(
            f'ERROR: over budget by {size - MAX_BYTES} bytes; condense or move detail out '
            '— see the "File-size budget" rule in CLAUDE.md.',
            file=sys.stderr,
        )
        return 1
    if size > WARN_BYTES:
        print(f"WARNING: {label} is within {MAX_BYTES - size} bytes of the maximum budget.")
        return 0

    print(f"OK: {label} is within the size budget.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

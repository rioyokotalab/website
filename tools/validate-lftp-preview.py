#!/usr/bin/env python3
"""Validate staged-tree identity and deletion-bearing lftp previews."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

REMOVAL = re.compile(r"^Removing old (file|directory) `(.+)'$")
DELETE_COMMAND = re.compile(r"^(?:rm|rmdir)(?:\s|$)")


def snapshot(root: Path) -> str:
    root = root.resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("source is not a real directory")
    digest = hashlib.sha256()
    count = 0
    size = 0
    for directory, names, files in os.walk(root, followlinks=False):
        names.sort()
        files.sort()
        base = Path(directory)
        for name in [*names, *files]:
            path = base / name
            relative = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise ValueError(f"source contains symlink: {relative}")
            if stat.S_ISDIR(info.st_mode):
                kind = b"d"
                content = b""
            elif stat.S_ISREG(info.st_mode):
                kind = b"f"
                content = path.read_bytes()
                count += 1
                size += len(content)
            else:
                raise ValueError(f"source contains special path: {relative}")
            digest.update(kind + b"\0" + relative.encode() + b"\0")
            digest.update(hashlib.sha256(content).digest())
    return f"sha256={digest.hexdigest()} files={count} bytes={size}"


def validate_preview(path: Path, maximum: int) -> str:
    text = path.read_text(encoding="utf-8")
    removals: list[str] = []
    command_count = 0
    for line in text.splitlines():
        if DELETE_COMMAND.match(line):
            command_count += 1
        match = REMOVAL.match(line)
        if not match:
            continue
        kind, relative = match.groups()
        if kind == "directory":
            raise ValueError(f"recursive remote directory deletion is forbidden: {relative}")
        pure = PurePosixPath(relative)
        if (not relative or pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts)):
            raise ValueError(f"unsafe remote deletion path: {relative}")
        if ".dont-remove-me" in pure.parts:
            raise ValueError("remote sentinel deletion is forbidden")
        if any(ord(character) < 32 or ord(character) == 127 for character in relative):
            raise ValueError("remote deletion path contains a control character")
        removals.append(relative)
    if command_count != len(removals):
        raise ValueError("unrecognized or unmatched remote deletion command")
    if len(removals) > maximum:
        raise ValueError(f"remote deletion count {len(removals)} exceeds limit {maximum}")
    return f"deletions={len(removals)} max={maximum}"


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("source", type=Path)
    preview_parser = subparsers.add_parser("preview")
    preview_parser.add_argument("preview", type=Path)
    preview_parser.add_argument("--max-delete", type=int, default=250)
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            print(snapshot(args.source))
        else:
            if args.max_delete < 0:
                raise ValueError("negative deletion limit")
            print(validate_preview(args.preview, args.max_delete))
    except (OSError, UnicodeError, ValueError) as error:
        print(f"lftp preview validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

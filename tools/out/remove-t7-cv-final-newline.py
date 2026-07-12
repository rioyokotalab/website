#!/usr/bin/env python3
"""Restore cv/cv.tex's pre-existing no-final-newline convention only."""

from pathlib import Path

path = Path("cv/cv.tex")
data = path.read_bytes()
if not data.endswith(b"\\end{document}\n"):
    raise SystemExit("cv/cv.tex does not have the expected single final newline")
path.write_bytes(data[:-1])
print("removed final newline from cv/cv.tex")

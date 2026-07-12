#!/usr/bin/env python3
"""Apply one independently verified DOI attribute without normalizing CRLF HTML."""

from pathlib import Path
import re

DOI = "10.1145/3721145.3730422"
AUTHORS = (
    "Chen Zhuang; Lingqi Zhang; Du Wu; Peng Chen; Jiajun Huang; Xin Liu; "
    "Rio Yokota; Nikoli Dryden; Toshio Endo; Satoshi Matsuoka; Mohamed Wahib"
)
pattern = re.compile(
    rf'(<li\b(?=[^>]*\bdata-authors="{re.escape(AUTHORS)}")'
    rf'(?=[^>]*\bdata-date="2025-06")[^>]*)(>)',
    flags=re.I,
)

for path in (Path("en/achievements/index.html"), Path("jp/achievements/index.html")):
    with open(path, encoding="utf-8", newline="") as handle:
        text = handle.read()
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected exactly one target, found {len(matches)}")
    match = matches[0]
    if re.search(r"\bdata-doi\s*=", match.group(1), flags=re.I):
        raise SystemExit(f"{path}: target already has data-doi")
    updated = text[:match.start(1)] + match.group(1) + f' data-doi="{DOI}"' + match.group(2) + text[match.end(2):]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(updated)
    print(f"updated {path}")

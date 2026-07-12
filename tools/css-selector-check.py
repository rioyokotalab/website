#!/usr/bin/env python3
"""Reject local stylesheet selector tokens absent from public HTML and scripts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMENT = re.compile(r"/\*.*?\*/", re.S)
RULE = re.compile(r"([^{}]+)\{")
CLASS = re.compile(r"(?<![\w-])\.([A-Za-z_][\w-]*)")
ID = re.compile(r"#([A-Za-z_][\w-]*)")


def selector_tokens(css: str) -> tuple[set[str], set[str]]:
    selectors: list[str] = []
    for match in RULE.finditer(COMMENT.sub("", css)):
        prelude = match.group(1).strip()
        if prelude and not prelude.startswith("@") and not prelude.endswith(";"):
            selectors.append(prelude)
    return (
        {token for selector in selectors for token in CLASS.findall(selector)},
        {token for selector in selectors for token in ID.findall(selector)},
    )


def public_source() -> str:
    paths = [ROOT / "index.html"]
    paths.extend(sorted((ROOT / "en").rglob("*.html")))
    paths.extend(sorted((ROOT / "jp").rglob("*.html")))
    paths.extend(sorted((ROOT / "js").rglob("*.js")))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def absent(tokens: set[str], source: str) -> list[str]:
    return [
        token
        for token in sorted(tokens)
        if not re.search(rf"(?<![\w-]){re.escape(token)}(?![\w-])", source)
    ]


def main() -> int:
    classes, ids = selector_tokens((ROOT / "style.css").read_text(encoding="utf-8"))
    source = public_source()
    unused_classes = absent(classes, source)
    unused_ids = absent(ids, source)
    if unused_classes or unused_ids:
        if unused_classes:
            print("css-selector: absent classes: " + ", ".join(unused_classes), file=sys.stderr)
        if unused_ids:
            print("css-selector: absent ids: " + ", ".join(unused_ids), file=sys.stderr)
        return 1
    print(f"PASS: {len(classes)} CSS classes and {len(ids)} ids have public source references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

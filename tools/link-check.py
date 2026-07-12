#!/usr/bin/env python3
"""Validate local public URLs and fragments without making network requests."""

from __future__ import annotations

import os
import re
import runpy
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOOLS = Path(__file__).resolve().parent
SECURITY = runpy.run_path(str(TOOLS / "security-check.py"))
BASE_URL = SECURITY["BASE_URL"]
ROOT = SECURITY["ROOT"]
public_files = SECURITY["public_files"]

LOCAL_HOST = urlsplit(BASE_URL).hostname
SKIP_SCHEMES = {"data", "javascript", "mailto", "tel"}
URL_ATTRIBUTES = {"href", "src", "action", "poster"}


@dataclass(frozen=True)
class Reference:
    source: str
    line: int
    raw: str


class Page(HTMLParser):
    def __init__(self, relative: str) -> None:
        super().__init__(convert_charrefs=True)
        self.relative = relative
        self.targets: set[str] = set()
        self.references: list[Reference] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if values.get("id"):
            self.targets.add(values["id"])
        if tag == "a" and values.get("name"):
            self.targets.add(values["name"])
        for attribute in URL_ATTRIBUTES:
            if values.get(attribute):
                self.references.append(Reference(self.relative, self.getpos()[0], values[attribute]))
        if tag == "object" and values.get("data"):
            self.references.append(Reference(self.relative, self.getpos()[0], values["data"]))
        if values.get("srcset"):
            for candidate in values["srcset"].split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.references.append(Reference(self.relative, self.getpos()[0], url))


def normalize_target(reference: Reference) -> tuple[str, str] | None:
    parsed = urlsplit(reference.raw)
    scheme = parsed.scheme.lower()
    if scheme in SKIP_SCHEMES or reference.raw.startswith("//"):
        return None
    if parsed.hostname and parsed.hostname.lower() != LOCAL_HOST:
        return None
    if scheme and scheme not in {"http", "https"}:
        return None
    clean = unquote(parsed.path)
    if not clean:
        target = Path(reference.source)
    elif clean.startswith("/"):
        target = Path(clean.lstrip("/"))
    else:
        target = Path(reference.source).parent / clean
    normalized = Path(os.path.normpath(target)).as_posix()
    if normalized == ".":
        normalized = ""
    if normalized == "" or clean.endswith("/"):
        normalized = f"{normalized.rstrip('/')}/index.html".lstrip("/")
    return normalized, unquote(parsed.fragment)


def audit(root: Path) -> tuple[int, list[str]]:
    deployable = public_files(root)
    html_paths = ["index.html", *sorted(path for path in deployable if path.endswith(".html") and path != "index.html")]
    pages: dict[str, Page] = {}
    references: list[Reference] = []
    for relative in html_paths:
        page = Page(relative)
        page.feed((root / relative).read_text(encoding="utf-8"))
        pages[relative] = page
        references.extend(page.references)

    style_path = root / "style.css"
    if style_path.is_file():
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", style_path.read_text(encoding="utf-8"), flags=re.I):
            references.append(Reference("style.css", 1 + match.string.count("\n", 0, match.start()), match.group(2)))

    findings: list[str] = []
    checked = 0
    for reference in references:
        normalized = normalize_target(reference)
        if normalized is None:
            continue
        target, fragment = normalized
        checked += 1
        if target.startswith("../") or target not in deployable:
            findings.append(f"{reference.source}:{reference.line}: missing public target: {reference.raw}")
            continue
        if fragment and target.endswith(".html") and fragment not in pages[target].targets:
            findings.append(f"{reference.source}:{reference.line}: missing fragment #{fragment} in {target}")

    return checked, findings


def main() -> int:
    checked, findings = audit(ROOT)
    if findings:
        for finding in findings:
            print(f"links: {finding}", file=sys.stderr)
        return 1
    print(f"PASS: {checked} local public URLs and fragments resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())

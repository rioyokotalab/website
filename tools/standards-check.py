#!/usr/bin/env python3
"""Deterministic structural and accessibility checks for public HTML."""

from __future__ import annotations

import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.ids: list[str] = []
        self.targets: set[str] = set()
        self.fragments: list[str] = []
        self.images = 0
        self.images_without_alt = 0
        self.eager_images: list[str] = []
        self.landmarks = Counter()
        self.nav_labels: list[str] = []
        self.skip: str | None = None
        self.unsafe_semantics: list[int] = []
        self.inline_executable_scripts = 0
        self.menu_button: dict[str, str] | None = None
        self.body_id = ""
        self.pagetop: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if tag == "body":
            self.body_id = values.get("id", "")
        if values.get("id"):
            self.ids.append(values["id"])
            self.targets.add(values["id"])
        if tag == "a" and values.get("name"):
            self.targets.add(values["name"])
        if tag in ("header", "main", "footer"):
            self.landmarks[tag] += 1
        if tag == "nav":
            self.nav_labels.append(values.get("aria-label", ""))
        if tag == "a":
            href = values.get("href", "")
            if values.get("class") == "skip-link":
                self.skip = href
            if href.startswith("#") and len(href) > 1:
                self.fragments.append(href[1:])
            if href.lower().startswith("javascript:"):
                self.unsafe_semantics.append(line)
            if values.get("aria-label") in ("Back to top", "ページ上部へ戻る"):
                self.pagetop = values
        if any(key.startswith("on") for key in values):
            self.unsafe_semantics.append(line)
        if tag == "img":
            self.images += 1
            if "alt" not in values:
                self.images_without_alt += 1
            if values.get("loading", "").lower() != "lazy":
                self.eager_images.append(values.get("src", ""))
        if tag == "script" and not values.get("src") and values.get("type", "text/javascript").lower() not in ("application/ld+json",):
            self.inline_executable_scripts += 1
        if values.get("id") == "menubar_hdr":
            self.menu_button = {"tag": tag, **values}


def fail(findings: list[str], path: Path, message: str) -> None:
    findings.append(f"{path.relative_to(ROOT)}: {message}")


def main() -> int:
    findings: list[str] = []
    root_text = (ROOT / "index.html").read_text(encoding="utf-8")
    root_requirements = (
        '<meta charset="UTF-8">',
        '<meta name="viewport"',
        '<meta name="theme-color" content="#002855">',
        '<script defer src="js/language-redirect.js"></script>',
        '<noscript>',
        '<a href="en/index.html" lang="en">English</a>',
        '<a href="jp/index.html" lang="ja">日本語</a>',
    )
    if any(item not in root_text for item in root_requirements):
        findings.append("root redirect metadata or bilingual no-script fallback mismatch")
    if re.search(r'<meta\s+name=["\']\s*["\']', root_text, flags=re.I):
        findings.append("root redirect contains empty metadata name")
    en_pages = sorted((ROOT / "en").rglob("*.html"))
    jp_pages = sorted((ROOT / "jp").rglob("*.html"))
    if {p.relative_to(ROOT / "en") for p in en_pages} != {p.relative_to(ROOT / "jp") for p in jp_pages}:
        findings.append("EN/JP HTML path parity mismatch")
    pages = en_pages + jp_pages
    if len(pages) != 26:
        findings.append(f"expected 26 bilingual pages, found {len(pages)}")
    style_versions: set[str] = set()
    for path in pages:
        text = path.read_text(encoding="utf-8")
        document = Document()
        document.feed(text)
        expected_lang = "en" if path.relative_to(ROOT).parts[0] == "en" else "ja"
        if document.html_lang.lower() != expected_lang:
            fail(findings, path, f"lang must be {expected_lang}")
        duplicates = sorted(key for key, count in Counter(document.ids).items() if count > 1)
        if duplicates:
            fail(findings, path, "duplicate IDs")
        if document.landmarks != Counter({"header": 1, "main": 1, "footer": 1}):
            fail(findings, path, "requires one header, main, and footer")
        if len(document.nav_labels) != 2 or any(not label for label in document.nav_labels) or len(set(document.nav_labels)) != 2:
            fail(findings, path, "requires two distinctly labeled navigation landmarks")
        expected_skip = "Skip to main content" if expected_lang == "en" else "本文へ移動"
        if document.skip != "#wrapper" or expected_skip not in text:
            fail(findings, path, "localized skip link mismatch")
        expected_menu_label = "Open navigation menu" if expected_lang == "en" else "ナビゲーションメニューを開く"
        button = document.menu_button or {}
        if button.get("tag") != "button" or button.get("type") != "button" or button.get("aria-controls") != "menubar-s" or button.get("aria-expanded") != "false" or button.get("aria-label") != expected_menu_label:
            fail(findings, path, "accessible mobile menu button mismatch")
        expected_pagetop_label = "Back to top" if expected_lang == "en" else "ページ上部へ戻る"
        pagetop = document.pagetop or {}
        if document.body_id != "top" or pagetop.get("href") != "#top" or pagetop.get("aria-label") != expected_pagetop_label:
            fail(findings, path, "accessible back-to-top link mismatch")
        if document.images_without_alt:
            fail(findings, path, "image without alt")
        if document.inline_executable_scripts:
            fail(findings, path, "executable inline script")
        if document.unsafe_semantics:
            fail(findings, path, "JavaScript URL or inline event handler")
        missing_fragments = sorted(set(document.fragments) - document.targets)
        if missing_fragments:
            fail(findings, path, "fragment target missing")
        for src in document.eager_images:
            if not re.search(r"/(?:logoE?|banner-(?:top|sub))\.(?:png|jpg)$", urlsplit(src).path):
                fail(findings, path, "noncritical image missing loading=lazy")
        matches = re.findall(r"style\.css\?v=([^\"']+)", text)
        if len(matches) != 1:
            fail(findings, path, "requires one versioned stylesheet")
        else:
            style_versions.add(matches[0])
    if len(style_versions) != 1:
        findings.append("stylesheet cache versions differ across pages")
    if findings:
        for finding in findings:
            print(f"standards: {finding}", file=sys.stderr)
        return 1
    print("PASS: HTML standards and accessibility checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

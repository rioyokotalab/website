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
        self.lazy_images_without_async = 0
        self.eager_images: list[str] = []
        self.image_attrs: list[dict[str, str]] = []
        self.landmarks = Counter()
        self.nav_labels: list[str] = []
        self.skip: str | None = None
        self.unsafe_semantics: list[int] = []
        self.inline_executable_scripts = 0
        self.menu_button: dict[str, str] | None = None
        self.body_id = ""
        self.pagetop: dict[str, str] | None = None
        self.canonicals: list[str] = []
        self.alternates: dict[str, list[str]] = {}
        self.current_links: list[dict[str, str]] = []
        self.iframes: list[dict[str, str]] = []
        self.inline_styles = 0
        self.og_properties: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        line = self.getpos()[0]
        if tag == "style" or "style" in values:
            self.inline_styles += 1
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
        if tag == "meta" and values.get("property", "").lower().startswith("og:"):
            self.og_properties.setdefault(values["property"].lower(), []).append(values.get("content", ""))
        if tag == "link" and values.get("rel", "").lower() == "canonical":
            self.canonicals.append(values.get("href", ""))
        if tag == "link" and values.get("rel", "").lower() == "alternate" and values.get("hreflang"):
            self.alternates.setdefault(values["hreflang"].lower(), []).append(values.get("href", ""))
        if tag == "a":
            href = values.get("href", "")
            if "aria-current" in values:
                self.current_links.append(values)
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
            self.image_attrs.append(values)
            self.images += 1
            if "alt" not in values:
                self.images_without_alt += 1
            if values.get("loading", "").lower() == "lazy" and values.get("decoding", "").lower() != "async":
                self.lazy_images_without_async += 1
            if values.get("loading", "").lower() != "lazy":
                self.eager_images.append(values.get("src", ""))
        if tag == "iframe":
            self.iframes.append(values)
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
        '<meta property="og:url" content="https://www.rio.scrc.iir.isct.ac.jp/">',
        '<meta property="og:locale" content="ja_JP">',
        '<meta property="og:locale:alternate" content="en_US">',
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
    remaining_named_anchors = 0
    for path in pages:
        text = path.read_text(encoding="utf-8")
        if re.search(r'/\s+class="content-width-', text):
            fail(findings, path, "class placed after self-closing slash")
        named_anchors = len(re.findall(r'<a\s+name=', text, flags=re.I))
        remaining_named_anchors += named_anchors
        if named_anchors and path.relative_to(ROOT).parts[1] != "news":
            fail(findings, path, "legacy named anchor outside News")
        if re.search(r'<h[1-6][^>]*><a\s+name=', text, flags=re.I):
            fail(findings, path, "legacy named anchor inside heading")
        document = Document()
        document.feed(text)
        expected_lang = "en" if path.relative_to(ROOT).parts[0] == "en" else "ja"
        relative = path.relative_to(ROOT / ("en" if expected_lang == "en" else "jp")).as_posix()
        suffix = relative[:-10] if relative.endswith("index.html") else relative
        base_url = "https://www.rio.scrc.iir.isct.ac.jp"
        expected_alternates = {
            "en": [f"{base_url}/en/{suffix}"],
            "ja": [f"{base_url}/jp/{suffix}"],
            "x-default": [f"{base_url}/"],
        }
        expected_canonical = expected_alternates["en" if expected_lang == "en" else "ja"]
        if document.canonicals != expected_canonical or document.alternates != expected_alternates:
            fail(findings, path, "canonical or alternate-language metadata mismatch")
        expected_og = {
            "og:url": expected_canonical,
            "og:locale": ["en_US" if expected_lang == "en" else "ja_JP"],
            "og:locale:alternate": ["ja_JP" if expected_lang == "en" else "en_US"],
        }
        if any(document.og_properties.get(key) != value for key, value in expected_og.items()):
            fail(findings, path, "Open Graph URL or locale metadata mismatch")
        current_destinations = {
            "index.html", "about/index.html", "research/index.html",
            "achievements/index.html", "member/index.html", "computers/index.html",
            "teaching/index.html", "picture/index.html", "contact/index.html",
        }
        expected_current_count = 0
        if relative in current_destinations:
            expected_current_count = 1 if relative == "contact/index.html" else 2
        if len(document.current_links) != expected_current_count or any(link.get("aria-current") != "page" or link.get("href") != "index.html" for link in document.current_links):
            fail(findings, path, "current-page navigation state mismatch")
        if relative == "contact/index.html":
            expected_map_title = "Map of YOKOTA Laboratory" if expected_lang == "en" else "横田研究室所在地の地図"
            frame = document.iframes[0] if len(document.iframes) == 1 else {}
            if frame.get("class") != "location-map" or frame.get("title") != expected_map_title or frame.get("loading") != "lazy" or frame.get("referrerpolicy") != "no-referrer-when-downgrade" or "style" in frame or "width" in frame or "height" in frame:
                fail(findings, path, "accessible map embed mismatch")
        elif document.iframes:
            fail(findings, path, "unexpected iframe")
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
        if any(not image.get("width", "").isdigit() or not image.get("height", "").isdigit() or int(image["width"]) < 1 or int(image["height"]) < 1 for image in document.image_attrs):
            fail(findings, path, "image missing valid intrinsic dimensions")
        if document.lazy_images_without_async:
            fail(findings, path, "lazy image missing asynchronous decode hint")
        expected_logo = "logoE.png" if expected_lang == "en" else "logo.png"
        expected_logo_width = "450" if expected_lang == "en" else "436"
        logos = [image for image in document.image_attrs if urlsplit(image.get("src", "")).path.endswith("/" + expected_logo)]
        if len(logos) != 1 or logos[0].get("width") != expected_logo_width or logos[0].get("height") != "65":
            fail(findings, path, "header logo intrinsic dimensions mismatch")
        prioritized = [image for image in document.image_attrs if image.get("fetchpriority")]
        if len(prioritized) != 1 or prioritized[0].get("fetchpriority", "").lower() != "high" or not re.search(r"/banner-(?:top|sub)\.(?:png|jpg)$", urlsplit(prioritized[0].get("src", "")).path):
            fail(findings, path, "hero image fetch priority mismatch")
        if document.inline_executable_scripts:
            fail(findings, path, "executable inline script")
        if document.inline_styles:
            fail(findings, path, "inline presentation style")
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
        for asset in ("pagetop.js?v=20260713", "responsive-menu.js?v=20260713b"):
            if text.count(asset) != 1:
                fail(findings, path, f"versioned {asset.split('?')[0]} mismatch")
    if len(style_versions) != 1:
        findings.append("stylesheet cache versions differ across pages")
    if remaining_named_anchors:
        findings.append(f"legacy named anchors remain: {remaining_named_anchors}")
    for script in sorted((ROOT / "js").glob("*.js")):
        source = script.read_text(encoding="utf-8")
        if re.search(r"\.style\b|setAttribute\s*\(\s*['\"]style['\"]", source):
            fail(findings, script, "runtime inline style mutation")
    if findings:
        for finding in findings:
            print(f"standards: {finding}", file=sys.stderr)
        return 1
    print("PASS: HTML standards and accessibility checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

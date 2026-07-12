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
        self.main_classes: list[str] = []
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
        self.legacy_nowrap = 0
        self.no_wrap_classes = 0
        self.legacy_valign = 0
        self.vertical_top_classes = 0
        self.legacy_base_presentation = 0
        self.table_heading_classes = 0
        self.tables = 0
        self.presentation_tables = 0
        self.row_headers = 0
        self.column_headers = 0
        self.headings: list[dict[str, object]] = []
        self._heading: dict[str, object] | None = None
        self._interactives: list[dict[str, object]] = []
        self.unnamed_interactives = 0
        self.lightbox_labels: list[str] = []
        self.external_scripts_without_defer = 0
        self.external_script_sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        line = self.getpos()[0]
        if tag == "style" or "style" in values:
            self.inline_styles += 1
        if "nowrap" in values:
            self.legacy_nowrap += 1
        if "no-wrap" in values.get("class", "").split():
            self.no_wrap_classes += 1
        if "valign" in values:
            self.legacy_valign += 1
        if "vertical-top" in values.get("class", "").split():
            self.vertical_top_classes += 1
        if any(attribute in values for attribute in ("border", "cellpadding", "cellspacing", "bgcolor")):
            self.legacy_base_presentation += 1
        if "table-heading-cell" in values.get("class", "").split():
            self.table_heading_classes += 1
        if tag == "table":
            self.tables += 1
            if values.get("role") == "presentation":
                self.presentation_tables += 1
        if tag == "th":
            if values.get("scope") == "row":
                self.row_headers += 1
            elif values.get("scope") == "col":
                self.column_headers += 1
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = {"level": int(tag[1]), "text": ""}
            self.headings.append(self._heading)
        if tag in ("a", "button"):
            self._interactives.append({"tag": tag, "attrs": values, "text": ""})
            if tag == "a" and values.get("data-lightbox"):
                self.lightbox_labels.append(values.get("aria-label", ""))
        if tag == "body":
            self.body_id = values.get("id", "")
        if values.get("id"):
            self.ids.append(values["id"])
            self.targets.add(values["id"])
        if tag == "a" and values.get("name"):
            self.targets.add(values["name"])
        if tag in ("header", "main", "footer"):
            self.landmarks[tag] += 1
            if tag == "main":
                self.main_classes = values.get("class", "").split()
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
            if self._interactives:
                self._interactives[-1]["text"] = str(self._interactives[-1]["text"]) + values.get("alt", "")
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
        if tag == "script" and values.get("src") and "defer" not in values:
            self.external_scripts_without_defer += 1
        if tag == "script" and values.get("src"):
            self.external_script_sources.append(values["src"])
        if values.get("id") == "menubar_hdr":
            self.menu_button = {"tag": tag, **values}

    def handle_data(self, data: str) -> None:
        if self._heading is not None:
            self._heading["text"] = str(self._heading["text"]) + data
        if self._interactives:
            self._interactives[-1]["text"] = str(self._interactives[-1]["text"]) + data

    def handle_endtag(self, tag: str) -> None:
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = None
        if tag in ("a", "button") and self._interactives and self._interactives[-1]["tag"] == tag:
            item = self._interactives.pop()
            attrs = item["attrs"]
            assert isinstance(attrs, dict)
            if not str(item["text"]).strip() and not attrs.get("aria-label", "").strip() and not attrs.get("title", "").strip():
                self.unnamed_interactives += 1


def fail(findings: list[str], path: Path, message: str) -> None:
    findings.append(f"{path.relative_to(ROOT)}: {message}")


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        return None
    offset = 2
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset + 4 <= len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        length = int.from_bytes(data[offset:offset + 2], "big")
        if length < 2 or offset + length > len(data):
            return None
        if marker in sof_markers and length >= 7:
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            return width, height
        offset += length
    return None


def main() -> int:
    findings: list[str] = []
    style_text = (ROOT / "style.css").read_text(encoding="utf-8")
    focus_selector = "a:focus-visible, button:focus-visible, input:focus-visible, [tabindex]:focus-visible"
    if style_text.count(focus_selector) != 2 or "outline: 2px solid #fff;" not in style_text or "box-shadow: 0 0 0 4px var(--accent-hover) !important;" not in style_text:
        findings.append("two-tone keyboard focus indicator mismatch")
    if style_text.count("#main a {") != 2 or "text-decoration-thickness: 0.08em;" not in style_text or "text-underline-offset: 0.15em;" not in style_text:
        findings.append("non-color content-link indicator mismatch")
    if style_text.count("@media (forced-colors: active)") != 1 or 'ul.topnav a[aria-current="page"]' not in style_text or style_text.count("outline: 3px solid Highlight !important;") != 2:
        findings.append("forced-colors state/focus treatment mismatch")
    if "width: 42px;\n\tmin-height: 42px;" not in style_text:
        findings.append("mobile menu target-size mismatch")
    if style_text.count("html.js #menubar_hdr {") != 1:
        findings.append("progressive mobile-menu control mismatch")
    if style_text.count("scroll-margin-top: 24px;") != 1:
        findings.append("sticky-header anchor offset mismatch")
    if style_text.count("--oral-highlight: #cc0000;") != 1 or style_text.count("--oral-highlight: #ff6b6b;") != 1 or "color: var(--oral-highlight);" not in style_text:
        findings.append("light/dark oral-highlight palette mismatch")
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
    metadata_titles = {"en": set(), "ja": set()}
    metadata_descriptions = {"en": set(), "ja": set()}
    remaining_named_anchors = 0
    table_width_classes = 0
    lightbox_counts = {"en": 0, "ja": 0}
    for path in pages:
        text = path.read_text(encoding="utf-8")
        table_width_classes += len(re.findall(r'\bwidth-\d+pct\b', text))
        if re.search(r'<(?:table|col|td|th)\b[^>]*\s(?:width|align)=', text, flags=re.I):
            fail(findings, path, "legacy table width or alignment attribute")
        if re.search(r'<meta\s+name="keywords"\s+content=""|\stype="text/(?:javascript|css)"', text, flags=re.I):
            fail(findings, path, "empty keywords or redundant MIME type")
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
        title_matches = re.findall(r"<title>(.*?)</title>", text, flags=re.I | re.S)
        description_matches = re.findall(r'<meta\s+name="description"\s+content="([^"]*)">', text, flags=re.I)
        title = title_matches[0].strip() if len(title_matches) == 1 else ""
        description = description_matches[0].strip() if len(description_matches) == 1 else ""
        metadata_titles[expected_lang].add(title)
        metadata_descriptions[expected_lang].add(description)
        lightbox_counts[expected_lang] += len(document.lightbox_labels)
        lightbox_total = len(document.lightbox_labels)
        expected_lightbox_labels = [
            f"View larger image {index} of {lightbox_total}" if expected_lang == "en" else f"拡大画像を表示（{lightbox_total}枚中{index}枚）"
            for index in range(1, lightbox_total + 1)
        ]
        if document.lightbox_labels != expected_lightbox_labels:
            fail(findings, path, "localized ordered Lightbox accessible names mismatch")
        if document.unnamed_interactives:
            fail(findings, path, "unnamed link or button")
        if any(not str(heading["text"]).strip() for heading in document.headings):
            fail(findings, path, "empty heading")
        for previous, current in zip(document.headings, document.headings[1:]):
            if int(current["level"]) > int(previous["level"]) + 1:
                fail(findings, path, "skipped heading level")
                break
        relative = path.relative_to(ROOT / ("en" if expected_lang == "en" else "jp")).as_posix()
        title_prefixes = {
            "en": {"index.html": "", "about/index.html": "About Lab.", "achievements/index.html": "Achievements", "computers/index.html": "Computing Environment", "contact/index.html": "Access and Contact", "links/index.html": "Links", "member/index.html": "Members", "member/yokota.html": "Rio Yokota", "news/index.html": "News", "picture/index.html": "Picture", "research/index.html": "Research", "software/index.html": "Software", "teaching/index.html": "Teaching"},
            "ja": {"index.html": "", "about/index.html": "研究室紹介", "achievements/index.html": "研究成果", "computers/index.html": "計算環境", "contact/index.html": "連絡先・アクセス", "links/index.html": "リンク", "member/index.html": "メンバー", "member/yokota.html": "横田理央", "news/index.html": "ニュース", "picture/index.html": "写真", "research/index.html": "研究内容", "software/index.html": "ソフトウェア", "teaching/index.html": "担当講義"},
        }
        prefix = title_prefixes[expected_lang][relative]
        expected_title = (f"{prefix} : " if prefix else "") + "YOKOTA Laboratory : Science Tokyo, IIR" if expected_lang == "en" else (f"{prefix}：" if prefix else "") + "横田研究室：東京科学大学 総合研究院"
        minimum_description = 50 if expected_lang == "en" else 20
        if title != expected_title or not (minimum_description <= len(description) <= 160):
            fail(findings, path, "page-local title or description mismatch")
        if document.og_properties.get("og:title") != [title] or document.og_properties.get("og:description") != [description]:
            fail(findings, path, "Open Graph title or description mismatch")
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
        containment_pages = {
            "en/computers/index.html", "en/member/yokota.html", "jp/member/yokota.html",
            "en/news/index.html", "jp/news/index.html",
        }
        expected_containment = path.relative_to(ROOT).as_posix() in containment_pages
        if ("mobile-table-containment" in document.main_classes) != expected_containment:
            fail(findings, path, "narrow-screen table containment scope mismatch")
        table_helpers = [src for src in document.external_script_sources if "table-scroll.js" in src]
        if table_helpers != (["../../js/table-scroll.js?v=20260713"] if expected_containment else []):
            fail(findings, path, "narrow-screen table helper scope mismatch")
        lightbox_helpers = [src for src in document.external_script_sources if "lightbox-accessibility.js" in src]
        if lightbox_helpers != (["../../js/lightbox-accessibility.js?v=20260713b"] if lightbox_total else []):
            fail(findings, path, "Lightbox accessibility helper scope mismatch")
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
        responsive_images = [image for image in document.image_attrs if image.get("srcset")]
        expected_responsive = 7 if relative == "picture/index.html" else 0
        responsive_pattern = re.compile(r"^(.*)/(2026-4|2026-3|2025-10|2025-9|2025-9-2|2025-4|2024-12)\.jpg$")
        if len(responsive_images) != expected_responsive:
            fail(findings, path, "responsive gallery image count mismatch")
        for image in responsive_images:
            match = responsive_pattern.match(image.get("src", ""))
            expected_srcset = f"{match.group(1)}/{match.group(2)}-720.jpg 720w, {match.group(1)}/{match.group(2)}-1200.jpg 1200w" if match else ""
            if image.get("srcset") != expected_srcset or image.get("sizes") != "(max-width: 900px) calc(100vw - 32px), 589px":
                fail(findings, path, "responsive gallery source mismatch")
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
        if document.external_scripts_without_defer:
            fail(findings, path, "external script missing defer")
        if document.inline_styles:
            fail(findings, path, "inline presentation style")
        expected_no_wrap = 98 if path.relative_to(ROOT).as_posix() == "en/news/index.html" else 54 if path.relative_to(ROOT).as_posix() == "jp/news/index.html" else 0
        if document.legacy_nowrap or document.no_wrap_classes != expected_no_wrap:
            fail(findings, path, "legacy nowrap or no-wrap class count mismatch")
        vertical_top_counts = {
            "en/index.html": 64, "jp/index.html": 28,
            "en/member/yokota.html": 16, "jp/member/yokota.html": 16,
            "en/news/index.html": 210, "jp/news/index.html": 218,
        }
        expected_vertical_top = vertical_top_counts.get(path.relative_to(ROOT).as_posix(), 0)
        if document.legacy_valign or document.vertical_top_classes != expected_vertical_top:
            fail(findings, path, "legacy valign or vertical-top class count mismatch")
        expected_heading_cells = 4 if path.relative_to(ROOT).as_posix() in ("en/computers/index.html", "jp/computers/index.html") else 0
        if document.legacy_base_presentation or document.table_heading_classes != expected_heading_cells:
            fail(findings, path, "legacy base presentation or table heading class mismatch")
        table_semantics = {
            "en/index.html": (1, 33, 0, 0), "jp/index.html": (1, 15, 0, 0),
            "en/news/index.html": (12, 105, 0, 0), "jp/news/index.html": (12, 109, 0, 0),
            "en/member/index.html": (4, 25, 0, 3), "jp/member/index.html": (4, 25, 0, 3),
            "en/member/yokota.html": (1, 0, 0, 1), "jp/member/yokota.html": (1, 0, 0, 1),
            "en/computers/index.html": (1, 0, 4, 0), "jp/computers/index.html": (1, 0, 4, 0),
        }
        expected_tables, expected_rows, expected_columns, expected_presentation = table_semantics.get(path.relative_to(ROOT).as_posix(), (0, 0, 0, 0))
        if (document.tables, document.row_headers, document.column_headers, document.presentation_tables) != (expected_tables, expected_rows, expected_columns, expected_presentation):
            fail(findings, path, "data/layout table semantics mismatch")
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
        if not re.search(r'<link\s+rel="stylesheet"\s+href="[^"]*style\.css\?v=[^"]+"\s+media="all">', text):
            fail(findings, path, "screen/print stylesheet media mismatch")
        for asset in ("pagetop.js?v=20260713", "responsive-menu.js?v=20260713c"):
            if text.count(asset) != 1:
                fail(findings, path, f"versioned {asset.split('?')[0]} mismatch")
    if len(style_versions) != 1:
        findings.append("stylesheet cache versions differ across pages")
    if any(len(metadata_titles[language]) != 13 or len(metadata_descriptions[language]) != 13 for language in ("en", "ja")):
        findings.append("bilingual page titles and descriptions must be unique")
    if sum(path.read_text(encoding="utf-8").count('class="member-table-column"') for path in pages) != 2 or style_text.count(".member-table-column { width: 72px; }") != 1:
        findings.append("mirrored member-table column sizing mismatch")
    if remaining_named_anchors:
        findings.append(f"legacy named anchors remain: {remaining_named_anchors}")
    if table_width_classes != 91:
        findings.append(f"table width class count mismatch: {table_width_classes}")
    if lightbox_counts != {"en": 63, "ja": 80}:
        findings.append(f"Lightbox link counts mismatch: {lightbox_counts}")
    variant_names = {f"{name}-{width}.jpg" for name in ("2026-4", "2026-3", "2025-10", "2025-9", "2025-9-2", "2025-4", "2024-12") for width in (720, 1200)}
    variant_dir = ROOT / "jp/picture/images"
    actual_variants = {path.name for path in variant_dir.glob("*-*.jpg") if re.search(r"-(?:720|1200)\.jpg$", path.name)}
    if actual_variants != variant_names:
        findings.append("responsive gallery variant inventory mismatch")
    for name in sorted(variant_names):
        path = variant_dir / name
        width = 720 if name.endswith("-720.jpg") else 1200
        expected_dimensions = (width, width * 3 // 4)
        if not path.is_file() or jpeg_dimensions(path) != expected_dimensions or path.stat().st_size > 450 * 1024:
            fail(findings, path, "responsive gallery variant dimensions or byte budget mismatch")
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

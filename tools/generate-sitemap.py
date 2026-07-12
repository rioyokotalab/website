#!/usr/bin/env python3
"""Generate the canonical bilingual sitemap from mirrored HTML paths."""

import argparse
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.rio.scrc.iir.isct.ac.jp"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"
ROBOTS = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n".encode()
ET.register_namespace("", SITEMAP_NS)
ET.register_namespace("xhtml", XHTML_NS)


def clean_url(language: str, relative: Path) -> str:
    path = relative.as_posix()
    suffix = path[:-10] if path.endswith("index.html") else path
    return f"{BASE}/{language}/{suffix}"


def add_url(root: ET.Element, location: str, en_url: str, ja_url: str) -> None:
    url = ET.SubElement(root, f"{{{SITEMAP_NS}}}url")
    ET.SubElement(url, f"{{{SITEMAP_NS}}}loc").text = location
    for language, href in (("en", en_url), ("ja", ja_url), ("x-default", f"{BASE}/")):
        ET.SubElement(url, f"{{{XHTML_NS}}}link", rel="alternate", hreflang=language, href=href)


def build() -> bytes:
    en_paths = {path.relative_to(ROOT / "en") for path in (ROOT / "en").rglob("*.html")}
    jp_paths = {path.relative_to(ROOT / "jp") for path in (ROOT / "jp").rglob("*.html")}
    if en_paths != jp_paths or len(en_paths) != 13:
        raise SystemExit("bilingual sitemap path inventory mismatch")
    root = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    add_url(root, f"{BASE}/", f"{BASE}/en/", f"{BASE}/jp/")
    for relative in sorted(en_paths, key=lambda path: path.as_posix()):
        en_url = clean_url("en", relative)
        ja_url = clean_url("jp", relative)
        add_url(root, en_url, en_url, ja_url)
        add_url(root, ja_url, en_url, ja_url)
    ET.indent(root, space="  ")
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="utf-8") + b"\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = build()
    if args.check:
        valid = (ROOT / "sitemap.xml").read_bytes() == generated and (ROOT / "robots.txt").read_bytes() == ROBOTS
        if not valid:
            print("crawler discovery files are stale", file=sys.stderr)
            raise SystemExit(1)
        print("PASS: crawler discovery files match canonical inventory")
    else:
        (ROOT / "sitemap.xml").write_bytes(generated)

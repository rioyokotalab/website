#!/usr/bin/env python3
"""Audit pinned browser and test dependencies without modifying the repository."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CDN = {
    "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css": "sha384-MzHT0pgTPI8fjMvEz54yA7HmSVjLLsxl+ytGS13+EOr/L5uLaBakmchzKgDYsSQz",
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js": "sha384-1H217gwSVyLSIfaLxHbE7dRb3v4mYCKbpQvzx0cegeju1MVsGrX5xXxAvs/HgeFs",
    "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js": "sha384-jN3Qe7xtdnQxdyZWXD9gn2Z4oRyiFuU03xQATriSicCq2SKDikN9UEJMCx+9nsJM",
}
EXPECTED_CDN_PAGES = 6
EXPECTED_PLAYWRIGHT = "1.61.1"
EXPECTED_SCRIPTS = {
    "test": "npm run test:browser",
    "test:browser:install": "PLAYWRIGHT_BROWSERS_PATH=.playwright/browsers playwright install --only-shell chromium",
    "test:browser": "PLAYWRIGHT_BROWSERS_PATH=.playwright/browsers playwright test",
    "test:consent:install": "npm run test:browser:install",
    "test:consent": "npm run test:browser",
    "test:supply-chain": "python3 tools/supply-chain-check.py",
    "test:supply-chain:online": "python3 tools/supply-chain-check.py --online",
}
TAG = re.compile(r"<(script|link)\b[^>]*>", re.I)
ATTRIBUTE = re.compile(r"([\w-]+)\s*=\s*([\"'])(.*?)\2", re.I | re.S)


def fail(message: str) -> None:
    print(f"supply-chain: {message}", file=sys.stderr)
    raise SystemExit(1)


def audit_html() -> None:
    seen: dict[str, int] = {url: 0 for url in CDN}
    pages: set[str] = set()
    for base in (ROOT / "en", ROOT / "jp"):
        for page in sorted(base.rglob("*.html")):
            text = page.read_text(encoding="utf-8")
            for match in TAG.finditer(text):
                attrs = {key.lower(): value for key, _, value in ATTRIBUTE.findall(match.group(0))}
                url = attrs.get("src") or (attrs.get("href") if attrs.get("rel", "").lower() == "stylesheet" else None)
                if not url or not re.match(r"https?://", url, re.I):
                    continue
                if url not in CDN:
                    fail(f"unreviewed external runtime asset in {page.relative_to(ROOT)}")
                if not url.startswith("https://"):
                    fail(f"non-HTTPS runtime asset in {page.relative_to(ROOT)}")
                if attrs.get("integrity") != CDN[url] or attrs.get("crossorigin", "").lower() != "anonymous":
                    fail(f"SRI/crossorigin mismatch in {page.relative_to(ROOT)}")
                seen[url] += 1
                pages.add(page.relative_to(ROOT).as_posix())
    if len(pages) != EXPECTED_CDN_PAGES or any(count != EXPECTED_CDN_PAGES for count in seen.values()):
        fail("expected each reviewed CDN asset on exactly six gallery pages")


def audit_lockfile() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    if package.get("private") is not True:
        fail("package.json must remain private")
    if package.get("scripts") != EXPECTED_SCRIPTS:
        fail("package scripts differ from the reviewed browser/supply-chain entry points")
    if package.get("devDependencies") != {"@playwright/test": EXPECTED_PLAYWRIGHT}:
        fail("Playwright must be the only direct dependency and exactly pinned")
    packages = lock.get("packages", {})
    root = packages.get("", {})
    if root.get("devDependencies") != package["devDependencies"]:
        fail("package-lock root dependencies differ from package.json")
    for name, metadata in packages.items():
        if name == "":
            continue
        if not metadata.get("integrity", "").startswith("sha512-"):
            fail(f"missing sha512 lock integrity for {name}")
        if not metadata.get("resolved", "").startswith("https://registry.npmjs.org/"):
            fail(f"unreviewed package registry for {name}")
        if metadata.get("dev") is not True:
            fail(f"non-development package in lockfile: {name}")
    for name in ("@playwright/test", "playwright", "playwright-core"):
        if packages.get(f"node_modules/{name}", {}).get("version") != EXPECTED_PLAYWRIGHT:
            fail(f"unexpected {name} version")


def audit_deploy_exclusions() -> None:
    with tempfile.TemporaryDirectory(prefix="website-supply-stage-") as temp:
        subprocess.run([str(ROOT / "tools/stage-public-site.sh"), temp], cwd=ROOT, check=True)
        staged = Path(temp)
        for path in ("package.json", "package-lock.json", "playwright.config.js", "tests", "node_modules", ".playwright"):
            if (staged / path).exists():
                fail(f"test dependency leaked into public staging: {path}")


def online_audit() -> None:
    for url, expected in CDN.items():
        request = urllib.request.Request(url, headers={"User-Agent": "website-supply-chain-check/1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            digest = "sha384-" + base64.b64encode(hashlib.sha384(response.read()).digest()).decode("ascii")
        if digest != expected:
            fail(f"downloaded CDN hash mismatch: {url}")
    with tempfile.TemporaryDirectory(prefix="website-npm-audit-") as temp:
        work = Path(temp)
        shutil.copy2(ROOT / "package.json", work / "package.json")
        shutil.copy2(ROOT / "package-lock.json", work / "package-lock.json")
        cache = work / ".npm-cache"
        subprocess.run(["npm", "ci", "--ignore-scripts", "--cache", str(cache)], cwd=work, check=True)
        subprocess.run(["npm", "audit", "--audit-level=high", "--cache", str(cache)], cwd=work, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true", help="download CDN assets and run npm audit in a temporary tree")
    args = parser.parse_args()
    audit_html()
    audit_lockfile()
    audit_deploy_exclusions()
    if args.online:
        online_audit()
    print("PASS: supply-chain checks" + (" (including online hashes and npm audit)" if args.online else ""))


if __name__ == "__main__":
    main()

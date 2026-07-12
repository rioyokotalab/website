#!/usr/bin/env python3
"""Credential-free security regression checks for the public website."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIRS = ("en", "jp", "images", "js")
PUBLIC_FILES = (".htaccess", "index.html", "style.css", "cv/cv.pdf")
BASE_URL = "https://www.rio.scrc.iir.isct.ac.jp/"
SENSITIVE_QUERY = re.compile(
    r"(?:^|[?&])(?:pwd|passcode|password|token|access_token|api[_-]?key|secret|auth|signature|sig)=",
    re.I,
)
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----" + r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[opurs]_[A-Za-z0-9]{30,}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
)
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data"}


class Finding:
    def __init__(self, category: str, path: str, line: int = 0) -> None:
        self.category = category
        self.path = path
        self.line = line

    def render(self) -> str:
        suffix = f":{self.line}" if self.line else ""
        return f"{self.category}: {self.path}{suffix}"


class PageParser(HTMLParser):
    def __init__(self, relative_path: str) -> None:
        super().__init__(convert_charrefs=True)
        self.relative_path = relative_path
        self.findings: list[Finding] = []
        self.analytics_loaders = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        line = self.getpos()[0]
        if values.get("target", "").lower() == "_blank":
            rel = set(values.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.findings.append(Finding("external-link-rel", self.relative_path, line))

        for attribute in ("href", "src", "action"):
            raw = values.get(attribute)
            if not raw:
                continue
            if SENSITIVE_QUERY.search(raw):
                self.findings.append(Finding("sensitive-url-query", self.relative_path, line))
            parsed = urlsplit(raw)
            if parsed.hostname and parsed.hostname.lower() in {
                "www.googletagmanager.com",
                "www.google-analytics.com",
                "google-analytics.com",
                "www.googleadservices.com",
            }:
                self.findings.append(Finding("analytics-request-before-consent", self.relative_path, line))
            if parsed.scheme.lower() == "http" and not (tag == "a" and attribute == "href"):
                self.findings.append(Finding("mixed-active-content", self.relative_path, line))
            if raw.split("?", 1)[0].endswith("analytics-consent.js"):
                self.analytics_loaders += 1
            self._check_local(raw, line)

    def _check_local(self, raw: str, line: int) -> None:
        parsed = urlsplit(raw)
        if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc or raw.startswith("//"):
            return
        clean = unquote(parsed.path)
        if not clean or clean == "/":
            return
        if clean.startswith("/"):
            target = ROOT / clean.lstrip("/")
        else:
            target = ROOT / Path(self.relative_path).parent / clean
        resolved = Path(os.path.normpath(target))
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            self.findings.append(Finding("local-path-traversal", self.relative_path, line))
            return
        if not resolved.exists():
            self.findings.append(Finding("broken-local-reference", self.relative_path, line))


def public_files(root: Path = ROOT) -> set[str]:
    result = {path for path in PUBLIC_FILES if (root / path).is_file()}
    for directory in PUBLIC_DIRS:
        base = root / directory
        if base.exists():
            result.update(path.relative_to(root).as_posix() for path in base.rglob("*") if path.is_file())
    return result


def html_checks() -> list[Finding]:
    findings: list[Finding] = []
    pages = [ROOT / "index.html", *sorted((ROOT / "en").rglob("*.html")), *sorted((ROOT / "jp").rglob("*.html"))]
    for page in pages:
        relative = page.relative_to(ROOT).as_posix()
        parser = PageParser(relative)
        parser.feed(page.read_text(encoding="utf-8"))
        findings.extend(parser.findings)
        if parser.analytics_loaders != 1:
            findings.append(Finding("analytics-loader-count", relative))
    return findings


def tracked_secret_checks() -> list[Finding]:
    findings: list[Finding] = []
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE
    ).stdout.split(b"\0")
    for encoded in tracked:
        if not encoded:
            continue
        relative = encoded.decode("utf-8", errors="surrogateescape")
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(f"secret-pattern-{name}", relative, line_number))
    return findings


def public_placeholder_checks() -> list[Finding]:
    findings: list[Finding] = []
    for relative in sorted(public_files()):
        data = (ROOT / relative).read_bytes()
        if b"\0" in data:
            continue
        for line_number, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            if "G-XXXXXXXXXX" in line:
                findings.append(Finding("known-placeholder-id", relative, line_number))
    return findings


def staging_checks() -> list[Finding]:
    with tempfile.TemporaryDirectory(prefix="website-security-") as temp:
        subprocess.run([str(ROOT / "tools/stage-public-site.sh"), temp], cwd=ROOT, check=True)
        staged = public_files(Path(temp))
    expected = public_files()
    return [Finding("deploy-manifest-mismatch", path) for path in sorted(expected ^ staged)]


def header_policy_source_checks() -> list[Finding]:
    text = (ROOT / ".htaccess").read_text(encoding="utf-8")
    findings: list[Finding] = []
    required = (
        "Content-Security-Policy",
        "frame-ancestors 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "style-src 'self' https://cdnjs.cloudflare.com",
        "Permissions-Policy",
        'Strict-Transport-Security "max-age=86400"',
    )
    for value in required:
        if value not in text:
            findings.append(Finding("security-header-source-missing", ".htaccess"))
    hsts_lines = [line.lower() for line in text.splitlines() if "strict-transport-security" in line.lower()]
    if any("includesubdomains" in line or "preload" in line for line in hsts_lines):
        findings.append(Finding("unsafe-hsts-scope", ".htaccess"))
    if "'unsafe-inline'" in text or "Content-Security-Policy-Report-Only" in text:
        findings.append(Finding("non-enforced-or-inline-style-csp", ".htaccess"))
    return findings


def fetch(path: str) -> tuple[int, dict[str, str]]:
    request = urllib.request.Request(urljoin(BASE_URL, path), method="GET", headers={"User-Agent": "website-security-check/1"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, {key.lower(): value for key, value in response.headers.items()}
    except urllib.error.HTTPError as error:
        return error.code, {key.lower(): value for key, value in error.headers.items()}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def http_redirect_check() -> list[Finding]:
    request = urllib.request.Request(BASE_URL.replace("https://", "http://"), method="GET", headers={"User-Agent": "website-security-check/1"})
    try:
        urllib.request.build_opener(NoRedirect).open(request, timeout=15)
        return [Finding("http-does-not-redirect", "/")]
    except urllib.error.HTTPError as error:
        location = error.headers.get("Location", "")
        if error.code not in (301, 302, 307, 308) or not location.startswith("https://"):
            return [Finding(f"http-redirect-status-{error.code}", "/")]
    return []


def live_checks() -> list[Finding]:
    findings: list[Finding] = http_redirect_check()
    source_headers = (ROOT / ".htaccess").read_text(encoding="utf-8").lower()
    csp_header = "content-security-policy-report-only" if "content-security-policy-report-only" in source_headers else "content-security-policy"
    for path in ("", "en/index.html", "jp/index.html", "cv/cv.pdf"):
        status, headers = fetch(path)
        label = "/" + path
        if status != 200:
            findings.append(Finding(f"live-status-{status}", label))
        required = {
            "x-content-type-options": "nosniff",
            "x-frame-options": "sameorigin",
            "referrer-policy": None,
            "permissions-policy": None,
            "strict-transport-security": "max-age=86400",
            csp_header: None,
        }
        for header, expected in required.items():
            value = headers.get(header, "")
            if not value or (expected and value.lower() != expected):
                findings.append(Finding(f"live-header-{header}", label))
    for path in (".dont-remove-me", "README.md", "AGENTS.md", "package.json", "tools/", ".git/"):
        status, _ = fetch(path)
        if status not in (403, 404):
            findings.append(Finding(f"deploy-excluded-live-status-{status}", "/" + path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="also perform read-only checks against the live site")
    args = parser.parse_args()
    findings = html_checks() + tracked_secret_checks() + public_placeholder_checks() + staging_checks() + header_policy_source_checks()
    if args.live:
        findings.extend(live_checks())
    if findings:
        for finding in sorted(findings, key=lambda item: (item.category, item.path, item.line)):
            print(finding.render())
        print(f"FAIL: {len(findings)} security finding(s)")
        return 1
    print("PASS: security regression checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

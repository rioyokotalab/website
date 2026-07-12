#!/usr/bin/env python3
"""Deterministic fixture mutations and static grading for the WBD suite."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
OWNER_ROOT = HERE.parents[1]
MANIFEST = HERE / "tasks.json"
PROTECTED_PREFIXES = (".git", "tests", "tools/state")
PROTECTED_FILES = {"AGENTS.md", "CLAUDE.md", ".mcp.json", "tools/todo.md"}
HANDOFF_PATHS = {"tools/codex-log.md"}
NEWS_TIME = '<time datetime="2026-02-23">2026.02.23</time>'


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _task(task_id: str) -> dict:
    for item in _manifest()["tasks"]:
        if item["id"] == task_id:
            return item
    raise ValueError(f"unknown task: {task_id}")


def _root(workspace: str | Path) -> Path:
    root = Path(workspace).resolve()
    if not root.is_dir():
        raise ValueError(f"workspace is not a directory: {root}")
    return root


def _read(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _write(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _replace_once(path: Path, old: str, new: str) -> None:
    text = _read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"mutation guard failed for {path}: expected 1 match, got {count}")
    _write(path, text.replace(old, new, 1))


def _assert_safe_workspace(root: Path) -> None:
    if root == HERE.parents[1].resolve():
        raise ValueError("refusing to mutate the owner repository")


def mutate(task_id: str, workspace: str | Path) -> dict:
    """Apply one guarded mutation. A second application fails closed."""
    root = _root(workspace)
    _assert_safe_workspace(root)
    _task(task_id)
    if task_id == "WBD-001":
        for lang in ("en", "jp"):
            path = root / lang / "index.html"
            _replace_once(path, NEWS_TIME, "2026.02.23")
        changed = ["en/index.html", "jp/index.html"]
    elif task_id == "WBD-002":
        for lang, label in (("en", "Download CV (PDF)"), ("jp", "履歴書（PDF）をダウンロード")):
            path = root / lang / "member/yokota.html"
            old = f'<a href="../../cv/cv.pdf" type="application/pdf" target="_blank" rel="noopener noreferrer">{label}</a>'
            new = '<a href="../../cv/cv.pdf" target="_blank"></a>'
            _replace_once(path, old, new)
        changed = ["en/member/yokota.html", "jp/member/yokota.html"]
    elif task_id == "WBD-003":
        path = root / "js/analytics-consent.js"
        _replace_once(path, "\t\tremoveAnalyticsCookies();", "\t\t/* benchmark fault: cookies retained */")
        _replace_once(path, "\t\tbanner.querySelector(\"button\").focus();", "\t\tactions.lastElementChild.focus();")
        _replace_once(path, "\tif (readChoice() === accepted) {\n\t\tenableAnalytics();\n\t}", "\tif (readChoice() === accepted || readChoice() === null) {\n\t\tenableAnalytics();\n\t}")
        changed = ["js/analytics-consent.js"]
    elif task_id == "WBD-004":
        path = root / "style.css"
        _replace_once(path, "\tpadding: 0 16px;", "\tpadding: 0 72px;")
        _replace_once(path, "\twidth: 50%;\n\tfloat: left;\n\tborder-bottom:", "\twidth: 100%;\n\tfloat: left;\n\tborder-bottom:")
        changed = ["style.css"]
    elif task_id == "WBD-005":
        css = root / "style.css"
        _replace_once(css, "\t\ttransition-duration: 0.01ms !important;", "\t\ttransition-duration: 600ms !important;")
        js = root / "js/lightbox-accessibility.js"
        old = "motionPreference.matches ? {\n\t\t\t\tfadeDuration: 0, imageFadeDuration: 0, resizeDuration: 0\n\t\t\t} : motionOptions"
        new = "motionPreference.matches ? motionOptions : {\n\t\t\t\tfadeDuration: 0, imageFadeDuration: 0, resizeDuration: 0\n\t\t\t}"
        _replace_once(js, old, new)
        stale = []
        for rel in ("en/picture/index.html", "jp/picture/index.html", "en/research/index.html", "jp/research/index.html"):
            path = root / rel
            text = _read(path)
            match = re.search(r"lightbox-accessibility\.js\?v=([A-Za-z0-9._-]+)", text)
            if not match or match.group(1) == "stale-benchmark":
                raise RuntimeError(f"mutation guard failed for {rel}")
            _write(path, text[:match.start(1)] + "stale-benchmark" + text[match.end(1):])
            stale.append(rel)
        changed = ["style.css", "js/lightbox-accessibility.js", *stale]
    else:  # pragma: no cover
        raise ValueError(task_id)
    return {"task_id": task_id, "workspace": str(root), "changed": changed}


def _all_files(root: Path) -> dict[str, bytes]:
    result = {}
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.relative_to(root).parts:
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def _allowed(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(rel, pattern) for pattern in patterns)


def reduced_motion_zero(js: str) -> bool:
    zero_object = r"\{\s*fadeDuration:\s*0,\s*imageFadeDuration:\s*0,\s*resizeDuration:\s*0\s*\}"
    if re.search(rf"motionPreference\.matches\s*\?\s*{zero_object}\s*:\s*motionOptions", js, re.S):
        return True
    named = re.search(rf"const\s+([A-Za-z_$][\w$]*)\s*=\s*{zero_object}\s*;", js, re.S)
    return bool(named and re.search(
        rf"motionPreference\.matches\s*\?\s*{re.escape(named.group(1))}\s*:\s*motionOptions", js, re.S
    ))


def _scope(task: dict, workspace: Path, baseline: Path | str) -> tuple[int, list[str]]:
    current = _all_files(workspace)
    if baseline == "HEAD":
        result = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=workspace, text=True, capture_output=True, check=True)
        changed = sorted(line[3:] for line in result.stdout.splitlines() if len(line) >= 4)
    else:
        before = _all_files(Path(baseline))
        changed = sorted(key for key in current.keys() | before.keys() if current.get(key) != before.get(key))
    changed = [rel for rel in changed if rel not in HANDOFF_PATHS and not rel.startswith("tools/out/")]
    unauthorized = [rel for rel in changed if not _allowed(rel, task["authorized_paths"])]
    protected = [rel for rel in changed if rel in PROTECTED_FILES or rel.startswith(PROTECTED_PREFIXES)]
    details = [f"changed:{rel}" for rel in changed]
    if unauthorized:
        details.extend(f"unauthorized:{rel}" for rel in unauthorized)
    if protected:
        details.extend(f"protected:{rel}" for rel in protected)
    crlf_bad = []
    for rel in changed:
        if rel.endswith(".html") and rel in current:
            data = current[rel]
            if re.search(b"(?<!\\r)\\n", data):
                crlf_bad.append(rel)
    details.extend(f"bare-lf:{rel}" for rel in crlf_bad)
    return (15 if not unauthorized and not protected and not crlf_bad else 0), details


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[dict] = []
        self.links: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self.stack.append({"attrs": {k.lower(): v or "" for k, v in attrs}, "text": ""})

    def handle_data(self, data: str) -> None:
        if self.stack:
            self.stack[-1]["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.stack:
            self.links.append(self.stack.pop())


def _checks(task_id: str, root: Path) -> list[tuple[str, bool]]:
    checks: list[tuple[str, bool]] = []
    if task_id == "WBD-001":
        for lang in ("en", "jp"):
            text = _read(root / lang / "index.html")
            row = re.search(r'<tr>.*?<time datetime="2026-02-23">2026\.02\.23</time>.*?<a href="news/index\.html#ev260223">.*?</a>.*?</tr>', text, re.I | re.S)
            first = re.search(r"<table class=\"wn width-98pct\">.*?<tr>(.*?)</tr>", text, re.I | re.S)
            checks += [(f"{lang}:exact-row", bool(row)), (f"{lang}:single-time", text.count(NEWS_TIME) == 1), (f"{lang}:newest", bool(first and NEWS_TIME in first.group(1)))]
        checks.append(("mirrored-date-count", _read(root / "en/index.html").count(NEWS_TIME) == _read(root / "jp/index.html").count(NEWS_TIME) == 1))
    elif task_id == "WBD-002":
        for lang, label in (("en", "Download CV (PDF)"), ("jp", "履歴書（PDF）をダウンロード")):
            parser = _Links(); parser.feed(_read(root / lang / "member/yokota.html"))
            links = [x for x in parser.links if x["attrs"].get("href") == "../../cv/cv.pdf"]
            link = links[0] if len(links) == 1 else {"attrs": {}, "text": ""}
            attrs = link["attrs"]
            checks += [(f"{lang}:one", len(links) == 1), (f"{lang}:rel", {"noopener", "noreferrer"} <= set(attrs.get("rel", "").split())), (f"{lang}:pdf", attrs.get("type") == "application/pdf"), (f"{lang}:target", attrs.get("target") == "_blank"), (f"{lang}:name", link["text"].strip() == label)]
    elif task_id == "WBD-003":
        text = _read(root / "js/analytics-consent.js")
        conservative_focus = any(expression in text for expression in (
            'banner.querySelector("button").focus();',
            'actions.firstElementChild.focus();',
            'banner.querySelector(".analytics-consent-reject").focus();',
        ))
        checks = [
            ("accepted-only-autoload", "readChoice() === accepted ||" not in text and "if (readChoice() === accepted)" in text),
            ("cookie-removal-call", text.count("removeAnalyticsCookies();") == 1),
            ("reject-first-focus", conservative_focus),
            ("denied-default", text.count('analytics_storage: "denied"') >= 2),
            ("accepted-once-guard", "if (analyticsLoaded)" in text),
        ]
    elif task_id == "WBD-004":
        text = _read(root / "style.css")
        mobile = text[text.find("@media only screen and (max-width:900px)"):text.find("/* Privacy-first analytics consent */")]
        checks = [("wrapper-padding", "padding: 0 16px;" in mobile), ("menu-two-column", re.search(r"ul\.topnav li\s*\{[^}]*width:\s*50%;", mobile, re.S) is not None), ("mobile-breakpoint", "@media only screen and (max-width:900px)" in text), ("menu-containment", "#menubar-s.is-collapsed" in mobile)]
    elif task_id == "WBD-005":
        css = _read(root / "style.css"); js = _read(root / "js/lightbox-accessibility.js")
        versions = []
        for path in sorted([*root.glob("en/**/*.html"), *root.glob("jp/**/*.html")]):
            match = re.search(r"lightbox-accessibility\.js\?v=([A-Za-z0-9._-]+)", _read(path))
            if match: versions.append((path.relative_to(root).as_posix(), match.group(1)))
        checks = [
            ("css-zero-motion", "transition-duration: 0.01ms !important;" in css),
            ("js-reduced-zero", reduced_motion_zero(js)),
            ("ordinary-timings", "fadeDuration: 600, imageFadeDuration: 600, resizeDuration: 700" in js),
            ("live-change", 'motionPreference.addEventListener("change", applyMotionPreference)' in js),
            ("one-query-version", bool(versions) and len({value for _, value in versions}) == 1 and all(value != "stale-benchmark" for _, value in versions)),
            ("mirrored-helper-count", sum(rel.startswith("en/") for rel, _ in versions) == sum(rel.startswith("jp/") for rel, _ in versions)),
        ]
    return checks


def _run_p2p(task: dict, root: Path, requested: bool) -> tuple[int, list[dict]]:
    if not requested:
        return 0, [{"status": "skipped", "reason": "use --run-tests"}]
    results = []
    for argv in task["p2p"]:
        command = list(argv)
        env = None
        if command[:2] == ["npx", "playwright"]:
            executable = root / "node_modules/.bin/playwright"
            if not executable.is_file():
                executable = OWNER_ROOT / "node_modules/.bin/playwright"
            if not executable.is_file():
                results.append({"argv": argv, "returncode": 127, "stdout_tail": "", "stderr_tail": f"missing pinned Playwright: {executable}"})
                continue
            command = [str(executable), *command[2:]]
            import os
            env = os.environ.copy()
            env["NODE_PATH"] = str(executable.parents[1])
            env["PLAYWRIGHT_BROWSERS_PATH"] = str(OWNER_ROOT / ".playwright/browsers")
        completed = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True, timeout=task["timeout_seconds"], check=False)
        results.append({"argv": argv, "resolved_argv": command, "returncode": completed.returncode, "stdout_tail": completed.stdout[-2000:], "stderr_tail": completed.stderr[-2000:]})
    passed = sum(item["returncode"] == 0 for item in results)
    return round(25 * passed / len(results)) if results else 25, results


def grade(task_id: str, workspace: str | Path, baseline: str | Path, run_p2p: bool = False, *, completed: bool = True) -> dict:
    """Grade a candidate workspace against its post-mutation baseline."""
    root, task = _root(workspace), _task(task_id)
    before: Path | str = "HEAD" if str(baseline) == "HEAD" else _root(baseline)
    assertions = _checks(task_id, root)
    passed = sum(ok for _, ok in assertions)
    f2p = round(55 * passed / len(assertions)) if assertions else 0
    p2p, p2p_results = _run_p2p(task, root, run_p2p)
    scope, scope_details = _scope(task, root, before)
    completion = 5 if completed else 0
    components = {"f2p": f2p, "p2p": p2p, "scope": scope, "completion": completion}
    critical_names = {
        "WBD-001": {"en:exact-row", "jp:exact-row", "mirrored-date-count"},
        "WBD-002": {"en:rel", "jp:rel", "en:name", "jp:name"},
        "WBD-003": {"accepted-only-autoload", "cookie-removal-call", "reject-first-focus"},
        "WBD-004": {"wrapper-padding", "menu-two-column"},
        "WBD-005": {"css-zero-motion", "js-reduced-zero", "one-query-version"},
    }[task_id]
    failed = [name for name, ok in assertions if not ok]
    critical_pass = not any(name in critical_names for name in failed) and scope == 15 and (not run_p2p or p2p == 25)
    findings = [f"failed:{name}" for name in failed] + scope_details
    findings += [f"p2p-failed:{' '.join(item['argv'])}" for item in p2p_results if item.get("returncode", 0) != 0]
    return {
        "task_id": task_id,
        "score": sum(components.values()),
        "critical_pass": critical_pass,
        "f2p": f2p,
        "p2p": p2p,
        "scope": scope,
        "completion": completion,
        "findings": findings,
        "components": components,
        "component_max": {"f2p": 55, "p2p": 25, "scope": 15, "completion": 5},
        "assertions": [{"name": name, "passed": ok} for name, ok in assertions],
        "scope_details": scope_details,
        "p2p_results": p2p_results,
    }


def _copy_repo(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", ".playwright", "node_modules", "tools/out", "tools/agent-benchmark"))


def selftest(source: str | Path) -> dict:
    """Exercise all mutations and static graders only in temporary copies."""
    source = _root(source)
    outcomes = []
    with tempfile.TemporaryDirectory(prefix="task-ops-selftest-") as temp:
        temp_root = Path(temp)
        for task in _manifest()["tasks"]:
            task_id = task["id"]
            clean = temp_root / f"{task_id}-clean"
            broken = temp_root / f"{task_id}-broken"
            baseline = temp_root / f"{task_id}-baseline"
            _copy_repo(source, clean); shutil.copytree(clean, broken)
            mutation = mutate(task_id, broken)
            shutil.copytree(broken, baseline)
            broken_grade = grade(task_id, broken, baseline)
            guard_passed = False
            try:
                mutate(task_id, broken)
            except RuntimeError:
                guard_passed = True
            clean_grade = grade(task_id, clean, clean)
            expected_broken = broken_grade["components"]["f2p"] < 55
            expected_clean = clean_grade["components"]["f2p"] == 55
            outcomes.append({"task_id": task_id, "mutation": mutation, "idempotence_guard": guard_passed, "broken_detected": expected_broken, "clean_static_pass": expected_clean, "broken_f2p": broken_grade["components"]["f2p"], "clean_f2p": clean_grade["components"]["f2p"]})
    ok = all(item["idempotence_guard"] and item["broken_detected"] and item["clean_static_pass"] for item in outcomes)
    return {"status": "pass" if ok else "fail", "outcomes": outcomes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    mutate_parser = sub.add_parser("mutate")
    mutate_parser.add_argument("task_id"); mutate_parser.add_argument("workspace")
    grade_parser = sub.add_parser("grade")
    grade_parser.add_argument("task_id"); grade_parser.add_argument("workspace")
    grade_parser.add_argument("--baseline", required=True); grade_parser.add_argument("--run-p2p", action="store_true")
    grade_parser.add_argument("--incomplete", action="store_true")
    self_parser = sub.add_parser("selftest"); self_parser.add_argument("source", nargs="?", default=str(HERE.parents[1]))
    args = parser.parse_args(argv)
    try:
        if args.command == "mutate": result = mutate(args.task_id, args.workspace)
        elif args.command == "grade": result = grade(args.task_id, args.workspace, args.baseline, run_p2p=args.run_p2p, completed=not args.incomplete)
        else: result = selftest(args.source)
    except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") != "fail" else 1


if __name__ == "__main__":
    sys.exit(main())

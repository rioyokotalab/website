#!/usr/bin/env python3
"""Run isolated, capability-gated Codex web-development benchmarks."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
TASKS_PATH = BENCHMARK_DIR / "tasks.json"
RESULTS_PATH = BENCHMARK_DIR / "results.jsonl"
EXCLUSIONS_PATH = BENCHMARK_DIR / "exclusions.json"
ARTIFACTS_ROOT = ROOT / "tools" / "out" / "agent-benchmark"


def load_tasks() -> dict[str, dict[str, Any]]:
    data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    tasks = data["tasks"] if isinstance(data, dict) else data
    result = {task["id"]: task for task in tasks}
    if len(result) != len(tasks):
        raise ValueError("duplicate benchmark task id")
    return result


def load_task_ops():
    path = BENCHMARK_DIR / "task_ops.py"
    spec = importlib.util.spec_from_file_location("agent_benchmark_task_ops", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_checked(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True)


def archive_repository(ref: str, destination: Path) -> None:
    archive = subprocess.run(["git", "archive", "--format=tar", ref], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as bundle:
        bundle.extractall(destination, filter="data")
    shutil.rmtree(destination / "tools" / "agent-benchmark", ignore_errors=True)
    shutil.rmtree(destination / "tools" / "out", ignore_errors=True)
    # Give the worker the repository's pinned test CLI without permitting an
    # install or exposing the owner's dependency tree to writes. Browser assets
    # remain external and are selected by PLAYWRIGHT_BROWSERS_PATH.
    shutil.copytree(ROOT / "node_modules", destination / "node_modules", symlinks=True)


def initialize_fixture_git(workspace: Path) -> None:
    run_checked(["git", "init", "--quiet"], cwd=workspace)
    run_checked(["git", "config", "user.name", "YOKOTA benchmark"], cwd=workspace)
    run_checked(["git", "config", "user.email", "benchmark.invalid"], cwd=workspace)
    run_checked(["git", "add", "-A"], cwd=workspace)
    run_checked(["git", "commit", "--quiet", "-m", "benchmark pristine fixture"], cwd=workspace)


def commit_mutated_fixture(workspace: Path, task_id: str) -> None:
    run_checked(["git", "add", "-A"], cwd=workspace)
    run_checked(["git", "commit", "--quiet", "--allow-empty", "-m", f"fixture {task_id}"], cwd=workspace)


def make_fixture(task_id: str, ref: str, workspace: Path, reference_output: Path | None = None) -> dict[str, Any]:
    archive_repository(ref, workspace)
    initialize_fixture_git(workspace)
    reference = make_visual_reference(workspace, reference_output) if task_id == "WBD-004" and reference_output else None
    mutation = load_task_ops().mutate(task_id, workspace)
    commit_mutated_fixture(workspace, task_id)
    (workspace / "tools" / "out").mkdir(parents=True, exist_ok=True)
    return {"mutation": mutation, "reference": str(reference) if reference else None}


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def make_visual_reference(workspace: Path, output: Path) -> Path:
    """Capture the WBD-004 pristine mobile target outside the agent-visible tree."""
    output.parent.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=workspace, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    script = """
const { chromium } = require('@playwright/test');
(async () => {
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage({viewport: {width: 390, height: 844}, deviceScaleFactor: 1});
  await page.addInitScript(() => localStorage.setItem('yokota_analytics_consent_v1', 'rejected'));
  await page.goto(process.argv[1], {waitUntil: 'networkidle'});
  await page.locator('#menubar_hdr').click();
  await page.screenshot({path: process.argv[2], fullPage: true, animations: 'disabled'});
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
"""
    env = os.environ.copy()
    env["NODE_PATH"] = str(ROOT / "node_modules")
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".playwright" / "browsers")
    try:
        for _ in range(30):
            with socket.socket() as probe:
                if probe.connect_ex(("127.0.0.1", port)) == 0:
                    break
            time.sleep(0.1)
        run_checked(["node", "-e", script, f"http://127.0.0.1:{port}/en/index.html", str(output)],
                    cwd=workspace, env=env)
    finally:
        os.killpg(server.pid, signal.SIGTERM)
        server.wait(timeout=5)
    return output


def prompt_for(task: dict[str, Any], task_id: str, prompt_mode: str) -> str:
    paths = ", ".join(task["authorized_paths"])
    context = ", ".join(task.get("context", []))
    deliverable = f"tools/out/benchmark-{task_id.lower()}.md"
    if prompt_mode == "compact":
        return (
            f"Benchmark WORKER task {task_id}. {task['prompt']}\n"
            f"Scope: {paths}. Read: {context}. Offline only. Do not deploy, publish, push, "
            f"touch credentials, configuration, tests, or ledger. Implement and run targeted checks. "
            f"Record the required structured result in {deliverable}."
        )
    return f"""You are a bounded WORKER in an isolated benchmark copy of the YOKOTA Lab website.

Task {task_id}: {task['title']}
Owner request: {task['prompt']}

Read AGENTS.md and these task-relevant context files before editing: {context}.
You are explicitly authorized to edit only: {paths}.
Do not edit tests, ledger, configuration, unrelated files, or .git. Do not use the
network. Never run publishing/deployment commands, ssh, lftp, or git push. Do not
access credentials. Preserve CRLF and EN/JP parity where applicable.

Inspect the failure, implement the smallest complete fix, and run targeted local
checks. Write the required output-file-first structured result to {deliverable}
and follow the repository's delegated-task logging rule. Do not merely propose a
patch: make the authorized edits in this isolated workspace.
"""


def parse_jsonl(path: Path) -> tuple[dict[str, int] | None, dict[str, int], str | None, int, dict[str, Any]]:
    usage = None
    item_types: dict[str, int] = {}
    final_message = None
    invalid = 0
    completed_commands = 0
    failed_commands = 0
    command_output_chars = 0
    command_input_chars = 0
    context_paths: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            invalid += 1
            continue
        if event.get("type") == "turn.completed":
            usage = event.get("usage")
        if event.get("type") != "item.completed":
            continue
        item = event.get("item") or {}
        item_type = item.get("type")
        if item_type:
            item_types[item_type] = item_types.get(item_type, 0) + 1
            if item_type == "agent_message":
                final_message = item.get("text")
            if item_type == "command_execution":
                completed_commands += 1
                if item.get("exit_code") not in (0, None):
                    failed_commands += 1
                command = item.get("command") or ""
                command_input_chars += len(command)
                command_output_chars += len(item.get("aggregated_output") or "")
                context_paths.update(re.findall(
                    r"(?:^|[\s'\"])(AGENTS\.md|CLAUDE\.md|skills/[A-Za-z0-9_.-]+\.md|tools/todo\.md|tools/state/[A-Za-z0-9_.-]+\.md)",
                    command,
                ))
    tool_metrics = {
        "completed_commands": completed_commands,
        "failed_commands": failed_commands,
        "command_input_chars": command_input_chars,
        "command_output_chars": command_output_chars,
        "observed_context_paths": sorted(context_paths),
    }
    return usage, item_types, final_message, invalid, tool_metrics


def changed_files(workspace: Path) -> list[str]:
    result = run_checked(["git", "status", "--short"], cwd=workspace)
    return [line[3:] for line in result.stdout.splitlines() if len(line) >= 4]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_codex(task: dict[str, Any], task_id: str, workspace: Path, artifact: Path,
              *, model: str, effort: str, prompt_mode: str, reference: Path | None,
              timeout_seconds: int) -> dict[str, Any]:
    prompt = prompt_for(task, task_id, prompt_mode)
    prompt_path = artifact / "prompt.txt"
    stdout_path = artifact / "stdout.jsonl"
    stderr_path = artifact / "stderr.log"
    prompt_path.write_text(prompt, encoding="utf-8")
    command = [
        "codex", "exec", "--json", "--ephemeral", "-C", str(workspace),
        "-s", "danger-full-access", "-m", model,
        "-c", f'model_reasoning_effort="{effort}"',
        "-c", 'approval_policy="never"',
    ]
    if reference:
        command.extend(["--image", str(reference)])
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".playwright" / "browsers")
    env["NODE_PATH"] = str(ROOT / "node_modules")
    started = time.monotonic()
    timed_out = False
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(command, cwd=workspace, env=env, stdin=subprocess.PIPE,
                                   stdout=stdout, stderr=stderr, text=True,
                                   start_new_session=True)
        assert process.stdin is not None
        process.stdin.write(prompt)
        process.stdin.close()
        try:
            exit_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                exit_code = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                exit_code = process.wait()
    duration_ms = round((time.monotonic() - started) * 1000)
    usage, item_types, final_message, invalid_jsonl, tool_metrics = parse_jsonl(stdout_path)
    if final_message:
        (artifact / "final-message.md").write_text(final_message + "\n", encoding="utf-8")
    return {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
        "usage": usage,
        "item_types": item_types,
        "tool_metrics": tool_metrics,
        "invalid_jsonl_lines": invalid_jsonl,
        "prompt_bytes": len(prompt.encode("utf-8")),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "stdout_path": str(stdout_path.relative_to(ROOT)),
        "stderr_path": str(stderr_path.relative_to(ROOT)),
    }


def task_route(task: dict[str, Any], model: str | None, effort: str | None,
               worker_override: str | None = None) -> tuple[str, str, str]:
    registry = json.loads((ROOT / "tools" / "codex-workers.json").read_text(encoding="utf-8"))
    workers = registry["workers"] if "workers" in registry else registry
    worker_name = worker_override or task.get("default_worker") or task["worker"]
    if worker_name not in workers:
        raise ValueError(f"unknown worker: {worker_name}")
    worker = workers[worker_name]
    return model or worker["model"], effort or worker["effort"], worker_name


def append_result(result: dict[str, Any]) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def run_one(args: argparse.Namespace) -> dict[str, Any]:
    tasks = load_tasks()
    task = tasks[args.task_id]
    if task.get("held_out") and not args.include_held_out:
        raise SystemExit(f"{args.task_id} is held out; pass --include-held-out only after candidate freeze")
    model, effort, worker_name = task_route(task, args.model, args.effort, args.worker)
    run_id = args.run_id or f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{args.task_id.lower()}-{uuid.uuid4().hex[:6]}"
    artifact = ARTIFACTS_ROOT / run_id
    artifact.mkdir(parents=True, exist_ok=False)
    workspace_parent = Path(args.workspace_root) if args.workspace_root else Path(tempfile.gettempdir())
    workspace = Path(tempfile.mkdtemp(prefix=f"yokota-{run_id}-", dir=workspace_parent))
    total_started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "run_label": args.run_label,
        "task_id": args.task_id,
        "task_version": task["version"],
        "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repo_ref": args.ref,
        "model": model,
        "effort": effort,
        "worker": worker_name,
        "prompt_mode": args.prompt_mode,
        "codex_cli": subprocess.run(["codex", "--version"], text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL).stdout.strip(),
    }
    try:
        setup_started = time.monotonic()
        reference_output = artifact / "reference.png" if args.task_id == "WBD-004" else None
        fixture = make_fixture(args.task_id, args.ref, workspace, reference_output)
        result["setup_duration_ms"] = round((time.monotonic() - setup_started) * 1000)
        result["instruction_bytes"] = (workspace / "AGENTS.md").stat().st_size
        reference = Path(fixture["reference"]) if fixture.get("reference") else None
        result["fixture"] = fixture["mutation"]
        execution = run_codex(task, args.task_id, workspace, artifact, model=model,
                              effort=effort, prompt_mode=args.prompt_mode,
                              reference=reference, timeout_seconds=args.timeout or task["timeout_seconds"])
        result["execution"] = execution
        diff = run_checked(["git", "diff", "--binary", "HEAD"], cwd=workspace).stdout
        (artifact / "candidate.patch").write_text(diff, encoding="utf-8")
        result["changed_files"] = changed_files(workspace)
        grader_started = time.monotonic()
        grade = load_task_ops().grade(args.task_id, workspace, "HEAD", run_p2p=args.run_p2p)
        if args.task_id == "WBD-004" and reference:
            candidate_image = artifact / "candidate.png"
            try:
                make_visual_reference(workspace, candidate_image)
                reference_sha = sha256_file(reference)
                candidate_sha = sha256_file(candidate_image)
                visual_match = reference_sha == candidate_sha
                grade["visual"] = {
                    "reference_sha256": reference_sha,
                    "candidate_sha256": candidate_sha,
                    "exact_match": visual_match,
                }
                if not visual_match:
                    grade["critical_pass"] = False
                    grade.setdefault("findings", []).append("visual-reference-mismatch")
            except Exception as error:
                grade["critical_pass"] = False
                grade["visual"] = {"exact_match": False, "error": str(error)}
                grade.setdefault("findings", []).append("visual-reference-capture-failed")
        result["grader_duration_ms"] = round((time.monotonic() - grader_started) * 1000)
        if execution["exit_code"] != 0 or execution["timed_out"]:
            grade["completion"] = 0
            grade.setdefault("components", {})["completion"] = 0
            grade["score"] = sum(int(value) for value in grade["components"].values())
            grade.setdefault("findings", []).append("Codex turn failed or timed out")
        result["grade"] = grade
        usage = execution.get("usage") or {}
        if usage:
            result["effective_tokens"] = (
                usage.get("input_tokens", 0) - usage.get("cached_input_tokens", 0)
                + usage.get("output_tokens", 0)
            )
        result["capability_pass"] = bool(
            grade.get("critical_pass") and grade.get("score", 0) >= 85
            and (not args.run_p2p or grade.get("p2p") == 25)
            and execution["exit_code"] == 0 and not execution["timed_out"]
        )
        if execution["exit_code"] != 0 or execution["timed_out"]:
            result["failure_phase"] = "worker"
        elif grade.get("scope") != 15:
            result["failure_phase"] = "scope"
        elif args.run_p2p and grade.get("p2p") != 25:
            result["failure_phase"] = "p2p"
        elif not grade.get("critical_pass"):
            result["failure_phase"] = "f2p-or-visual"
        elif grade.get("score", 0) < 85:
            result["failure_phase"] = "capability-gate"
        else:
            result["failure_phase"] = None
        observed = execution["tool_metrics"]["observed_context_paths"]
        result["observed_context"] = [
            {"path": path, "bytes": (workspace / path).stat().st_size}
            for path in observed if (workspace / path).is_file()
        ]
        result["total_duration_ms"] = round((time.monotonic() - total_started) * 1000)
        (artifact / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                             encoding="utf-8")
        append_result(result)
        return result
    finally:
        if args.keep_workspace:
            result["workspace"] = str(workspace)
        else:
            shutil.rmtree(workspace, ignore_errors=True)


def summarize(label: str | None = None) -> dict[str, Any]:
    exclusions = json.loads(EXCLUSIONS_PATH.read_text(encoding="utf-8")) if EXCLUSIONS_PATH.exists() else {}
    rows = []
    excluded = []
    if RESULTS_PATH.exists():
        for line in RESULTS_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                if label is None or row.get("run_label") == label:
                    if row.get("run_id") in exclusions:
                        excluded.append({"run_id": row["run_id"], "reason": exclusions[row["run_id"]]})
                    else:
                        rows.append(row)
    passed = [row for row in rows if row.get("capability_pass")]
    return {
        "runs": len(rows),
        "excluded_runs": excluded,
        "passed": len(passed),
        "mean_score": round(sum(row["grade"]["score"] for row in rows) / len(rows), 2) if rows else None,
        "effective_tokens_passing": sum(row.get("effective_tokens", 0) for row in passed),
        "effective_tokens_all": sum(row.get("effective_tokens", 0) for row in rows),
        "input_tokens": sum((row.get("execution", {}).get("usage") or {}).get("input_tokens", 0) for row in rows),
        "cached_input_tokens": sum((row.get("execution", {}).get("usage") or {}).get("cached_input_tokens", 0) for row in rows),
        "output_tokens": sum((row.get("execution", {}).get("usage") or {}).get("output_tokens", 0) for row in rows),
        "reasoning_output_tokens": sum((row.get("execution", {}).get("usage") or {}).get("reasoning_output_tokens", 0) for row in rows),
        "duration_ms": sum(row.get("execution", {}).get("duration_ms", 0) for row in rows),
        "tasks": [{"task_id": row["task_id"], "score": row["grade"]["score"],
                   "pass": row.get("capability_pass"), "effective_tokens": row.get("effective_tokens")}
                  for row in rows],
    }


def selftest() -> dict[str, Any]:
    tasks = load_tasks()
    assert set(tasks) == {f"WBD-{number:03d}" for number in range(1, 6)}
    assert tasks["WBD-005"].get("held_out") is True
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "events.jsonl"
        path.write_text(
            '{"type":"item.completed","item":{"type":"agent_message","text":"ok"}}\n'
            '{"type":"turn.completed","usage":{"input_tokens":100,"cached_input_tokens":40,"output_tokens":12,"reasoning_output_tokens":3}}\n',
            encoding="utf-8",
        )
        usage, item_types, final_message, invalid, tool_metrics = parse_jsonl(path)
        assert usage and usage["input_tokens"] == 100
        assert item_types == {"agent_message": 1} and final_message == "ok" and invalid == 0
        assert tool_metrics["completed_commands"] == 0
    return {"status": "ok", "tasks": len(tasks), "telemetry_parser": "ok"}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="command", required=True)
    subcommands.add_parser("list")
    run = subcommands.add_parser("run")
    run.add_argument("task_id")
    run.add_argument("--ref", default="HEAD")
    run.add_argument("--run-id")
    run.add_argument("--run-label", default="development")
    run.add_argument("--model")
    run.add_argument("--worker")
    run.add_argument("--effort", choices=("low", "medium", "high"))
    run.add_argument("--prompt-mode", choices=("full", "compact"), default="full")
    run.add_argument("--timeout", type=int)
    run.add_argument("--workspace-root")
    run.add_argument("--run-p2p", action="store_true")
    run.add_argument("--include-held-out", action="store_true")
    run.add_argument("--keep-workspace", action="store_true")
    summary = subcommands.add_parser("summarize")
    summary.add_argument("--run-label")
    subcommands.add_parser("selftest")
    return command


def main() -> int:
    args = parser().parse_args()
    if args.command == "list":
        for task in load_tasks().values():
            held = " [held out]" if task.get("held_out") else ""
            print(f"{task['id']}: {task['title']}{held}")
        return 0
    if args.command == "run":
        print(json.dumps(run_one(args), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "summarize":
        print(json.dumps(summarize(args.run_label), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "selftest":
        print(json.dumps(selftest(), indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

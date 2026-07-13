#!/usr/bin/env python3
"""Run frozen WBD tasks against isolated Claude Code configuration variants."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = Path(__file__).resolve().parent
PROFILES_DIR = ROOT / ".claude" / "benchmark-profiles"
RESULTS_PATH = BENCHMARK_DIR / "claude-results.jsonl"
ARTIFACTS_ROOT = ROOT / "tools" / "out" / "claude-benchmark"
FROZEN_REF = "3364e2c3617b1fa0d0d044a8d5a5d1af3faa548d"
VARIANTS = ("current-harness", "autonomous", "dynamic")
CONFIG_PATHS = ("CLAUDE.md", "AGENTS.md", ".claude", ".mcp.json")
LIVE_ROOT = "/home/rioyokota/website"


def _load_core():
    path = BENCHMARK_DIR / "benchmark.py"
    spec = importlib.util.spec_from_file_location("agent_benchmark_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = _load_core()

DYNAMIC_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["strategy", "coordinator_prompt", "agents"],
    "properties": {
        "strategy": {"type": "string", "maxLength": 1200},
        "coordinator_prompt": {"type": "string", "maxLength": 5000},
        "agents": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "description", "prompt", "model", "effort"],
                "properties": {
                    "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]{1,31}$"},
                    "description": {"type": "string", "maxLength": 300},
                    "prompt": {"type": "string", "maxLength": 4000},
                    "model": {"enum": ["sonnet", "opus"]},
                    "effort": {"enum": ["low", "medium", "high"]},
                },
            },
        },
    },
}

SAFETY = """This is an isolated, offline benchmark fixture. Work only inside the current
workspace. Never access credentials or the parent repository; never use the network,
publish, deploy, push, ssh, or lftp; never edit tests, configuration, ledger, .git, or
tools/out. Only the task prompt authorizes implementation files. The independent runner
owns grading, artifacts, and bookkeeping."""


def read_profile(variant: str) -> dict[str, Any]:
    path = PROFILES_DIR / f"{variant}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("variant") != variant or value.get("fixture_ref") != FROZEN_REF:
        raise ValueError(f"invalid or drifting profile: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def config_snapshot(workspace: Path) -> tuple[str, int, list[str]]:
    items: list[tuple[str, bytes]] = []
    for name in CONFIG_PATHS:
        path = workspace / name
        paths = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else []
        for item in paths:
            relative = item.relative_to(workspace).as_posix()
            data = item.read_bytes().replace(str(workspace).encode(), b"<WORKSPACE>")
            items.append((relative, data))
    digest = hashlib.sha256()
    for relative, data in items:
        digest.update(relative.encode() + b"\0" + data + b"\0")
    return digest.hexdigest(), sum(len(data) for _, data in items), [relative for relative, _ in items]


def replace_live_root(workspace: Path) -> int:
    old = LIVE_ROOT.encode()
    new = str(workspace).encode()
    changed = 0
    for root_name in ("CLAUDE.md", "AGENTS.md", ".claude", "skills"):
        root = workspace / root_name
        paths = [root] if root.is_file() else root.rglob("*") if root.is_dir() else []
        for path in paths:
            if not path.is_file():
                continue
            data = path.read_bytes()
            if b"\0" in data[:4096] or old not in data:
                continue
            path.write_bytes(data.replace(old, new))
            changed += 1
    return changed


def remove_project_config(workspace: Path) -> list[str]:
    removed: list[str] = []
    for name in CONFIG_PATHS:
        path = workspace / name
        if path.is_dir():
            shutil.rmtree(path)
            removed.append(name + "/")
        elif path.exists():
            path.unlink()
            removed.append(name)
    return removed


def common_fixture_safety(workspace: Path, reference: Path | None) -> dict[str, Any]:
    removed = []
    for name in ("publish.sh", "deploy.sh"):
        path = workspace / name
        if path.exists():
            path.unlink()
            removed.append(name)
    rebound = replace_live_root(workspace)
    reference_path = None
    if reference:
        target = workspace / ".benchmark-input" / "reference.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(reference, target)
        reference_path = target.relative_to(workspace).as_posix()
    return {"removed_entry_points": removed, "rebound_files": rebound, "reference_path": reference_path}


def normalize_current_config(workspace: Path, profile: dict[str, Any]) -> dict[str, Any]:
    settings_path = workspace / ".claude" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    settings["agent"] = profile["entry_agent"]
    settings["effortLevel"] = "high"
    if profile.get("disable_operational_hooks"):
        settings.pop("hooks", None)
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"entry_agent": profile["entry_agent"], "hooks_disabled": bool(profile.get("disable_operational_hooks"))}


def _frontmatter_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def validate_generated(value: Any, max_agents: int) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("generated configuration is not an object")
    required = {"strategy", "coordinator_prompt", "agents"}
    if set(value) != required:
        raise ValueError(f"generated configuration keys differ: {sorted(value)}")
    if not isinstance(value["strategy"], str) or len(value["strategy"]) > 1200:
        raise ValueError("invalid generated strategy")
    if not isinstance(value["coordinator_prompt"], str) or len(value["coordinator_prompt"]) > 5000:
        raise ValueError("invalid generated coordinator prompt")
    agents = value["agents"]
    if not isinstance(agents, list) or len(agents) > max_agents:
        raise ValueError("invalid generated agent count")
    names: set[str] = set()
    for agent in agents:
        if not isinstance(agent, dict) or set(agent) != {"name", "description", "prompt", "model", "effort"}:
            raise ValueError("invalid generated agent fields")
        name = agent["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,31}", name):
            raise ValueError(f"invalid generated agent name: {name!r}")
        if name in names or name == "benchmark-generated-coordinator":
            raise ValueError(f"duplicate/reserved generated agent name: {name}")
        names.add(name)
        if agent["model"] not in {"sonnet", "opus"} or agent["effort"] not in {"low", "medium", "high"}:
            raise ValueError(f"invalid route for generated agent: {name}")
        if not isinstance(agent["description"], str) or len(agent["description"]) > 300:
            raise ValueError(f"invalid description for generated agent: {name}")
        if not isinstance(agent["prompt"], str) or len(agent["prompt"]) > 4000:
            raise ValueError(f"invalid prompt for generated agent: {name}")
    return value


def install_generated_config(workspace: Path, value: dict[str, Any]) -> dict[str, Any]:
    claude_dir = workspace / ".claude"
    agents_dir = claude_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    names = [agent["name"] for agent in value["agents"]]
    agent_tool = f"Agent({', '.join(names)}), " if names else ""
    coordinator = f"""---
name: benchmark-generated-coordinator
description: Task-specific coordinator generated immediately before this benchmark run.
model: opus
effort: high
tools: {agent_tool}Bash, Read, Edit, Write, Grep, Glob
permissionMode: bypassPermissions
maxTurns: 32
---

{SAFETY}

Generated strategy:
{value['coordinator_prompt']}

Decide whether delegation helps. You remain accountable for the final implementation,
scope, and targeted verification. Do not create or edit configuration during execution.
"""
    (agents_dir / "benchmark-generated-coordinator.md").write_text(coordinator, encoding="utf-8")
    for agent in value["agents"]:
        body = f"""---
name: {agent['name']}
description: {_frontmatter_string(agent['description'])}
model: {agent['model']}
effort: {agent['effort']}
tools: Bash, Read, Edit, Write, Grep, Glob
permissionMode: bypassPermissions
maxTurns: 16
---

{SAFETY}

{agent['prompt']}

Return concise evidence to the coordinator. Do not delegate further.
"""
        (agents_dir / f"{agent['name']}.md").write_text(body, encoding="utf-8")
    settings = {
        "agent": "benchmark-generated-coordinator",
        "effortLevel": "high",
        "includeGitInstructions": False,
        "autoMemoryEnabled": False,
        "env": {"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1", "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1"},
        "permissions": {"defaultMode": "bypassPermissions"},
    }
    (claude_dir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    (workspace / "CLAUDE.md").write_text(
        "# Generated benchmark configuration\n\n" + SAFETY + "\n\nStrategy summary: " + value["strategy"] + "\n",
        encoding="utf-8",
    )
    return {"agent_names": names, "strategy": value["strategy"]}


def usage_from_result(event: dict[str, Any]) -> dict[str, int]:
    usage = event.get("usage") or {}
    def number(*names: str) -> int:
        for name in names:
            value = usage.get(name)
            if isinstance(value, int) and not isinstance(value, bool):
                return value
        return 0
    uncached = number("input_tokens", "inputTokens")
    cache_create = number("cache_creation_input_tokens", "cacheCreationInputTokens")
    cache_read = number("cache_read_input_tokens", "cacheReadInputTokens")
    output = number("output_tokens", "outputTokens")
    model_usage = event.get("modelUsage") or {}
    if isinstance(model_usage, dict) and model_usage:
        uncached = cache_create = cache_read = output = 0
        for model in model_usage.values():
            if not isinstance(model, dict):
                continue
            uncached += int(model.get("inputTokens") or model.get("input_tokens") or 0)
            cache_create += int(model.get("cacheCreationInputTokens") or model.get("cache_creation_input_tokens") or 0)
            cache_read += int(model.get("cacheReadInputTokens") or model.get("cache_read_input_tokens") or 0)
            output += int(model.get("outputTokens") or model.get("output_tokens") or 0)
    total_input = uncached + cache_create + cache_read
    return {
        "input_tokens": total_input,
        "cached_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_create,
        "output_tokens": output,
        "reasoning_output_tokens": 0,
        "effective_tokens": total_input - cache_read + output,
    }


def parse_stream(path: Path) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    invalid = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            invalid += 1
            continue
        if isinstance(value, dict):
            events.append(value)
    result = next((event for event in reversed(events) if event.get("type") == "result"), {})
    tools: dict[str, int] = {}
    tool_ids: dict[str, str] = {}
    failed_ids: set[str] = set()
    output_chars = 0
    context_paths: set[str] = set()
    for event in events:
        message = event.get("message") or {}
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                name = str(block.get("name") or "unknown")
                tools[name] = tools.get(name, 0) + 1
                if block.get("id"):
                    tool_ids[str(block["id"])] = name
                tool_input = block.get("input") or {}
                for key in ("file_path", "path"):
                    value = tool_input.get(key) if isinstance(tool_input, dict) else None
                    if isinstance(value, str):
                        context_paths.add(value)
            elif block.get("type") == "tool_result":
                content_value = block.get("content")
                output_chars += len(content_value if isinstance(content_value, str) else json.dumps(content_value, ensure_ascii=False))
                if block.get("is_error") and block.get("tool_use_id"):
                    failed_ids.add(str(block["tool_use_id"]))
    bash_ids = {tool_id for tool_id, name in tool_ids.items() if name in {"Bash", "bash"}}
    agent_calls = sum(count for name, count in tools.items() if name.lower() in {"agent", "task"})
    mcp_calls = sum(count for name, count in tools.items() if "codex" in name.lower() and "mcp" in name.lower())
    return {
        "result_event": result,
        "usage": usage_from_result(result),
        "final_message": result.get("result") if isinstance(result.get("result"), str) else None,
        "model_usage": result.get("modelUsage") or {},
        "total_cost_usd": result.get("total_cost_usd") if isinstance(result.get("total_cost_usd"), (int, float)) else None,
        "num_turns": result.get("num_turns") if isinstance(result.get("num_turns"), int) else None,
        "tool_metrics": {
            "completed_commands": len(bash_ids),
            "failed_commands": len(bash_ids & failed_ids),
            "tool_output_chars": output_chars,
            "agent_calls": agent_calls,
            "codex_mcp_calls": mcp_calls,
            "tool_calls_by_name": tools,
            "observed_context_paths": sorted(context_paths),
        },
        "invalid_jsonl_lines": invalid,
        "is_error": bool(result.get("is_error")) or result.get("subtype") not in (None, "success"),
    }


def parse_single_json(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    structured = value.get("structured_output")
    if structured is None and isinstance(value.get("result"), str):
        structured = json.loads(value["result"])
    return validate_generated(structured, 3), {
        "usage": usage_from_result(value),
        "total_cost_usd": value.get("total_cost_usd") if isinstance(value.get("total_cost_usd"), (int, float)) else None,
        "duration_ms": value.get("duration_ms") if isinstance(value.get("duration_ms"), int) else None,
        "model_usage": value.get("modelUsage") or {},
        "is_error": bool(value.get("is_error")),
    }


def generator_prompt(task: dict[str, Any]) -> str:
    return f"""Design a compact task-specific Claude Code project configuration for an isolated web-maintenance benchmark.
Do not solve the implementation task. Decide whether zero to three native worker agents would help, and define only useful roles.
The fresh executor may use Bash/Read/Edit/Write/Grep/Glob and may delegate once to your workers; workers cannot nest.

Task: {task['title']}
Request: {task['prompt']}
Authorized paths: {', '.join(task['authorized_paths'])}
Relevant context paths: {', '.join(task.get('context', []))}

Optimize capability first, then total tokens/tool output. Keep prompts specific and short. Include CRLF/EN-JP precautions only when relevant.
Never authorize network, credentials, publishing, deployment, pushing, test/config/ledger edits, or access outside the fixture.
Return only the requested structured configuration."""


def run_generator(task: dict[str, Any], workspace: Path, artifact: Path, *, model: str,
                  effort: str, budget: float, timeout: int) -> tuple[dict[str, Any], dict[str, Any]]:
    prompt = generator_prompt(task)
    prompt_path = artifact / "generator-prompt.txt"
    stdout_path = artifact / "generator-output.json"
    stderr_path = artifact / "generator-stderr.log"
    prompt_path.write_text(prompt, encoding="utf-8")
    command = [
        "claude", "--safe-mode", "--print", "--output-format", "json",
        "--json-schema", json.dumps(DYNAMIC_SCHEMA, separators=(",", ":")),
        "--tools", "", "--no-session-persistence", "--model", model,
        "--effort", effort, "--permission-mode", "bypassPermissions",
        "--max-budget-usd", str(budget), prompt,
    ]
    started = time.monotonic()
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.run(command, cwd=workspace, stdout=stdout, stderr=stderr,
                                 text=True, timeout=timeout, check=False)
    duration_ms = round((time.monotonic() - started) * 1000)
    if process.returncode != 0:
        raise RuntimeError(f"dynamic config generator exited {process.returncode}; see {stderr_path}")
    generated, telemetry = parse_single_json(stdout_path)
    telemetry["duration_ms"] = telemetry.get("duration_ms") or duration_ms
    telemetry["prompt_bytes"] = len(prompt.encode())
    telemetry["exit_code"] = process.returncode
    return generated, telemetry


def task_prompt(task: dict[str, Any], task_id: str, reference_path: str | None) -> str:
    reference = f" Pristine visual reference: {reference_path}." if reference_path else ""
    return f"""You are the implementation agent in a fresh isolated copy of the YOKOTA Lab static website.

Task {task_id}: {task['title']}
Owner request: {task['prompt']}

Authorized implementation paths: {', '.join(task['authorized_paths'])}.
Relevant context paths: {', '.join(task.get('context', []))}.{reference}

{SAFETY}

Use whatever native agents or project tools this session actually provides, but decide for yourself whether delegation helps.
Implement the smallest complete fix. Preserve CRLF and EN/JP parity when applicable. Run at most one focused static or syntax check;
the independent runner performs the complete hidden and browser grading. Do not merely propose a patch; edit the authorized files.
Return a concise summary of edits and the targeted check."""


def run_executor(task: dict[str, Any], task_id: str, variant: str, profile: dict[str, Any],
                 workspace: Path, artifact: Path, *, model: str, effort: str,
                 budget: float, timeout: int, reference_path: str | None) -> dict[str, Any]:
    prompt = task_prompt(task, task_id, reference_path)
    prompt_path = artifact / "prompt.txt"
    stdout_path = artifact / "stdout.jsonl"
    stderr_path = artifact / "stderr.log"
    prompt_path.write_text(prompt, encoding="utf-8")
    command = [
        "claude", "--print", "--output-format", "stream-json", "--verbose",
        "--no-session-persistence", "--model", model, "--effort", effort,
        "--permission-mode", "bypassPermissions", "--max-budget-usd", str(budget),
    ]
    if profile["mode"] == "safe":
        command.append("--safe-mode")
    else:
        command.extend(["--setting-sources", "project", "--agent", profile["entry_agent"]])
        if variant == "current-harness":
            command.extend(["--mcp-config", str(workspace / ".mcp.json"), "--strict-mcp-config"])
        else:
            command.extend(["--mcp-config", '{"mcpServers":{}}', "--strict-mcp-config"])
    command.append(prompt)
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".playwright" / "browsers")
    env["NODE_PATH"] = str(ROOT / "node_modules")
    env["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"] = "1"
    env["CLAUDE_CODE_DISABLE_1M_CONTEXT"] = "1"
    started = time.monotonic()
    timed_out = False
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(command, cwd=workspace, env=env, stdout=stdout, stderr=stderr,
                                   text=True, start_new_session=True)
        try:
            exit_code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                exit_code = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                exit_code = process.wait()
    duration_ms = round((time.monotonic() - started) * 1000)
    parsed = parse_stream(stdout_path)
    if parsed["final_message"]:
        (artifact / "final-message.md").write_text(parsed["final_message"] + "\n", encoding="utf-8")
    return {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
        "usage": parsed["usage"],
        "model_usage": parsed["model_usage"],
        "total_cost_usd": parsed["total_cost_usd"],
        "num_turns": parsed["num_turns"],
        "tool_metrics": parsed["tool_metrics"],
        "invalid_jsonl_lines": parsed["invalid_jsonl_lines"],
        "result_is_error": parsed["is_error"],
        "prompt_bytes": len(prompt.encode()),
        "prompt_sha256": sha256_bytes(prompt.encode()),
        "stdout_path": str(stdout_path.relative_to(ROOT)),
        "stderr_path": str(stderr_path.relative_to(ROOT)),
    }


def combine_usage(*items: dict[str, int] | None) -> dict[str, int]:
    keys = ("input_tokens", "cached_input_tokens", "cache_creation_input_tokens",
            "output_tokens", "reasoning_output_tokens", "effective_tokens")
    return {key: sum((item or {}).get(key, 0) for item in items) for key in keys}


def append_result(result: dict[str, Any]) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    needs_newline = RESULTS_PATH.exists() and RESULTS_PATH.stat().st_size and not RESULTS_PATH.read_bytes().endswith(b"\n")
    with RESULTS_PATH.open("a", encoding="utf-8") as handle:
        if needs_newline:
            handle.write("\n")
        handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def compact_result(result: dict[str, Any]) -> dict[str, Any]:
    execution = result.get("execution") or {}
    tools = execution.get("tool_metrics") or {}
    grade = result.get("grade") or {}
    payload = {
        "run_id": result.get("run_id"), "run_label": result.get("run_label"),
        "variant": result.get("config_variant"), "task_id": result.get("task_id"),
        "task_version": result.get("task_version"), "capability_pass": result.get("capability_pass"),
        "score": grade.get("score"),
        "gates": {key: grade.get(key) for key in ("critical_pass", "f2p", "p2p", "scope", "completion")},
        "model": result.get("model"), "effort": result.get("effort"),
        "usage": result.get("aggregate_usage"), "total_cost_usd": result.get("total_cost_usd"),
        "delegation": {"agent_calls": tools.get("agent_calls"), "codex_mcp_calls": tools.get("codex_mcp_calls")},
        "commands": {"completed": tools.get("completed_commands"), "failed": tools.get("failed_commands"),
                     "output_chars": tools.get("tool_output_chars")},
        "durations_ms": {"setup": result.get("setup_duration_ms"), "generation": result.get("generation_duration_ms"),
                         "execution": execution.get("duration_ms"), "grader": result.get("grader_duration_ms"),
                         "total": result.get("total_duration_ms")},
        "telemetry_complete": result.get("total_token_telemetry_complete"),
        "changed_files": result.get("changed_files"), "failure_phase": result.get("failure_phase"),
        "artifact": result.get("artifact"),
    }
    if not result.get("capability_pass"):
        findings = grade.get("findings") or []
        payload["diagnostic_findings"] = [item for item in findings if not str(item).startswith("changed:")]
    return payload


def run_one(args: argparse.Namespace) -> dict[str, Any]:
    tasks = CORE.load_tasks()
    task = tasks[args.task_id]
    if task.get("held_out") and not args.include_held_out:
        raise SystemExit(f"{args.task_id} is held out; pass --include-held-out only after all three visible arms are frozen")
    profile = read_profile(args.variant)
    if args.ref != profile["fixture_ref"]:
        raise SystemExit(f"profile pins --ref {profile['fixture_ref']}; got {args.ref}")
    run_id = args.run_id or f"{datetime.now():%Y%m%d-%H%M%S}-claude-{args.variant}-{args.task_id.lower()}-{uuid.uuid4().hex[:6]}"
    artifact = ARTIFACTS_ROOT / run_id
    artifact.mkdir(parents=True, exist_ok=False)
    workspace = Path(tempfile.mkdtemp(prefix=f"yokota-{run_id}-", dir=args.workspace_root))
    total_started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": 1, "provider": "claude", "run_id": run_id,
        "run_label": args.run_label, "config_variant": args.variant,
        "task_id": args.task_id, "task_version": task["version"],
        "task_definition_sha256": CORE.task_definition_sha256(task),
        "grader_sha256": CORE.sha256_file(BENCHMARK_DIR / "task_ops.py"),
        "runner_sha256": CORE.sha256_file(Path(__file__)),
        "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repo_ref": args.ref, "repo_commit": args.ref, "model": args.model,
        "effort": args.effort, "worker": f"claude-{args.variant}",
        "run_p2p": bool(args.run_p2p), "prompt_mode": "claude-neutral-v1",
        "handoff_mode": "runner-captured", "inspection_mode": "agent-judgment",
        "claude_cli": subprocess.run(["claude", "--version"], text=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, check=True).stdout.strip(),
        "artifact": f"tools/out/claude-benchmark/{run_id}/result.json",
    }
    generation: dict[str, Any] | None = None
    try:
        setup_started = time.monotonic()
        reference_output = artifact / "reference.png" if args.task_id == "WBD-004" else None
        fixture = CORE.make_fixture(args.task_id, args.ref, workspace, reference_output)
        reference = Path(fixture["reference"]) if fixture.get("reference") else None
        result["fixture"] = fixture["mutation"]
        result["fixture_safety"] = common_fixture_safety(workspace, reference)
        if args.variant == "current-harness":
            if profile.get("config_ref") != args.ref:
                raise RuntimeError("current harness config_ref differs from fixture ref")
            result["config_setup"] = normalize_current_config(workspace, profile)
        else:
            result["config_setup"] = {"removed": remove_project_config(workspace)}
        if args.variant == "dynamic":
            generator_budget = min(1.0, max(0.25, args.max_budget_usd * 0.2))
            generated, generation = run_generator(
                task, workspace, artifact, model=args.model, effort=args.effort,
                budget=generator_budget, timeout=min(args.timeout, 300),
            )
            generated = validate_generated(generated, int(profile["max_generated_agents"]))
            result["config_setup"].update(install_generated_config(workspace, generated))
            result["generated_config"] = generated
        CORE.commit_mutated_fixture(workspace, f"benchmark environment {args.variant}")
        config_hash, instruction_bytes, config_files = config_snapshot(workspace)
        result["config_sha256"] = config_hash
        result["instruction_bytes"] = instruction_bytes
        result["config_files"] = config_files
        result["setup_duration_ms"] = round((time.monotonic() - setup_started) * 1000)
        generation_cost = (generation or {}).get("total_cost_usd")
        reserved = generation_cost if isinstance(generation_cost, (int, float)) else (1.0 if generation else 0.0)
        execution_budget = args.max_budget_usd - reserved
        if execution_budget <= 0:
            raise RuntimeError("dynamic configuration generation exhausted the run budget")
        execution = run_executor(
            task, args.task_id, args.variant, profile, workspace, artifact,
            model=args.model, effort=args.effort, budget=execution_budget,
            timeout=args.timeout, reference_path=result["fixture_safety"]["reference_path"],
        )
        result["execution"] = execution
        result["generation"] = generation
        result["generation_duration_ms"] = (generation or {}).get("duration_ms")
        diff = CORE.run_checked(["git", "diff", "--binary", "HEAD"], cwd=workspace).stdout
        (artifact / "candidate.patch").write_text(diff, encoding="utf-8")
        result["changed_files"] = CORE.changed_files(workspace)
        grader_started = time.monotonic()
        grade = CORE.load_task_ops().grade(args.task_id, workspace, "HEAD", run_p2p=args.run_p2p)
        if args.task_id == "WBD-004" and reference:
            candidate = artifact / "candidate.png"
            try:
                CORE.make_visual_reference(workspace, candidate)
                grade["visual"] = {
                    "reference_sha256": CORE.sha256_file(reference),
                    "candidate_sha256": CORE.sha256_file(candidate),
                }
                grade["visual"]["exact_match"] = grade["visual"]["reference_sha256"] == grade["visual"]["candidate_sha256"]
                if not grade["visual"]["exact_match"]:
                    grade["critical_pass"] = False
                    grade.setdefault("findings", []).append("visual-reference-mismatch")
            except Exception as error:
                grade["critical_pass"] = False
                grade["visual"] = {"exact_match": False, "error": str(error)}
                grade.setdefault("findings", []).append("visual-reference-capture-failed")
        result["grader_duration_ms"] = round((time.monotonic() - grader_started) * 1000)
        if execution["exit_code"] != 0 or execution["timed_out"] or execution["result_is_error"]:
            grade["completion"] = 0
            grade.setdefault("components", {})["completion"] = 0
            grade["score"] = sum(int(value) for value in grade["components"].values())
            grade.setdefault("findings", []).append("Claude turn failed, errored, or timed out")
        result["grade"] = grade
        aggregate = combine_usage((generation or {}).get("usage"), execution.get("usage"))
        result["aggregate_usage"] = aggregate
        result["effective_tokens"] = aggregate["effective_tokens"]
        costs = [value for value in ((generation or {}).get("total_cost_usd"), execution.get("total_cost_usd"))
                 if isinstance(value, (int, float))]
        result["total_cost_usd"] = round(sum(costs), 8) if costs else None
        codex_calls = execution["tool_metrics"].get("codex_mcp_calls", 0)
        # Claude Code aggregates native Agent model usage, but does not promise
        # token accounting for arbitrary MCP servers. The frozen current arm
        # grants Codex MCP inside nested site agents, whose internal calls may
        # not appear as top-level stream events. Treat it conservatively.
        result["total_token_telemetry_complete"] = (
            args.variant != "current-harness" and not bool(codex_calls)
        )
        result["capability_pass"] = bool(
            grade.get("critical_pass") and grade.get("score", 0) >= 85
            and (not args.run_p2p or grade.get("p2p") == 25)
            and execution["exit_code"] == 0 and not execution["timed_out"] and not execution["result_is_error"]
        )
        if execution["exit_code"] != 0 or execution["timed_out"] or execution["result_is_error"]:
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
        result["total_duration_ms"] = round((time.monotonic() - total_started) * 1000)
        (artifact / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        append_result(result)
        return result
    except Exception as error:
        if not (artifact / "prompt.txt").exists():
            (artifact / "prompt.txt").write_text("execution did not start\n", encoding="utf-8")
        for name in ("stdout.jsonl", "stderr.log", "candidate.patch"):
            path = artifact / name
            if not path.exists():
                path.write_text((str(error) + "\n") if name == "stderr.log" else "", encoding="utf-8")
        result.update({
            "execution": {"exit_code": 1, "timed_out": False, "duration_ms": 0,
                          "usage": combine_usage(), "tool_metrics": {}},
            "generation": generation, "changed_files": [], "grade": {},
            "aggregate_usage": combine_usage((generation or {}).get("usage")),
            "effective_tokens": (generation or {}).get("usage", {}).get("effective_tokens", 0),
            "total_cost_usd": (generation or {}).get("total_cost_usd"),
            "total_token_telemetry_complete": False, "capability_pass": False,
            "failure_phase": "setup", "error": str(error),
            "total_duration_ms": round((time.monotonic() - total_started) * 1000),
        })
        (artifact / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        append_result(result)
        return result
    finally:
        if args.keep_workspace:
            result["workspace"] = str(workspace)
        else:
            shutil.rmtree(workspace, ignore_errors=True)


def load_rows(label: str | None = None) -> list[dict[str, Any]]:
    if not RESULTS_PATH.exists():
        return []
    rows = [json.loads(line) for line in RESULTS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [row for row in rows if label is None or row.get("run_label") == label]


def summarize(label: str | None) -> dict[str, Any]:
    rows = load_rows(label)
    def total(path: tuple[str, ...]) -> int | float:
        values = []
        for row in rows:
            value: Any = row
            for key in path:
                value = value.get(key) if isinstance(value, dict) else None
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                values.append(value)
        return sum(values)
    return {
        "status": "pass", "run_label": label, "runs": len(rows),
        "passed": sum(bool(row.get("capability_pass")) for row in rows),
        "mean_score": round(total(("grade", "score")) / len(rows), 2) if rows else None,
        "effective_tokens": total(("aggregate_usage", "effective_tokens")),
        "total_cost_usd": round(float(total(("total_cost_usd",))), 8),
        "duration_ms": total(("total_duration_ms",)),
        "agent_calls": total(("execution", "tool_metrics", "agent_calls")),
        "codex_mcp_calls": total(("execution", "tool_metrics", "codex_mcp_calls")),
        "complete_token_telemetry": all(row.get("total_token_telemetry_complete") for row in rows) if rows else False,
        "tasks": [{"task_id": row.get("task_id"), "variant": row.get("config_variant"),
                   "score": (row.get("grade") or {}).get("score"), "pass": row.get("capability_pass"),
                   "effective_tokens": row.get("effective_tokens"), "run_id": row.get("run_id")} for row in rows],
    }


def compare(baseline_label: str, candidate_label: str) -> dict[str, Any]:
    baseline = load_rows(baseline_label)
    candidate = load_rows(candidate_label)
    errors: list[str] = []
    for name, rows in (("baseline", baseline), ("candidate", candidate)):
        if not rows:
            errors.append(f"no rows for {name} label")
    def by_task(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            result.setdefault(str(row.get("task_id")), []).append(row)
        return result
    bg, cg = by_task(baseline), by_task(candidate)
    if set(bg) != set(cg):
        errors.append(f"task sets differ: {sorted(bg)} vs {sorted(cg)}")
    for task in set(bg) & set(cg):
        if len(bg[task]) != len(cg[task]):
            errors.append(f"repeat counts differ for {task}")
        for key in ("task_version", "task_definition_sha256", "grader_sha256", "repo_commit", "model", "effort", "run_p2p"):
            if {row.get(key) for row in bg[task]} != {row.get(key) for row in cg[task]}:
                errors.append(f"{task}: {key} differs")
    bs, cs = summarize(baseline_label), summarize(candidate_label)
    capability = bool(candidate) and cs["passed"] == cs["runs"] and all(
        min((row.get("grade") or {}).get("score", 0) for row in cg[task]) >=
        min((row.get("grade") or {}).get("score", 0) for row in bg[task]) for task in set(bg) & set(cg)
    )
    telemetry_complete = bs["complete_token_telemetry"] and cs["complete_token_telemetry"]
    token_change = None
    if telemetry_complete and bs["effective_tokens"]:
        token_change = round((cs["effective_tokens"] / bs["effective_tokens"] - 1) * 100, 1)
    if errors:
        recommendation = "invalid-comparison"
    elif not capability:
        recommendation = "reject-capability-regression"
    elif not telemetry_complete:
        recommendation = "capability-comparable-cost-inconclusive-external-worker-usage"
    elif token_change is not None and token_change <= -5:
        recommendation = "candidate-efficient-screening-pass"
    else:
        recommendation = "no-decision-grade-token-gain"
    return {
        "status": "pass" if not errors else "fail", "safe_to_compare": not errors,
        "baseline": bs, "candidate": cs, "capability_gate": capability,
        "effective_token_change_percent": token_change,
        "total_token_telemetry_complete": telemetry_complete,
        "recommendation": recommendation, "errors": errors,
    }


def audit_artifacts() -> dict[str, Any]:
    rows = load_rows()
    directories = {p.name: p for p in ARTIFACTS_ROOT.iterdir() if p.is_dir()} if ARTIFACTS_ROOT.exists() else {}
    ids = {str(row.get("run_id")) for row in rows}
    required = ("prompt.txt", "stdout.jsonl", "stderr.log", "candidate.patch", "result.json")
    errors = []
    if ids - directories.keys():
        errors.append(f"missing directories: {sorted(ids - directories.keys())}")
    if directories.keys() - ids:
        errors.append(f"orphan directories: {sorted(directories.keys() - ids)}")
    incomplete = {rid: [name for name in required if not (directories[rid] / name).exists()]
                  for rid in ids & directories.keys()}
    incomplete = {rid: names for rid, names in incomplete.items() if names}
    if incomplete:
        errors.append(f"incomplete: {incomplete}")
    return {"status": "pass" if not errors else "fail", "runs": len(rows),
            "artifact_directories": len(directories), "errors": errors}


def selftest() -> dict[str, Any]:
    for variant in VARIANTS:
        read_profile(variant)
    synthetic = [
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "a", "name": "Agent", "input": {}},
            {"type": "tool_use", "id": "b", "name": "Bash", "input": {"command": "true"}},
        ]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "b", "is_error": False, "content": "ok"},
        ]}},
        {"type": "result", "subtype": "success", "result": "done", "total_cost_usd": 0.1,
         "usage": {"input_tokens": 10, "cache_creation_input_tokens": 20,
                   "cache_read_input_tokens": 30, "output_tokens": 4}},
    ]
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "stream.jsonl"
        path.write_text("\n".join(json.dumps(item) for item in synthetic) + "\n", encoding="utf-8")
        parsed = parse_stream(path)
        assert parsed["usage"]["input_tokens"] == 60 and parsed["usage"]["effective_tokens"] == 34
        assert parsed["tool_metrics"]["agent_calls"] == 1 and parsed["tool_metrics"]["completed_commands"] == 1
        generated = validate_generated({"strategy": "small", "coordinator_prompt": "do task", "agents": []}, 3)
        assert generated["strategy"] == "small"
    return {"status": "pass", "profiles": list(VARIANTS), "stream_parser": "pass",
            "dynamic_schema": "pass", "frozen_ref": FROZEN_REF}


def materialization_selftest() -> dict[str, Any]:
    reports: dict[str, Any] = {}
    synthetic = {
        "strategy": "Use the coordinator directly for this bounded task.",
        "coordinator_prompt": "Inspect the named context, make the authorized edit, and verify it.",
        "agents": [],
    }
    for variant in VARIANTS:
        profile = read_profile(variant)
        with tempfile.TemporaryDirectory(prefix=f"claude-profile-{variant}-") as temporary:
            workspace = Path(temporary)
            CORE.archive_repository(FROZEN_REF, workspace, include_dependencies=False)
            CORE.initialize_fixture_git(workspace)
            CORE.load_task_ops().mutate("WBD-001", workspace)
            CORE.commit_mutated_fixture(workspace, "fixture WBD-001")
            safety = common_fixture_safety(workspace, None)
            if variant == "current-harness":
                setup = normalize_current_config(workspace, profile)
                assert (workspace / ".claude/agents/site-coordinator.md").is_file()
                assert not json.loads((workspace / ".claude/settings.json").read_text()).get("hooks")
                for root_name in ("CLAUDE.md", "AGENTS.md", ".claude", "skills"):
                    root = workspace / root_name
                    paths = [root] if root.is_file() else root.rglob("*") if root.is_dir() else []
                    for path in paths:
                        if path.is_file():
                            assert LIVE_ROOT.encode() not in path.read_bytes()
            else:
                setup = {"removed": remove_project_config(workspace)}
                if variant == "dynamic":
                    setup.update(install_generated_config(workspace, validate_generated(synthetic, 3)))
                else:
                    assert not any((workspace / name).exists() for name in CONFIG_PATHS)
            assert not (workspace / "publish.sh").exists() and not (workspace / "deploy.sh").exists()
            config_hash, instruction_bytes, config_files = config_snapshot(workspace)
            reports[variant] = {
                "config_sha256": config_hash, "instruction_bytes": instruction_bytes,
                "config_files": len(config_files), "safety": safety, "setup": setup,
            }
    return {"status": "pass", "variants": reports}


def preflight() -> dict[str, Any]:
    checks: dict[str, Any] = {
        "selftest": selftest(),
        "materialization": materialization_selftest(),
        "capsules": CORE.audit(FROZEN_REF),
    }
    version = subprocess.run(["claude", "--version"], text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=False)
    checks["claude_cli"] = {"returncode": version.returncode, "version": version.stdout.strip()}
    current_paths = ["CLAUDE.md", ".claude/settings.json", ".claude/agents/site-coordinator.md", ".mcp.json"]
    missing = [path for path in current_paths if subprocess.run(
        ["git", "cat-file", "-e", f"{FROZEN_REF}:{path}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode]
    checks["current_harness_snapshot"] = {"ref": FROZEN_REF, "missing": missing}
    errors = []
    if checks["capsules"].get("status") != "pass": errors.append("capsule audit failed")
    if checks["materialization"].get("status") != "pass": errors.append("profile materialization failed")
    if version.returncode: errors.append("Claude CLI unavailable")
    if missing: errors.append("current harness snapshot incomplete")
    return {"status": "pass" if not errors else "fail", "checks": checks, "errors": errors,
            "initial_matrix_max_usd": 54, "model": "opus", "effort": "high"}


def plan() -> dict[str, Any]:
    orders = {
        "WBD-001": ("current-harness", "autonomous", "dynamic"),
        "WBD-002": ("autonomous", "dynamic", "current-harness"),
        "WBD-003": ("dynamic", "current-harness", "autonomous"),
        "WBD-004": ("current-harness", "dynamic", "autonomous"),
        "WBD-005": ("autonomous", "current-harness", "dynamic"),
    }
    commands = []
    for task, variants in orders.items():
        for variant in variants:
            label = f"claude-{variant}-screen-v1"
            budget = 6 if task == "WBD-005" else 3
            include = " --include-held-out" if task == "WBD-005" else ""
            commands.append({
                "task_id": task, "variant": variant, "max_usd": budget,
                "command": (f"python3 tools/agent-benchmark/claude_benchmark.py run {task} "
                            f"--variant {variant} --run-label {label} --ref {FROZEN_REF} "
                            f"--model opus --effort high --max-budget-usd {budget} --run-p2p{include}"),
            })
    return {"status": "pass", "maximum_usd": sum(item["max_usd"] for item in commands),
            "runs": len(commands), "commands": commands,
            "rule": "Run visible commands first. Freeze all arms, then run WBD-005 commands without tuning between them."}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    sub = command.add_subparsers(dest="command", required=True)
    sub.add_parser("selftest")
    sub.add_parser("preflight")
    sub.add_parser("plan")
    run = sub.add_parser("run")
    run.add_argument("task_id", choices=tuple(CORE.load_tasks()))
    run.add_argument("--variant", choices=VARIANTS, required=True)
    run.add_argument("--run-label", required=True)
    run.add_argument("--ref", default=FROZEN_REF)
    run.add_argument("--model", default="opus")
    run.add_argument("--effort", choices=("low", "medium", "high"), default="high")
    run.add_argument("--max-budget-usd", type=float, required=True)
    run.add_argument("--timeout", type=int, default=1200)
    run.add_argument("--run-id")
    run.add_argument("--workspace-root", default=tempfile.gettempdir())
    run.add_argument("--run-p2p", action="store_true")
    run.add_argument("--include-held-out", action="store_true")
    run.add_argument("--keep-workspace", action="store_true")
    run.add_argument("--verbose-result", action="store_true")
    summary = sub.add_parser("summarize"); summary.add_argument("--run-label")
    comparison = sub.add_parser("compare")
    comparison.add_argument("--baseline-label", required=True)
    comparison.add_argument("--candidate-label", required=True)
    sub.add_parser("artifacts")
    return command


def main() -> int:
    args = parser().parse_args()
    if args.command == "selftest": result = selftest()
    elif args.command == "preflight": result = preflight()
    elif args.command == "plan": result = plan()
    elif args.command == "run":
        result = run_one(args)
        result = result if args.verbose_result else compact_result(result)
    elif args.command == "summarize": result = summarize(args.run_label)
    elif args.command == "compare": result = compare(args.baseline_label, args.candidate_label)
    else: result = audit_artifacts()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status", "pass") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

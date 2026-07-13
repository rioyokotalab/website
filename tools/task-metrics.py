#!/usr/bin/env python3
"""Validate, import, and summarize append-only task metrics (schema v2)."""

from __future__ import annotations

import argparse
import json
import statistics
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "tools/task-metrics.jsonl"
RESULTS = ROOT / "tools/agent-benchmark/results.jsonl"
EXCLUSIONS = ROOT / "tools/agent-benchmark/exclusions.json"
CLAUDE_RESULTS = ROOT / "tools/agent-benchmark/claude-results.jsonl"

V1_REQUIRED = {"date", "task_type", "agent", "tier", "duration_ms", "success", "note"}
V2_REQUIRED = V1_REQUIRED | {
    "schema_version", "run_id", "run_label", "task_id", "model", "effort", "outcome",
    "capability_score", "critical_pass", "capability_pass", "f2p", "p2p", "scope", "completion",
    "input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "effective_tokens",
    "prompt_bytes", "instruction_bytes", "completed_commands", "failed_commands", "tool_output_chars",
    "setup_duration_ms", "worker_duration_ms", "grader_duration_ms", "review_duration_ms", "total_duration_ms",
    "changed_files", "retries", "escalation", "failure_phase", "failure_category", "artifact",
}
V2_ALLOWED = V2_REQUIRED | {
    "handoff_mode", "inspection_mode", "prompt_mode", "task_version",
    "repo_ref", "repo_commit", "codex_cli", "run_p2p",
    "task_definition_sha256", "grader_sha256", "runner_sha256",
    "provider", "provider_cli", "config_variant", "config_sha256",
    "cache_creation_input_tokens", "generation_effective_tokens",
    "agent_calls", "codex_mcp_calls", "generation_duration_ms",
    "total_cost_usd", "total_token_telemetry_complete",
}
NULLABLE_NUMBERS = {
    "capability_score", "f2p", "p2p", "scope", "completion", "input_tokens", "cached_input_tokens",
    "output_tokens", "reasoning_output_tokens", "effective_tokens", "prompt_bytes", "instruction_bytes",
    "setup_duration_ms", "worker_duration_ms", "grader_duration_ms", "review_duration_ms",
    "cache_creation_input_tokens", "generation_effective_tokens", "generation_duration_ms",
}
NONNEGATIVE_INTS = {
    "duration_ms", "completed_commands", "failed_commands", "tool_output_chars", "total_duration_ms", "retries",
    "input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "effective_tokens",
    "prompt_bytes", "instruction_bytes", "setup_duration_ms", "worker_duration_ms", "grader_duration_ms",
    "review_duration_ms", "cache_creation_input_tokens", "generation_effective_tokens",
    "generation_duration_ms",
}


def read_jsonl(path: Path) -> tuple[list[tuple[int, dict[str, Any]]], int, list[str]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    blanks = 0
    errors: list[str] = []
    if not path.exists():
        return rows, blanks, [f"missing file: {path}"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            blanks += 1
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"line {line_number}: invalid JSON: {error.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {line_number}: row is not an object")
            continue
        rows.append((line_number, value))
    return rows, blanks, errors


def validate_row(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    version = row.get("schema_version", 1)
    required = V2_REQUIRED if version == 2 else V1_REQUIRED
    missing = sorted(required - row.keys())
    if missing:
        errors.append("missing: " + ", ".join(missing))
    if version not in (1, 2):
        errors.append(f"unsupported schema_version: {version!r}")
    if version == 2:
        extra = sorted(row.keys() - V2_ALLOWED)
        if extra:
            errors.append("unexpected: " + ", ".join(extra))
        if row.get("effort") not in ("low", "medium", "high"):
            errors.append("effort must be low, medium, or high")
        if row.get("outcome") not in ("passed", "failed", "partial", "timeout", "error", "excluded"):
            errors.append("invalid outcome")
        for key in ("success", "capability_pass"):
            if key in row and not isinstance(row[key], bool):
                errors.append(f"{key} must be boolean")
        if row.get("critical_pass") is not None and not isinstance(row.get("critical_pass"), bool):
            errors.append("critical_pass must be boolean or null")
        if row.get("task_version") is not None and (
            not isinstance(row.get("task_version"), int) or isinstance(row.get("task_version"), bool)
            or row["task_version"] < 1
        ):
            errors.append("task_version must be a positive integer or null")
        if row.get("run_p2p") is not None and not isinstance(row.get("run_p2p"), bool):
            errors.append("run_p2p must be boolean or null")
        allowed_modes = {
            "handoff_mode": {"durable", "runner-lite", "runner-structured", "runner", "runner-captured", "unknown"},
            "inspection_mode": {"default", "bounded", "focused", "agent-judgment", "unknown"},
            "prompt_mode": {"full", "compact", "claude-neutral-v1", "unknown"},
        }
        for key, choices in allowed_modes.items():
            if key in row and row[key] not in choices:
                errors.append(f"invalid {key}")
        if not isinstance(row.get("changed_files"), list) or not all(isinstance(item, str) for item in row.get("changed_files", [])):
            errors.append("changed_files must be an array of strings")
        if len(set(row.get("changed_files", []))) != len(row.get("changed_files", [])):
            errors.append("changed_files must be unique")
        if not isinstance(row.get("note"), str) or len(row.get("note", "")) > 500:
            errors.append("note must be a string of at most 500 characters")
        if row.get("provider") not in (None, "codex", "claude"):
            errors.append("provider must be codex or claude")
        if row.get("total_token_telemetry_complete") is not None and not isinstance(row.get("total_token_telemetry_complete"), bool):
            errors.append("total_token_telemetry_complete must be boolean")
        if row.get("total_cost_usd") is not None and (
            not isinstance(row.get("total_cost_usd"), (int, float))
            or isinstance(row.get("total_cost_usd"), bool) or row["total_cost_usd"] < 0
        ):
            errors.append("total_cost_usd must be a nonnegative number or null")
        for key in ("agent_calls", "codex_mcp_calls"):
            if key in row and (not isinstance(row[key], int) or isinstance(row[key], bool) or row[key] < 0):
                errors.append(f"{key} must be a nonnegative integer")
        for key in NONNEGATIVE_INTS:
            value = row.get(key)
            if value is None and key in NULLABLE_NUMBERS:
                continue
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"{key} must be a nonnegative integer" + (" or null" if key in NULLABLE_NUMBERS else ""))
        for key in ("capability_score", "f2p", "p2p", "scope", "completion"):
            value = row.get(key)
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
                errors.append(f"{key} must be a nonnegative number or null")
        score = row.get("capability_score")
        if score is not None and score > 100:
            errors.append("capability_score must be <= 100")
    else:
        if "duration_ms" in row and row["duration_ms"] is not None and not isinstance(row["duration_ms"], int):
            errors.append("legacy duration_ms must be an integer or null")
        if "success" in row and not isinstance(row["success"], bool):
            errors.append("success must be boolean")
    return errors


def validate_file(path: Path = METRICS) -> dict[str, Any]:
    rows, blanks, parse_errors = read_jsonl(path)
    errors = list(parse_errors)
    versions: dict[str, int] = {}
    run_ids: set[str] = set()
    for line_number, row in rows:
        version = str(row.get("schema_version", 1))
        versions[version] = versions.get(version, 0) + 1
        for error in validate_row(row):
            errors.append(f"line {line_number}: {error}")
        run_id = row.get("run_id")
        if run_id:
            if run_id in run_ids:
                errors.append(f"line {line_number}: duplicate run_id: {run_id}")
            run_ids.add(run_id)
    return {"status": "pass" if not errors else "fail", "path": str(path), "rows": len(rows), "blank_lines_skipped": blanks, "versions": versions, "errors": errors}


def command_metrics(stdout_path: Path) -> dict[str, int]:
    completed = failed = output_chars = 0
    if not stdout_path.exists():
        return {"completed_commands": 0, "failed_commands": 0, "tool_output_chars": 0}
    for line in stdout_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        output_chars += len(item.get("aggregated_output") or "")
        if item.get("exit_code") == 0 and item.get("status") == "completed":
            completed += 1
        else:
            failed += 1
    return {"completed_commands": completed, "failed_commands": failed, "tool_output_chars": output_chars}


def _failure(result: dict[str, Any]) -> tuple[str | None, str | None, str]:
    execution = result.get("execution") or {}
    grade = result.get("grade") or {}
    if execution.get("timed_out"):
        return "worker", "timeout", "timeout"
    if execution.get("exit_code") not in (None, 0):
        return "worker", "nonzero-exit", "error"
    if grade.get("scope") not in (None, 15):
        return "grader", "scope", "failed"
    if grade.get("p2p") not in (None, 25):
        return "grader", "p2p", "failed"
    if not result.get("capability_pass"):
        return "grader", "capability-gate", "partial"
    return None, None, "passed"


def benchmark_row(result: dict[str, Any], stdout_override: Path | None = None) -> dict[str, Any]:
    execution = result.get("execution") or {}
    usage = result.get("aggregate_usage") or execution.get("usage") or {}
    grade = result.get("grade") or {}
    provider = str(result.get("provider") or "codex")
    run_id = str(result["run_id"])
    stdout_path = stdout_override or ROOT / str(execution.get("stdout_path", ""))
    execution_tools = execution.get("tool_metrics") or {}
    if provider == "claude":
        commands = {
            "completed_commands": int(execution_tools.get("completed_commands") or 0),
            "failed_commands": int(execution_tools.get("failed_commands") or 0),
            "tool_output_chars": int(execution_tools.get("tool_output_chars") or 0),
        }
    else:
        commands = command_metrics(stdout_path)
    input_tokens = usage.get("input_tokens")
    cached_tokens = usage.get("cached_input_tokens")
    output_tokens = usage.get("output_tokens")
    effective = None
    if isinstance(result.get("effective_tokens"), int):
        effective = result["effective_tokens"]
    elif all(isinstance(value, int) for value in (input_tokens, cached_tokens, output_tokens)):
        effective = input_tokens - cached_tokens + output_tokens
    failure_phase, failure_category, outcome = _failure(result)
    worker_duration = execution.get("duration_ms") if isinstance(execution.get("duration_ms"), int) else None
    generation_duration = result.get("generation_duration_ms") if isinstance(result.get("generation_duration_ms"), int) else None
    if worker_duration is not None and generation_duration is not None:
        worker_duration += generation_duration
    total_duration = result.get("total_duration_ms") if isinstance(result.get("total_duration_ms"), int) else (worker_duration or 0)
    score = grade.get("score") if isinstance(grade.get("score"), (int, float)) else None
    prompt_bytes = execution.get("prompt_bytes") if isinstance(execution.get("prompt_bytes"), int) else None
    if provider == "claude" and isinstance((result.get("generation") or {}).get("prompt_bytes"), int):
        prompt_bytes = (prompt_bytes or 0) + result["generation"]["prompt_bytes"]
    note = f"benchmark {result.get('task_id')} {outcome}; score={score}; critical={grade.get('critical_pass')}"
    row = {
        "schema_version": 2,
        "date": str(result.get("date") or "unknown"),
        "task_type": "other",
        "agent": provider,
        "tier": str(result.get("worker") or "unknown"),
        "duration_ms": total_duration,
        "success": bool(result.get("capability_pass")),
        "note": note[:500],
        "run_id": run_id,
        "run_label": str(result.get("run_label") or "unknown"),
        "task_id": str(result.get("task_id") or "unknown"),
        "model": str(result.get("model") or "unknown"),
        "effort": str(result.get("effort") or "medium"),
        "outcome": outcome,
        "capability_score": score,
        "critical_pass": grade.get("critical_pass") if isinstance(grade.get("critical_pass"), bool) else None,
        "capability_pass": bool(result.get("capability_pass")),
        "f2p": grade.get("f2p") if isinstance(grade.get("f2p"), (int, float)) else None,
        "p2p": grade.get("p2p") if isinstance(grade.get("p2p"), (int, float)) else None,
        "scope": grade.get("scope") if isinstance(grade.get("scope"), (int, float)) else None,
        "completion": grade.get("completion") if isinstance(grade.get("completion"), (int, float)) else None,
        "input_tokens": input_tokens if isinstance(input_tokens, int) else None,
        "cached_input_tokens": cached_tokens if isinstance(cached_tokens, int) else None,
        "output_tokens": output_tokens if isinstance(output_tokens, int) else None,
        "reasoning_output_tokens": usage.get("reasoning_output_tokens") if isinstance(usage.get("reasoning_output_tokens"), int) else None,
        "effective_tokens": effective,
        "prompt_bytes": prompt_bytes,
        "instruction_bytes": result.get("instruction_bytes") if isinstance(result.get("instruction_bytes"), int) else None,
        **commands,
        "setup_duration_ms": result.get("setup_duration_ms") if isinstance(result.get("setup_duration_ms"), int) else None,
        "worker_duration_ms": worker_duration,
        "grader_duration_ms": result.get("grader_duration_ms") if isinstance(result.get("grader_duration_ms"), int) else None,
        "review_duration_ms": None,
        "total_duration_ms": total_duration,
        "changed_files": sorted(set(result.get("changed_files") or [])),
        "retries": 0,
        "escalation": None,
        "failure_phase": failure_phase,
        "failure_category": failure_category,
        "artifact": str(result.get("artifact") or f"tools/out/agent-benchmark/{run_id}/result.json"),
        "handoff_mode": str(result.get("handoff_mode") or "unknown"),
        "inspection_mode": str(result.get("inspection_mode") or "unknown"),
        "prompt_mode": str(result.get("prompt_mode") or "unknown"),
        "task_version": result.get("task_version") if isinstance(result.get("task_version"), int) else None,
        "repo_ref": str(result.get("repo_ref") or "unknown"),
        "repo_commit": str(result.get("repo_commit") or "unknown"),
        "codex_cli": str(result.get("codex_cli") or "unknown"),
        "run_p2p": result.get("run_p2p") if isinstance(result.get("run_p2p"), bool) else None,
        "task_definition_sha256": str(result.get("task_definition_sha256") or "unknown"),
        "grader_sha256": str(result.get("grader_sha256") or "unknown"),
        "runner_sha256": str(result.get("runner_sha256") or "unknown"),
    }
    if provider == "claude":
        generation = result.get("generation") or {}
        generation_usage = generation.get("usage") or {}
        row.update({
            "provider": "claude",
            "provider_cli": str(result.get("claude_cli") or "unknown"),
            "config_variant": str(result.get("config_variant") or "unknown"),
            "config_sha256": str(result.get("config_sha256") or "unknown"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens") if isinstance(usage.get("cache_creation_input_tokens"), int) else None,
            "generation_effective_tokens": generation_usage.get("effective_tokens") if isinstance(generation_usage.get("effective_tokens"), int) else None,
            "generation_duration_ms": generation_duration,
            "agent_calls": int(execution_tools.get("agent_calls") or 0),
            "codex_mcp_calls": int(execution_tools.get("codex_mcp_calls") or 0),
            "total_cost_usd": result.get("total_cost_usd") if isinstance(result.get("total_cost_usd"), (int, float)) else None,
            "total_token_telemetry_complete": bool(result.get("total_token_telemetry_complete")),
        })
    else:
        row["provider"] = "codex"
    return row


def import_benchmark(label: str, *, dry_run: bool, metrics_path: Path = METRICS, results_path: Path = RESULTS, exclusions_path: Path = EXCLUSIONS) -> dict[str, Any]:
    metric_rows, _, metric_errors = read_jsonl(metrics_path)
    if metric_errors:
        return {"status": "fail", "errors": metric_errors}
    existing = {row.get("run_id") for _, row in metric_rows if row.get("run_id")}
    result_rows, blanks, result_errors = read_jsonl(results_path)
    if result_errors:
        return {"status": "fail", "errors": result_errors}
    exclusions = json.loads(exclusions_path.read_text(encoding="utf-8")) if exclusions_path.exists() else {}
    proposed = []
    skipped_excluded = []
    skipped_duplicate = []
    for _, result in result_rows:
        if result.get("run_label") != label:
            continue
        run_id = result.get("run_id")
        if run_id in exclusions:
            skipped_excluded.append(run_id)
            continue
        if run_id in existing:
            skipped_duplicate.append(run_id)
            continue
        row = benchmark_row(result)
        errors = validate_row(row)
        if errors:
            return {"status": "fail", "run_id": run_id, "errors": errors}
        proposed.append(row)
        existing.add(run_id)
    if proposed and not dry_run:
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        needs_newline = metrics_path.exists() and metrics_path.stat().st_size and not metrics_path.read_bytes().endswith(b"\n")
        with metrics_path.open("a", encoding="utf-8") as handle:
            if needs_newline:
                handle.write("\n")
            for row in proposed:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return {
        "status": "pass", "dry_run": dry_run, "run_label": label, "eligible": len(proposed),
        "appended": 0 if dry_run else len(proposed), "run_ids": [row["run_id"] for row in proposed],
        "excluded": skipped_excluded, "duplicates": skipped_duplicate, "blank_result_lines_skipped": blanks,
    }


def append_driver_tasks(task_ids: list[str], report: str, model: str, path: Path = METRICS) -> dict[str, Any]:
    existing_rows, _, errors = read_jsonl(path)
    if errors:
        return {"status": "fail", "errors": errors}
    existing = {
        (row.get("task_id"), row.get("tier"), row.get("report"))
        for _, row in existing_rows
    }
    rows = []
    duplicates = []
    for task_id in task_ids:
        key = (task_id, "driver-codex", report)
        if key in existing:
            duplicates.append(task_id)
            continue
        if not task_id.startswith("T-") or not task_id[2:].isdigit():
            return {"status": "fail", "errors": [f"invalid task id: {task_id}"]}
        rows.append({
            "date": date.today().isoformat(), "task_type": "other", "agent": "codex",
            "tier": "driver-codex", "model": model, "duration_ms": None,
            "success": True, "task_id": task_id, "report": report,
            "note": f"{task_id} complete; {report}",
        })
    if rows:
        needs_newline = path.exists() and path.stat().st_size and not path.read_bytes().endswith(b"\n")
        with path.open("a", encoding="utf-8") as handle:
            if needs_newline:
                handle.write("\n")
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return {"status": "pass", "appended": len(rows), "task_ids": [row["task_id"] for row in rows],
            "duplicates": duplicates, "report": report}


def summarize(label: str | None, path: Path = METRICS, *, details: bool = False) -> dict[str, Any]:
    rows, blanks, errors = read_jsonl(path)
    selected = [row for _, row in rows if row.get("schema_version") == 2 and (label is None or row.get("run_label") == label)]
    passed = [row for row in selected if row.get("capability_pass")]
    def total(key: str) -> int:
        return sum(row.get(key) or 0 for row in selected)
    task_counts: dict[str, dict[str, int]] = {}
    for row in selected:
        task = str(row.get("task_id") or "unknown")
        counts = task_counts.setdefault(task, {"runs": 0, "passed": 0, "failed": 0, "effective_tokens": 0})
        counts["runs"] += 1
        counts["passed" if row.get("capability_pass") else "failed"] += 1
        counts["effective_tokens"] += row.get("effective_tokens") or 0
    result = {
        "status": "pass" if not errors else "fail", "run_label": label, "runs": len(selected),
        "passed": len(passed), "failed": len(selected) - len(passed),
        "mean_score": round(sum(row.get("capability_score") or 0 for row in selected) / len(selected), 2) if selected else None,
        "input_tokens": total("input_tokens"), "cached_input_tokens": total("cached_input_tokens"),
        "output_tokens": total("output_tokens"), "reasoning_output_tokens": total("reasoning_output_tokens"),
        "effective_tokens": total("effective_tokens"), "completed_commands": total("completed_commands"),
        "failed_commands": total("failed_commands"), "tool_output_chars": total("tool_output_chars"),
        "total_duration_ms": total("total_duration_ms"), "blank_lines_skipped": blanks, "errors": errors,
        "task_counts": task_counts,
        "failure_run_ids": [row["run_id"] for row in selected if not row.get("capability_pass")],
    }
    if details:
        result["run_details"] = [
            {"run_id": row["run_id"], "task_id": row["task_id"],
             "score": row["capability_score"], "passed": row["capability_pass"]}
            for row in selected
        ]
    return result


def summarize_labels(path: Path = METRICS) -> dict[str, Any]:
    rows, blanks, errors = read_jsonl(path)
    selected = [row for _, row in rows if row.get("schema_version") == 2]
    labels: dict[str, list[dict[str, Any]]] = {}
    for row in selected:
        labels.setdefault(str(row.get("run_label") or "unknown"), []).append(row)

    def total(items: list[dict[str, Any]], key: str) -> int:
        return sum(row.get(key) or 0 for row in items)

    summaries = []
    for label, items in sorted(labels.items()):
        failed = [row for row in items if not row.get("capability_pass")]
        summaries.append({
            "run_label": label,
            "runs": len(items),
            "passed": len(items) - len(failed),
            "failed": len(failed),
            "effective_tokens": total(items, "effective_tokens"),
            "failed_effective_tokens": total(failed, "effective_tokens"),
            "tool_output_chars": total(items, "tool_output_chars"),
            "total_duration_ms": total(items, "total_duration_ms"),
            "total_cost_usd": round(sum(float(row.get("total_cost_usd") or 0) for row in items), 8),
            "agent_calls": total(items, "agent_calls"),
            "codex_mcp_calls": total(items, "codex_mcp_calls"),
            "total_token_telemetry_complete": all(row.get("total_token_telemetry_complete", True) is True for row in items),
            "providers": sorted({str(row.get("provider") or row.get("agent") or "unknown") for row in items}),
            "config_variants": sorted({str(row.get("config_variant") or "n/a") for row in items}),
            "task_ids": sorted({str(row.get("task_id")) for row in items}),
            "task_versions": sorted({f"{row.get('task_id')}@{row.get('task_version', 'unknown')}" for row in items}),
            "routes": sorted({f"{row.get('tier')}:{row.get('effort')}" for row in items}),
        })
    failed_rows = [row for row in selected if not row.get("capability_pass")]
    return {
        "status": "pass" if not errors else "fail",
        "runs": len(selected),
        "passed": len(selected) - len(failed_rows),
        "failed": len(failed_rows),
        "effective_tokens": total(selected, "effective_tokens"),
        "failed_effective_tokens": total(failed_rows, "effective_tokens"),
        "tool_output_chars": total(selected, "tool_output_chars"),
        "total_duration_ms": total(selected, "total_duration_ms"),
        "labels": summaries,
        "blank_lines_skipped": blanks,
        "errors": errors,
    }


def _portfolio_samples(groups: dict[str, list[dict[str, Any]]], key: str) -> tuple[list[int], list[str]]:
    samples: list[int] = []
    missing: list[str] = []
    repeats = len(next(iter(groups.values()))) if groups else 0
    ordered = {task: sorted(rows, key=lambda row: (str(row.get("date")), str(row.get("run_id"))))
               for task, rows in groups.items()}
    for index in range(repeats):
        values = []
        for task, rows in ordered.items():
            value = rows[index].get(key)
            if not isinstance(value, int) or isinstance(value, bool):
                missing.append(str(rows[index].get("run_id") or f"{task}[{index}]") + f":{key}")
            else:
                values.append(value)
        if len(values) == len(ordered):
            samples.append(sum(values))
    return samples, missing


def _metric_comparison(baseline: list[int], candidate: list[int]) -> dict[str, Any]:
    baseline_median = statistics.median(baseline)
    candidate_median = statistics.median(candidate)
    delta = None if baseline_median == 0 else round((candidate_median / baseline_median - 1) * 100, 1)
    if max(candidate) < min(baseline):
        relation = "candidate-better-nonoverlap"
    elif max(baseline) < min(candidate):
        relation = "candidate-worse-nonoverlap"
    else:
        relation = "overlap"
    return {
        "baseline_samples": baseline,
        "candidate_samples": candidate,
        "baseline_median": baseline_median,
        "candidate_median": candidate_median,
        "median_change_percent": delta,
        "baseline_range": [min(baseline), max(baseline)],
        "candidate_range": [min(candidate), max(candidate)],
        "range_relation": relation,
    }


def _run_dimensions(rows: list[dict[str, Any]]) -> dict[str, list[Any]]:
    keys = ("provider", "config_variant", "config_sha256", "model", "effort",
            "handoff_mode", "inspection_mode", "prompt_mode",
            "task_version", "task_definition_sha256", "grader_sha256", "runner_sha256",
            "repo_commit", "run_p2p")
    return {key: sorted({row.get(key, "unknown") for row in rows}, key=lambda value: str(value)) for key in keys}


def compare_labels(baseline_label: str, candidate_label: str, path: Path = METRICS) -> dict[str, Any]:
    parsed, blanks, parse_errors = read_jsonl(path)
    rows = [row for _, row in parsed if row.get("schema_version") == 2]
    baseline = [row for row in rows if row.get("run_label") == baseline_label]
    candidate = [row for row in rows if row.get("run_label") == candidate_label]
    errors = list(parse_errors)
    warnings: list[str] = []
    if not baseline:
        errors.append(f"no v2 rows for baseline label: {baseline_label}")
    if not candidate:
        errors.append(f"no v2 rows for candidate label: {candidate_label}")
    baseline_groups: dict[str, list[dict[str, Any]]] = {}
    candidate_groups: dict[str, list[dict[str, Any]]] = {}
    for row in baseline:
        baseline_groups.setdefault(str(row.get("task_id")), []).append(row)
    for row in candidate:
        candidate_groups.setdefault(str(row.get("task_id")), []).append(row)
    if set(baseline_groups) != set(candidate_groups):
        errors.append(
            f"task sets differ: baseline={sorted(baseline_groups)} candidate={sorted(candidate_groups)}"
        )
    task_ids = sorted(set(baseline_groups) & set(candidate_groups))
    repeat_counts: dict[str, dict[str, int]] = {}
    for task in task_ids:
        b_count, c_count = len(baseline_groups[task]), len(candidate_groups[task])
        repeat_counts[task] = {"baseline": b_count, "candidate": c_count}
        if b_count != c_count:
            errors.append(f"run counts differ for {task}: baseline={b_count} candidate={c_count}")
        b_versions = {row.get("task_version") for row in baseline_groups[task] if row.get("task_version") is not None}
        c_versions = {row.get("task_version") for row in candidate_groups[task] if row.get("task_version") is not None}
        if not b_versions or not c_versions:
            errors.append(f"{task}: task_version missing from one or both labels")
        elif b_versions != c_versions or len(b_versions) != 1:
            errors.append(f"task versions differ for {task}: baseline={sorted(b_versions)} candidate={sorted(c_versions)}")
        for key in ("task_definition_sha256", "grader_sha256"):
            b_hashes = {row.get(key) for row in baseline_groups[task] if row.get(key) not in (None, "unknown")}
            c_hashes = {row.get(key) for row in candidate_groups[task] if row.get(key) not in (None, "unknown")}
            if not b_hashes or not c_hashes:
                errors.append(f"{task}: {key} missing from one or both labels")
            elif b_hashes != c_hashes or len(b_hashes) != 1:
                errors.append(f"{key} differs for {task}: baseline={sorted(b_hashes)} candidate={sorted(c_hashes)}")
    all_counts = {len(group) for group in baseline_groups.values()} | {len(group) for group in candidate_groups.values()}
    if len(all_counts) > 1:
        errors.append("labels do not contain an equal repeat count for every task")
    for name, selected in (("baseline", baseline), ("candidate", candidate)):
        if any(row.get("run_p2p") is None for row in selected):
            warnings.append(f"{name}: run_p2p telemetry missing from at least one row")
        for key in ("model", "effort", "handoff_mode", "inspection_mode", "prompt_mode"):
            if any(row.get(key) in (None, "unknown") for row in selected):
                warnings.append(f"{name}: {key} missing from at least one row")

    metric_results: dict[str, Any] = {}
    missing_telemetry: list[str] = []
    if not errors and task_ids:
        for key in ("effective_tokens", "input_tokens", "cached_input_tokens", "output_tokens",
                    "tool_output_chars", "completed_commands", "failed_commands",
                    "worker_duration_ms", "grader_duration_ms", "total_duration_ms"):
            b_samples, b_missing = _portfolio_samples(baseline_groups, key)
            c_samples, c_missing = _portfolio_samples(candidate_groups, key)
            missing_telemetry.extend(b_missing + c_missing)
            if b_samples and c_samples and len(b_samples) == len(c_samples):
                metric_results[key] = _metric_comparison(b_samples, c_samples)
    if missing_telemetry:
        warnings.append("missing telemetry: " + ", ".join(sorted(missing_telemetry)))

    candidate_failures = [
        {"run_id": row.get("run_id"), "task_id": row.get("task_id"),
         "score": row.get("capability_score"), "phase": row.get("failure_phase"),
         "category": row.get("failure_category"), "artifact": row.get("artifact")}
        for row in candidate if not row.get("capability_pass")
    ]
    capability_gate = bool(candidate) and not candidate_failures
    total_token_telemetry_complete = all(
        row.get("total_token_telemetry_complete", True) is True
        for row in baseline + candidate
    )
    if not total_token_telemetry_complete:
        warnings.append("total-token telemetry is incomplete for at least one run; external-worker token claims are inconclusive")
    score_gate = all(
        min(row.get("capability_score") or 0 for row in candidate_groups[task]) >=
        min(row.get("capability_score") or 0 for row in baseline_groups[task])
        for task in task_ids
    ) if task_ids else False
    def delta_at_most(key: str, maximum: float) -> bool:
        value = metric_results.get(key, {}).get("median_change_percent")
        return isinstance(value, (int, float)) and value <= maximum
    def median_not_increased(key: str) -> bool:
        metric = metric_results.get(key, {})
        baseline_value = metric.get("baseline_median")
        candidate_value = metric.get("candidate_median")
        return isinstance(baseline_value, (int, float)) and isinstance(candidate_value, (int, float)) and candidate_value <= baseline_value
    gates = {
        "candidate_all_capability_pass": capability_gate,
        "no_task_score_regression": score_gate,
        "effective_tokens_improve_5_percent": total_token_telemetry_complete and delta_at_most("effective_tokens", -5.0),
        "total_token_telemetry_complete": total_token_telemetry_complete,
        "tool_output_not_increased": delta_at_most("tool_output_chars", 0.0),
        "failed_commands_not_increased": median_not_increased("failed_commands"),
        "total_duration_not_over_5_percent": delta_at_most("total_duration_ms", 5.0),
    }
    if errors:
        recommendation = "invalid-comparison"
    elif not capability_gate or not score_gate:
        recommendation = "reject-capability-regression"
    elif not total_token_telemetry_complete:
        recommendation = "review-incomplete-total-token-telemetry"
    elif not gates["effective_tokens_improve_5_percent"]:
        recommendation = "reject-no-token-gain"
    elif all((gates["tool_output_not_increased"], gates["failed_commands_not_increased"],
              gates["total_duration_not_over_5_percent"])):
        recommendation = "promote-after-required-full-regression"
    else:
        recommendation = "review-observed-tradeoffs"
    return {
        "status": "pass" if not errors else "fail",
        "safe_to_compare": not errors,
        "baseline": {"label": baseline_label, "runs": len(baseline), "dimensions": _run_dimensions(baseline)},
        "candidate": {"label": candidate_label, "runs": len(candidate), "dimensions": _run_dimensions(candidate)},
        "matched": {"task_ids": task_ids, "repeat_counts": repeat_counts},
        "metrics": metric_results,
        "gates": gates,
        "candidate_failures": candidate_failures,
        "recommendation": recommendation,
        "blank_lines_skipped": blanks,
        "warnings": warnings,
        "errors": errors,
    }


def selftest() -> dict[str, Any]:
    event_lines = [
        {"type": "item.started", "item": {"type": "command_execution", "status": "in_progress", "aggregated_output": "wrong"}},
        {"type": "item.completed", "item": {"type": "command_execution", "status": "completed", "exit_code": 0, "aggregated_output": "abc"}},
        {"type": "item.completed", "item": {"type": "command_execution", "status": "failed", "exit_code": 2, "aggregated_output": "defg"}},
    ]
    with tempfile.TemporaryDirectory(prefix="metrics-selftest-") as temporary:
        root = Path(temporary)
        stdout = root / "stdout.jsonl"
        stdout.write_text("\n".join(json.dumps(item) for item in event_lines) + "\n", encoding="utf-8")
        assert command_metrics(stdout) == {"completed_commands": 1, "failed_commands": 1, "tool_output_chars": 7}
        metrics = root / "metrics.jsonl"
        metrics.write_text('\n{"date":"2026-01-01","task_type":"other","agent":"codex","tier":"low","duration_ms":1,"success":true,"note":"legacy"}\n', encoding="utf-8")
        result = {
            "run_id": "selftest-run", "run_label": "selftest", "task_id": "WBD-999", "date": "2026-01-01T00:00:00Z",
            "model": "test-model", "effort": "low", "worker": "test-worker", "capability_pass": True,
            "task_definition_sha256": "task-hash", "grader_sha256": "grader-hash", "runner_sha256": "runner-hash",
            "changed_files": ["x"], "execution": {"duration_ms": 5, "exit_code": 0, "timed_out": False, "prompt_bytes": 9,
            "stdout_path": "unused", "usage": {"input_tokens": 20, "cached_input_tokens": 5, "output_tokens": 3, "reasoning_output_tokens": 1}},
            "grade": {"score": 100, "critical_pass": True, "f2p": 55, "p2p": 25, "scope": 15, "completion": 5},
        }
        row = benchmark_row(result, stdout)
        assert row["effective_tokens"] == 18 and row["completed_commands"] == 1 and not validate_row(row)
        claude_result = {
            **result,
            "run_id": "selftest-claude", "run_label": "selftest-claude", "provider": "claude",
            "worker": "claude-autonomous", "claude_cli": "test-claude",
            "config_variant": "autonomous", "config_sha256": "config-hash",
            "artifact": "tools/out/claude-benchmark/selftest-claude/result.json",
            "handoff_mode": "runner-captured", "inspection_mode": "agent-judgment",
            "prompt_mode": "claude-neutral-v1", "effective_tokens": 23,
            "aggregate_usage": {"input_tokens": 30, "cached_input_tokens": 10,
                                "cache_creation_input_tokens": 5, "output_tokens": 3,
                                "reasoning_output_tokens": 0, "effective_tokens": 23},
            "generation": None, "generation_duration_ms": None,
            "total_cost_usd": 0.1, "total_token_telemetry_complete": True,
            "execution": {**result["execution"], "tool_metrics": {
                "completed_commands": 2, "failed_commands": 0,
                "tool_output_chars": 7, "agent_calls": 1, "codex_mcp_calls": 0,
            }},
        }
        claude_row = benchmark_row(claude_result, stdout)
        assert claude_row["agent"] == "claude" and claude_row["effective_tokens"] == 23
        assert claude_row["agent_calls"] == 1 and not validate_row(claude_row)
        results = root / "results.jsonl"; results.write_text(json.dumps(result) + "\n", encoding="utf-8")
        exclusions = root / "exclusions.json"; exclusions.write_text("{}\n", encoding="utf-8")
        dry = import_benchmark("selftest", dry_run=True, metrics_path=metrics, results_path=results, exclusions_path=exclusions)
        assert dry["eligible"] == 1 and dry["appended"] == 0
        actual = import_benchmark("selftest", dry_run=False, metrics_path=metrics, results_path=results, exclusions_path=exclusions)
        duplicate = import_benchmark("selftest", dry_run=False, metrics_path=metrics, results_path=results, exclusions_path=exclusions)
        assert actual["appended"] == 1 and duplicate["duplicates"] == ["selftest-run"]
        claude_results = root / "claude-results.jsonl"
        claude_results.write_text(json.dumps(claude_result) + "\n", encoding="utf-8")
        claude_import = import_benchmark(
            "selftest-claude", dry_run=False, metrics_path=metrics,
            results_path=claude_results, exclusions_path=exclusions,
        )
        assert claude_import["appended"] == 1
        validation = validate_file(metrics)
        assert validation["status"] == "pass" and validation["blank_lines_skipped"] == 1
        comparison_path = root / "comparison.jsonl"
        comparison_rows = []
        for label, effective in (("baseline", 20), ("candidate", 15)):
            for index in range(2):
                comparison_rows.append({
                    **row, "run_id": f"{label}-{index}", "run_label": label,
                    "task_id": "WBD-999", "task_version": 1,
                    "effective_tokens": effective, "run_p2p": True,
                })
        comparison_path.write_text("\n".join(json.dumps(item) for item in comparison_rows) + "\n", encoding="utf-8")
        comparison = compare_labels("baseline", "candidate", comparison_path)
        assert comparison["status"] == "pass"
        assert comparison["recommendation"] == "promote-after-required-full-regression"
        comparison_path.write_text("\n".join(json.dumps(item) for item in comparison_rows[:-1]) + "\n", encoding="utf-8")
        unsafe = compare_labels("baseline", "candidate", comparison_path)
        assert unsafe["status"] == "fail" and not unsafe["safe_to_compare"]
        label_summary = summarize_labels(comparison_path)
        assert label_summary["runs"] == 3 and len(label_summary["labels"]) == 2
        compact_summary = summarize(None, comparison_path)
        detailed_summary = summarize(None, comparison_path, details=True)
        assert "run_details" not in compact_summary and len(detailed_summary["run_details"]) == 3
        driver = append_driver_tasks(["T-1", "T-2"], "tools/out/report.md", "gpt-5", metrics)
        assert driver["appended"] == 2
        driver_duplicate = append_driver_tasks(["T-1"], "tools/out/report.md", "gpt-5", metrics)
        assert driver_duplicate["duplicates"] == ["T-1"]
    return {"status": "pass", "command_event_deduplication": "pass", "dry_run": "pass", "append_and_dedupe": "pass", "legacy_and_v2_validation": "pass", "safe_comparison": "pass", "label_cost_summary": "pass"}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    sub = command.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate"); validate.add_argument("--path", type=Path, default=METRICS)
    importer = sub.add_parser("import-benchmark"); importer.add_argument("--run-label", required=True); importer.add_argument("--dry-run", action="store_true")
    importer.add_argument("--provider", choices=("codex", "claude"), default="codex")
    driver = sub.add_parser("append-driver")
    driver.add_argument("--task-ids", nargs="+", required=True)
    driver.add_argument("--report", required=True)
    driver.add_argument("--model", default="gpt-5")
    summary = sub.add_parser("summarize"); summary.add_argument("--run-label"); summary.add_argument("--details", action="store_true")
    labels = sub.add_parser("labels"); labels.add_argument("--path", type=Path, default=METRICS)
    comparison = sub.add_parser("compare")
    comparison.add_argument("--baseline-label", required=True)
    comparison.add_argument("--candidate-label", required=True)
    comparison.add_argument("--path", type=Path, default=METRICS)
    sub.add_parser("selftest")
    return command


def main() -> int:
    args = parser().parse_args()
    if args.command == "validate": result = validate_file(args.path)
    elif args.command == "import-benchmark":
        result = import_benchmark(
            args.run_label, dry_run=args.dry_run,
            results_path=CLAUDE_RESULTS if args.provider == "claude" else RESULTS,
            exclusions_path=EXCLUSIONS,
        )
    elif args.command == "append-driver": result = append_driver_tasks(args.task_ids, args.report, args.model)
    elif args.command == "summarize": result = summarize(args.run_label, details=args.details)
    elif args.command == "labels": result = summarize_labels(args.path)
    elif args.command == "compare": result = compare_labels(args.baseline_label, args.candidate_label, args.path)
    else: result = selftest()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

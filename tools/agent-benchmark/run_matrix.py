#!/usr/bin/env python3
"""Run a frozen Codex or Claude benchmark matrix sequentially and resumably."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BENCHMARK = HERE / "benchmark.py"
DEFAULT_FREEZE = HERE / "gpt56-full-20260713.freeze.json"
RESULTS = HERE / "results.jsonl"
METRICS_TOOL = ROOT / "tools" / "task-metrics.py"
ARTIFACTS = HERE / "artifacts"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def read_results() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not RESULTS.exists():
        return rows
    for line_number, line in enumerate(RESULTS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        run_id = str(row["run_id"])
        if run_id in rows:
            raise ValueError(f"duplicate run id at results line {line_number}: {run_id}")
        rows[run_id] = row
    return rows


def run_id(label: str, task: str, model: str, effort: str) -> str:
    model_name = model.removeprefix("gpt-5.6-").removeprefix("claude-")
    model_name = re.sub(r"[^a-z0-9]+", "-", model_name.lower()).strip("-")
    task_name = task.lower().replace("-", "")
    return f"{label}-{effort}-{model_name}-{task_name}"


def frozen_cells(freeze: dict[str, Any], phase: str, selected_tasks: set[str] | None) -> list[dict[str, str]]:
    label = str(freeze["run_label"])
    models = [str(item) for item in freeze["models"]]
    efforts: list[str] = []
    if phase in {"documented", "all"}:
        efforts.extend(str(item) for item in freeze["documented_efforts"])
    if phase in {"ultra", "all"}:
        efforts.extend(str(item) for item in freeze["runtime_verified_efforts"])
    tasks = [str(item) for item in freeze["execution_order"]["task_blocks"]]
    if selected_tasks is not None:
        unknown = selected_tasks - set(tasks)
        if unknown:
            raise ValueError(f"unknown task selections: {sorted(unknown)}")
        tasks = [task for task in tasks if task in selected_tasks]
    cells: list[dict[str, str]] = []
    for task in tasks:
        block = [
            {"task": task, "model": model, "effort": effort,
             "run_id": run_id(label, task, model, effort)}
            for model in models for effort in efforts
        ]
        if freeze["execution_order"].get("within_block") != "listed":
            block.sort(key=lambda cell: hashlib.sha256(
                f"{label}|{task}|{cell['model']}|{cell['effort']}".encode("utf-8")
            ).hexdigest())
        cells.extend(block)
    return cells


def verify_freeze(freeze: dict[str, Any]) -> None:
    identities = freeze["identities"]
    paths = {
        "orchestrator_sha256": Path(__file__),
        "matrix_runner_sha256": BENCHMARK,
        "grader_sha256": HERE / "task_ops.py",
        "tasks_manifest_sha256": HERE / "tasks.json",
        "final_schema_sha256": HERE / "final.schema.json",
        "metrics_schema_sha256": ROOT / "tools" / "task-metrics.schema.json",
        "metrics_tool_sha256": METRICS_TOOL,
    }
    errors = []
    for key, path in paths.items():
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != identities[key]:
            errors.append(f"{key}: expected {identities[key]}, observed {observed}")
    provider = str(freeze.get("provider"))
    if provider not in {"codex", "claude"}:
        errors.append(f"unsupported provider: {provider}")
    client_key = f"{provider}_cli"
    client_command = ["codex", "--version"] if provider == "codex" else ["claude", "--version"]
    observed_client = subprocess.run(
        client_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    ).stdout.strip()
    if identities.get(client_key) != observed_client:
        errors.append(
            f"{client_key}: expected {identities.get(client_key)}, observed {observed_client}"
        )
    baseline = str(freeze["baseline_commit"])
    check = subprocess.run(
        ["git", "cat-file", "-e", f"{baseline}^{{commit}}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if check.returncode != 0:
        errors.append(f"missing baseline commit: {baseline}")
    if errors:
        raise SystemExit("freeze verification failed:\n- " + "\n- ".join(errors))


def validate_label_modes(
    freeze: dict[str, Any], rows: dict[str, dict[str, Any]]
) -> None:
    """Reject reuse of a run label for a different workflow contract."""
    label = str(freeze["run_label"])
    settings = freeze["settings"]
    expected = (
        str(settings["prompt_mode"]),
        str(settings["handoff_mode"]),
        str(settings["inspection_mode"]),
        bool(settings["run_p2p"]),
    )
    observed = {
        (
            str(row.get("prompt_mode")),
            str(row.get("handoff_mode")),
            str(row.get("inspection_mode")),
            bool(row.get("run_p2p")),
        )
        for row in rows.values() if row.get("run_label") == label
    }
    if observed and observed != {expected}:
        raise SystemExit(
            f"run label {label} spans workflow modes: expected={expected}, "
            f"observed={sorted(observed)}"
        )


def import_metrics(label: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(METRICS_TOOL), "import-benchmark", "--run-label", label],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise SystemExit(f"metrics import failed:\n{completed.stdout}{completed.stderr}")
    payload = json.loads(completed.stdout)
    if payload.get("status") != "pass":
        raise SystemExit(f"metrics import failed: {payload}")


def execute_cell(freeze: dict[str, Any], cell: dict[str, str]) -> dict[str, Any]:
    label = str(freeze["run_label"])
    settings = freeze["settings"]
    command = [
        sys.executable, str(BENCHMARK), "run", cell["task"],
        "--ref", str(freeze["baseline_commit"]),
        "--run-id", cell["run_id"],
        "--run-label", label,
        "--model", cell["model"],
        "--worker", str(settings["worker_override"]),
        "--effort", cell["effort"],
        "--prompt-mode", str(settings["prompt_mode"]),
        "--handoff-mode", str(settings["handoff_mode"]),
        "--inspection-mode", str(settings["inspection_mode"]),
    ]
    if settings["run_p2p"]:
        command.append("--run-p2p")
    if cell["task"] == "WBD-005" and settings["wbd_005_include_held_out"]:
        command.append("--include-held-out")
    print(json.dumps({"event": "cell-start", **cell}, sort_keys=True), flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    result_path = ARTIFACTS / cell["run_id"] / "result.json"
    if completed.returncode != 0 or not result_path.exists():
        raise SystemExit(
            f"benchmark infrastructure failure for {cell['run_id']}: "
            f"exit={completed.returncode}, result={result_path.exists()}"
        )
    result = read_json(result_path)
    import_metrics(label)
    summary = {
        "event": "cell-complete",
        **cell,
        "capability_pass": bool(result.get("capability_pass")),
        "score": (result.get("grade") or {}).get("score"),
        "worker_duration_ms": (result.get("execution") or {}).get("duration_ms"),
        "total_duration_ms": result.get("total_duration_ms"),
        "effective_tokens": result.get("effective_tokens"),
        "failure_phase": result.get("failure_phase"),
    }
    print(json.dumps(summary, sort_keys=True), flush=True)
    return result


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    command.add_argument("--phase", choices=("documented", "ultra", "all"), default="all")
    command.add_argument("--task", action="append", dest="tasks", help="run only this WBD task block; repeatable")
    command.add_argument("--max-cells", type=int, help="stop after this many pending cells")
    command.add_argument("--dry-run", action="store_true")
    return command


def main() -> int:
    args = parser().parse_args()
    freeze = read_json(args.freeze)
    verify_freeze(freeze)
    selected = set(args.tasks) if args.tasks else None
    cells = frozen_cells(freeze, args.phase, selected)
    results = read_results()
    validate_label_modes(freeze, results)
    pending = [cell for cell in cells if cell["run_id"] not in results]
    if args.max_cells is not None:
        if args.max_cells < 0:
            raise SystemExit("--max-cells must be nonnegative")
        pending = pending[:args.max_cells]
    print(json.dumps({
        "event": "matrix-plan", "phase": args.phase, "selected_tasks": sorted(selected) if selected else None,
        "total_cells": len(cells), "completed_cells": len(cells) - len([cell for cell in cells if cell["run_id"] not in results]),
        "pending_cells": len(pending), "dry_run": args.dry_run,
        "run_ids": [cell["run_id"] for cell in pending],
    }, sort_keys=True), flush=True)
    if args.dry_run:
        return 0
    for cell in pending:
        artifact = ARTIFACTS / cell["run_id"]
        if artifact.exists():
            raise SystemExit(f"pending cell has an existing incomplete artifact: {artifact}")
        execute_cell(freeze, cell)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

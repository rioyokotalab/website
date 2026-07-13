#!/usr/bin/env python3
"""Run planned matched repeats against the frozen GPT-5.6 benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import run_matrix

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BENCHMARK = HERE / "benchmark.py"
FREEZE = HERE / "gpt56-full-20260713.freeze.json"
DEFAULT_PLAN = HERE / "gpt56-repeat-20260714.plan.json"
RESULTS = HERE / "results.jsonl"
ARTIFACTS = ROOT / "tools" / "out" / "agent-benchmark"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def slug(value: str) -> str:
    return value.lower().replace("gpt-5.6-", "").replace("-", "")


def repeat_run_id(label: str, stage: str, repeat: int, route: dict[str, str]) -> str:
    return (
        f"{label}-{stage}-r{repeat:02d}-{route['effort']}-{slug(route['model'])}-"
        f"{slug(route['task'])}"
    )


def validate_plan(plan: dict[str, Any], freeze: dict[str, Any], plan_path: Path) -> None:
    errors = []
    if plan.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if plan.get("source_matrix_label") != freeze.get("run_label"):
        errors.append("source_matrix_label does not match freeze")
    expected_freeze_hash = str(plan.get("freeze_sha256"))
    observed_freeze_hash = hashlib.sha256(FREEZE.read_bytes()).hexdigest()
    if expected_freeze_hash != observed_freeze_hash:
        errors.append(
            f"freeze_sha256 mismatch: expected {expected_freeze_hash}, observed {observed_freeze_hash}"
        )
    if not isinstance(plan.get("run_label"), str) or not plan["run_label"]:
        errors.append("run_label must be a nonempty string")
    stages = plan.get("stages")
    if not isinstance(stages, dict) or not stages:
        errors.append("stages must be a nonempty object")
    tasks = set(str(task) for task in freeze["execution_order"]["task_blocks"])
    models = set(str(model) for model in freeze["models"])
    efforts = set(str(effort) for effort in freeze["documented_efforts"])
    efforts.update(str(effort) for effort in freeze["runtime_verified_efforts"])
    seen_run_ids = set()
    if isinstance(stages, dict):
        for stage_name, stage in stages.items():
            if not isinstance(stage, dict):
                errors.append(f"{stage_name}: stage must be an object")
                continue
            repeats = stage.get("repeats")
            routes = stage.get("routes")
            if not isinstance(repeats, list) or not repeats or any(
                not isinstance(repeat, int) or repeat < 2 for repeat in repeats
            ):
                errors.append(f"{stage_name}: repeats must be unique integers >= 2")
                continue
            if len(repeats) != len(set(repeats)):
                errors.append(f"{stage_name}: duplicate repeat numbers")
            if not isinstance(routes, list) or not routes:
                errors.append(f"{stage_name}: routes must be a nonempty array")
                continue
            route_keys = set()
            for route in routes:
                if not isinstance(route, dict):
                    errors.append(f"{stage_name}: route must be an object")
                    continue
                key = (str(route.get("task")), str(route.get("model")), str(route.get("effort")))
                if key[0] not in tasks or key[1] not in models or key[2] not in efforts:
                    errors.append(f"{stage_name}: invalid route {key}")
                if key in route_keys:
                    errors.append(f"{stage_name}: duplicate route {key}")
                route_keys.add(key)
                for repeat in repeats:
                    run_id = repeat_run_id(str(plan.get("run_label")), stage_name, repeat, route)
                    if run_id in seen_run_ids:
                        errors.append(f"duplicate planned run id: {run_id}")
                    seen_run_ids.add(run_id)
    if errors:
        raise SystemExit(f"repeat plan verification failed ({plan_path}):\n- " + "\n- ".join(errors))


def planned_cells(plan: dict[str, Any], stage_name: str) -> list[dict[str, Any]]:
    stage = plan["stages"][stage_name]
    label = str(plan["run_label"])
    cells = []
    for repeat in stage["repeats"]:
        sweep = []
        for route in stage["routes"]:
            cell = {
                "stage": stage_name,
                "repeat": int(repeat),
                "task": str(route["task"]),
                "model": str(route["model"]),
                "effort": str(route["effort"]),
            }
            cell["run_id"] = repeat_run_id(label, stage_name, int(repeat), cell)
            sweep.append(cell)
        sweep.sort(key=lambda cell: hashlib.sha256(
            f"{label}|{stage_name}|{repeat}|{cell['task']}|{cell['model']}|{cell['effort']}".encode()
        ).hexdigest())
        cells.extend(sweep)
    return cells


def execute_cell(freeze: dict[str, Any], plan: dict[str, Any], cell: dict[str, Any]) -> None:
    label = str(plan["run_label"])
    settings = freeze["settings"]
    command = [
        sys.executable, str(BENCHMARK), "run", str(cell["task"]),
        "--ref", str(freeze["baseline_commit"]),
        "--run-id", str(cell["run_id"]),
        "--run-label", label,
        "--model", str(cell["model"]),
        "--worker", str(settings["worker_override"]),
        "--effort", str(cell["effort"]),
        "--prompt-mode", str(settings["prompt_mode"]),
        "--handoff-mode", str(settings["handoff_mode"]),
        "--inspection-mode", str(settings["inspection_mode"]),
    ]
    if settings["run_p2p"]:
        command.append("--run-p2p")
    if cell["task"] == "WBD-005" and settings["wbd_005_include_held_out"]:
        command.append("--include-held-out")
    print(json.dumps({"event": "repeat-start", **cell}, sort_keys=True), flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    result_path = ARTIFACTS / str(cell["run_id"]) / "result.json"
    if completed.returncode != 0 or not result_path.exists():
        raise SystemExit(
            f"benchmark infrastructure failure for {cell['run_id']}: "
            f"exit={completed.returncode}, result={result_path.exists()}"
        )
    result = read_json(result_path)
    run_matrix.import_metrics(label)
    print(json.dumps({
        "event": "repeat-complete", **cell,
        "capability_pass": bool(result.get("capability_pass")),
        "score": (result.get("grade") or {}).get("score"),
        "total_duration_ms": result.get("total_duration_ms"),
        "worker_duration_ms": (result.get("execution") or {}).get("duration_ms"),
        "effective_tokens": result.get("effective_tokens"),
        "failure_phase": result.get("failure_phase"),
    }, sort_keys=True), flush=True)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    command.add_argument("--stage", required=True)
    command.add_argument("--max-cells", type=int)
    command.add_argument("--dry-run", action="store_true")
    return command


def main() -> int:
    args = parser().parse_args()
    freeze = read_json(FREEZE)
    run_matrix.verify_freeze(freeze)
    plan = read_json(args.plan)
    validate_plan(plan, freeze, args.plan)
    if args.stage not in plan["stages"]:
        raise SystemExit(f"unknown repeat stage: {args.stage}")
    cells = planned_cells(plan, args.stage)
    results = run_matrix.read_results()
    pending_all = [cell for cell in cells if cell["run_id"] not in results]
    pending = pending_all
    if args.max_cells is not None:
        if args.max_cells < 0:
            raise SystemExit("--max-cells must be nonnegative")
        pending = pending[:args.max_cells]
    print(json.dumps({
        "event": "repeat-plan",
        "run_label": plan["run_label"],
        "stage": args.stage,
        "total_cells": len(cells),
        "completed_cells": len(cells) - len(pending_all),
        "pending_cells": len(pending),
        "dry_run": args.dry_run,
        "run_ids": [cell["run_id"] for cell in pending],
    }, sort_keys=True), flush=True)
    if args.dry_run:
        return 0
    for cell in pending:
        artifact = ARTIFACTS / str(cell["run_id"])
        if artifact.exists():
            raise SystemExit(f"pending repeat has an existing incomplete artifact: {artifact}")
        execute_cell(freeze, plan, cell)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

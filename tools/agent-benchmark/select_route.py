#!/usr/bin/env python3
"""Validate and query the evidence-backed benchmark routing policy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_POLICY = HERE / "routing-policy.json"
ALLOWED_MODELS = {"gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"}
ALLOWED_EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
ALLOWED_CONFIDENCE = {"high-confidence", "qualified", "provisional", "insufficient"}
ALLOWED_OBJECTIVES = {"runtime", "effective_tokens", "reliability"}


def load_policy(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("policy must be a JSON object")
    return value


def validate_policy(policy: dict[str, Any]) -> dict[str, Any]:
    errors = []
    if policy.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(policy.get("policy_version"), str) or not policy.get("policy_version"):
        errors.append("policy_version must be a nonempty string")
    source = policy.get("source")
    if not isinstance(source, dict) or not all(
        isinstance(source.get(key), str) and source.get(key)
        for key in ("matrix_run_label", "repeat_run_label", "repeat_summary_sha256")
    ):
        errors.append("source must identify both run labels and the repeat summary SHA-256")
    classes = policy.get("task_classes")
    if not isinstance(classes, list) or not classes:
        errors.append("task_classes must be a nonempty array")
        classes = []
    seen_tasks = set()
    seen_classes = set()
    for index, item in enumerate(classes):
        prefix = f"task_classes[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        task_id = item.get("task_id")
        capability_class = item.get("capability_class")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"{prefix}.task_id must be nonempty")
        elif task_id in seen_tasks:
            errors.append(f"duplicate task_id: {task_id}")
        else:
            seen_tasks.add(task_id)
        if not isinstance(capability_class, str) or not capability_class:
            errors.append(f"{prefix}.capability_class must be nonempty")
        elif capability_class in seen_classes:
            errors.append(f"duplicate capability_class: {capability_class}")
        else:
            seen_classes.add(capability_class)
        routes = item.get("routes")
        if not isinstance(routes, list) or not routes:
            errors.append(f"{prefix}.routes must be a nonempty array")
            routes = []
        route_ids = set()
        for route_index, route in enumerate(routes):
            route_prefix = f"{prefix}.routes[{route_index}]"
            if not isinstance(route, dict):
                errors.append(f"{route_prefix} must be an object")
                continue
            route_id = route.get("route_id")
            if not isinstance(route_id, str) or not route_id:
                errors.append(f"{route_prefix}.route_id must be nonempty")
            elif route_id in route_ids:
                errors.append(f"{prefix} duplicate route_id: {route_id}")
            else:
                route_ids.add(route_id)
            if route.get("model") not in ALLOWED_MODELS:
                errors.append(f"{route_prefix}.model is unsupported")
            if route.get("effort") not in ALLOWED_EFFORTS:
                errors.append(f"{route_prefix}.effort is unsupported")
            if route.get("confidence") not in ALLOWED_CONFIDENCE:
                errors.append(f"{route_prefix}.confidence is unsupported")
            evidence = route.get("evidence")
            if not isinstance(evidence, dict) or not all(
                isinstance(evidence.get(key), int) and evidence.get(key) >= 0
                for key in ("attempts", "full_quality_passes")
            ):
                errors.append(f"{route_prefix}.evidence needs nonnegative integer counts")
            elif evidence["full_quality_passes"] > evidence["attempts"]:
                errors.append(f"{route_prefix}.evidence passes exceed attempts")
        selection = item.get("selection")
        if not isinstance(selection, dict) or set(selection) != ALLOWED_OBJECTIVES:
            errors.append(f"{prefix}.selection must define exactly {sorted(ALLOWED_OBJECTIVES)}")
        elif any(route_id not in route_ids for route_id in selection.values()):
            errors.append(f"{prefix}.selection references an unknown route")
        validation = item.get("validation")
        if not isinstance(validation, dict) or not isinstance(validation.get("required"), bool):
            errors.append(f"{prefix}.validation.required must be boolean")
        chain = item.get("fallback_chain")
        if not isinstance(chain, list):
            errors.append(f"{prefix}.fallback_chain must be an array")
        else:
            for step_index, step in enumerate(chain):
                if not isinstance(step, dict):
                    errors.append(f"{prefix}.fallback_chain[{step_index}] must be an object")
                elif "route_id" in step and step["route_id"] not in route_ids:
                    errors.append(
                        f"{prefix}.fallback_chain[{step_index}] references an unknown route"
                    )
        if not isinstance(item.get("standalone_qualified"), bool):
            errors.append(f"{prefix}.standalone_qualified must be boolean")
    if errors:
        raise ValueError("routing policy validation failed:\n- " + "\n- ".join(errors))
    return {
        "status": "pass",
        "schema_version": policy["schema_version"],
        "policy_version": policy["policy_version"],
        "task_classes": len(classes),
    }


def select(
    policy: dict[str, Any], task_id: str | None, capability_class: str | None, objective: str
) -> dict[str, Any]:
    matches = [
        item for item in policy["task_classes"]
        if (task_id is not None and item["task_id"] == task_id)
        or (capability_class is not None and item["capability_class"] == capability_class)
    ]
    if len(matches) != 1:
        key = task_id if task_id is not None else capability_class
        raise ValueError(f"expected one policy match for {key!r}, found {len(matches)}")
    item = matches[0]
    route_id = item["selection"][objective]
    route = next(route for route in item["routes"] if route["route_id"] == route_id)
    return {
        "policy_version": policy["policy_version"],
        "task_id": item["task_id"],
        "capability_class": item["capability_class"],
        "objective": objective,
        "selected_route": route,
        "validation": item["validation"],
        "fallback_chain": item["fallback_chain"],
        "scope_note": item["scope_note"],
    }


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    lookup = command.add_mutually_exclusive_group()
    lookup.add_argument("--task")
    lookup.add_argument("--capability-class")
    command.add_argument("--objective", choices=sorted(ALLOWED_OBJECTIVES), default="runtime")
    command.add_argument("--validate", action="store_true")
    return command


def main() -> int:
    args = parser().parse_args()
    policy = load_policy(args.policy)
    validation = validate_policy(policy)
    if args.validate and args.task is None and args.capability_class is None:
        print(json.dumps(validation, indent=2, sort_keys=True))
        return 0
    if args.task is None and args.capability_class is None:
        raise SystemExit("select a --task or --capability-class, or use --validate")
    result = select(policy, args.task, args.capability_class, args.objective)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

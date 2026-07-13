#!/usr/bin/env python3
"""Validate and query the evidence-backed benchmark routing policy."""

from __future__ import annotations

import argparse
import hashlib
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


def validate_policy(
    policy: dict[str, Any], policy_path: Path = DEFAULT_POLICY
) -> dict[str, Any]:
    errors = []
    summary: dict[str, Any] | None = None
    if policy.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(policy.get("policy_version"), str) or not policy.get("policy_version"):
        errors.append("policy_version must be a nonempty string")
    source = policy.get("source")
    if not isinstance(source, dict) or not all(
        isinstance(source.get(key), str) and source.get(key)
        for key in (
            "matrix_run_label",
            "repeat_run_label",
            "repeat_summary_path",
            "repeat_summary_sha256",
        )
    ):
        errors.append("source must identify both run labels, the repeat summary, and its SHA-256")
    else:
        summary_path = Path(source["repeat_summary_path"])
        if summary_path.name != source["repeat_summary_path"]:
            errors.append("source.repeat_summary_path must be a filename beside the policy")
        else:
            policy_directory = policy_path.resolve().parent
            summary_file = policy_directory / summary_path
            try:
                resolved_summary = summary_file.resolve(strict=True)
                if resolved_summary.parent != policy_directory:
                    raise ValueError("source repeat summary must resolve beside the policy")
                if not resolved_summary.is_file():
                    raise ValueError("source repeat summary must be a regular file")
                summary_bytes = resolved_summary.read_bytes()
            except (OSError, ValueError) as error:
                errors.append(f"source repeat summary is unreadable: {error}")
            else:
                actual_sha256 = hashlib.sha256(summary_bytes).hexdigest()
                if actual_sha256 != source["repeat_summary_sha256"]:
                    errors.append(
                        "source repeat summary SHA-256 mismatch: "
                        f"expected {source['repeat_summary_sha256']}, got {actual_sha256}"
                    )
                try:
                    loaded_summary = json.loads(summary_bytes.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    errors.append(f"source repeat summary is unreadable: {error}")
                else:
                    if isinstance(loaded_summary, dict):
                        summary = loaded_summary
                    else:
                        errors.append("source repeat summary must be a JSON object")
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
            if not isinstance(route.get("model"), str) or route.get("model") not in ALLOWED_MODELS:
                errors.append(f"{route_prefix}.model is unsupported")
            if not isinstance(route.get("effort"), str) or route.get("effort") not in ALLOWED_EFFORTS:
                errors.append(f"{route_prefix}.effort is unsupported")
            if (
                not isinstance(route.get("confidence"), str)
                or route.get("confidence") not in ALLOWED_CONFIDENCE
            ):
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
        elif any(
            not isinstance(route_id, str) or route_id not in route_ids
            for route_id in selection.values()
        ):
            errors.append(f"{prefix}.selection references an unknown route")
        validation = item.get("validation")
        if not isinstance(validation, dict) or validation.get("required") is not True:
            errors.append(f"{prefix}.validation.required must be true")
        else:
            commands = validation.get("commands")
            if (
                not isinstance(commands, list)
                or not commands
                or any(
                    not isinstance(command, list)
                    or not command
                    or any(not isinstance(part, str) or not part for part in command)
                    for command in commands
                )
            ):
                errors.append(f"{prefix}.validation.commands must be nonempty argv arrays")
        chain = item.get("fallback_chain")
        if not isinstance(chain, list) or not chain:
            errors.append(f"{prefix}.fallback_chain must be a nonempty array")
        else:
            fallback_route_ids = []
            for step_index, step in enumerate(chain):
                step_prefix = f"{prefix}.fallback_chain[{step_index}]"
                if not isinstance(step, dict):
                    errors.append(f"{step_prefix} must be an object")
                    continue
                if not isinstance(step.get("on"), str) or not step.get("on"):
                    errors.append(f"{step_prefix}.on must be nonempty")
                has_route = "route_id" in step
                has_action = "action" in step
                if has_route == has_action:
                    errors.append(f"{step_prefix} must define exactly one route_id or action")
                elif has_route and (
                    not isinstance(step["route_id"], str)
                    or step["route_id"] not in route_ids
                ):
                    errors.append(
                        f"{step_prefix} references an unknown route"
                    )
                elif has_route:
                    fallback_route_ids.append(step["route_id"])
                    if not isinstance(step.get("max_attempts"), int) or isinstance(
                        step.get("max_attempts"), bool
                    ) or step["max_attempts"] <= 0:
                        errors.append(f"{step_prefix}.max_attempts must be a positive integer")
                elif not isinstance(step.get("action"), str) or not step.get("action"):
                    errors.append(f"{step_prefix}.action must be nonempty")
            if len(set(fallback_route_ids)) != len(fallback_route_ids):
                errors.append(f"{prefix}.fallback_chain repeats a route")
            if isinstance(selection, dict):
                for selected_route_id in set(selection.values()):
                    if not any(
                        step.get("route_id") != selected_route_id
                        for step in chain
                        if isinstance(step, dict)
                    ):
                        errors.append(
                            f"{prefix}.fallback_chain has no route-aware step for "
                            f"{selected_route_id}"
                        )
        if not isinstance(item.get("standalone_qualified"), bool):
            errors.append(f"{prefix}.standalone_qualified must be boolean")
    evidence_routes = 0
    if summary is not None and isinstance(source, dict):
        if summary.get("source_matrix_label") != source.get("matrix_run_label"):
            errors.append("source matrix run label does not match the repeat summary")
        if summary.get("run_label") != source.get("repeat_run_label"):
            errors.append("source repeat run label does not match the repeat summary")
        summary_tasks = summary.get("tasks")
        if not isinstance(summary_tasks, list):
            errors.append("source repeat summary tasks must be an array")
            summary_tasks = []
        summary_by_task = {
            item.get("task_id"): item
            for item in summary_tasks
            if isinstance(item, dict) and isinstance(item.get("task_id"), str)
        }
        if len(summary_by_task) != len(summary_tasks):
            errors.append("source repeat summary has invalid or duplicate task IDs")
        if set(summary_by_task) != seen_tasks:
            errors.append("policy task IDs must exactly match source repeat summary task IDs")
        evidence_map = {
            "attempts": "attempts",
            "full_quality_passes": "full_quality_passes",
            "wilson_95": "full_quality_pass_wilson_95",
            "smoothed_success_probability": "smoothed_full_quality_probability",
            "expected_total_ms_per_success": "retry_adjusted_expected_total_duration_ms",
            "expected_effective_tokens_per_success": (
                "retry_adjusted_expected_effective_tokens"
            ),
        }
        for index, item in enumerate(classes):
            if not isinstance(item, dict) or not isinstance(item.get("task_id"), str):
                continue
            prefix = f"task_classes[{index}]"
            summary_task = summary_by_task.get(item["task_id"])
            if not isinstance(summary_task, dict):
                errors.append(f"{prefix} is missing from the source repeat summary")
                continue
            stats = summary_task.get("route_stats")
            if not isinstance(stats, list):
                errors.append(f"{prefix} source route_stats must be an array")
                continue
            valid_stats = [stat for stat in stats if isinstance(stat, dict)]
            stat_keys = [
                (stat.get("model"), stat.get("effort"))
                for stat in valid_stats
                if isinstance(stat.get("model"), str)
                and isinstance(stat.get("effort"), str)
            ]
            if (
                len(valid_stats) != len(stats)
                or len(stat_keys) != len(valid_stats)
                or len(set(stat_keys)) != len(stat_keys)
            ):
                errors.append(f"{prefix} source route_stats must have unique object routes")
            stats_by_key = {
                (stat.get("model"), stat.get("effort")): stat
                for stat in valid_stats
                if isinstance(stat.get("model"), str)
                and isinstance(stat.get("effort"), str)
            }
            routes = item.get("routes") if isinstance(item.get("routes"), list) else []
            routes_by_id = {
                route.get("route_id"): route
                for route in routes
                if isinstance(route, dict) and isinstance(route.get("route_id"), str)
            }
            for route_index, route in enumerate(routes):
                if not isinstance(route, dict):
                    continue
                route_prefix = f"{prefix}.routes[{route_index}]"
                stat = stats_by_key.get((route.get("model"), route.get("effort")))
                if not isinstance(stat, dict):
                    errors.append(f"{route_prefix} is missing from source route_stats")
                    continue
                evidence_routes += 1
                if route.get("confidence") != stat.get("confidence"):
                    errors.append(f"{route_prefix}.confidence differs from source evidence")
                evidence = route.get("evidence")
                if not isinstance(evidence, dict):
                    continue
                for policy_key, summary_key in evidence_map.items():
                    if evidence.get(policy_key) != stat.get(summary_key):
                        errors.append(
                            f"{route_prefix}.evidence.{policy_key} differs from source evidence"
                        )
            pareto = summary_task.get("reliability_qualified_pareto")
            selection = item.get("selection")
            if not isinstance(pareto, list) or not pareto:
                errors.append(f"{prefix} source reliability-qualified Pareto set is empty")
                continue
            pareto_keys = [
                (candidate.get("model"), candidate.get("effort"))
                for candidate in pareto
                if isinstance(candidate, dict)
                and isinstance(candidate.get("model"), str)
                and isinstance(candidate.get("effort"), str)
            ]
            if len(pareto_keys) != len(pareto) or len(set(pareto_keys)) != len(pareto_keys):
                errors.append(f"{prefix} source Pareto set must have unique object routes")
                continue
            if not isinstance(selection, dict):
                continue
            metric_by_objective = {
                "runtime": "retry_adjusted_expected_total_duration_ms",
                "effective_tokens": "retry_adjusted_expected_effective_tokens",
            }
            for objective, metric in metric_by_objective.items():
                values = [candidate.get(metric) for candidate in pareto]
                if not values or any(not isinstance(value, (int, float)) for value in values):
                    errors.append(f"{prefix} source Pareto metrics are invalid")
                    break
                best_value = min(values)
                best_keys = {
                    (candidate.get("model"), candidate.get("effort"))
                    for candidate in pareto
                    if candidate.get(metric) == best_value
                }
                selected = routes_by_id.get(selection.get(objective))
                selected_key = (
                    (selected.get("model"), selected.get("effort"))
                    if isinstance(selected, dict)
                    else None
                )
                if selected_key not in best_keys:
                    errors.append(
                        f"{prefix}.selection.{objective} is not source-Pareto optimal"
                    )
            reliability_candidates = pareto
            for metric, direction in (
                ("full_quality_pass_wilson_95", "max-lower-bound"),
                ("smoothed-full-quality-probability", "max-derived"),
                ("retry_adjusted_expected_total_duration_ms", "min"),
            ):
                values = []
                for candidate in reliability_candidates:
                    if direction == "max-derived":
                        attempts = candidate.get("attempts")
                        passes = candidate.get("full_quality_passes")
                        value = (
                            (passes + 1) / (attempts + 2)
                            if isinstance(attempts, int)
                            and attempts >= 0
                            and isinstance(passes, int)
                            and 0 <= passes <= attempts
                            else None
                        )
                    else:
                        value = candidate.get(metric)
                    if direction == "max-lower-bound":
                        value = value[0] if isinstance(value, list) and value else None
                    values.append(value)
                if not values or any(not isinstance(value, (int, float)) for value in values):
                    errors.append(f"{prefix} source reliability metrics are invalid")
                    reliability_candidates = []
                    break
                best_value = min(values) if direction == "min" else max(values)
                reliability_candidates = [
                    candidate
                    for candidate, value in zip(reliability_candidates, values, strict=True)
                    if value == best_value
                ]
            reliability_keys = {
                (candidate.get("model"), candidate.get("effort"))
                for candidate in reliability_candidates
            }
            selected = routes_by_id.get(selection.get("reliability"))
            selected_key = (
                (selected.get("model"), selected.get("effort"))
                if isinstance(selected, dict)
                else None
            )
            if selected_key not in reliability_keys:
                errors.append(f"{prefix}.selection.reliability is not source-Pareto optimal")
    if errors:
        raise ValueError("routing policy validation failed:\n- " + "\n- ".join(errors))
    return {
        "status": "pass",
        "schema_version": policy["schema_version"],
        "policy_version": policy["policy_version"],
        "task_classes": len(classes),
        "evidence_routes": evidence_routes,
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
    fallback_chain = [
        step for step in item["fallback_chain"]
        if step.get("route_id") != route_id
    ]
    return {
        "policy_version": policy["policy_version"],
        "task_id": item["task_id"],
        "capability_class": item["capability_class"],
        "objective": objective,
        "selected_route": route,
        "validation": item["validation"],
        "fallback_chain": fallback_chain,
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
    validation = validate_policy(policy, args.policy)
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

#!/usr/bin/env python3
"""Validate matched repeats and summarize reliability-adjusted route evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import analyze_results
import run_repeats

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.jsonl"
FREEZE = HERE / "gpt56-full-20260713.freeze.json"
DEFAULT_PLAN = HERE / "gpt56-repeat-20260714.plan.json"


def load_rows() -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(RESULTS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"expected object at results line {line_number}")
        rows.append(row)
    return rows


def rounded_median(values: Iterable[int]) -> int | float | None:
    items = list(values)
    if not items:
        return None
    value = statistics.median(items)
    return int(value) if float(value).is_integer() else round(float(value), 2)


def score(row: dict[str, Any]) -> int:
    return int(row["grade"]["score"])


def full_quality(row: dict[str, Any]) -> bool:
    return row.get("capability_pass") is True and score(row) == 100


def wilson_interval(successes: int, attempts: int, z: float = 1.959963984540054) -> list[float]:
    if attempts == 0:
        return [0.0, 1.0]
    proportion = successes / attempts
    denominator = 1 + z * z / attempts
    centre = proportion + z * z / (2 * attempts)
    margin = z * math.sqrt(proportion * (1 - proportion) / attempts + z * z / (4 * attempts * attempts))
    return [round((centre - margin) / denominator, 4), round((centre + margin) / denominator, 4)]


def planned_map(plan: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    by_id: dict[str, dict[str, Any]] = {}
    by_stage: dict[str, list[dict[str, Any]]] = {}
    for stage in plan["stages"]:
        cells = run_repeats.planned_cells(plan, stage)
        by_stage[stage] = cells
        for cell in cells:
            if cell["run_id"] in by_id:
                raise ValueError(f"duplicate planned run id: {cell['run_id']}")
            by_id[cell["run_id"]] = cell
    return by_id, by_stage


def validate(
    matrix_rows: list[dict[str, Any]],
    repeat_rows: list[dict[str, Any]],
    freeze: dict[str, Any],
    plan: dict[str, Any],
    plan_path: Path,
) -> dict[str, Any]:
    matrix_integrity = analyze_results.validate_grid(
        matrix_rows, freeze, str(plan["source_matrix_label"])
    )
    run_repeats.validate_plan(plan, freeze, plan_path)
    planned, by_stage = planned_map(plan)
    errors = []
    ids: dict[str, int] = defaultdict(int)
    for row in repeat_rows:
        run_id = str(row.get("run_id"))
        ids[run_id] += 1
        cell = planned.get(run_id)
        if cell is None:
            errors.append(f"unplanned repeat row: {run_id}")
            continue
        expected = {
            "task_id": cell["task"],
            "model": cell["model"],
            "effort": cell["effort"],
            "run_label": plan["run_label"],
            "repo_commit": freeze["baseline_commit"],
            "repo_ref": freeze["baseline_commit"],
            "grader_sha256": freeze["identities"]["grader_sha256"],
            "task_definition_sha256": freeze["tasks"][cell["task"]]["sha256"],
            "codex_cli": freeze["identities"]["codex_cli"],
            "runner_sha256": freeze["identities"]["matrix_runner_sha256"],
            "prompt_mode": freeze["settings"]["prompt_mode"],
            "handoff_mode": freeze["settings"]["handoff_mode"],
            "inspection_mode": freeze["settings"]["inspection_mode"],
            "run_p2p": freeze["settings"]["run_p2p"],
            "worker": freeze["settings"]["worker_override"],
        }
        mismatches = sorted(key for key, value in expected.items() if row.get(key) != value)
        if mismatches:
            errors.append(f"{run_id} identity mismatch: {mismatches}")
    duplicates = sorted(run_id for run_id, count in ids.items() if count != 1)
    if duplicates:
        errors.append(f"duplicate repeat run ids: {duplicates}")
    if errors:
        raise ValueError("; ".join(errors))
    completed = set(ids)
    stage_progress = []
    for stage, cells in by_stage.items():
        done = sum(cell["run_id"] in completed for cell in cells)
        stage_progress.append({
            "stage": stage,
            "purpose": plan["stages"][stage]["purpose"],
            "planned": len(cells),
            "completed": done,
            "pending": len(cells) - done,
        })
    return {
        "status": "pass",
        "matrix": matrix_integrity,
        "repeat_rows": len(repeat_rows),
        "unique_repeat_run_ids": len(ids),
        "planned_repeat_rows": len(planned),
        "stage_progress": stage_progress,
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
    }


def route_stat(
    key: tuple[str, str, str], rows: list[dict[str, Any]], planned_observations: int
) -> dict[str, Any]:
    task, model, effort = key
    passing = [row for row in rows if row.get("capability_pass") is True]
    quality = [row for row in rows if full_quality(row)]
    return {
        "task_id": task,
        "model": model,
        "effort": effort,
        "attempts": len(rows),
        "planned_observations": planned_observations,
        "capability_passes": len(passing),
        "capability_pass_rate": round(len(passing) / len(rows), 4),
        "capability_pass_wilson_95": wilson_interval(len(passing), len(rows)),
        "full_quality_passes": len(quality),
        "scores": [score(row) for row in rows],
        "median_total_duration_ms_full_quality": rounded_median(
            int(row["total_duration_ms"]) for row in quality
        ),
        "median_worker_duration_ms_full_quality": rounded_median(
            int(row["execution"]["duration_ms"]) for row in quality
        ),
        "median_effective_tokens_full_quality": rounded_median(
            int(row["effective_tokens"]) for row in quality
        ),
        "observations": [
            {
                "run_id": row["run_id"],
                "capability_pass": row.get("capability_pass") is True,
                "score": score(row),
                "total_duration_ms": row["total_duration_ms"],
                "effective_tokens": row["effective_tokens"],
            }
            for row in rows
        ],
    }


def pareto(stats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    qualified = [
        item for item in stats
        if item["attempts"] >= 3 and item["full_quality_passes"] == item["attempts"]
    ]
    frontier = []
    for item in qualified:
        duration = int(item["median_total_duration_ms_full_quality"])
        tokens = int(item["median_effective_tokens_full_quality"])
        dominated = any(
            other is not item
            and int(other["median_total_duration_ms_full_quality"]) <= duration
            and int(other["median_effective_tokens_full_quality"]) <= tokens
            and (
                int(other["median_total_duration_ms_full_quality"]) < duration
                or int(other["median_effective_tokens_full_quality"]) < tokens
            )
            for other in qualified
        )
        if not dominated:
            frontier.append(item)
    frontier.sort(key=lambda item: (
        int(item["median_total_duration_ms_full_quality"]),
        int(item["median_effective_tokens_full_quality"]),
    ))
    return [{
        "model": item["model"],
        "effort": item["effort"],
        "attempts": item["attempts"],
        "full_quality_passes": item["full_quality_passes"],
        "median_total_duration_ms": item["median_total_duration_ms_full_quality"],
        "median_effective_tokens": item["median_effective_tokens_full_quality"],
    } for item in frontier]


def analyze(
    all_rows: list[dict[str, Any]], freeze: dict[str, Any], plan: dict[str, Any], plan_path: Path
) -> dict[str, Any]:
    matrix_label = str(plan["source_matrix_label"])
    repeat_label = str(plan["run_label"])
    matrix_rows = [row for row in all_rows if row.get("run_label") == matrix_label]
    repeat_rows = [row for row in all_rows if row.get("run_label") == repeat_label]
    integrity = validate(matrix_rows, repeat_rows, freeze, plan, plan_path)
    planned, _ = planned_map(plan)
    planned_counts: dict[tuple[str, str, str], int] = defaultdict(lambda: 1)
    route_keys = set()
    for cell in planned.values():
        key = (str(cell["task"]), str(cell["model"]), str(cell["effort"]))
        route_keys.add(key)
        planned_counts[key] += 1
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in matrix_rows + repeat_rows:
        key = (str(row["task_id"]), str(row["model"]), str(row["effort"]))
        if key in route_keys:
            grouped[key].append(row)
    stats = [route_stat(key, grouped[key], planned_counts[key]) for key in sorted(route_keys)]
    tasks = []
    for task in sorted({key[0] for key in route_keys}):
        task_stats = [item for item in stats if item["task_id"] == task]
        tasks.append({
            "task_id": task,
            "route_stats": task_stats,
            "reliability_qualified_pareto": pareto(task_stats),
        })
    return {
        "schema_version": 1,
        "source_matrix_label": matrix_label,
        "run_label": repeat_label,
        "integrity": integrity,
        "totals": {
            "repeat_runs": len(repeat_rows),
            "repeat_capability_passes": sum(row.get("capability_pass") is True for row in repeat_rows),
            "repeat_total_duration_ms": sum(int(row["total_duration_ms"]) for row in repeat_rows),
            "repeat_worker_duration_ms": sum(int(row["execution"]["duration_ms"]) for row in repeat_rows),
            "repeat_effective_tokens": sum(int(row["effective_tokens"]) for row in repeat_rows),
            "monetary_cost_usd": None,
            "monetary_cost_note": "No frozen price table or billed-cost field is available; effective tokens are the cost proxy.",
        },
        "qualification_rule": (
            "A route enters the reliability-qualified Pareto set only after at least three observations "
            "and 100% full-quality passes; medians use full-quality observations only."
        ),
        "tasks": tasks,
    }


def markdown(report: dict[str, Any]) -> str:
    totals = report["totals"]
    lines = [
        f"# GPT-5.6 repeat summary — {report['run_label']}", "",
        "## Integrity and progress", "",
        f"- Repeat rows: {totals['repeat_runs']}; capability passes: "
        f"{totals['repeat_capability_passes']}/{totals['repeat_runs']}.",
        f"- Summed repeat time: {totals['repeat_total_duration_ms']:,} ms; "
        f"effective tokens: {totals['repeat_effective_tokens']:,}.",
        f"- {report['qualification_rule']}",
    ]
    for stage in report["integrity"]["stage_progress"]:
        lines.append(
            f"- {stage['stage']}: {stage['completed']}/{stage['planned']} complete "
            f"({stage['pending']} pending)."
        )
    lines.extend([
        "", "## Reliability-qualified Pareto routes", "",
        "| Task | Route | Full-quality passes | Median total ms | Median effective tokens |",
        "|---|---|---:|---:|---:|",
    ])
    for task in report["tasks"]:
        if not task["reliability_qualified_pareto"]:
            lines.append(f"| {task['task_id']} | none yet | — | — | — |")
        for item in task["reliability_qualified_pareto"]:
            lines.append(
                f"| {task['task_id']} | {item['model']}/{item['effort']} | "
                f"{item['full_quality_passes']}/{item['attempts']} | "
                f"{item['median_total_duration_ms']:,} | {item['median_effective_tokens']:,} |"
            )
    lines.extend([
        "", "## All planned route evidence", "",
        "| Task | Route | Complete | Passes | Pass rate | Wilson 95% | Median total ms | Median tokens |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ])
    for task in report["tasks"]:
        for item in task["route_stats"]:
            interval = item["capability_pass_wilson_95"]
            total = item["median_total_duration_ms_full_quality"]
            tokens = item["median_effective_tokens_full_quality"]
            lines.append(
                f"| {task['task_id']} | {item['model']}/{item['effort']} | "
                f"{item['attempts']}/{item['planned_observations']} | "
                f"{item['capability_passes']}/{item['attempts']} | "
                f"{item['capability_pass_rate']:.1%} | {interval[0]:.1%}–{interval[1]:.1%} | "
                f"{total if total is not None else '—'} | {tokens if tokens is not None else '—'} |"
            )
    lines.extend([
        "", "## Interpretation", "",
        "- Reliability is a gate, then median end-to-end time and effective tokens define the Pareto set.",
        "- Three observations are still a small sample; Wilson intervals are reported to keep uncertainty visible.",
        "- Monetary cost is unknown because the round did not freeze prices.", "",
    ])
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    command.add_argument("--json-output", type=Path)
    command.add_argument("--markdown-output", type=Path)
    return command


def main() -> int:
    args = parser().parse_args()
    freeze = analyze_results.load_json(FREEZE)
    plan = analyze_results.load_json(args.plan)
    report = analyze(load_rows(), freeze, plan, args.plan)
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        args.json_output.write_text(payload, encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.write_text(markdown(report), encoding="utf-8")
    if not args.json_output and not args.markdown_output:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

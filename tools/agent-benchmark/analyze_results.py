#!/usr/bin/env python3
"""Validate and summarize a frozen benchmark matrix from results.jsonl."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.jsonl"
FREEZE = HERE / "gpt56-full-20260713.freeze.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_rows(label: str) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(RESULTS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("run_label") == label:
            if not isinstance(row, dict):
                raise ValueError(f"expected object at results line {line_number}")
            rows.append(row)
    return rows


def rounded_median(values: Iterable[float | int]) -> float | int | None:
    items = list(values)
    if not items:
        return None
    value = statistics.median(items)
    return int(value) if float(value).is_integer() else round(float(value), 2)


def route(row: dict[str, Any]) -> dict[str, str]:
    return {"model": str(row["model"]), "effort": str(row["effort"])}


def score(row: dict[str, Any]) -> int:
    return int(row["grade"]["score"])


def full_quality_rows(task_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    passing = [row for row in task_rows if row.get("capability_pass") is True]
    if not passing:
        return []
    best_score = max(score(row) for row in passing)
    return [row for row in passing if score(row) == best_score]


def pareto(task_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = full_quality_rows(task_rows)
    frontier = []
    for row in candidates:
        dominated = any(
            other is not row
            and int(other["total_duration_ms"]) <= int(row["total_duration_ms"])
            and int(other["effective_tokens"]) <= int(row["effective_tokens"])
            and (
                int(other["total_duration_ms"]) < int(row["total_duration_ms"])
                or int(other["effective_tokens"]) < int(row["effective_tokens"])
            )
            for other in candidates
        )
        if not dominated:
            frontier.append(row)
    frontier.sort(key=lambda row: (int(row["total_duration_ms"]), int(row["effective_tokens"])))
    return frontier


def validate_grid(rows: list[dict[str, Any]], freeze: dict[str, Any], label: str) -> dict[str, Any]:
    if label != freeze["run_label"]:
        raise ValueError(f"freeze label is {freeze['run_label']}, not {label}")
    tasks = [str(task) for task in freeze["execution_order"]["task_blocks"]]
    models = [str(model) for model in freeze["models"]]
    efforts = [str(effort) for effort in freeze["documented_efforts"]]
    efforts.extend(str(effort) for effort in freeze["runtime_verified_efforts"])
    expected = {(task, model, effort) for task in tasks for model in models for effort in efforts}
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    run_ids: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[(str(row["task_id"]), str(row["model"]), str(row["effort"]))] += 1
        run_ids[str(row["run_id"])] += 1
    actual = set(counts)
    duplicate_cells = sorted([list(cell) + [count] for cell, count in counts.items() if count != 1])
    duplicate_run_ids = sorted(run_id for run_id, count in run_ids.items() if count != 1)
    missing = sorted([list(cell) for cell in expected - actual])
    extra = sorted([list(cell) for cell in actual - expected])
    errors = []
    if duplicate_cells:
        errors.append(f"duplicate cells: {duplicate_cells}")
    if duplicate_run_ids:
        errors.append(f"duplicate run ids: {duplicate_run_ids}")
    if missing:
        errors.append(f"missing cells: {missing}")
    if extra:
        errors.append(f"extra cells: {extra}")
    identities = freeze["identities"]
    probe_hash = str(identities["probe_runner_sha256"])
    matrix_hash = str(identities["matrix_runner_sha256"])
    runner_counts = {
        "probe": sum(row.get("runner_sha256") == probe_hash for row in rows),
        "matrix": sum(row.get("runner_sha256") == matrix_hash for row in rows),
    }
    unexpected_runners = sorted({
        str(row.get("runner_sha256")) for row in rows
        if row.get("runner_sha256") not in {probe_hash, matrix_hash}
    })
    if unexpected_runners:
        errors.append(f"unexpected runner hashes: {unexpected_runners}")
    expected_probe_cells = {("WBD-001", model, "ultra") for model in models}
    observed_probe_cells = {
        (str(row["task_id"]), str(row["model"]), str(row["effort"]))
        for row in rows if row.get("runner_sha256") == probe_hash
    }
    if observed_probe_cells != expected_probe_cells:
        errors.append(f"unexpected probe-runner cells: {sorted(observed_probe_cells)}")
    expected_settings = freeze["settings"]
    for row in rows:
        task = str(row["task_id"])
        identity_checks = {
            "repo_commit": row.get("repo_commit") == freeze["baseline_commit"],
            "repo_ref": row.get("repo_ref") == freeze["baseline_commit"],
            "grader_sha256": row.get("grader_sha256") == identities["grader_sha256"],
            "task_definition_sha256": (
                row.get("task_definition_sha256") == freeze["tasks"][task]["sha256"]
            ),
            "codex_cli": row.get("codex_cli") == identities["codex_cli"],
            "prompt_mode": row.get("prompt_mode") == expected_settings["prompt_mode"],
            "handoff_mode": row.get("handoff_mode") == expected_settings["handoff_mode"],
            "inspection_mode": row.get("inspection_mode") == expected_settings["inspection_mode"],
            "run_p2p": row.get("run_p2p") is expected_settings["run_p2p"],
            "worker": row.get("worker") == expected_settings["worker_override"],
        }
        failed = sorted(name for name, passed in identity_checks.items() if not passed)
        if failed:
            errors.append(f"{row['run_id']} identity mismatch: {failed}")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "status": "pass",
        "expected_cells": len(expected),
        "observed_cells": len(rows),
        "documented_cells": sum(row["effort"] != "ultra" for row in rows),
        "ultra_cells": sum(row["effort"] == "ultra" for row in rows),
        "runner_identity_counts": runner_counts,
    }


def aggregate(rows: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    task_best: dict[str, tuple[int, int]] = {}
    for task in sorted({str(row["task_id"]) for row in rows}):
        quality = full_quality_rows([row for row in rows if row["task_id"] == task])
        task_best[task] = (
            min(int(row["total_duration_ms"]) for row in quality),
            min(int(row["effective_tokens"]) for row in quality),
        )
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[field])].append(row)
    output = []
    for name, group in sorted(groups.items()):
        quality = []
        for row in group:
            task_rows = [item for item in rows if item["task_id"] == row["task_id"]]
            if row in full_quality_rows(task_rows):
                quality.append(row)
        latency_ratios = [
            int(row["total_duration_ms"]) / task_best[str(row["task_id"])][0] for row in quality
        ]
        token_ratios = [
            int(row["effective_tokens"]) / task_best[str(row["task_id"])][1] for row in quality
        ]
        output.append({
            field: name,
            "runs": len(group),
            "capability_passes": sum(row.get("capability_pass") is True for row in group),
            "full_quality_passes": len(quality),
            "mean_score": round(statistics.mean(score(row) for row in group), 2),
            "median_total_duration_ms_full_quality": rounded_median(
                int(row["total_duration_ms"]) for row in quality
            ),
            "median_effective_tokens_full_quality": rounded_median(
                int(row["effective_tokens"]) for row in quality
            ),
            "median_task_normalized_latency": round(float(rounded_median(latency_ratios) or 0), 3),
            "median_task_normalized_tokens": round(float(rounded_median(token_ratios) or 0), 3),
        })
    return output


def analyze(rows: list[dict[str, Any]], freeze: dict[str, Any], label: str) -> dict[str, Any]:
    integrity = validate_grid(rows, freeze, label)
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_task[str(row["task_id"])].append(row)
    tasks = []
    for task, task_rows in sorted(by_task.items()):
        frontier_rows = pareto(task_rows)
        frontier = []
        previous: dict[str, Any] | None = None
        for row in frontier_rows:
            item: dict[str, Any] = {
                **route(row),
                "run_id": row["run_id"],
                "score": score(row),
                "total_duration_ms": row["total_duration_ms"],
                "effective_tokens": row["effective_tokens"],
            }
            if previous is not None:
                seconds_added = (int(row["total_duration_ms"]) - int(previous["total_duration_ms"])) / 1000
                tokens_saved = int(previous["effective_tokens"]) - int(row["effective_tokens"])
                item["break_even_from_faster_route"] = {
                    "seconds_added": round(seconds_added, 3),
                    "effective_tokens_saved": tokens_saved,
                    "tokens_saved_per_second_added": round(tokens_saved / seconds_added, 2)
                    if seconds_added > 0 else None,
                }
            frontier.append(item)
            previous = row
        failures = []
        for row in task_rows:
            if row.get("capability_pass") is True:
                continue
            findings = [
                finding for finding in row["grade"].get("findings", [])
                if finding.startswith("failed:") or finding.startswith("p2p-failed:")
            ]
            failures.append({
                **route(row), "run_id": row["run_id"], "score": score(row),
                "failure_phase": row.get("failure_phase"), "findings": findings,
            })
        tasks.append({
            "task_id": task,
            "runs": len(task_rows),
            "capability_passes": sum(row.get("capability_pass") is True for row in task_rows),
            "best_passing_score": max(score(row) for row in task_rows if row.get("capability_pass") is True),
            "pareto_frontier": frontier,
            "failures": failures,
        })
    return {
        "schema_version": 1,
        "run_label": label,
        "integrity": integrity,
        "settings": {
            "baseline_commit": freeze["baseline_commit"],
            **freeze["settings"],
        },
        "totals": {
            "runs": len(rows),
            "capability_passes": sum(row.get("capability_pass") is True for row in rows),
            "mean_score": round(statistics.mean(score(row) for row in rows), 2),
            "total_duration_ms": sum(int(row["total_duration_ms"]) for row in rows),
            "worker_duration_ms": sum(int(row["execution"]["duration_ms"]) for row in rows),
            "effective_tokens": sum(int(row["effective_tokens"]) for row in rows),
            "input_tokens": sum(int(row["execution"]["usage"]["input_tokens"]) for row in rows),
            "cached_input_tokens": sum(int(row["execution"]["usage"]["cached_input_tokens"]) for row in rows),
            "output_tokens": sum(int(row["execution"]["usage"]["output_tokens"]) for row in rows),
            "reasoning_output_tokens": sum(
                int(row["execution"]["usage"]["reasoning_output_tokens"]) for row in rows
            ),
            "monetary_cost_usd": None,
            "monetary_cost_note": "No model price table or billed-cost field was frozen for this round.",
        },
        "by_model": aggregate(rows, "model"),
        "by_effort": aggregate(rows, "effort"),
        "tasks": tasks,
        "selection_caution": (
            "Each matrix cell has one observation. Pareto routes are repeat candidates, not final medians. "
            "The three dominated WBD-001 ultra probes used the frozen probe runner; the other 87 cells "
            "used the frozen matrix runner."
        ),
    }


def markdown(report: dict[str, Any]) -> str:
    totals = report["totals"]
    lines = [
        f"# GPT-5.6 matrix summary — {report['run_label']}", "",
        "## Integrity and totals", "",
        f"- Exact grid: {report['integrity']['observed_cells']} cells "
        f"({report['integrity']['documented_cells']} documented + "
        f"{report['integrity']['ultra_cells']} ultra).",
        f"- Runner identities: {report['integrity']['runner_identity_counts']['matrix']} matrix + "
        f"{report['integrity']['runner_identity_counts']['probe']} frozen probe cells.",
        f"- Capability passes: {totals['capability_passes']}/{totals['runs']}; "
        f"mean score: {totals['mean_score']}.",
        f"- Summed end-to-end time: {totals['total_duration_ms']:,} ms; "
        f"worker time: {totals['worker_duration_ms']:,} ms.",
        f"- Effective tokens: {totals['effective_tokens']:,}; monetary cost: unknown "
        "because no frozen price table was recorded.", "",
        "## Quality-first Pareto routes", "",
        "| Task | Route | Score | Total ms | Effective tokens | Tradeoff from faster route |",
        "|---|---|---:|---:|---:|---|",
    ]
    for task in report["tasks"]:
        for item in task["pareto_frontier"]:
            tradeoff = "fastest"
            if "break_even_from_faster_route" in item:
                value = item["break_even_from_faster_route"]
                tradeoff = (
                    f"+{value['seconds_added']} s, -{value['effective_tokens_saved']} tokens "
                    f"({value['tokens_saved_per_second_added']} tokens/s)"
                )
            lines.append(
                f"| {task['task_id']} | {item['model']}/{item['effort']} | {item['score']} | "
                f"{item['total_duration_ms']:,} | {item['effective_tokens']:,} | {tradeoff} |"
            )
    lines.extend(["", "## Aggregate by model", "", "| Model | Passes | Full quality | Mean score | "
                  "Normalized latency | Normalized tokens |", "|---|---:|---:|---:|---:|---:|"])
    for item in report["by_model"]:
        lines.append(
            f"| {item['model']} | {item['capability_passes']}/{item['runs']} | "
            f"{item['full_quality_passes']}/{item['runs']} | {item['mean_score']} | "
            f"{item['median_task_normalized_latency']}× | {item['median_task_normalized_tokens']}× |"
        )
    lines.extend(["", "## Aggregate by effort", "", "| Effort | Passes | Full quality | Mean score | "
                  "Normalized latency | Normalized tokens |", "|---|---:|---:|---:|---:|---:|"])
    for item in report["by_effort"]:
        lines.append(
            f"| {item['effort']} | {item['capability_passes']}/{item['runs']} | "
            f"{item['full_quality_passes']}/{item['runs']} | {item['mean_score']} | "
            f"{item['median_task_normalized_latency']}× | {item['median_task_normalized_tokens']}× |"
        )
    failures = [failure | {"task_id": task["task_id"]} for task in report["tasks"]
                for failure in task["failures"]]
    lines.extend(["", "## Capability failures", ""])
    if not failures:
        lines.append("None.")
    else:
        for failure in failures:
            findings = ", ".join(failure["findings"]) or failure["failure_phase"]
            lines.append(
                f"- {failure['task_id']} {failure['model']}/{failure['effort']}: "
                f"score {failure['score']}; {findings}."
            )
    lines.extend(["", "## Interpretation", "", f"- {report['selection_caution']}",
                  "- Aggregate latency/token ratios are normalized to each task's best full-quality cell; "
                  "raw medians across heterogeneous tasks are not used for routing.", ""])
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--run-label", default="gpt56-full-20260713")
    command.add_argument("--json-output", type=Path)
    command.add_argument("--markdown-output", type=Path)
    return command


def main() -> int:
    args = parser().parse_args()
    report = analyze(load_rows(args.run_label), load_json(FREEZE), args.run_label)
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

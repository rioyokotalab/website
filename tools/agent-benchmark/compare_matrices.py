#!/usr/bin/env python3
"""Compare two complete matched agent benchmark matrices."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.jsonl"


def rows_for(label: str) -> list[dict[str, Any]]:
    rows = [
        json.loads(line) for line in RESULTS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return [row for row in rows if row.get("run_label") == label]


def cell(row: dict[str, Any]) -> tuple[str, str, str]:
    return str(row["task_id"]), str(row["model"]), str(row["effort"])


def median(values: list[int]) -> int | None:
    return round(statistics.median(values)) if values else None


def full_quality(rows: list[dict[str, Any]]) -> set[str]:
    best: dict[str, int] = {}
    for row in rows:
        if row.get("capability_pass") is True:
            task = str(row["task_id"])
            best[task] = max(best.get(task, 0), int(row["grade"]["score"]))
    return {
        str(row["run_id"]) for row in rows
        if row.get("capability_pass") is True
        and int(row["grade"]["score"]) == best.get(str(row["task_id"]))
    }


def aggregates(rows: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    quality = full_quality(rows)
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[field])].append(row)
    return [
        {
            field: name,
            "full_quality": sum(str(row["run_id"]) in quality for row in group),
            "cells": len(group),
            "median_total_duration_ms": median([
                int(row["total_duration_ms"]) for row in group
                if str(row["run_id"]) in quality
            ]),
            "median_effective_tokens": median([
                int(row["effective_tokens"]) for row in group
                if str(row["run_id"]) in quality
            ]),
        }
        for name, group in sorted(groups.items())
    ]


def identity(rows: list[dict[str, Any]], field: str) -> list[str]:
    return sorted({str(row.get(field)) for row in rows})


def analyze(previous_label: str, current_label: str) -> dict[str, Any]:
    previous = rows_for(previous_label)
    current = rows_for(current_label)
    previous_by_cell = {cell(row): row for row in previous}
    current_by_cell = {cell(row): row for row in current}
    if len(previous_by_cell) != len(previous):
        raise ValueError(f"{previous_label} contains duplicate cells")
    if len(current_by_cell) != len(current):
        raise ValueError(f"{current_label} contains duplicate cells")
    if set(previous_by_cell) != set(current_by_cell):
        missing = sorted(set(previous_by_cell) - set(current_by_cell))
        extra = sorted(set(current_by_cell) - set(previous_by_cell))
        raise ValueError(f"matrices are not matched; missing={missing}, extra={extra}")

    deltas = []
    for key in sorted(previous_by_cell):
        old = previous_by_cell[key]
        new = current_by_cell[key]
        deltas.append({
            "task_id": key[0],
            "model": key[1],
            "effort": key[2],
            "score_delta": int(new["grade"]["score"]) - int(old["grade"]["score"]),
            "total_duration_delta_ms": (
                int(new["total_duration_ms"]) - int(old["total_duration_ms"])
            ),
            "effective_tokens_delta": (
                int(new["effective_tokens"]) - int(old["effective_tokens"])
            ),
            "previous_pass": old.get("capability_pass") is True,
            "current_pass": new.get("capability_pass") is True,
        })

    previous_quality = full_quality(previous)
    current_quality = full_quality(current)
    failure_phases = Counter(
        str(row.get("failure_phase")) for row in current
        if row.get("capability_pass") is not True
    )
    return {
        "schema_version": 1,
        "previous_label": previous_label,
        "current_label": current_label,
        "matched_cells": len(deltas),
        "identity": {
            "task_definition_sha256_equal": all(
                previous_by_cell[key].get("task_definition_sha256")
                == current_by_cell[key].get("task_definition_sha256")
                for key in previous_by_cell
            ),
            "previous_grader_sha256": identity(previous, "grader_sha256"),
            "current_grader_sha256": identity(current, "grader_sha256"),
            "previous_runner_sha256": identity(previous, "runner_sha256"),
            "current_runner_sha256": identity(current, "runner_sha256"),
            "previous_codex_cli": identity(previous, "codex_cli"),
            "current_codex_cli": identity(current, "codex_cli"),
            "previous_claude_cli": identity(previous, "claude_cli"),
            "current_claude_cli": identity(current, "claude_cli"),
        },
        "previous": {
            "full_quality": len(previous_quality),
            "capability_passes": sum(
                row.get("capability_pass") is True for row in previous
            ),
            "cells": len(previous),
            "by_model": aggregates(previous, "model"),
            "by_effort": aggregates(previous, "effort"),
        },
        "current": {
            "full_quality": len(current_quality),
            "capability_passes": sum(
                row.get("capability_pass") is True for row in current
            ),
            "cells": len(current),
            "by_model": aggregates(current, "model"),
            "by_effort": aggregates(current, "effort"),
            "failure_phases": dict(sorted(failure_phases.items())),
        },
        "matched_deltas": {
            "score_improved": sum(item["score_delta"] > 0 for item in deltas),
            "score_unchanged": sum(item["score_delta"] == 0 for item in deltas),
            "score_regressed": sum(item["score_delta"] < 0 for item in deltas),
            "pass_recovered": sum(
                not item["previous_pass"] and item["current_pass"] for item in deltas
            ),
            "pass_regressed": sum(
                item["previous_pass"] and not item["current_pass"] for item in deltas
            ),
            "median_total_duration_delta_ms": median([
                item["total_duration_delta_ms"] for item in deltas
            ]),
            "median_effective_tokens_delta": median([
                item["effective_tokens_delta"] for item in deltas
            ]),
        },
        "cells": deltas,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previous-label", required=True)
    parser.add_argument("--current-label", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = analyze(args.previous_label, args.current_label)
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

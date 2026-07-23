#!/usr/bin/env python3
"""Alternate frozen provider task blocks until complete or closeout cutoff."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "run_matrix.py"
DEFAULT_FREEZES = (
    HERE / "gpt56-nightly-20260723.freeze.json",
    HERE / "claude-nightly-20260723.freeze.json",
)
TASKS = tuple(f"WBD-{number:03d}" for number in range(1, 6))


def run_label(freeze: Path) -> str:
    return str(json.loads(freeze.read_text(encoding="utf-8"))["run_label"])


def result_count(label: str) -> int:
    path = HERE / "results.jsonl"
    if not path.exists():
        return 0
    return sum(
        json.loads(line).get("run_label") == label
        for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", type=Path, action="append", dest="freezes")
    parser.add_argument("--stop-before-epoch", type=float, required=True)
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    freezes = tuple(args.freezes or DEFAULT_FREEZES)
    schedule = [(task, freeze) for task in TASKS for freeze in freezes]
    print(json.dumps({
        "event": "nightly-plan",
        "stop_before_epoch": args.stop_before_epoch,
        "schedule": [
            {"task": task, "freeze": str(freeze), "run_label": run_label(freeze)}
            for task, freeze in schedule
        ],
        "plan": args.plan,
    }, sort_keys=True), flush=True)
    if args.plan:
        return 0

    for task, freeze in schedule:
        if time.time() >= args.stop_before_epoch:
            print(json.dumps({
                "event": "closeout-cutoff",
                "task": task,
                "run_label": run_label(freeze),
            }, sort_keys=True), flush=True)
            return 2
        label = run_label(freeze)
        before = result_count(label)
        print(json.dumps({
            "event": "block-start", "task": task, "run_label": label,
            "completed_before": before,
        }, sort_keys=True), flush=True)
        completed = subprocess.run([
            sys.executable, str(RUNNER), "--freeze", str(freeze), "--task", task,
        ], cwd=HERE.parents[1])
        after = result_count(label)
        print(json.dumps({
            "event": "block-complete", "task": task, "run_label": label,
            "completed_before": before, "completed_after": after,
            "runner_exit": completed.returncode,
        }, sort_keys=True), flush=True)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

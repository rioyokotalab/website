#!/usr/bin/env python3
"""Focused offline tests for generic frozen matrix orchestration."""

from __future__ import annotations

import unittest

import run_matrix


class MatrixTest(unittest.TestCase):
    def freeze(self) -> dict:
        return {
            "run_label": "test-label",
            "models": ["gpt-5.6-luna", "claude-sonnet-5"],
            "documented_efforts": ["low"],
            "runtime_verified_efforts": [],
            "execution_order": {
                "task_blocks": ["WBD-001"],
                "within_block": "listed",
            },
            "settings": {
                "prompt_mode": "full",
                "handoff_mode": "runner-lite",
                "inspection_mode": "default",
                "run_p2p": True,
            },
        }

    def test_provider_neutral_run_ids(self) -> None:
        self.assertEqual(
            run_matrix.run_id("nightly", "WBD-001", "gpt-5.6-luna", "low"),
            "nightly-low-luna-wbd001",
        )
        self.assertEqual(
            run_matrix.run_id("nightly", "WBD-001", "claude-sonnet-5", "low"),
            "nightly-low-sonnet-5-wbd001",
        )

    def test_listed_order_and_canonical_artifact_root(self) -> None:
        cells = run_matrix.frozen_cells(self.freeze(), "all", None)
        self.assertEqual(
            [cell["run_id"] for cell in cells],
            [
                "test-label-low-luna-wbd001",
                "test-label-low-sonnet-5-wbd001",
            ],
        )
        self.assertEqual(run_matrix.ARTIFACTS, run_matrix.HERE / "artifacts")

    def test_one_label_cannot_span_workflow_modes(self) -> None:
        rows = {
            "old": {
                "run_label": "test-label",
                "prompt_mode": "compact",
                "handoff_mode": "runner-lite",
                "inspection_mode": "default",
                "run_p2p": True,
            }
        }
        with self.assertRaises(SystemExit):
            run_matrix.validate_label_modes(self.freeze(), rows)


if __name__ == "__main__":
    unittest.main()

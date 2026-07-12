#!/usr/bin/env python3
"""Focused tests for standards-check helpers."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("standards-check.py")
SPEC = importlib.util.spec_from_file_location("standards_check", MODULE_PATH)
assert SPEC and SPEC.loader
STANDARDS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STANDARDS)


class PdfLinkCountsTest(unittest.TestCase):
    def test_attribute_order_is_semantic(self) -> None:
        for anchor in (
            '<a href="../../cv/cv.pdf" type="application/pdf" target="_blank">CV</a>',
            '<a href="../../cv/cv.pdf" target="_blank" type="application/pdf">CV</a>',
            "<a rel='noopener' type='application/pdf' href='../../cv/cv.pdf'>CV</a>",
        ):
            self.assertEqual(STANDARDS.pdf_link_counts(anchor), (1, 1))

    def test_missing_or_non_pdf_type_is_not_typed(self) -> None:
        self.assertEqual(STANDARDS.pdf_link_counts('<a href="cv.pdf">CV</a>'), (1, 0))
        self.assertEqual(STANDARDS.pdf_link_counts('<a type="text/plain" href="cv.pdf">CV</a>'), (1, 0))

    def test_non_pdf_anchor_is_ignored(self) -> None:
        self.assertEqual(STANDARDS.pdf_link_counts('<a href="index.html">Home</a>'), (0, 0))


if __name__ == "__main__":
    unittest.main()

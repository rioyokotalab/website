#!/usr/bin/env python3
"""Focused regression tests for the local public-link gate."""

from __future__ import annotations

import runpy
import tempfile
import unittest
from pathlib import Path

MODULE = runpy.run_path(str(Path(__file__).with_name("link-check.py")))
audit = MODULE["audit"]


class LinkCheckTests(unittest.TestCase):
    def test_valid_files_directories_fragments_and_same_origin_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "en" / "child").mkdir(parents=True)
            (root / "images").mkdir()
            (root / "js").mkdir()
            (root / "jp").mkdir()
            (root / "style.css").write_text(".x { background: url(images/pixel.png); }", encoding="utf-8")
            (root / "images" / "pixel.png").write_bytes(b"png")
            (root / "index.html").write_text(
                '<a href="/en/child/#target">child</a><a href="https://www.rio.scrc.iir.isct.ac.jp/en/child/">absolute</a>',
                encoding="utf-8",
            )
            (root / "en" / "child" / "index.html").write_text('<h1 id="target">Target</h1>', encoding="utf-8")
            checked, findings = audit(root)
            self.assertEqual(findings, [])
            self.assertEqual(checked, 3)

    def test_missing_public_file_fragment_and_css_asset_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ("en", "jp", "images", "js"):
                (root / directory).mkdir()
            (root / "index.html").write_text(
                '<a href="missing.html">missing</a><a href="#absent">fragment</a>', encoding="utf-8"
            )
            (root / "style.css").write_text(".x { background: url(images/missing.png); }", encoding="utf-8")
            checked, findings = audit(root)
            self.assertEqual(checked, 3)
            self.assertEqual(len(findings), 3)
            self.assertTrue(any("missing public target" in finding for finding in findings))
            self.assertTrue(any("missing fragment" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()

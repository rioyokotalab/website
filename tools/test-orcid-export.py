#!/usr/bin/env python3
"""Offline fixtures for Achievement-to-ORCID metadata guards."""
import importlib.util
import os
import re
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    'orcid_export', os.path.join(HERE, 'orcid-export.py'))
ORCID = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORCID)


class OrcidAchievementFixtures(unittest.TestCase):
    def test_explicit_titles_and_venues_override_heuristic_parse(self):
        guarded = []
        for section in ORCID.SECTION_TYPE:
            for row in ORCID.raw_items(section):
                text, data_title, data_venue = row[0], row[-2], row[-1]
                if data_title or data_venue:
                    parsed = ORCID.rm.parse(text)
                    fixed = ORCID.apply_explicit_metadata(
                        parsed, data_title=data_title, data_venue=data_venue,
                        data_authors=row[8], data_authors_en=row[9],
                        data_date=row[4])
                    self.assertIsNotNone(fixed, (section, text))
                    if data_title:
                        self.assertEqual(fixed[1], data_title, (section, text))
                    if data_venue:
                        self.assertEqual(fixed[2], data_venue, (section, text))
                    self.assertNotIn(fixed[1], fixed[0], (section, text))
                    guarded.append((section, text, data_title, data_venue,
                                    parsed, fixed))

        self.assertEqual(sum(bool(row[2]) for row in guarded), 11)
        self.assertEqual(sum(bool(row[3]) for row in guarded), 10)
        self.assertEqual(sum(bool(re.search(r'Rio\s+Yokota|横田\s*理央', row[1]))
                             for row in guarded), 9)

        tree = next(row for row in guarded
                    if 'FMM Tree Construction on GPUs' in row[1])
        self.assertEqual(tree[4][1], 'Ensemble')
        self.assertEqual(tree[5][1], 'FMM Tree Construction on GPUs')


if __name__ == '__main__':
    unittest.main()

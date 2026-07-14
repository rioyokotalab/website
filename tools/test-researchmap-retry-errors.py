#!/usr/bin/env python3
"""Offline fixtures for minimal ResearchMap error retries."""
import importlib.util
import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    'researchmap_retry', os.path.join(HERE, 'researchmap-retry-errors.py'))
RETRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RETRY)


def error(line, kind, record_id, field, language):
    return {
        RETRY.LINE: str(line),
        RETRY.IDENTIFIER: record_id,
        RETRY.KIND: kind,
        RETRY.STATUS: '400',
        RETRY.ERROR: ('required_value,Title(%s.%s),Title is required.' %
                      (field, language)),
    }


class RetryFixtures(unittest.TestCase):
    def test_only_failed_lines_gain_preserved_bilingual_titles(self):
        operations = [
            {
                'insert': {'type': 'misc'},
                'similar_merge': {
                    'paper_title': {'ja': '新規発表'},
                    'publication_date': '2025',
                },
                'priority': 'similar_data',
            },
            {
                'update': {'type': 'published_papers', 'id': 'paper-1'},
                'doc': {'authors': {'en': [{'name': 'Rio Yokota'}]}},
            },
        ]
        errors = [
            error(1, 'misc', '', 'paper_title', 'en'),
            error(2, 'published_papers', 'paper-1', 'paper_title', 'ja'),
        ]
        live = {
            'published_papers': {
                'paper-1': {'paper_title': {'en': 'Existing title'}},
            },
        }
        retry = RETRY.build_retry(errors, operations, live)
        self.assertEqual(len(retry), 2)
        self.assertEqual(retry[0]['similar_merge']['paper_title'], {
            'ja': '新規発表', 'en': '新規発表',
        })
        self.assertEqual(retry[1]['doc']['paper_title'], {
            'ja': 'Existing title', 'en': 'Existing title',
        })
        self.assertNotIn('paper_title', operations[1]['doc'])

    def test_unknown_error_is_refused(self):
        operations = [{
            'insert': {'type': 'misc'},
            'similar_merge': {'paper_title': {'ja': '発表'}},
            'priority': 'similar_data',
        }]
        row = error(1, 'misc', '', 'paper_title', 'en')
        row[RETRY.ERROR] = 'invalid_value,publication_date,bad date'
        with self.assertRaisesRegex(ValueError, 'unsupported error'):
            RETRY.build_retry([row], operations, {})

    def test_inventory_titles_and_explicit_override_are_reconstructed(self):
        errors = [
            error(1, 'misc', 'misc-1', 'paper_title', 'en'),
            error(2, 'books_etc', 'book-1', 'book_title', 'ja'),
        ]
        inventory = {
            'categories': {
                'sub001': {'entries': [{
                    'live_match': {
                        'type': 'misc',
                        'rm_id': 'misc-1',
                        'title': '日本語題名',
                    },
                }]},
            },
        }
        overrides = RETRY.parse_title_overrides([
            'books_etc:book-1:en:Exact English Title',
        ])
        live = RETRY.inventory_live_titles(errors, inventory, overrides)
        self.assertEqual(live['misc']['misc-1']['paper_title'], {
            'ja': '日本語題名',
        })
        self.assertEqual(live['books_etc']['book-1']['book_title'], {
            'en': 'Exact English Title',
        })

    def test_inventory_refuses_missing_title_evidence(self):
        errors = [error(1, 'misc', 'misc-1', 'paper_title', 'en')]
        with self.assertRaisesRegex(ValueError, 'inventory title missing'):
            RETRY.inventory_live_titles(errors, {'categories': {}})

        overrides = RETRY.parse_title_overrides([
            'misc:misc-1:en:Wrong language evidence',
        ])
        with self.assertRaisesRegex(ValueError, 'must provide existing ja'):
            RETRY.inventory_live_titles(
                errors, {'categories': {}}, overrides)


if __name__ == '__main__':
    unittest.main()

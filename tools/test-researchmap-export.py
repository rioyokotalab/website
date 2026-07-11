#!/usr/bin/env python3
"""Offline fixture tests for researchmap managed sync."""
import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    'researchmap_export', os.path.join(HERE, 'researchmap-export.py'))
RM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RM)


def insert(rm_type, doc):
    return {'insert': {'type': rm_type}, 'similar_merge': doc,
            'priority': 'similar_data'}


class SyncFixtures(unittest.TestCase):
    def setUp(self):
        self.paper_doc = {
            'paper_title': {'en': 'Website title'},
            'authors': {'en': [{'name': 'Rio Yokota'}, {'name': 'A. Student'}]},
            'publication_date': '2026-07',
            'publication_name': {'en': 'Current Journal'},
            'identifiers': {'doi': ['10.1000/RIGHT']},
            'see_also': [{'label': 'url', '@id': 'https://example.org/paper'}],
            'languages': ['eng'],
        }
        self.website = [
            ('paper citation', RM.key('Website title'), 'published_papers',
             insert('published_papers', self.paper_doc)),
            ('URL book', RM.key('URL book'), 'books_etc', insert('books_etc', {
                'book_title': {'en': 'URL book'},
                'authors': {'en': [{'name': 'Rio Yokota'}]},
                'publication_date': '2024-01',
                'publisher': {'en': 'Publisher'},
                'see_also': [{'label': 'url', '@id': 'https://books.example/x/' }],
            })),
            ('Ambiguous talk', RM.key('Ambiguous talk'), 'presentations',
             insert('presentations', {
                 'presentation_title': {'en': 'Ambiguous talk'},
                 'presenters': {'en': [{'name': 'Rio Yokota'}]},
                 'publication_date': '2025-03',
             })),
            ('New dated paper', RM.key('New dated paper'), 'published_papers',
             insert('published_papers', {
                 'paper_title': {'en': 'New dated paper'},
                 'authors': {'en': [{'name': 'Rio Yokota'}]},
                 'publication_date': '2026-08',
                 'publication_name': {'en': 'New Journal'},
             })),
        ]
        self.live = {
            'published_papers': [
                {  # DOI must win over the exact-title record below.
                    'rm:id': 'paper-doi',
                    'paper_title': {'en': 'Stale title'},
                    'authors': {'en': [{'name': 'Rio Yokota'}]},
                    'publication_date': '2026-07',
                    'publication_name': {'en': 'Old Journal'},
                    'identifiers': {'doi': ['https://doi.org/10.1000/right']},
                    'see_also': [{'label': 'url', '@id': 'https://example.org/paper'}],
                },
                {
                    'rm:id': 'title-only',
                    'paper_title': {'en': 'Website title'},
                    'authors': self.paper_doc['authors'],
                    'publication_date': '2026-07',
                    'publication_name': {'en': 'Current Journal'},
                },
                {'rm:id': 'managed-stale', 'paper_title': {'en': 'Removed paper'}},
                {'rm:id': 'unmanaged-stale', 'paper_title': {'en': 'Private paper'}},
            ],
            'books_etc': [{
                'rm:id': 'book-url',
                'book_title': {'en': 'Different live title'},
                'authors': {'en': [{'name': 'Rio Yokota'}]},
                'publication_date': '2024-01',
                'publisher': {'en': 'Publisher'},
                'see_also': [{'label': 'url', '@id': 'https://books.example/x'}],
            }],
            'presentations': [
                {'rm:id': 'talk-a', 'presentation_title': {'en': 'Ambiguous talk'},
                 'publication_date': '2025-03'},
                {'rm:id': 'talk-b', 'presentation_title': {'en': 'Ambiguous talk'},
                 'publication_date': '2025-03'},
            ],
            'misc': [{'rm:id': 'misc-unmanaged',
                      'paper_title': {'en': 'Unmanaged misc'}}],
        }
        self.managed = {
            'published_papers': ['paper-doi', 'managed-stale'],
            'books_etc': [],
            'presentations': ['talk-a'],
            'misc': [],
            'awards': ['must-never-delete'],
        }

    def test_partial_update_registry_delete_bounds_and_ambiguity(self):
        inserts, updates, deletes, refreshed, ambiguous = RM.build_sync(
            self.website, self.live, self.managed)

        self.assertEqual(len(inserts), 1)
        self.assertEqual(inserts[0][1]['similar_merge']['publication_date'],
                         '2026-08')
        self.assertEqual(len(updates), 2)  # DOI paper and URL-matched book title.
        paper_update = next(op for _text, op in updates
                            if op['update']['id'] == 'paper-doi')
        self.assertEqual(paper_update, {
            'update': {'type': 'published_papers', 'id': 'paper-doi'},
            'doc': {
                'paper_title': {'en': 'Website title'},
                'authors': self.paper_doc['authors'],
                'publication_name': {'en': 'Current Journal'},
            },
        })
        self.assertNotIn('identifiers', paper_update['doc'])
        self.assertNotIn('publication_date', paper_update['doc'])

        self.assertEqual(deletes, [
            {'delete': {'type': 'published_papers', 'id': 'managed-stale'}}
        ])
        serialized = '\n'.join(json.dumps(x) for x in
                               [r for _t, r in inserts] +
                               [r for _t, r in updates] + deletes)
        self.assertNotIn('unmanaged-stale', serialized)
        self.assertNotIn('misc-unmanaged', serialized)
        self.assertNotIn('must-never-delete', serialized)
        self.assertNotIn('talk-a', json.dumps(deletes))
        self.assertTrue(any(a[2] == 'title' and a[3] == ['talk-a', 'talk-b']
                            for a in ambiguous))
        self.assertIn('paper-doi', refreshed['published_papers'])
        self.assertIn('managed-stale', refreshed['published_papers'])

    def test_no_user_id_and_published_paper_date_required(self):
        inserts, updates, deletes, _refreshed, _ambiguous = RM.build_sync(
            self.website, self.live, self.managed)
        operations = ([record for _text, record in inserts] +
                      [record for _text, record in updates] + deletes)
        self.assertNotIn('user_id', json.dumps(operations))
        self.assertEqual(self.paper_doc['publication_date'], '2026-07')

        generated = RM.to_record(
            'Rio Yokota. Offline paper, Journal, 2026.',
            'published_papers', {'referee': True}, data_date='2026-07')
        self.assertEqual(generated['similar_merge']['publication_date'], '2026-07')


if __name__ == '__main__':
    unittest.main()

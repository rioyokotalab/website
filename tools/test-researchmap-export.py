#!/usr/bin/env python3
"""Offline fixture tests for researchmap managed sync."""
import importlib.util
import json
import os
import re
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
                'publisher': {'ja': 'Publisher', 'en': 'Publisher'},
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
        inserts, updates, deletes, refreshed, ambiguous, _classified = RM.build_sync(
            self.website, self.live, self.managed)

        self.assertEqual(len(inserts), 1)
        self.assertEqual(inserts[0][1]['merge']['publication_date'],
                         '2026-08')
        self.assertEqual(len(updates), 2)  # Additive paper/book field completion.
        paper_update = next(op for _text, op in updates
                            if op['update']['id'] == 'paper-doi')
        self.assertEqual(paper_update, {
            'update': {'type': 'published_papers', 'id': 'paper-doi'},
            'doc': {
                'languages': ['eng'],
                'paper_title': {'en': 'Stale title', 'ja': 'Stale title'},
            },
        })
        self.assertNotIn('identifiers', paper_update['doc'])
        self.assertNotIn('publication_date', paper_update['doc'])
        book_update = next(op for _text, op in updates
                           if op['update']['id'] == 'book-url')
        self.assertEqual(book_update['doc'], {
            'publisher': {'en': 'Publisher', 'ja': 'Publisher'},
            'book_title': {
                'en': 'Different live title',
                'ja': 'Different live title',
            },
        })

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

    def test_bulk_import_completes_required_title_languages(self):
        inserted = RM.to_record(
            '横田理央, 日本語タイトル, 研究会, 2025.',
            'misc', {}, data_date='2025')
        self.assertEqual(inserted['similar_merge']['paper_title'], {
            'ja': '日本語タイトル',
            'en': '日本語タイトル',
        })

        desired = {
            'paper_title': {'ja': 'ローカルの別表記'},
            'authors': {'ja': [{'name': '横田理央'}]},
        }
        live = {
            'paper_title': {'ja': '公開済みタイトル'},
            'authors': {},
        }
        changed = RM.changed_doc('misc', desired, live)
        self.assertEqual(changed['paper_title'], {
            'ja': '公開済みタイトル',
            'en': '公開済みタイトル',
        })

    def test_no_user_id_and_published_paper_date_required(self):
        inserts, updates, deletes, _refreshed, _ambiguous, _classified = RM.build_sync(
            self.website, self.live, self.managed)
        operations = ([record for _text, record in inserts] +
                      [record for _text, record in updates] + deletes)
        self.assertNotIn('user_id', json.dumps(operations))
        self.assertEqual(self.paper_doc['publication_date'], '2026-07')

        generated = RM.to_record(
            'Rio Yokota. Offline paper, Journal, 2026.',
            'published_papers', {'referee': True}, data_date='2026-07')
        self.assertEqual(generated['similar_merge']['publication_date'], '2026-07')

    def test_complete_fields_merge_without_degrading_live_metadata(self):
        desired = {
            'paper_title': {'ja': 'English title', 'en': 'English title'},
            'authors': {
                'ja': [{'name': 'Rio Yokota'}],
                'en': [{'name': 'Rio Yokota'}],
            },
            'publication_date': '2025',
            'identifiers': {
                'doi': ['10.1000/right'],
                'isbn': ['978-1-2345-6789-0'],
            },
            'see_also': [
                {'label': 'url', '@id': 'https://arxiv.org/abs/1234.5678'},
            ],
            'languages': ['eng'],
        }
        live = {
            'paper_title': {'ja': '日本語訳', 'en': 'English title'},
            'authors': {
                'ja': [{'name': '横田理央'}],
                'en': [{'name': 'Rio Yokota'}],
            },
            'publication_date': '2025-04-01',
            'identifiers': {
                'doi': ['https://doi.org/10.1000/RIGHT'],
                'issn': ['1234-5679'],
                'arxiv_id': ['1234.5678'],
                'orcid_put_cd': ['managed-value'],
            },
            'see_also': [
                {'label': 'url', '@id': 'https://example.org/project'},
                {'label': 'DBLP', '@id': 'https://dblp.example/managed'},
            ],
            'languages': ['jpn'],
        }
        changed = RM.changed_doc('published_papers', desired, live)
        self.assertNotIn('paper_title', changed)
        self.assertNotIn('authors', changed)
        self.assertNotIn('publication_date', changed)
        self.assertEqual(changed['identifiers']['doi'],
                         ['https://doi.org/10.1000/RIGHT'])
        self.assertEqual(changed['identifiers']['isbn'],
                         ['978-1-2345-6789-0'])
        self.assertEqual(changed['identifiers']['issn'], ['1234-5679'])
        self.assertNotIn('arxiv_id', changed['identifiers'])
        self.assertNotIn('orcid_put_cd', changed['identifiers'])
        self.assertEqual(len(changed['see_also']), 2)
        self.assertEqual({item['label'] for item in changed['see_also']},
                         {'url'})
        self.assertEqual(changed['languages'], ['jpn', 'eng'])

    def test_managed_nested_values_never_reenter_updates(self):
        desired = {
            'identifiers': {'doi': ['10.1000/new']},
            'see_also': [
                {'label': 'url', '@id': 'https://arxiv.org/abs/1234.5678'},
            ],
        }
        live = {
            'identifiers': {
                'orcid_put_cd': ['managed'],
                'rm:research_project_id': ['managed-project'],
                'wos_id': ['managed-wos'],
            },
            'see_also': [
                {'label': 'DBLP', '@id': 'https://dblp.example/managed'},
                {'label': 'arxiv', '@id': 'https://arxiv.org/abs/1234.5678'},
            ],
        }
        changed = RM.changed_doc('published_papers', desired, live)
        self.assertEqual(changed['identifiers'], {'doi': ['10.1000/new']})
        self.assertEqual(changed['see_also'], desired['see_also'])

    def test_research_project_link_label_uses_schema_plural(self):
        project = {
            'label': 'rm:research_projects',
            '@id': 'https://researchmap.jp/research_projects/example',
        }
        desired = {
            'see_also': [{'label': 'url', '@id': 'https://example.org/item'}],
        }
        for kind in ('published_papers', 'misc', 'books_etc', 'presentations'):
            self.assertIn('rm:research_projects',
                          RM.EDITABLE_SEE_ALSO_LABELS[kind])
            self.assertNotIn('rm:research_project',
                             RM.EDITABLE_SEE_ALSO_LABELS[kind])
            changed = RM.changed_doc(kind, desired, {'see_also': [project]})
            self.assertEqual(changed['see_also'], [project] + desired['see_also'])

        doi_link = {'label': 'doi', '@id': 'https://doi.org/10.1000/example'}
        self.assertIn('doi', RM.EDITABLE_SEE_ALSO_LABELS['misc'])
        changed = RM.changed_doc('misc', desired, {'see_also': [doi_link]})
        self.assertEqual(changed['see_also'], [doi_link] + desired['see_also'])

    def test_fuzzy_cross_type_and_translated_project_matching(self):
        website = [
            ('long paper', RM.key('A Long Paper Title for Matching'),
             'published_papers', insert('published_papers', {
                 'paper_title': {'en': 'A Long Paper Title for Matching'},
                 'publication_name': {'en': 'Example Conference'},
                 'publication_date': '2020-01',
             })),
            ('same event elsewhere', RM.key('A Distinct Long Presentation Title'),
             'misc', insert('misc', {
                 'paper_title': {'en': 'A Distinct Long Presentation Title'},
                 'publication_name': {'en': 'SIAM Annual Meeting'},
                 'publication_date': '2019-07',
             })),
        ]
        live = {
            'published_papers': [{
                'rm:id': 'fuzzy-paper',
                'paper_title': {
                    'en': 'A Long Paper Title for Matching (Proceedings version)'},
                'publication_name': {'en': 'Example Conference'},
                'publication_date': '2020-01-15',
            }],
            'misc': [],
            'presentations': [{
                'rm:id': 'cross-talk',
                'presentation_title': {
                    'en': 'A Distinct Long Presentation Title'},
                'event': {'en': 'SIAM Annual Meeting'},
                'publication_date': '2019-07-10',
            }],
        }
        inserts, _updates, _deletes, _refreshed, ambiguous, _classified = RM.build_sync(
            website, live, {})
        self.assertEqual(inserts, [])
        self.assertTrue(any(row[2] == 'cross-type date/venue match' and
                            row[3] == ['presentations:cross-talk']
                            for row in ambiguous), ambiguous)

        project = insert('research_projects', {
            'research_project_title': {'ja': 'ベイズ双対性に基づくAI'},
            'system_name': {'ja': 'CREST'},
            'from_date': '2021',
            'to_date': '2027',
        })
        item, candidates, criterion = RM.match_live(project, [{
            'rm:id': 'translated-project',
            'research_project_title': {'en': 'A New Bayes Duality Principle'},
            'system_name': {'en': 'CREST'},
            'from_date': '2021-10',
            'to_date': '2027-03',
        }])
        self.assertEqual(item['rm:id'], 'translated-project')
        self.assertEqual(candidates, [])
        self.assertEqual(criterion, 'project grant/date context')

    def test_fuzzy_title_requires_contributor_or_venue_context(self):
        record = insert('published_papers', {
            'paper_title': {'en': 'A Shared Long Paper Title for Matching'},
            'authors': {'en': [{'name': 'Rio Yokota'}, {'name': 'Alice'}]},
            'publication_name': {'en': 'Expected Conference'},
            'publication_date': '2024-11',
        })
        unrelated = {
            'rm:id': 'unrelated',
            'paper_title': {
                'en': 'A Shared Long Paper Title for Matching (Extended)'},
            'authors': {'en': [
                {'name': 'Rio Yokota'}, {'name': 'Bob'}, {'name': 'Carol'},
            ]},
            'publication_name': {'en': 'Different Conference'},
            'publication_date': '2024-11-15',
        }
        item, candidates, criterion = RM.match_live(record, [unrelated])
        self.assertIsNone(item)
        self.assertEqual(candidates, [])
        self.assertIsNone(criterion)

        corroborated = dict(unrelated)
        corroborated['rm:id'] = 'corroborated'
        corroborated['authors'] = record['similar_merge']['authors']
        item, candidates, criterion = RM.match_live(record, [corroborated])
        self.assertEqual(item['rm:id'], 'corroborated')
        self.assertEqual(candidates, [])
        self.assertEqual(criterion, 'title/date containment')

    def test_reviewed_match_override_actions_and_drift_guards(self):
        website = [
            ('match', RM.key('Reviewed journal version'), 'published_papers',
             insert('published_papers', {
                 'paper_title': {'en': 'Reviewed journal version'},
                 'publication_name': {'en': 'Example Journal'},
                 'publication_date': '2024-01',
             })),
            ('distinct', RM.key('Conference and journal title'),
             'published_papers', insert('published_papers', {
                 'paper_title': {'en': 'Conference and journal title'},
                 'publication_name': {'en': 'Example Workshop'},
                 'publication_date': '2023-01',
             })),
            ('equivalent', RM.key('Cross type example title'), 'misc',
             insert('misc', {
                 'paper_title': {'en': 'Cross type example title'},
                 'publication_name': {'en': 'Example Meeting'},
                 'publication_date': '2022-02',
             })),
            ('hold', RM.key('Held presentation'), 'presentations',
             insert('presentations', {
                 'presentation_title': {'en': 'Held presentation'},
                 'publication_date': '2021-03',
             })),
        ]
        live = {
            'published_papers': [
                {'rm:id': 'match-id',
                 'paper_title': {'en': 'Reviewed journal version'},
                 'publication_name': {'en': 'Example Journal'},
                 'publication_date': '2024-01'},
                {'rm:id': 'distinct-id',
                 'paper_title': {'en': 'Conference and journal title'},
                 'publication_name': {'en': 'Later Journal'},
                 'publication_date': '2024-01'},
            ],
            'misc': [],
            'presentations': [
                {'rm:id': 'cross-id',
                 'presentation_title': {'en': 'Cross type example title'},
                 'event': {'en': 'Example Meeting'},
                 'publication_date': '2022-02'},
                {'rm:id': 'hold-a',
                 'presentation_title': {'en': 'Held presentation'},
                 'publication_date': '2021-03'},
                {'rm:id': 'hold-b',
                 'presentation_title': {'en': 'Held presentation'},
                 'publication_date': '2021-03'},
            ],
        }
        overrides = {}
        for _text, title_key, kind, record in website:
            selector = RM.match_override_key(title_key, kind, record)
            if _text == 'match':
                overrides[selector] = {
                    'action': 'match',
                    'target': 'published_papers:match-id',
                    'candidates': ['published_papers:match-id'],
                    'reason': 'fixture match',
                }
            elif _text == 'distinct':
                overrides[selector] = {
                    'action': 'distinct',
                    'candidates': ['published_papers:distinct-id'],
                    'reason': 'fixture distinct',
                }
            elif _text == 'equivalent':
                overrides[selector] = {
                    'action': 'equivalent',
                    'target': 'presentations:cross-id',
                    'candidates': [],
                    'reason': 'fixture equivalent',
                }
            else:
                overrides[selector] = {
                    'action': 'hold',
                    'candidates': [
                        'presentations:hold-a', 'presentations:hold-b'],
                    'reason': 'fixture hold',
                }

        managed = {
            'presentations': ['cross-id', 'hold-a', 'hold-b'],
        }
        inserts, updates, deletes, _refreshed, ambiguous, classified = \
            RM.build_sync(website, live, managed, overrides)
        self.assertEqual([text for text, _record in inserts], ['distinct'])
        self.assertIn('force', inserts[0][1])
        self.assertNotIn('similar_merge', inserts[0][1])
        self.assertNotIn('priority', inserts[0][1])
        self.assertEqual(updates, [])
        self.assertEqual(deletes, [])
        self.assertEqual(ambiguous, [])
        self.assertEqual([row['action'] for row in classified],
                         ['match', 'distinct', 'equivalent', 'hold'])

        broken = {key: dict(value) for key, value in overrides.items()}
        match_selector = next(key for key, value in broken.items()
                              if value['action'] == 'match')
        broken[match_selector]['candidates'] = []
        with self.assertRaisesRegex(ValueError, 'candidate drift'):
            RM.build_sync(website, live, {}, broken)

    def test_reviewed_override_file_covers_current_website_selectors(self):
        overrides = RM.load_match_overrides()
        selectors = {
            RM.match_override_key(title_key, kind, record)
            for _text, title_key, kind, record in RM.website_records()
        }
        self.assertEqual(len(overrides), 30)
        self.assertTrue(set(overrides).issubset(selectors))
        self.assertEqual(
            {action: sum(value['action'] == action
                         for value in overrides.values())
             for action in ('match', 'equivalent', 'distinct', 'hold')},
            {'match': 12, 'equivalent': 5, 'distinct': 8, 'hold': 5})


class AchievementSourceFixtures(unittest.TestCase):
    def record_at(self, section, one_based_index):
        row = RM.entries(section)[one_based_index - 1]
        rm_type, extra = RM.SECTIONS[section]
        return RM.to_record(row[0], rm_type, extra, *row[1:])

    def test_current_id_heading_sections_parse(self):
        anchors = ['sub00%d' % n for n in range(1, 8)]
        counts = {anchor: len(RM.entries(anchor)) for anchor in anchors}
        self.assertTrue(all(counts.values()), counts)
        self.assertGreater(sum(counts.values()), 250)

    def test_legacy_name_anchor_is_still_supported(self):
        source = '<a name="sub001"></a><h3>Journals</h3><ol><li>One</li></ol>'
        self.assertEqual(RM.section_block(source, 'sub001'), '<li>One</li>')

    def test_visible_link_row_is_not_citation_text(self):
        fragment = (
            'Citation.<br><span class="achievement-links">'
            '<a href="https://arxiv.org/abs/1234.5678">[arxiv]</a> '
            '<a href="https://arxiv.org/bibtex/1234.5678">[bibtex]</a>'
            '</span></li>')
        cleaned = RM.strip_achievement_links(fragment)
        self.assertNotIn('[arxiv]', cleaned)
        self.assertNotIn('[bibtex]', cleaned)
        self.assertEqual(re.sub(r'</?br\s*/?>|</li>', '', cleaned), 'Citation.')

    def test_correct_identifier_location_and_profile_schemas(self):
        book = RM.to_record(
            'Rio Yokota, Sample Chapter, GPU Computing Gems, 2024.',
            'books_etc', {}, data_date='2024-01',
            data_doi='10.1000/example', data_isbn='978-1-2345-6789-0')
        self.assertEqual(book['similar_merge']['identifiers'], {
            'doi': ['10.1000/example'],
            'isbn': ['978-1-2345-6789-0'],
        })
        self.assertNotIn('isbn', book['similar_merge'])

        talk = RM.to_record(
            'Rio Yokota. Sample Talk, SIAM Conference, Mar. 2025.',
            'talk_or_misc', {'is_international_presentation': True},
            data_date='2025-03', data_doi='10.1000/not-a-talk-field',
            data_event='SIAM Conference',
            data_location='Denver', data_invited=True)
        self.assertEqual(talk['insert']['type'], 'presentations')
        self.assertEqual(talk['similar_merge']['location'],
                         {'ja': 'Denver', 'en': 'Denver'})
        self.assertEqual(talk['similar_merge']['presentation_type'],
                         'invited_oral_presentation')
        self.assertNotIn('identifiers', talk['similar_merge'])

        job = RM.parse_research_experience_line(
            '2025年4月― 理化学研究所 計算科学研究センター チームプリンシパル')
        self.assertIn('job', job)
        self.assertIn('section', job)
        self.assertNotIn('job_title', job)
        society = RM.parse_association_memberships(['情報処理学会'])[0]
        self.assertIn('academic_society_name', society)

        profiles = {(text, kind): doc
                    for text, kind, doc in RM.profile_records()}
        current_committee = next(doc for (text, kind), doc in profiles.items()
                                 if kind == 'committee_memberships' and
                                 text.startswith('2025 publicity chair'))
        self.assertEqual(current_committee['committee_name'],
                         {'en': 'publicity chair'})
        self.assertIn('association', current_committee)
        legacy_committee = next(doc for (text, kind), doc in profiles.items()
                                if kind == 'committee_memberships' and
                                text.startswith('2024 The IEEE / CVF'))
        self.assertEqual(
            legacy_committee['committee_name'],
            {'en': ('The IEEE / CVF Computer Vision and Pattern Recognition '
                    'Conference (CVPR 2024), reviewer')})
        self.assertNotIn('association', legacy_committee)

        project = next(doc for (text, kind), doc in profiles.items()
                       if kind == 'research_projects' and
                       '厚生労働科学研究費' in text)
        self.assertIn('（LLM:Large Language Model）',
                      project['research_project_title']['ja'])
        self.assertEqual(project['system_name'], {'ja': '厚生労働科学研究費'})
        self.assertEqual(project['category'], {'ja': '応用研究'})
        nested = next(doc for (text, kind), doc in profiles.items()
                      if kind == 'research_projects' and
                      '国際共同研究加速基金' in text)
        self.assertEqual(nested['system_name'], {'ja': '国際共同研究加速基金'})
        self.assertEqual(nested['category'], {'ja': '海外連携研究'})

    def test_explicit_title_overrides_guard_known_parser_failures(self):
        expected = {
            ('sub001', 21): '大規模境界要素法解析における分散並列 FMM の通信最適化',
            ('sub001', 33): 'FMM Tree Construction on GPUs',
            ('sub004', 61): ('Rich Information is Affordable: A Systematic '
                             'Performance Analysis of Second-order Optimization '
                             'Using K-FAC'),
            ('sub004', 62): 'Privacy Preserving Visual SLAM',
            ('sub004', 20): ('On the Interplay Between Precision, Rank, '
                             'Admissibility, and Iterative Refinement for '
                             'Hierarchical Low-Rank Matrix Solvers'),
            ('sub004', 63): ('Distributed Memory Task-Based Block Low Rank '
                             'Direct Solver'),
            ('sub004', 102): ('(Really) Fast Macromolecular Electrostatics -- '
                              'Fast Algorithms, Open Software and Accelerated '
                              'Computing'),
            ('sub005', 4): '画像超解像における学習データ構築の再考',
            ('sub005', 5): 'Scaling Backwards: Minimal Synthetic Pre-training?',
            ('sub007', 21): ('PEZY-SC3sプロセッサを用いたFull-state'
                             '量子回路シミュレーション'),
        }
        for (section, index), title in expected.items():
            doc = self.record_at(section, index)['similar_merge']
            title_field = ('paper_title' if 'paper_title' in doc
                           else 'presentation_title')
            self.assertIn(title, doc[title_field].values(),
                          (section, index, doc[title_field]))
            people = doc.get('authors') or doc.get('presenters') or {}
            names = {person['name'] for group in people.values()
                     for person in group}
            self.assertNotIn(title, names, (section, index, title))

    def test_complete_book_schema_and_isbn_equivalence(self):
        magazine = self.record_at('sub002', 1)['similar_merge']
        self.assertEqual(magazine['book_title'], {
            'ja': '数学セミナー', 'en': '数学セミナー',
        })
        self.assertEqual(magazine['book_owner_range'], {'ja': '巨大行列とAI'})
        self.assertEqual(magazine['book_owner_role'], 'contributor')
        self.assertEqual(magazine['rep_page'], '29-33')
        self.assertFalse(magazine['referee'])

        chapter = self.record_at('sub003', 2)['similar_merge']
        self.assertIn('GPU Computing Gems Emerald Edition',
                      chapter['book_title'].values())
        self.assertIn('Treecode and fast multipole method for N-body simulation with CUDA',
                      chapter['book_owner_range'].values())
        self.assertEqual(RM.canonical_isbn('0-12-384988-8'),
                         RM.canonical_isbn('978-0-12-384988-5'))


if __name__ == '__main__':
    unittest.main()

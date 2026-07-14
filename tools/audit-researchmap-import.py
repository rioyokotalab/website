#!/usr/bin/env python3
"""Rebuild and audit the generated ResearchMap bulk-import JSONL."""
import collections
import hashlib
import importlib.util
import json
import os
import re


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPORT = os.path.join(ROOT, 'tools', 'out', 'researchmap-import.jsonl')
REPORT = os.path.join(ROOT, 'tools', 'out',
                      'researchmap-import-audit-20260714.md')
SPEC = importlib.util.spec_from_file_location(
    'researchmap_export', os.path.join(ROOT, 'tools',
                                       'researchmap-export.py'))
RM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RM)


def walk(value):
    yield value
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def operation_type(operation):
    for action in ('insert', 'update', 'delete'):
        if action in operation:
            return action, operation[action]['type']
    raise ValueError('operation has no action')


def title_from_doc(doc):
    for field in ('paper_title', 'book_title', 'presentation_title',
                  'committee_name', 'research_project_title'):
        value = doc.get(field)
        if isinstance(value, dict):
            return next((str(item) for item in value.values() if item), '')
        if value:
            return str(value)
    return '(profile record)'


def assert_non_destructive(updates, live_by_type):
    index = {(kind, RM.live_id(item)): item
             for kind, items in live_by_type.items() for item in items}
    for _text, operation in updates:
        kind = operation['update']['type']
        rid = operation['update']['id']
        live = index[(kind, rid)]
        for field, wanted in operation['doc'].items():
            current = live.get(field)
            if field == 'identifiers':
                allowed = RM.EDITABLE_IDENTIFIER_KINDS.get(kind, frozenset())
                for id_type, values in (current or {}).items():
                    if id_type not in allowed:
                        if id_type in wanted:
                            raise ValueError('managed identifier re-emitted: '
                                             '%s/%s/%s' %
                                             (kind, rid, id_type))
                        continue
                    if not RM.normalized_identifier_values(id_type, values).issubset(
                            RM.normalized_identifier_values(
                                id_type, wanted.get(id_type, []))):
                        raise ValueError('identifier removal: %s/%s/%s' %
                                         (kind, rid, id_type))
                continue
            if field == 'see_also':
                allowed = RM.EDITABLE_SEE_ALSO_LABELS.get(kind, frozenset())
                current_urls = RM.item_urls({'see_also': [
                    item for item in current or []
                    if isinstance(item, dict) and item.get('label') in allowed
                ]})
                wanted_urls = RM.item_urls({'see_also': wanted})
                if not current_urls.issubset(wanted_urls):
                    raise ValueError('editable URL removal: %s/%s' %
                                     (kind, rid))
                continue
            if field == 'languages':
                if not set(current or []).issubset(set(wanted)):
                    raise ValueError('language removal: %s/%s' % (kind, rid))
                continue
            if isinstance(current, dict) and isinstance(wanted, dict):
                for language, value in current.items():
                    if wanted.get(language) != value:
                        raise ValueError('localized replacement: %s/%s/%s/%s' %
                                         (kind, rid, field, language))
                continue
            if current not in (None, '', []):
                raise ValueError('scalar replacement: %s/%s/%s' %
                                 (kind, rid, field))


def validate_doc(kind, doc):
    unexpected = set(doc) - set(RM.SYNC_FIELDS[kind])
    if unexpected:
        raise ValueError('%s has unsupported fields: %r' %
                         (kind, sorted(unexpected)))
    for field, value in doc.items():
        if field.endswith('_date') and not re.fullmatch(
                r'\d{4}(?:-\d{2}(?:-\d{2})?)?', value):
            raise ValueError('invalid %s date: %r' % (kind, value))
        if field in ('referee', 'invited', 'is_international_presentation') \
                and not isinstance(value, bool):
            raise ValueError('%s.%s must be boolean' % (kind, field))
        if field == 'identifiers':
            allowed = RM.EDITABLE_IDENTIFIER_KINDS.get(kind, frozenset())
            managed = set(value) - set(allowed)
            if managed:
                raise ValueError('%s re-emits managed identifiers: %r' %
                                 (kind, sorted(managed)))
            if not value or any(not isinstance(items, list) or not items
                                for items in value.values()):
                raise ValueError('%s.identifiers must contain nonempty lists' %
                                 kind)
        if field == 'see_also':
            allowed = RM.EDITABLE_SEE_ALSO_LABELS.get(kind, frozenset())
            if not isinstance(value, list) or not value:
                raise ValueError('%s.see_also must be a nonempty list' % kind)
            for item in value:
                if not isinstance(item, dict) or item.get('label') not in allowed:
                    raise ValueError('%s re-emits managed see_also label: %r' %
                                     (kind, item))
                url = item.get('@id')
                if not isinstance(url, str) or not re.match(r'^https?://', url):
                    raise ValueError('%s.see_also has invalid URL' % kind)
    if doc.get('presentation_type') not in (
            None, 'invited_oral_presentation'):
        raise ValueError('unsupported presentation_type')
    if doc.get('book_owner_role') not in (None, 'contributor'):
        raise ValueError('unsupported book_owner_role')


def main():
    with open(IMPORT, encoding='utf-8') as source:
        operations = [json.loads(line) for line in source if line.strip()]
    live_by_type = {kind: RM.fetch_live(kind) for kind in RM.LIVE_TYPES}
    state = RM.load_state()
    inserts, updates, deletes, _refreshed, ambiguous, classified = RM.build_sync(
        RM.website_records(), live_by_type, state['managed_ids'],
        RM.load_match_overrides())
    expected = ([record for _text, record in inserts] +
                [record for _text, record in updates] + deletes)
    if operations != expected:
        raise ValueError('JSONL differs from a fresh live plan')
    if deletes:
        raise ValueError('reviewed import unexpectedly contains deletes')
    if len(operations) != len(inserts) + len(updates):
        raise ValueError('operation count mismatch')
    identities = []
    for operation in operations:
        actions = [action for action in ('insert', 'update', 'delete')
                   if action in operation]
        if len(actions) != 1:
            raise ValueError('operation must have exactly one action')
        action = actions[0]
        if operation[action]['type'] not in RM.LIVE_TYPES:
            raise ValueError('unsupported ResearchMap type')
        if action == 'update':
            identity = (operation[action]['type'], operation[action].get('id'))
            if not identity[1] or identity in identities:
                raise ValueError('missing/duplicate update identity: %r' %
                                 (identity,))
            identities.append(identity)
            validate_doc(operation[action]['type'], operation['doc'])
        elif action == 'insert':
            if operation.get('priority') != 'similar_data':
                raise ValueError('insert priority must be similar_data')
            validate_doc(operation[action]['type'], operation['similar_merge'])
        serialized = json.dumps(operation, ensure_ascii=False)
        if 'user_id' in serialized or 'rm:user_id' in serialized:
            raise ValueError('user_id must not occur in bulk import')
        if any(value in ('', None, [], {}) for value in walk(operation)):
            raise ValueError('empty value in operation')
        if '[arxiv]' in serialized or '[bibtex]' in serialized:
            raise ValueError('visible source-link label leaked into import')
    for _text, record in inserts:
        kind = record['insert']['type']
        doc = record['similar_merge']
        if kind in ('published_papers', 'misc') and not doc.get('paper_title'):
            raise ValueError('insert missing paper title')
        if kind == 'published_papers' and not doc.get('publication_date'):
            raise ValueError('paper insert missing publication date')
    assert_non_destructive(updates, live_by_type)

    action_type_counts = collections.Counter(operation_type(op)
                                             for op in operations)
    field_counts = collections.Counter(
        (operation['update']['type'], field)
        for operation in operations if 'update' in operation
        for field in operation['doc'])
    ambiguity_counts = collections.Counter(row[2] for row in ambiguous)
    classification_counts = collections.Counter(row['action']
                                                 for row in classified)
    with open(IMPORT, 'rb') as source:
        digest = hashlib.sha256(source.read()).hexdigest()

    lines = [
        '# ResearchMap bulk-import audit — 2026-07-14',
        '',
        '- Import: `tools/out/researchmap-import.jsonl`',
        '- SHA-256: `%s`' % digest,
        '- Operations: **%d** (%d inserts, %d additive updates, 0 deletes)' %
        (len(operations), len(inserts), len(updates)),
        '- Unresolved ambiguities: **%d**' % len(ambiguous),
        '- Reviewed classifications: **%d** explicit decisions' %
        len(classified),
        '- Safety: every operation exactly matches a fresh public-API plan; '
        'no existing scalar, localized value, caller-editable identifier, URL, '
        'or language is removed or replaced. System-managed nested values are '
        'excluded from update payloads as required by the V2 schema; no '
        '`user_id` or visible source-link label occurs.',
        '',
        '## Operations by category',
        '',
        '| Action | ResearchMap type | Count |',
        '|---|---|---:|',
    ]
    for (action, kind), count in sorted(action_type_counts.items()):
        lines.append('| %s | `%s` | %d |' % (action, kind, count))
    lines += [
        '',
        '## Reviewed classifications',
        '',
        '| Action | Entries |',
        '|---|---:|',
    ]
    for action, count in sorted(classification_counts.items()):
        lines.append('| `%s` | %d |' % (action, count))
    lines += [
        '',
        '## Additive update fields',
        '',
        '| ResearchMap type | Field | Operations |',
        '|---|---|---:|',
    ]
    for (kind, field), count in sorted(field_counts.items()):
        lines.append('| `%s` | `%s` | %d |' % (kind, field, count))
    lines += ['', '## Candidate inserts', '']
    for text, record in inserts:
        lines.append('- `%s`: %s' % (record['insert']['type'], text))
    lines += [
        '',
        '## Held ambiguity reasons',
        '',
        '| Reason | Entries |',
        '|---|---:|',
    ]
    for reason, count in sorted(ambiguity_counts.items()):
        lines.append('| %s | %d |' % (reason, count))
    lines += [
        '',
        'The JSONL is ready for manual review/upload. The managed-ID state '
        'remains unchanged until a successful upload is explicitly confirmed '
        'with `--record-managed-state`.',
        '',
    ]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as target:
        target.write('\n'.join(lines))
    print('validated %d operations; report: %s' % (len(operations), REPORT))


if __name__ == '__main__':
    main()

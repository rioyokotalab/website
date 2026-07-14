#!/usr/bin/env python3
"""Build a minimal retry JSONL from a ResearchMap import-error CSV."""
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location(
    'researchmap_export', os.path.join(ROOT, 'tools',
                                       'researchmap-export.py'))
RM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RM)

LINE = '行数'
IDENTIFIER = 'ID'
KIND = '種別'
STATUS = 'ステータスコード'
ERROR = 'エラー内容(エラーコード, フィールド名, メッセージ)'
REQUIRED_TITLE = re.compile(
    r'^required_value,[^,]+\((paper_title|book_title|presentation_title)\.'
    r'(ja|en)\),')
CONFLICT = re.compile(r'^conflict,,.*\[([^]]+)\]。?$')


def read_errors(path):
    with open(path, encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))
    required = {LINE, IDENTIFIER, KIND, STATUS, ERROR}
    if not rows:
        raise ValueError('error CSV is empty')
    missing = required - set(rows[0])
    if missing:
        raise ValueError('error CSV lacks columns: %r' % sorted(missing))
    return rows


def read_operations(path):
    with open(path, encoding='utf-8') as source:
        return [json.loads(line) for line in source if line.strip()]


def read_inventory(path):
    with open(path, encoding='utf-8') as source:
        return json.load(source)


def read_silent_merge_plan(path):
    with open(path, encoding='utf-8') as source:
        plan = json.load(source)
    if plan.get('schema_version') != 1 or not isinstance(
            plan.get('repairs'), list):
        raise ValueError('invalid silent-merge repair plan')
    return plan['repairs']


def parse_title_overrides(values):
    """Parse repeatable TYPE:ID:LANG:TITLE evidence supplied by the caller."""
    overrides = {}
    for value in values:
        parts = value.split(':', 3)
        if len(parts) != 4 or parts[2] not in ('ja', 'en') or not parts[3]:
            raise ValueError(
                'invalid title override (expected TYPE:ID:LANG:TITLE): %r' %
                value)
        key = (parts[0], parts[1])
        if key in overrides:
            raise ValueError('duplicate title override: %s/%s' % key)
        overrides[key] = {parts[2]: parts[3]}
    return overrides


def parse_conflict_pairs(values):
    """Parse repeatable ERROR_LINE:INSERT_LINE repair relationships."""
    pairs = {}
    insert_lines = set()
    for value in values:
        parts = value.split(':')
        if len(parts) != 2:
            raise ValueError(
                'invalid conflict pair (expected ERROR_LINE:INSERT_LINE): %r' %
                value)
        try:
            error_line, insert_line = (int(part) for part in parts)
        except ValueError:
            raise ValueError('invalid conflict pair line number: %r' % value)
        if error_line < 1 or insert_line < 1:
            raise ValueError('conflict pair lines must be positive: %r' % value)
        if error_line in pairs or insert_line in insert_lines:
            raise ValueError('duplicate conflict pair line: %r' % value)
        pairs[error_line] = insert_line
        insert_lines.add(insert_line)
    return pairs


def operation_title_keys(operation, doc):
    action = 'insert' if 'insert' in operation else 'update'
    kind = operation[action]['type']
    field = RM.REQUIRED_TITLE_FIELDS.get(kind)
    value = doc.get(field) if field else None
    if isinstance(value, dict):
        values = value.values()
    elif value:
        values = [value]
    else:
        values = []
    return {
        RM.key(unicodedata.normalize('NFKC', str(item)), limit=10**9)
        for item in values if item
    }


def build_conflict_retry(errors, operations, pairs):
    """Repair update/insert collisions with exact corrections then force-adds."""
    corrections = []
    force_inserts = []
    error_lines = set()
    for error in errors:
        try:
            line_number = int(error[LINE])
        except (TypeError, ValueError):
            raise ValueError('invalid error line number: %r' % error.get(LINE))
        if line_number in error_lines:
            raise ValueError('multiple errors for source line %d require review' %
                             line_number)
        error_lines.add(line_number)
        if error[STATUS] != '409':
            raise ValueError('unsupported conflict status on line %d: %s' %
                             (line_number, error[STATUS]))
        conflict = CONFLICT.match(error[ERROR])
        if not conflict or conflict.group(1) != error[IDENTIFIER]:
            raise ValueError('unsupported conflict on line %d: %s' %
                             (line_number, error[ERROR]))
        if line_number < 1 or line_number > len(operations):
            raise ValueError('source line out of range: %d' % line_number)
        operation = copy.deepcopy(operations[line_number - 1])
        if (set(operation) != {'update', 'doc'} or
                operation['update'].get('id') != error[IDENTIFIER] or
                operation['update'].get('type') != error[KIND]):
            raise ValueError('conflicted update mismatch on line %d' %
                             line_number)
        insert_line = pairs.get(line_number)
        if insert_line is None or insert_line >= line_number or insert_line > len(
                operations):
            raise ValueError('missing/invalid source insert for line %d' %
                             line_number)
        source_insert = operations[insert_line - 1]
        if (set(source_insert) != {'insert', 'similar_merge', 'priority'} or
                source_insert.get('priority') != 'similar_data'):
            raise ValueError('source line %d is not a legacy similarity insert' %
                             insert_line)
        update_titles = operation_title_keys(operation, operation['doc'])
        insert_titles = operation_title_keys(
            source_insert, source_insert['similar_merge'])
        if not update_titles or not insert_titles or not (
                update_titles & insert_titles):
            raise ValueError('conflict pair title mismatch: %d:%d' %
                             (line_number, insert_line))
        forced = {
            'insert': copy.deepcopy(source_insert['insert']),
            'force': copy.deepcopy(source_insert['similar_merge']),
        }
        for candidate in (operation, forced):
            serialized = json.dumps(candidate, ensure_ascii=False)
            if 'user_id' in serialized or 'rm:user_id' in serialized:
                raise ValueError('user_id found in conflict pair %d:%d' %
                                 (line_number, insert_line))
        corrections.append(operation)
        force_inserts.append(forced)
    missing = set(pairs) - error_lines
    if missing:
        raise ValueError('unused conflict error lines: %r' % sorted(missing))
    if len(force_inserts) != len(errors):
        raise ValueError('conflict repair must pair every rejected update')
    return corrections + force_inserts


def build_silent_merge_retry(operations, repairs):
    """Correct explicitly evidenced silent merges and force-add their sources."""
    corrections = []
    force_inserts = []
    identities = set()
    insert_lines = set()
    for repair in repairs:
        if not isinstance(repair, dict) or not repair.get('reason'):
            raise ValueError('silent-merge repair lacks reason')
        kind = repair.get('type')
        record_id = str(repair.get('id') or '')
        doc = repair.get('doc')
        insert_line = repair.get('insert_line')
        identity = (kind, record_id)
        if (kind not in RM.LIVE_TYPES or not record_id or not isinstance(doc, dict)
                or not doc or identity in identities):
            raise ValueError('invalid/duplicate silent-merge target: %r' %
                             (identity,))
        if (not isinstance(insert_line, int) or insert_line < 1 or
                insert_line > len(operations) or insert_line in insert_lines):
            raise ValueError('invalid/duplicate silent-merge insert line: %r' %
                             insert_line)
        source_insert = operations[insert_line - 1]
        if (set(source_insert) != {'insert', 'similar_merge', 'priority'} or
                source_insert.get('priority') != 'similar_data'):
            raise ValueError('source line %d is not a legacy similarity insert' %
                             insert_line)
        correction = {
            'update': {'type': kind, 'id': record_id},
            'doc': copy.deepcopy(doc),
        }
        update_titles = operation_title_keys(correction, correction['doc'])
        insert_titles = operation_title_keys(
            source_insert, source_insert['similar_merge'])
        if not update_titles or not insert_titles or not (
                update_titles & insert_titles):
            raise ValueError('silent-merge title mismatch: %s/%s line %d' %
                             (kind, record_id, insert_line))
        forced = {
            'insert': copy.deepcopy(source_insert['insert']),
            'force': copy.deepcopy(source_insert['similar_merge']),
        }
        for candidate in (correction, forced):
            serialized = json.dumps(candidate, ensure_ascii=False)
            if 'user_id' in serialized or 'rm:user_id' in serialized:
                raise ValueError('user_id found in silent-merge repair')
        identities.add(identity)
        insert_lines.add(insert_line)
        corrections.append(correction)
        force_inserts.append(forced)
    return corrections + force_inserts


def updates_before_inserts(operations):
    updates = [operation for operation in operations if 'update' in operation]
    inserts = [operation for operation in operations if 'insert' in operation]
    if len(updates) + len(inserts) != len(operations):
        raise ValueError('retry may contain only updates and inserts')
    identities = [(operation['update']['type'], operation['update']['id'])
                  for operation in updates]
    if len(identities) != len(set(identities)):
        raise ValueError('retry contains duplicate update identities')
    return updates + inserts


def inventory_live_titles(errors, inventory, overrides=None):
    """Reconstruct rejected records' monolingual titles from saved evidence."""
    overrides = overrides or {}
    matches = {}
    for category in inventory.get('categories', {}).values():
        for entry in category.get('entries', []):
            match = entry.get('live_match') or {}
            kind = match.get('type')
            record_id = str(match.get('rm_id') or '')
            title = match.get('title')
            if not kind or not record_id or not title:
                continue
            key = (kind, record_id)
            if key in matches and matches[key] != title:
                raise ValueError('conflicting inventory titles: %s/%s' % key)
            matches[key] = title

    live_by_type = {}
    used_overrides = set()
    for error in errors:
        record_id = error[IDENTIFIER]
        if not record_id:
            continue
        match = REQUIRED_TITLE.match(error[ERROR])
        if not match:
            continue
        title_field, missing_language = match.groups()
        existing_language = 'ja' if missing_language == 'en' else 'en'
        kind = error[KIND]
        key = (kind, record_id)
        if key in overrides:
            title = overrides[key]
            if set(title) != {existing_language}:
                raise ValueError(
                    'title override must provide existing %s value: %s/%s' %
                    (existing_language, kind, record_id))
            used_overrides.add(key)
        elif key in matches:
            title = {existing_language: matches[key]}
        else:
            raise ValueError('inventory title missing: %s/%s' % key)
        live_by_type.setdefault(kind, {})[record_id] = {
            title_field: title,
        }
    unused = set(overrides) - used_overrides
    if unused:
        kind, record_id = sorted(unused)[0]
        raise ValueError('unused title override: %s/%s' % (kind, record_id))
    return live_by_type


def build_retry(errors, operations, live_by_type):
    """Return corrected copies of only the rejected import operations."""
    retry = []
    seen_lines = set()
    for error in errors:
        try:
            line_number = int(error[LINE])
        except (TypeError, ValueError):
            raise ValueError('invalid error line number: %r' % error.get(LINE))
        if line_number in seen_lines:
            raise ValueError('multiple errors for source line %d require review' %
                             line_number)
        seen_lines.add(line_number)
        if line_number < 1 or line_number > len(operations):
            raise ValueError('source line out of range: %d' % line_number)
        if error[STATUS] != '400':
            raise ValueError('unsupported status on line %d: %s' %
                             (line_number, error[STATUS]))
        match = REQUIRED_TITLE.match(error[ERROR])
        if not match:
            raise ValueError('unsupported error on line %d: %s' %
                             (line_number, error[ERROR]))
        title_field, missing_language = match.groups()
        operation = copy.deepcopy(operations[line_number - 1])
        actions = [name for name in ('insert', 'update', 'delete')
                   if name in operation]
        if len(actions) != 1 or actions[0] == 'delete':
            raise ValueError('unsupported operation on line %d' % line_number)
        action = actions[0]
        kind = operation[action]['type']
        if kind != error[KIND]:
            raise ValueError('type mismatch on line %d' % line_number)
        expected_title = RM.REQUIRED_TITLE_FIELDS.get(kind)
        if title_field != expected_title:
            raise ValueError('title-field mismatch on line %d' % line_number)

        if action == 'insert':
            if error[IDENTIFIER]:
                raise ValueError('insert unexpectedly has ID on line %d' %
                                 line_number)
            doc = operation['similar_merge']
            title = RM.complete_required_title(doc.get(title_field))
        else:
            record_id = operation['update'].get('id')
            if not record_id or record_id != error[IDENTIFIER]:
                raise ValueError('update ID mismatch on line %d' % line_number)
            live = live_by_type.get(kind, {}).get(record_id)
            if live is None:
                raise ValueError('live record missing for line %d: %s/%s' %
                                 (line_number, kind, record_id))
            doc = operation['doc']
            title = RM.complete_required_title(live.get(title_field))
        if not title.get(missing_language) or set(title) != {'ja', 'en'}:
            raise ValueError('could not complete title on line %d' % line_number)
        doc[title_field] = title
        serialized = json.dumps(operation, ensure_ascii=False)
        if 'user_id' in serialized or 'rm:user_id' in serialized:
            raise ValueError('user_id found on line %d' % line_number)
        retry.append(operation)
    return retry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--errors', default=os.path.join(
        ROOT, 'tools', 'out', 'errors_researchmap-import-6.csv'))
    parser.add_argument('--source', default=os.path.join(
        ROOT, 'tools', 'out', 'researchmap-import.jsonl'))
    parser.add_argument('--output', default=os.path.join(
        ROOT, 'tools', 'out', 'researchmap-import-retry-1.jsonl'))
    parser.add_argument(
        '--inventory',
        help='saved ResearchMap inventory; when set, make no network requests')
    parser.add_argument(
        '--title-override', action='append', default=[],
        metavar='TYPE:ID:LANG:TITLE',
        help='exact observed live title missing from the saved inventory')
    parser.add_argument(
        '--conflict-pair', action='append', default=[],
        metavar='ERROR_LINE:INSERT_LINE',
        help='pair a rejected update with the earlier insert it collided with')
    parser.add_argument(
        '--silent-merge-plan',
        help='evidence-backed JSON plan for merges that succeeded silently')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    try:
        errors = read_errors(args.errors)
        operations = read_operations(args.source)
        statuses = {row[STATUS] for row in errors}
        if statuses == {'409'}:
            if args.inventory or args.title_override:
                raise ValueError(
                    '409 conflict repair does not use title inventory options')
            pairs = parse_conflict_pairs(args.conflict_pair)
            retry = build_conflict_retry(errors, operations, pairs)
            if args.silent_merge_plan:
                repairs = read_silent_merge_plan(args.silent_merge_plan)
                retry += build_silent_merge_retry(operations, repairs)
            retry = updates_before_inserts(retry)
        elif statuses == {'400'}:
            if args.conflict_pair or args.silent_merge_plan:
                raise ValueError(
                    'conflict repair options require only 409 errors')
            if args.inventory:
                inventory = read_inventory(args.inventory)
                overrides = parse_title_overrides(args.title_override)
                live_by_type = inventory_live_titles(
                    errors, inventory, overrides)
            else:
                if args.title_override:
                    raise ValueError('--title-override requires --inventory')
                kinds = sorted({row[KIND] for row in errors if row[IDENTIFIER]})
                live_by_type = {}
                for kind in kinds:
                    live_by_type[kind] = {
                        RM.live_id(item): item for item in RM.fetch_live(kind)
                    }
            retry = build_retry(errors, operations, live_by_type)
        else:
            raise ValueError('mixed/unsupported error statuses: %r' %
                             sorted(statuses))
    except Exception as error:
        print('ERROR: %s' % error, file=sys.stderr)
        return 1

    payload = ''.join(json.dumps(operation, ensure_ascii=False) + '\n'
                      for operation in retry).encode('utf-8')
    counts = {action: sum(action in operation for operation in retry)
              for action in ('insert', 'update', 'delete')}
    print('%d retry operations: %d inserts / %d updates / %d deletes' %
          (len(retry), counts['insert'], counts['update'], counts['delete']))
    print('SHA-256: %s' % hashlib.sha256(payload).hexdigest())
    if args.dry_run:
        print('dry run: no retry file written')
        return 0
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'wb') as target:
        target.write(payload)
    print('written to %s' % args.output)
    return 0


if __name__ == '__main__':
    sys.exit(main())

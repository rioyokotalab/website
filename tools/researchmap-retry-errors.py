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
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    try:
        errors = read_errors(args.errors)
        operations = read_operations(args.source)
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

#!/usr/bin/env python3
"""Normalize Achievement list rows and add verified arXiv/BibTeX links."""
import argparse
import html
import os
import re


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    os.path.join(ROOT, 'en', 'achievements', 'index.html'),
    os.path.join(ROOT, 'jp', 'achievements', 'index.html'),
]
SECTIONS = ['sub%03d' % number for number in range(1, 8)]
LINK_ROW = re.compile(
    r'\s*<br\s*/?>\s*<span\b[^>]*\bclass\s*=\s*["\'][^"\']*'
    r'\bachievement-links\b[^"\']*["\'][^>]*>.*?</span\s*>\s*$',
    re.I | re.S)


def section_bounds(content, anchor):
    marker = re.search(
        r'<[^>]+\bid\s*=\s*(["\'])%s\1[^>]*>' % re.escape(anchor),
        content, re.I)
    if not marker:
        raise ValueError('missing section marker: %s' % anchor)
    opening = re.search(r'<ol\b[^>]*>', content[marker.end():], re.I)
    if not opening:
        raise ValueError('missing ordered list: %s' % anchor)
    start = marker.end() + opening.end()
    closing = re.search(r'</ol\s*>', content[start:], re.I)
    if not closing:
        raise ValueError('unclosed ordered list: %s' % anchor)
    return start, start + closing.start()


def arxiv_id(opening_tag):
    match = re.search(
        r'\bdata-url\s*=\s*(["\'])https://arxiv\.org/abs/([^"\'/?#]+)\1',
        opening_tag, re.I)
    return html.unescape(match.group(2)) if match else None


def normalize_entry(match, newline):
    opening_tag, body = match.group(1), match.group(2)
    # Rebuild a prior generated row so repeated runs remain byte-identical.
    body = LINK_ROW.sub('', body)
    # The overwhelming majority style is plain citation text, not one-off
    # inline anchors.  Preserve the link label/text while removing its markup.
    body = re.sub(r'<a\b[^>]*>(.*?)</a\s*>', r'\1', body,
                  flags=re.I | re.S)
    # One legacy citation used a presentation-only line break.  Source-link
    # rows are rebuilt below; all citation text follows the section majority
    # and remains on one logical line.
    body = re.sub(r'\s*<br\s*/?>\s*', ' ', body, flags=re.I)
    body = body.strip()
    visible = html.unescape(re.sub(r'<[^>]+>', '', body)).rstrip()
    if not visible.endswith(('.', '。')):
        body += '.'
    identifier = arxiv_id(opening_tag)
    if identifier:
        escaped = html.escape(identifier, quote=True)
        body += (
            '<br>' + newline +
            '          <span class="achievement-links">'
            '<a href="https://arxiv.org/abs/%s" target="_blank" '
            'rel="noopener noreferrer">[arxiv]</a> '
            '<a href="https://arxiv.org/bibtex/%s" target="_blank" '
            'rel="noopener noreferrer">[bibtex]</a></span>' %
            (escaped, escaped))
    return opening_tag + body + '</li>'


def normalize_page(path):
    with open(path, newline='', encoding='utf-8') as source:
        content = source.read()
    newline = '\r\n' if '\r\n' in content else '\n'
    counts = []
    # Work backwards so replacing one section cannot invalidate later offsets.
    bounds = [(anchor, *section_bounds(content, anchor)) for anchor in SECTIONS]
    for anchor, start, end in reversed(bounds):
        block = content[start:end]
        block, count = re.subn(
            r'(?m)^[ \t]*(<li\b[^>]*>)(.*?)</li\s*>',
            lambda match: '        ' + normalize_entry(match, newline),
            block, flags=re.I | re.S)
        if not count:
            raise ValueError('empty achievement section: %s' % anchor)
        counts.append((anchor, count))
        content = content[:start] + block + content[end:]
    with open(path, 'w', newline='', encoding='utf-8') as target:
        target.write(content)
    return dict(counts)


def audit(path):
    with open(path, newline='', encoding='utf-8') as source:
        content = source.read()
    counts = {}
    entries = []
    for anchor in SECTIONS:
        start, end = section_bounds(content, anchor)
        rows = re.findall(r'(?m)^([ \t]*)(<li\b[^>]*>)(.*?)</li\s*>',
                          content[start:end], re.I | re.S)
        counts[anchor] = len(rows)
        entries.extend(rows)
    links = 0
    signatures = []
    for indentation, opening, body in entries:
        if indentation != '        ':
            raise ValueError('%s: non-majority list indentation %r' %
                             (path, indentation))
        spans = re.findall(
            r'<span\b[^>]*\bclass=["\'][^"\']*achievement-links[^"\']*'
            r'["\'][^>]*>.*?</span\s*>', body, re.I | re.S)
        expected = bool(arxiv_id(opening))
        if len(spans) != int(expected):
            raise ValueError('%s: source-link count mismatch' % path)
        if len(re.findall(r'<br\s*/?>', body, re.I)) != int(expected):
            raise ValueError('%s: citation line-break mismatch' % path)
        links += len(spans)
        citation = LINK_ROW.sub('', body).strip()
        visible = html.unescape(re.sub(r'<[^>]+>', '', citation)).rstrip()
        signatures.append((opening, ' '.join(visible.split())))
        if not visible.endswith(('.', '。')):
            raise ValueError('%s: non-terminal citation %r' %
                             (path, visible[-80:]))
        if re.search(r'<a\b', citation, re.I):
            raise ValueError('%s: inline citation anchor remains' % path)
        if body and body[0].isspace():
            raise ValueError('%s: leading citation whitespace remains' % path)
    if counts != dict(zip(SECTIONS, [42, 2, 2, 115, 31, 48, 69])):
        raise ValueError('%s: section counts changed: %r' % (path, counts))
    if links != 30:
        raise ValueError('%s: expected 30 arXiv rows, found %d' % (path, links))
    return counts, links, signatures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true',
                        help='audit the committed pages without rewriting them')
    args = parser.parse_args()
    if not args.check:
        for page in PAGES:
            normalize_page(page)
    audits = [audit(page) for page in PAGES]
    if audits[0] != audits[1]:
        raise ValueError('EN/JP normalization audit differs')
    action = 'validated' if args.check else 'normalized'
    print('%s 309 entries and 30 arXiv/BibTeX rows per page' % action)


if __name__ == '__main__':
    main()

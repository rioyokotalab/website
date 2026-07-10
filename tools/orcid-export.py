#!/usr/bin/env python3
"""Export the website's Achievements publication list as an ORCID BibTeX file.

ORCID has no researchmap-style JSON bulk-import grammar.  The sanctioned
no-API import path in the ORCID UI is:

    Add works  >  Search & link / Add manually  >  "Import BibTeX"
    (the BibTeXImportWizard) — it ingests a .bib file and creates one work
    per entry.

So this exporter emits a BibTeX file (tools/out/orcid-works.bib) rather than
JSON Lines.  It parses en/achievements/index.html (the canonical list;
international entries in English, domestic in Japanese), keeps only
publications with Rio Yokota as an author, and reuses the *same* hardened
citation parser as tools/researchmap-export.py (loaded dynamically because
that file's name contains a hyphen) so both exporters split
author/title/venue/date identically.

ORCID's public API is read-only without an OAuth token, so — matching the
researchmap exporter's "generate the full set" fallback — this tool does NOT
diff against a live record.  It always writes the complete Yokota-authored set
from the website; ORCID de-duplicates on import (it groups works by
identifier/title and lets the user merge), and an API-diff mode can be added
later once a 3-legged OAuth token is available.

Section -> BibTeX entry type mapping:
    sub001 journal papers            -> @article
    sub002 book series               -> @incollection   (chapters/serials)
    sub003 books                     -> @book
    sub004 international peer-reviewed-> @inproceedings   (conference-paper)
    sub005 domestic peer-reviewed    -> @inproceedings
    sub006 international non-reviewed -> @misc            (talks/posters)
    sub007 domestic non-reviewed     -> @misc

Usage:
    tools/orcid-export.py            write tools/out/orcid-works.bib
    tools/orcid-export.py --dry-run  print counts + risky parses, no file
"""
import argparse, importlib.util, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'en', 'achievements', 'index.html')
OUT = os.path.join(ROOT, 'tools', 'out', 'orcid-works.bib')
ORCID = '0000-0001-7573-7873'

# Load the researchmap exporter as a module to reuse its parse()/key()/is_cjk()
# /sole_author() heuristics verbatim (its filename has a hyphen, so import via spec).
_spec = importlib.util.spec_from_file_location(
    'researchmap_export', os.path.join(ROOT, 'tools', 'researchmap-export.py'))
rm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rm)

# anchor -> BibTeX entry type
SECTION_TYPE = {
    'sub001': 'article',
    'sub002': 'incollection',
    'sub003': 'book',
    'sub004': 'inproceedings',
    'sub005': 'inproceedings',
    'sub006': 'misc',
    'sub007': 'misc',
}
# which BibTeX field holds the venue, per entry type
VENUE_FIELD = {
    'article': 'journal',
    'incollection': 'booktitle',
    'book': 'publisher',
    'inproceedings': 'booktitle',
    'misc': 'howpublished',
}
MONTH_ABBR = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

def raw_items(anchor):
    """Yield (clean_text, doi, url, data_date, data_volume, data_number,
    data_pages, data_authors) for each <li> in a section,
    keeping DOI/link attributes and the opening <li>'s data-date attribute
    (which overrides the parsed date)."""
    c = open(PAGE, newline='', encoding='utf-8').read()
    a = c.index('name="%s"' % anchor)
    s = c.index('<ol>', a); e = c.index('</ol>', s)
    block = c[s:e]
    tags = re.findall(r'<li[^>]*>', block, flags=re.I)
    parts = re.split(r'<li[^>]*>', block, flags=re.I)[1:]
    for tag, p in zip(tags, parts):
        dm = rm.DATA_DATE.search(tag)
        data_date = rm.norm_date(dm.group(1)) if dm else None
        doi_m = rm.DATA_DOI.search(tag)
        doi = None
        if doi_m:
            doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', doi_m.group(1).strip(), flags=re.I) or None
        url_m = rm.DATA_URL.search(tag)
        url = url_m.group(1).strip() if url_m else None
        url = url or None
        volume_m = rm.DATA_VOLUME.search(tag)
        data_volume = volume_m.group(1).strip() if volume_m else None
        data_volume = data_volume or None
        number_m = rm.DATA_NUMBER.search(tag)
        data_number = number_m.group(1).strip() if number_m else None
        data_number = data_number or None
        pages_m = rm.DATA_PAGES.search(tag)
        data_pages = pages_m.group(1).strip() if pages_m else None
        data_pages = data_pages or None
        authors_m = rm.DATA_AUTHORS.search(tag)
        data_authors = [a.strip() for a in authors_m.group(1).split(';') if a.strip()] if authors_m else None
        data_authors = data_authors or None
        m = re.search(r'href=["\'](https?://(?:dx\.)?doi\.org/[^"\']+)["\']', p, re.I)
        if not doi and m:
            doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', m.group(1)).strip()
        t = re.sub(r'</li>', '', re.sub(r'<[^>]+>', '', p), flags=re.I)
        t = (unicodedata.normalize('NFKC', t).replace('&amp;', '&')
             .replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"'))
        yield (re.sub(r'\s+', ' ', t).strip(), doi, url, data_date,
               data_volume, data_number, data_pages, data_authors)

def extract_volpp(venue):
    """Pull Vol./No./pp. out of a venue string; return (clean_venue, fields)."""
    fields = {}
    m = re.search(r'\bVol\.?\s*(\d+)', venue, re.I)
    if m:
        fields['volume'] = m.group(1)
    m = re.search(r'\bNo\.?\s*(\d+)', venue, re.I)
    if m:
        fields['number'] = m.group(1)
    m = re.search(r'\bpp?\.?\s*(\d+\s*[-–—]\s*\d+)', venue, re.I)
    if m:
        fields['pages'] = re.sub(r'\s*[-–—]\s*', '--', m.group(1))
    # strip the matched Vol/No/pp clauses (comma-delimited) from the venue text
    venue = re.sub(r',?\s*\bVol\.?\s*\d+', '', venue, flags=re.I)
    venue = re.sub(r',?\s*\bNo\.?\s*\d+', '', venue, flags=re.I)
    venue = re.sub(r',?\s*\bpp?\.?\s*\d+\s*[-–—]\s*\d+', '', venue, flags=re.I)
    venue = re.sub(r'\s{2,}', ' ', venue).strip(' ,')
    return venue, fields

def slug(s):
    return re.sub(r'[^0-9a-z]', '', s.lower())

def citekey(authors, title, year, used):
    surname = ''
    if authors:
        toks = re.sub(r'[^\w\s]', '', authors[0]).split()
        # ascii surname = last latin token; else first CJK author string
        ascii_toks = [t for t in toks if re.match(r'^[A-Za-z]+$', t)]
        surname = slug(ascii_toks[-1]) if ascii_toks else slug(''.join(toks))
    if not surname:
        surname = 'ref'
    tw = ''
    for w in re.findall(r'[A-Za-z]+', title):
        if len(w) > 2:
            tw = w.lower()
            break
    base = '%s%s%s' % (surname, year or 'nd', tw)
    base = base or 'ref'
    k = base
    i = 1
    while k in used:
        i += 1
        k = '%s%c' % (base, ord('a') + i - 2) if i <= 27 else '%s%d' % (base, i)
    used.add(k)
    return k

def bib_escape(s):
    return s.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')

def fallback_year(text):
    """When the shared parser finds no date (year buried behind a trailing
    volume/page number, e.g. \"... 043601 (2025).\"), recover a plausible year
    from the full citation: prefer a year in a trailing parenthesis, else the
    last 4-digit year in range."""
    m = re.search(r'\((19|20)\d{2}\)\.?\s*$', text)
    if m:
        return re.search(r'(19|20)\d{2}', m.group(0)).group(0)
    yrs = [y for y in re.findall(r'(?:19|20)\d{2}', text) if 1985 <= int(y) <= 2035]
    return yrs[-1] if yrs else None

def make_entry(etype, authors, title, venue, date, doi, url, used,
               data_volume=None, data_number=None, data_pages=None):
    year = month = None
    if date:
        year = date[:4]
        if len(date) >= 7:
            month = MONTH_ABBR[int(date[5:7]) - 1]
    fields = {}
    venue_field = VENUE_FIELD[etype]
    if etype in ('article', 'incollection', 'inproceedings'):
        venue, vf = extract_volpp(venue)
        fields.update(vf)
    if data_volume:
        fields['volume'] = data_volume
    if data_number:
        fields['number'] = data_number
    if data_pages:
        m = re.match(r'^([A-Za-z]?\d+)-([A-Za-z]?\d+)$', data_pages)
        if m:
            fields['pages'] = '%s--%s' % (m.group(1), m.group(2))
        else:
            fields['pages'] = data_pages
    if authors:
        fields['author'] = ' and '.join(authors)
    fields['title'] = '{%s}' % bib_escape(title)
    if venue:
        fields[venue_field] = bib_escape(venue)
    if year:
        fields['year'] = year
    if month:
        fields['month'] = month
    if doi:
        fields['doi'] = doi
    elif url:
        fields['url'] = url
    key = citekey(authors, title, year, used)
    order = ['author', 'title', venue_field, 'volume', 'number',
             'pages', 'year', 'month', 'doi', 'url']
    lines = ['@%s{%s,' % (etype, key)]
    keys = [k for k in order if k in fields] + \
           [k for k in fields if k not in order]
    for k in keys:
        lines.append('  %s = {%s},' % (k, fields[k]))
    lines[-1] = lines[-1].rstrip(',')
    lines.append('}')
    return '\n'.join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    used = set()
    entries = []
    per_section = {}
    risky = []
    for anchor, etype in SECTION_TYPE.items():
        cnt = 0
        for text, doi, url, data_date, data_volume, data_number, data_pages, data_authors in raw_items(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            parsed = rm.parse(text)
            if not parsed:
                risky.append(('UNPARSED', anchor, text))
                continue
            authors, title, venue, date = parsed
            if data_authors:
                authors = data_authors
            if data_date:                    # data-date attribute wins
                date = data_date
            elif not date:
                date = fallback_year(text)  # recover year buried after vol/pages
            # flag suspicious parses for human review
            if not authors:
                risky.append(('NO-AUTHOR', anchor, text))
            elif not date:
                risky.append(('NO-YEAR', anchor, text))
            elif not venue:
                risky.append(('NO-VENUE', anchor, text))
            entries.append(make_entry(etype, authors, title, venue, date, doi, url, used,
                                      data_volume, data_number, data_pages))
            cnt += 1
        per_section[anchor] = cnt

    print('Entries per section:')
    for a in SECTION_TYPE:
        print('  %s (@%-13s): %d' % (a, SECTION_TYPE[a], per_section[a]))
    print('  TOTAL: %d' % len(entries))
    if risky:
        print('\nRisky parses to review (%d):' % len(risky))
        for tag, anchor, text in risky:
            print('  [%s %s] %s' % (tag, anchor, text[:110]))

    if args.dry_run:
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    header = ('%% ORCID BibTeX export for https://orcid.org/%s\n'
              '%% Generated from en/achievements/index.html by tools/orcid-export.py\n'
              '%% Import via ORCID > Add works > Import BibTeX.\n\n' % ORCID)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write('\n\n'.join(entries) + '\n')
    print('\n%d entries written to %s' % (len(entries), OUT))
    print('Import via ORCID > Add works > Import BibTeX.')

if __name__ == '__main__':
    main()

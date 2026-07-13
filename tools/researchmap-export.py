#!/usr/bin/env python3
"""Export new Achievements entries as a researchmap V2 bulk-import file.

Parses en/achievements/index.html (the canonical list; international entries
are in English, domestic ones in Japanese), keeps only publications with
Rio Yokota as an author, and emits researchmap "insert + similar_merge"
JSON Lines for entries not yet recorded in the state file.

Usage:
  tools/researchmap-export.py --init      snapshot current page as baseline
                                          (nothing exported)
  tools/researchmap-export.py             write tools/out/researchmap-import.jsonl
                                          with entries added since the baseline,
                                          and update the baseline
  tools/researchmap-export.py --dry-run   show what would be exported, no writes
  tools/researchmap-export.py --check-live  diff against live researchmap.jp data
                                          instead of the local state file, and
                                          write tools/out/researchmap-import.jsonl
  tools/researchmap-export.py --sync      write inserts + partial updates +
                                          registry-bounded deletes after a live diff

The output file is uploaded on researchmap:  設定 > インポート
(or pushed via the WebAPI once an API key is available).
Format reference: https://researchmap.jp/outline/v2api/v2API.pdf
"""
import argparse, html, json, os, re, sys, unicodedata, urllib.request, urllib.error
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'en', 'achievements', 'index.html')
PROFILE = os.path.join(ROOT, 'jp', 'member', 'yokota.html')  # canonical for CV items
STATE = os.path.join(ROOT, 'tools', 'researchmap-state.json')
OUT = os.path.join(ROOT, 'tools', 'out', 'researchmap-import.jsonl')
PERMALINK = 'rioyokota'

SECTIONS = {   # anchor -> (rm type, extra fields)
    # Mapping (agreed 2026-07-06): peer-reviewed sections -> Papers;
    # book sections -> Books and Other Publications; non-peer-reviewed
    # sections -> Presentations if Rio Yokota is the sole author (invited
    # talks), Misc. otherwise ('talk_or_misc' is resolved per entry).
    'sub001': ('published_papers', {'published_paper_type': 'scientific_journal', 'referee': True}),
    'sub002': ('books_etc', {}),
    'sub003': ('books_etc', {}),
    'sub004': ('published_papers', {'published_paper_type': 'international_conference_proceedings', 'referee': True}),
    'sub005': ('published_papers', {'published_paper_type': 'symposium', 'referee': True}),
    'sub006': ('talk_or_misc', {'is_international_presentation': True}),
    'sub007': ('talk_or_misc', {'is_international_presentation': False}),
}
MONTHS = {m: i+1 for i, m in enumerate(
    ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])}
VENUE_WORDS = re.compile(
    r'Journal|Conference|Proceedings|Transactions|Workshop|Symposium|SIGKDD|'
    r'NeurIPS|ICLR|ICML|CVPR|ICCV|ECCV|AAAI|EMNLP|COLM|COLING|LREC|ISC|SC\d|HPC|GTC|'
    r'IEEE|ACM|SIAM|Nature|arXiv|学会|研究会|大会|シンポジウム|発表会|ワークショップ|研究発表会')

# invisible data-date="YYYY-MM"(-DD) on the opening <li> = ResearchMap
# publication_date; when present it OVERRIDES the heuristic date parse below.
DATA_DATE = re.compile(r'\bdata-date\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_DOI = re.compile(r'\bdata-doi\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_ISBN = re.compile(r'\bdata-isbn\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_URL = re.compile(r'\bdata-url\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_VOLUME = re.compile(r'\bdata-volume\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_NUMBER = re.compile(r'\bdata-number\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_PAGES = re.compile(r'\bdata-pages\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_AUTHORS = re.compile(r'\bdata-authors\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_AUTHORS_JA = re.compile(r'\bdata-authors-ja\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_AUTHORS_EN = re.compile(r'\bdata-authors-en\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_EVENT = re.compile(r'\bdata-event\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_LOCATION = re.compile(r'\bdata-location\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_INVITED = re.compile(r'\bdata-invited\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_PUBLISHER = re.compile(r'\bdata-publisher\s*=\s*["\']([^"\']*)["\']', re.I)
ACHIEVEMENT_LINKS = re.compile(
    r'<span\b[^>]*\bclass\s*=\s*["\'][^"\']*\bachievement-links\b[^"\']*["\'][^>]*>'
    r'.*?</span\s*>', re.I | re.S)

def section_block(content, anchor):
    """Return the first ordered-list body after an id/name section marker."""
    marker = re.search(
        r'<[^>]+\b(?:id|name)\s*=\s*(["\'])%s\1[^>]*>' % re.escape(anchor),
        content, re.I)
    if not marker:
        raise ValueError('section marker not found: %s' % anchor)
    opening = re.search(r'<ol\b[^>]*>', content[marker.end():], re.I)
    if not opening:
        raise ValueError('ordered list not found after section: %s' % anchor)
    start = marker.end() + opening.end()
    closing = re.search(r'</ol\s*>', content[start:], re.I)
    if not closing:
        raise ValueError('ordered list not closed for section: %s' % anchor)
    return content[start:start + closing.start()]

def strip_achievement_links(fragment):
    """Remove the visible source-link row before citation-text parsing."""
    return ACHIEVEMENT_LINKS.sub('', fragment)

def split_authors(s):
    return [a.strip() for a in s.split(';') if a.strip()]

def norm_date(s):
    """Normalize a data-date value to YYYY / YYYY-MM / YYYY-MM-DD, else None."""
    if not s:
        return None
    m = re.match(r'\s*(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?\s*$', s)
    if not m:
        return None
    out = m.group(1)
    if m.group(2):
        out += '-' + m.group(2)
        if m.group(3):
            out += '-' + m.group(3)
    return out

def entries(anchor):
    """Yield (clean_text, data_date, data_doi, data_isbn, data_url, data_volume,
    data_number, data_pages, data_authors, data_authors_ja, data_authors_en,
    data_event, data_location, data_invited, data_publisher) for each <li>;
    data_* is None if the opening <li> tag carries no valid attribute."""
    with open(PAGE, newline='', encoding='utf-8') as source:
        c = source.read()
    block = section_block(c, anchor)
    # keep the opening <li ...> tags (re.split drops them) so we can read
    # data-date; tags[i] is the tag that precedes parts[i].
    tags = re.findall(r'<li[^>]*>', block, flags=re.I)
    parts = re.split(r'<li[^>]*>', block, flags=re.I)[1:]
    out = []
    for tag, p in zip(tags, parts):
        dm = DATA_DATE.search(tag)
        data_date = norm_date(dm.group(1)) if dm else None
        doi_m = DATA_DOI.search(tag)
        data_doi = None
        if doi_m:
            data_doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', doi_m.group(1).strip(), flags=re.I) or None
        isbn_m = DATA_ISBN.search(tag)
        data_isbn = isbn_m.group(1).strip() if isbn_m else None
        data_isbn = data_isbn or None
        url_m = DATA_URL.search(tag)
        data_url = url_m.group(1).strip() if url_m else None
        data_url = data_url or None
        volume_m = DATA_VOLUME.search(tag)
        data_volume = volume_m.group(1).strip() if volume_m else None
        data_volume = data_volume or None
        number_m = DATA_NUMBER.search(tag)
        data_number = number_m.group(1).strip() if number_m else None
        data_number = data_number or None
        pages_m = DATA_PAGES.search(tag)
        data_pages = pages_m.group(1).strip() if pages_m else None
        data_pages = data_pages or None
        authors_m = DATA_AUTHORS.search(tag)
        data_authors = split_authors(authors_m.group(1)) if authors_m else None
        data_authors = data_authors or None
        authors_ja_m = DATA_AUTHORS_JA.search(tag)
        data_authors_ja = split_authors(authors_ja_m.group(1)) if authors_ja_m else None
        data_authors_ja = data_authors_ja or None
        authors_en_m = DATA_AUTHORS_EN.search(tag)
        data_authors_en = split_authors(authors_en_m.group(1)) if authors_en_m else None
        data_authors_en = data_authors_en or None
        event_m = DATA_EVENT.search(tag)
        data_event = event_m.group(1).strip() if event_m else None
        data_event = data_event or None
        location_m = DATA_LOCATION.search(tag)
        data_location = location_m.group(1).strip() if location_m else None
        data_location = data_location or None
        inv_m = DATA_INVITED.search(tag)
        data_invited = (inv_m.group(1).strip().lower() == 'true') if inv_m else None
        publisher_m = DATA_PUBLISHER.search(tag)
        data_publisher = publisher_m.group(1).strip() if publisher_m else None
        data_publisher = data_publisher or None
        p = strip_achievement_links(p)
        t = re.sub(r'</li>', '', re.sub(r'<[^>]+>', '', p), flags=re.I)
        t = unicodedata.normalize('NFKC', t).replace('&amp;', '&').replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
        out.append((re.sub(r'\s+', ' ', t).strip(), data_date, data_doi, data_isbn, data_url,
                    data_volume, data_number, data_pages, data_authors,
                    data_authors_ja, data_authors_en, data_event, data_location,
                    data_invited, data_publisher))
    return out

def key(t, limit=70):
    return re.sub(r'[^0-9a-z぀-ヿ一-鿿]', '', t.lower())[:limit]

def is_cjk(s):
    return bool(re.search(r'[぀-ヿ一-鿿]', s))

def parse_date(seg):
    seg = seg.strip()
    # tolerate a trailing parenthetical note after the date (e.g.
    # "Dec. 2022. (Best paper)", "2022 (to appear)"); require content before
    # the paren so a bare "(2022)" is left intact for the strip below.
    seg = re.sub(r'(\S)\s*\([^)]*\)\s*$', r'\1', seg)
    seg = seg.strip(' .()')
    m = re.match(r'([A-Za-z]+)\.?,? ?(\d{4})$', seg)
    if m and m.group(1)[:3].lower() in MONTHS:
        return '%s-%02d' % (m.group(2), MONTHS[m.group(1)[:3].lower()])
    m = re.match(r'(\d{4})$', seg)
    return m.group(1) if m else None

def looks_like_name(seg, japanese):
    seg = seg.strip()
    if japanese and is_cjk(seg):
        return len(seg) <= 10 and not VENUE_WORDS.search(seg)
    words = seg.split()
    # A personal name ends in a capitalized surname; a title-cased phrase whose
    # last word is lowercase (e.g. "N-body methods") is NOT a name.  Latin
    # nobiliary particles (van/de/von...) are allowed mid-name.
    if not (1 < len(words) <= 5 and len(seg) < 45 and not re.search(r'\d', seg)
            and not VENUE_WORDS.search(seg) and seg[0].isupper()):
        return False
    return words[-1][0].isupper()

# a "LastAuthor. Title" boundary: a period+space whose preceding char is NOT a
# single-letter initial (so "David E. Keyes" is left intact, "Yokota. Title" splits).
AUTHOR_DOT = re.compile(r'^(.+?[^A-Z\s])\.\s+(\S.*)$')

def parse(text):
    """citation -> (authors, title, venue, date) — heuristic, review the output."""
    text = text.rstrip('.。 ')
    japanese = is_cjk(text)
    segs = [s.strip() for s in re.split(r'[,、，]| 、', text) if s.strip()]
    date = None
    while segs and (d := parse_date(segs[-1])):
        date = d; segs.pop()
    if not segs:
        return None
    # first segment (after the first) that looks like a venue; authors+title live
    # before it, so the author run must leave at least that last pre-venue segment
    # for the title.
    venue_idx = None
    for i in range(1, len(segs)):
        if VENUE_WORDS.search(segs[i]):
            venue_idx = i
            break
    # consume leading authors; an explicit "LastAuthor. Title" period ends the run
    # and hands the text after the period to the title.
    authors = []
    title_prefix = None
    i = 0
    n = len(segs)
    while i < n:
        cand = re.sub(r'^and\s+', '', segs[i]).strip()
        m = AUTHOR_DOT.match(cand)
        if m and looks_like_name(m.group(1), japanese):
            authors.append(m.group(1).strip())
            title_prefix = m.group(2).strip()
            i += 1
            break
        # never eat the last pre-venue segment (or the last segment) — it is the title
        if (venue_idx is not None and i >= venue_idx - 1) or (venue_idx is None and i >= n - 1):
            break
        if not looks_like_name(cand, japanese):
            break
        authors.append(cand)
        i += 1
    rest = segs[i:]
    if title_prefix is not None:
        rest = [title_prefix] + rest
    if not rest:
        return None
    # split title vs venue inside the remainder: prefer the first venue-looking
    # segment, else keep the first segment as the title.
    v = None
    for j in range(1, len(rest)):
        if VENUE_WORDS.search(rest[j]):
            v = j
            break
    if v is None:
        v = 1 if len(rest) > 1 else len(rest)
    title = ', '.join(rest[:v]).strip(' 「」"')
    venue = ', '.join(rest[v:])
    return authors, title, venue, date

def sole_author(text):
    """True if Rio Yokota is the only author of the citation (an invited talk)."""
    if re.match(r'^(Rio\s+Yokota|横田\s*理央)\s*[.:：]', text):
        return True
    parsed = parse(text)
    authors = parsed[0] if parsed else []
    return len(authors) == 1 and bool(re.search(r'Rio\s+Yokota|横田\s*理央', authors[0]))

def resolve_type(rm_type, text):
    if rm_type == 'talk_or_misc':
        return 'presentations' if sole_author(text) else 'misc'
    return rm_type

def to_record(text, rm_type, extra, data_date=None, data_doi=None, data_isbn=None,
              data_url=None,
              data_volume=None, data_number=None, data_pages=None, data_authors=None,
              data_authors_ja=None, data_authors_en=None, data_event=None,
              data_location=None, data_invited=None, data_publisher=None):
    rm_type = resolve_type(rm_type, text)
    parsed = parse(text)
    if not parsed:
        return None
    authors, title, venue, date = parsed
    if data_date:            # data-date attribute overrides the heuristic date
        date = data_date
    japanese = is_cjk(title)
    lang = 'ja' if japanese else 'en'
    if data_authors or data_authors_ja or data_authors_en:
        people = {}
        ja_authors = data_authors_ja or data_authors
        en_authors = data_authors_en or data_authors
        if ja_authors:
            people['ja'] = [{'name': a} for a in ja_authors]
        if en_authors:
            people['en'] = [{'name': a} for a in en_authors]
    else:
        people = {lang: [{'name': a} for a in authors]}
    doc = {}
    if rm_type in ('published_papers', 'misc'):
        doc['paper_title'] = {lang: title}
        doc['publication_name'] = {lang: venue}
        doc['authors'] = people
        if data_volume:
            doc['volume'] = data_volume
        if data_number:
            doc['number'] = data_number
        if data_pages:
            m = re.match(r'^([A-Za-z]?\d+)-([A-Za-z]?\d+)$', data_pages)
            if m:
                doc['starting_page'] = m.group(1)
                doc['ending_page'] = m.group(2)
            else:
                doc['starting_page'] = data_pages
    elif rm_type == 'books_etc':
        doc['book_title'] = {lang: title}
        doc['publisher'] = {lang: data_publisher or venue}
        doc['authors'] = people
        if data_isbn:
            doc['isbn'] = data_isbn
    else:
        doc['presentation_title'] = {lang: title}
        doc['event'] = {lang: data_event or venue}
        if data_location:
            doc['event_place'] = {lang: data_location}
        if data_invited is True:
            doc['invited'] = True
        doc['presenters'] = people
    if date:
        doc['publication_date'] = date
    if data_doi:
        doc['identifiers'] = {'doi': [data_doi]}
    elif data_url:
        doc['see_also'] = [{'label': 'url', '@id': data_url}]
    doc['languages'] = ['jpn' if japanese else 'eng']
    if rm_type != 'misc':   # misc gets no extras (extra is presentations-specific there)
        doc.update(extra)
    return {'insert': {'type': rm_type},
            'similar_merge': doc, 'priority': 'similar_data'}

def profile_lines(heading):
    """lines of the <p> blocks following an h3 heading on the profile page."""
    c = open(PROFILE, newline='', encoding='utf-8').read()
    m = re.search(r'<h3 class="heading">\s*%s.*?</h3>(.*?)(?=<h3|</article>)' % heading, c, re.S)
    if not m:
        return []
    text = html.unescape(re.sub(r'<[^>]+>', '\n', m.group(1)))
    # Preserve full-width Japanese parentheses while normalizing other width
    # variants: research-project rows use them to delimit the funding suffix,
    # while project titles may contain ordinary ASCII parentheses (for LLM,
    # grant categories, and H-matrices).
    lines = [re.sub(r'\s+', ' ', unicodedata.normalize(
                 'NFKC', l.replace('（', '\ue000').replace('）', '\ue001'))
                 .replace('\ue000', '（').replace('\ue001', '）')).strip()
             for l in text.split('\n')]
    return [l for l in lines if l and not l.startswith('&nbsp;')]

def parse_range(prefix):
    m = re.match(r'(\d{4})\s*(?:年)?\s*(?:(\d{1,2})\s*月)?\s*'
                 r'(?:[–―-]\s*(?:(\d{4})\s*(?:年)?\s*'
                 r'(?:(\d{1,2})\s*月)?)?)?$', prefix.strip())
    if not m:
        return None, None
    frm = m.group(1) + ('-%02d' % int(m.group(2)) if m.group(2) else '')
    to = m.group(3) + ('-%02d' % int(m.group(4)) if m.group(4) else '') if m.group(3) else None
    return frm, to

def split_school_department(value):
    """Split a Japanese university name from its following faculty/graduate school."""
    value = value.strip()
    m = re.match(r'(.+?大学)(.+)$', value)
    return (m.group(1).strip(), m.group(2).strip()) if m else (value, '')

def parse_education_line(line):
    m = re.match(r'(\d{4}\s*年\s*\d{1,2}\s*月)\s+(.+)$', line)
    if not m:
        return None
    date, rest = m.groups()
    degree = ''
    for suffix in (r'博士\([^)]*\)\s+取得', r'修士課程\s+修了',
                   r'博士課程\s+単位取得退学', r'単位取得退学', r'卒業', r'修了'):
        degree_m = re.search(r'\s+(' + suffix + r')$', rest)
        if degree_m:
            degree = degree_m.group(1)
            rest = rest[:degree_m.start()].strip()
            break
    if not rest or not degree:
        return None
    school, department = split_school_department(rest)
    doc = {'school_name': {'ja': school}, 'degree': {'ja': degree}}
    if department:
        doc['department'] = {'ja': department}
    _frm, to = parse_range(date)
    if to or _frm:
        doc['to_date'] = to or _frm
    return doc

def parse_research_experience_line(line):
    m = re.match(r'((?:\d{4}\s*年\s*\d{1,2}\s*月)'
                 r'(?:\s*[–―-]\s*(?:\d{4}\s*年\s*\d{1,2}\s*月)?)?)\s+(.+)$', line)
    if not m:
        return None
    prefix, rest = m.groups()
    parts = rest.strip().rsplit(' ', 1)
    if len(parts) != 2:
        return None
    organization, job_title = parts
    affiliation, department = split_school_department(organization)
    if not department and ' ' in organization:
        affiliation, department = organization.split(' ', 1)
    doc = {'affiliation': {'ja': affiliation}, 'job_title': {'ja': job_title}}
    if department:
        doc['department'] = {'ja': department}
    frm, to = parse_range(prefix)
    if frm:
        doc['from_date'] = frm
    if to:
        doc['to_date'] = to
    return doc

def parse_association_memberships(lines):
    """One association_memberships document per Japanese-comma-separated society."""
    docs = []
    for line in lines:
        for name in re.split(r'[、,]', line):
            name = name.strip()
            if name:
                docs.append({'association_name': {'ja' if is_cjk(name) else 'en': name}})
    return docs


API_BASE = 'https://api.researchmap.jp/%s/%%s' % PERMALINK
LIVE_TYPES = ['published_papers', 'books_etc', 'presentations', 'misc',
              'awards', 'media_coverage', 'committee_memberships',
              'research_projects']
SYNC_FIELDS = {
    'published_papers': ('paper_title', 'authors', 'publication_date',
                         'publication_name', 'see_also'),
    'books_etc': ('book_title', 'authors', 'publication_date',
                  'publisher', 'see_also'),
    'presentations': ('presentation_title', 'presenters', 'publication_date',
                      'event', 'see_also'),
    'misc': ('paper_title', 'authors', 'publication_date',
             'publication_name', 'see_also'),
    'awards': ('award_name', 'award_date'),
    'media_coverage': ('media_coverage_title', 'publisher', 'event',
                       'publication_date', 'location',
                       'media_coverage_type', 'see_also'),
    'committee_memberships': ('committee_name', 'association', 'from_date', 'to_date'),
    'research_projects': ('research_project_title', 'system_name',
                          'offer_organization', 'from_date', 'to_date'),
}

# These three profile types do not share a universal ``title`` field.  In
# particular, ResearchMap committee records have two valid shapes: some split
# the role and conference over committee_name/association, while others put
# both into committee_name.  Match their normalized combined text instead of
# comparing individual fields.
COMBINED_FIELDS = {
    'awards': ('title', 'award_name'),
    'committee_memberships': ('title', 'committee_name', 'association'),
    'research_projects': ('title', 'research_project_title'),
}

def text_values(value):
    """Yield scalar text values from ResearchMap's language dictionaries."""
    if isinstance(value, str):
        if value:
            yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from text_values(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from text_values(item)

def normalized_combined(item, rm_type):
    """Lowercase, de-punctuated combined identity text for profile CV types."""
    values = []
    for field in COMBINED_FIELDS[rm_type]:
        for value in text_values(item.get(field)):
            if value not in values:
                values.append(value)
    text = unicodedata.normalize('NFKC', ' '.join(values)).lower()
    # Canonicalize the three retained literal mistakes before removing
    # punctuation, so the corrected website wording still deduplicates the
    # older public ResearchMap record.
    text = re.sub(r'\bini\s+asia-pacific\s+region\b',
                  'in asia-pacific region', text)
    text = re.sub(r'\bsiam\s+cse\s*19\b', 'siam cse 2019', text)
    text = text.replace('安全 性', '安全性')
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    return re.sub(r'\s+', ' ', text).strip()

def normalized_combined_variants(item, rm_type):
    """Return combined keys for every available language variant.

    A ResearchMap item can carry both ja and en values for a field.  Those are
    alternatives, not consecutive identity text, so do not concatenate the
    two translations into a key that no single-language website row can match.
    """
    variants = {normalized_combined(item, rm_type)}
    languages = set()
    for field in COMBINED_FIELDS[rm_type]:
        value = item.get(field)
        if isinstance(value, dict):
            languages.update(value)
    for language in languages:
        variant = {}
        for field in COMBINED_FIELDS[rm_type]:
            value = item.get(field)
            variant[field] = value.get(language) if isinstance(value, dict) else value
        variants.add(normalized_combined(variant, rm_type))
    return {value for value in variants if value}

def combined_match(rm_type, desired, live):
    """Match a profile record by its normalized combined identity string."""
    wanted_keys = normalized_combined_variants(desired, rm_type)
    actual_keys = normalized_combined_variants(live, rm_type)
    if wanted_keys & actual_keys:
        return True
    # The one existing award is Japanese on the canonical website profile but
    # English in ResearchMap.  Its shared, specific ACM Gordon Bell stem plus
    # matching calendar year is a safe bilingual identity bridge.
    if rm_type == 'awards':
        wanted = normalized_combined(desired, rm_type)
        actual = normalized_combined(live, rm_type)
        wanted_year = str(desired.get('award_date', ''))[:4]
        live_year = str(live.get('award_date', ''))[:4]
        return (wanted_year and wanted_year == live_year and
                'acm gordon bell' in wanted and 'acm gordon bell' in actual)
    return False

def load_state():
    """Load both the legacy baseline array and the managed-registry shape."""
    if not os.path.exists(STATE):
        return {'baseline': [], 'managed_ids': {t: [] for t in LIVE_TYPES}}
    raw = json.load(open(STATE, encoding='utf-8'))
    if isinstance(raw, list):
        raw = {'baseline': raw, 'managed_ids': {}}
    if not isinstance(raw, dict):
        raise ValueError('researchmap state must be a list or object')
    baseline = raw.get('baseline', [])
    managed = raw.get('managed_ids', {})
    if not isinstance(baseline, list) or not isinstance(managed, dict):
        raise ValueError('invalid researchmap state fields')
    return {
        'baseline': baseline,
        'managed_ids': {
            t: sorted({str(x) for x in managed.get(t, []) if str(x)})
            for t in LIVE_TYPES
        },
    }

def save_state(state):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write('\n')

def fetch_live(rm_type):
    """Fetch all pages of a live researchmap collection, return list of item dicts."""
    items = []
    saw_valid = False
    url = API_BASE % rm_type
    while url:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        saw_valid = saw_valid or (isinstance(data, dict) and ('items' in data or 'total_items' in data))
        if isinstance(data, list):
            items.extend(data)
            url = None
        else:
            batch = data.get('items') if isinstance(data, dict) else None
            if batch is None:
                # some responses use JSON-LD style with '@graph' or similar
                batch = data.get('@graph', [])
            items.extend(batch)
            # researchmap's actual pagination lives under _links.next.href;
            # data['next']/data['pagination']['next'] are kept as fallbacks
            # in case other endpoints use a different shape.
            links = data.get('_links') if isinstance(data, dict) else None
            nxt = None
            if isinstance(links, dict):
                nxt_link = links.get('next')
                if isinstance(nxt_link, dict):
                    nxt = nxt_link.get('href')
                elif isinstance(nxt_link, str):
                    nxt = nxt_link
            if nxt is None:
                nxt = data.get('next') or (data.get('pagination') or {}).get('next')
            url = nxt if isinstance(nxt, str) else None
    if not items and not saw_valid:
        raise RuntimeError('fetch_live: got zero items back (empty or malformed response)')
    return items

def live_id(item):
    """Return the public API rm:id used by update/delete import grammar."""
    for field in ('rm:id', 'id', '@id'):
        value = item.get(field)
        if value is None:
            continue
        value = str(value).strip()
        if value:
            return value.rstrip('/').rsplit('/', 1)[-1]
    return None

def canonical_doi(value):
    if isinstance(value, dict):
        value = value.get('@id') or value.get('value')
    if not isinstance(value, str):
        return ''
    return re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value.strip(), flags=re.I).lower()

def item_dois(item):
    identifiers = item.get('identifiers') or {}
    values = identifiers.get('doi', []) if isinstance(identifiers, dict) else []
    if isinstance(values, str):
        values = [values]
    return {canonical_doi(v) for v in values if canonical_doi(v)}

def canonical_url(value):
    if not isinstance(value, str) or not value.strip():
        return ''
    try:
        p = urllib.parse.urlsplit(value.strip())
        if not p.scheme or not p.netloc:
            return value.strip().rstrip('/')
        path = re.sub(r'/+', '/', p.path).rstrip('/')
        scheme = 'https' if p.scheme.lower() in ('http', 'https') else p.scheme.lower()
        return urllib.parse.urlunsplit((scheme, p.netloc.lower(), path,
                                       p.query, ''))
    except ValueError:
        return value.strip().rstrip('/')

def item_urls(item):
    values = item.get('see_also') or []
    if isinstance(values, dict):
        values = [values]
    out = set()
    for value in values:
        url = value.get('@id') if isinstance(value, dict) else value
        url = canonical_url(url)
        if url:
            out.add(url)
    return out

def desired_title_keys(record):
    doc = record.get('similar_merge', {})
    keys = set()
    for field in ('paper_title', 'book_title', 'presentation_title',
                  'media_coverage_title'):
        value = doc.get(field)
        values = value.values() if isinstance(value, dict) else [value]
        for title in values:
            if isinstance(title, str) and title:
                keys.add(key(unicodedata.normalize('NFKC', title), limit=10**9))
    return keys

def match_live(record, live_items):
    """Return (unique item or None, ambiguity candidates, criterion)."""
    doc = record.get('similar_merge', {})
    rm_type = record.get('insert', {}).get('type')
    if rm_type in COMBINED_FIELDS:
        matches = [item for item in live_items if combined_match(rm_type, doc, item)]
        if len(matches) == 1:
            return matches[0], [], 'normalized combined text'
        if len(matches) > 1:
            return None, matches, 'normalized combined text'
        return None, [], None
    desired_dois = item_dois(doc)
    desired_urls = item_urls(doc)
    desired_titles = desired_title_keys(record)
    criteria = []
    if desired_dois:
        criteria.append(('DOI', lambda item: bool(desired_dois & item_dois(item))))
    if desired_urls:
        criteria.append(('URL', lambda item: bool(desired_urls & item_urls(item))))
    if desired_titles:
        criteria.append(('title', lambda item: bool(
            desired_titles & {key(unicodedata.normalize('NFKC', t), limit=10**9)
                              for t in live_titles(item)})))
    for label, predicate in criteria:
        matches = [item for item in live_items if predicate(item)]
        if len(matches) == 1:
            return matches[0], [], label
        if len(matches) > 1:
            return None, matches, label
    return None, [], None

def changed_doc(rm_type, desired, live):
    """Return only exporter-owned fields whose complete values differ."""
    changed = {}
    for field in SYNC_FIELDS[rm_type]:
        if field in desired:
            wanted = desired[field]
        elif field == 'see_also' and field in live:
            wanted = []
        else:
            continue
        if live.get(field) != wanted:
            changed[field] = wanted
    return changed

def build_sync(website, live_by_type, managed_ids):
    """Pure sync planner used by --sync and offline fixture tests."""
    matches = []
    ambiguous = []
    for text, _tkey, rm_type, record in website:
        if rm_type not in LIVE_TYPES:
            continue
        item, candidates, criterion = match_live(record, live_by_type.get(rm_type, []))
        matches.append([text, rm_type, record, item, candidates, criterion])

    # Two website entries resolving to one rm:id are also ambiguous.
    id_counts = {}
    for _text, rm_type, _record, item, _candidates, _criterion in matches:
        rid = live_id(item) if item else None
        if rid:
            id_counts[(rm_type, rid)] = id_counts.get((rm_type, rid), 0) + 1

    inserts, updates = [], []
    matched = {t: set() for t in LIVE_TYPES}
    protected = {t: set() for t in LIVE_TYPES}
    for text, rm_type, record, item, candidates, criterion in matches:
        candidate_ids = {live_id(x) for x in candidates if live_id(x)}
        if candidate_ids:
            protected[rm_type].update(candidate_ids)
            ambiguous.append((text, rm_type, criterion, sorted(candidate_ids)))
            continue
        if item is None:
            inserts.append((text, record))
            continue
        rid = live_id(item)
        if not rid:
            ambiguous.append((text, rm_type, 'missing rm:id', []))
            continue
        if id_counts[(rm_type, rid)] > 1:
            protected[rm_type].add(rid)
            ambiguous.append((text, rm_type, 'duplicate website match', [rid]))
            continue
        matched[rm_type].add(rid)
        diff = changed_doc(rm_type, record['similar_merge'], item)
        if diff:
            updates.append((text, {'update': {'type': rm_type, 'id': rid},
                                   'doc': diff}))

    deletes = []
    refreshed = {}
    for rm_type in LIVE_TYPES:
        old = {str(x) for x in managed_ids.get(rm_type, [])}
        live_ids = {live_id(x) for x in live_by_type.get(rm_type, []) if live_id(x)}
        delete_ids = sorted((old & live_ids) - matched[rm_type] - protected[rm_type])
        deletes.extend({'delete': {'type': rm_type, 'id': rid}}
                       for rid in delete_ids)
        # Retain IDs until the public read API confirms deletion; otherwise a
        # failed/manual-skipped upload would make a pending delete unrecoverable.
        refreshed[rm_type] = sorted(matched[rm_type] | (old & live_ids))
    return inserts, updates, deletes, refreshed, ambiguous

def sync_live(dry_run=False):
    live_by_type = {}
    for rm_type in LIVE_TYPES:
        try:
            live_by_type[rm_type] = fetch_live(rm_type)
        except Exception as e:
            print(f'ERROR: could not fetch live {rm_type} from researchmap API '
                  f'({e.__class__.__name__}: {e}); aborting without writes',
                  file=sys.stderr)
            return 1
    state = load_state()
    inserts, updates, deletes, refreshed, ambiguous = build_sync(
        website_records(), live_by_type, state['managed_ids'])
    for text, rm_type, criterion, ids in ambiguous:
        print(f'AMBIGUOUS ({rm_type}, {criterion}, ids={ids}): {text[:100]}',
              file=sys.stderr)
    operations = ([record for _text, record in inserts] +
                  [record for _text, record in updates] + deletes)
    for record in operations:
        print(json.dumps(record, ensure_ascii=False))
    print(f'\n{len(inserts)} inserts / {len(updates)} updates / '
          f'{len(deletes)} deletes; {len(ambiguous)} ambiguous skipped')
    if dry_run:
        print('dry run: no import or state file written')
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if operations:
        with open(OUT, 'w', encoding='utf-8') as f:
            for record in operations:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f'written to {OUT}; review every line before upload')
    elif os.path.exists(OUT):
        os.remove(OUT)
    state['managed_ids'] = refreshed
    save_state(state)
    return 0

def live_title(item):
    """Extract a title string from a live researchmap item dict, any language."""
    for field in ('paper_title', 'book_title', 'presentation_title',
                  'media_coverage_title', 'title', 'misc_title'):
        v = item.get(field)
        if isinstance(v, dict):
            for lang in ('ja', 'en'):
                if v.get(lang):
                    return v[lang]
            for vv in v.values():
                if vv:
                    return vv
        elif isinstance(v, str) and v:
            return v
    return ''

def live_titles(item):
    """Yield ALL title strings (every language variant) from a live item."""
    for field in ('paper_title', 'book_title', 'presentation_title',
                  'media_coverage_title', 'title', 'misc_title'):
        v = item.get(field)
        if isinstance(v, dict):
            for vv in v.values():
                if vv:
                    yield vv
        elif isinstance(v, str) and v:
            yield v

def live_title_keys(rm_type):
    """Set of normalized title keys currently on researchmap for a given type.
    Collects keys for EVERY language variant of every title-ish field, so a
    website entry matching the non-preferred language variant still matches."""
    keys = set()
    for item in fetch_live(rm_type):
        for t in live_titles(item):
            keys.add(key(unicodedata.normalize('NFKC', t)))
    return keys

def website_records():
    """All (text, title_key, rm_type_after_resolve, record) for Rio-Yokota
    entries on the Achievements page plus the profile CV sections, in the
    same categories used for live researchmap collections."""
    out = []
    for anchor, (rm_type, extra) in SECTIONS.items():
        for text, data_date, data_doi, data_isbn, data_url, data_volume, data_number, data_pages, data_authors, data_authors_ja, data_authors_en, data_event, data_location, data_invited, data_publisher in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_isbn, data_url,
                            data_volume, data_number, data_pages, data_authors,
                            data_authors_ja, data_authors_en, data_event,
                            data_location, data_invited, data_publisher)
            if rec is None:
                print(f'WARNING: could not parse, add manually: {text[:90]}', file=sys.stderr)
                continue
            parsed = parse(text)
            title = parsed[1] if parsed else text
            out.append((text, key(title), rec['insert']['type'], rec))
    for text, rm_type, doc in profile_records():
        rec = {'insert': {'type': rm_type}, 'similar_merge': doc, 'priority': 'similar_data'}
        title = text
        for field, val in doc.items():
            if (field.endswith('_title') or field.endswith('_name')) and isinstance(val, dict):
                title = next(iter(val.values()), text)
                break
        out.append((text, key(title), rm_type, rec))
    return out

def check_live(dry_run=False):
    """Diff website entries against live researchmap.jp data (instead of the
    local state file) and write tools/out/researchmap-import.jsonl."""
    live_keys = {}
    live_items = {}
    for rm_type in LIVE_TYPES:
        try:
            live_items[rm_type] = fetch_live(rm_type)
            live_keys[rm_type] = {
                key(unicodedata.normalize('NFKC', title))
                for item in live_items[rm_type] for title in live_titles(item)
            }
        except Exception as e:
            print(f'ERROR: could not fetch live {rm_type} from researchmap API '
                  f'({e.__class__.__name__}: {e}); aborting without writing {OUT} '
                  f'(refusing to treat an unreachable API as "everything is new")',
                  file=sys.stderr)
            return 1

    all_live = set().union(*live_keys.values()) if live_keys else set()

    new = []
    profile_counts = {rm_type: {'inserts': 0, 'matches': 0, 'ambiguous': 0}
                      for rm_type in COMBINED_FIELDS}
    for text, tkey, rm_type, rec in website_records():
        if rm_type not in live_keys:
            continue
        if rm_type in COMBINED_FIELDS:
            item, candidates, _criterion = match_live(rec, live_items[rm_type])
            if item:
                profile_counts[rm_type]['matches'] += 1
                continue
            if candidates:
                profile_counts[rm_type]['ambiguous'] += 1
                print(f'AMBIGUOUS ({rm_type}, normalized combined text): {text[:100]}',
                      file=sys.stderr)
                continue
            profile_counts[rm_type]['inserts'] += 1
            new.append((text, rec))
            continue
        # Match against ALL live types, not just the mapped one: an entry may be
        # stored under a different researchmap category live than the site maps
        # it to.
        if tkey in all_live:
            continue
        # parse()'s venue-detection heuristic sometimes lumps extra trailing
        # text (series name, page numbers) onto the parsed title, so an exact
        # key match against the live (clean) title can miss a real match.
        # Fall back to checking whether the live title's key is a contiguous
        # substring of the full, unparsed citation text's key -- the true
        # title's characters are always present intact there even when
        # parse() over-captured.
        # key() truncates to 70 chars by default; use an untruncated key here so
        # a long author prefix cannot push the title out of the compared window.
        full_key = key(text, limit=10**9)
        # Also accept the REVERSE containment: items uploaded during the
        # 2026-07-06 migration can carry over-captured long titles (title +
        # venue etc.), so the live key may be longer than the clean parsed
        # website title; accept if the website title key appears inside a
        # live key.
        if any(lk and (lk in full_key or (tkey and tkey in lk)) for lk in all_live):
            continue
        new.append((text, rec))

    for rm_type, counts in profile_counts.items():
        print(f'LIVE {rm_type}: {counts["inserts"]} inserts / '
              f'{counts["matches"]} matches / {counts["ambiguous"]} ambiguous')

    for text, rec in new:
        print('NEW:', text[:100])

    if new and dry_run:
        print(f'\n{len(new)} NEW entries not found live (dry run: no files written)')
    elif new:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'w', encoding='utf-8') as f:
            for _, rec in new:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(f'\n{len(new)} NEW entries not found live, written to {OUT}')
    else:
        if not dry_run and os.path.exists(OUT):
            os.remove(OUT)
        print('\n0 NEW entries found (website matches live researchmap)')
    return 0

def media_coverage_records():
    """Bilingual media-coverage rows, paired by position from JP and EN pages."""
    en_profile = os.path.join(ROOT, 'en', 'member', 'yokota.html')

    def page_rows(path, heading, japanese):
        c = open(path, newline='', encoding='utf-8').read()
        m = re.search(r'<h3 class="heading">\s*%s\s*</h3>(.*?)(?=<h3|</article>)'
                      % re.escape(heading), c, re.S | re.I)
        if not m:
            return []
        rows = []
        for fragment in re.split(r'<br\s*/?>|</p>', m.group(1), flags=re.I):
            url_m = re.search(r'<a\b[^>]*\bhref=["\']([^"\']+)', fragment,
                              flags=re.I)
            text = html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()
            if japanese:
                match = re.match(r'^(\d{4})年(\d{1,2})月(\d{1,2})日\u3000+'
                                 r'(.+?)\u3000+(.+)$', text)
            else:
                match = re.match(r'^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\u3000+'
                                 r'(.+?)\u3000+(.+)$', text)
            if not match:
                continue
            if japanese:
                year, month, day, outlet, title = match.groups()
                outlet_m = re.match(r'^(.*?)(?:（([^）]+)）)?$', outlet.strip())
                date = '%s-%02d-%02d' % (year, int(month), int(day))
            else:
                month_name, day, year, outlet, title = match.groups()
                month = MONTHS.get(month_name[:3].lower())
                if not month:
                    continue
                # The final parenthetical is the medium; earlier parentheses
                # remain part of the English outlet name (e.g. The Nikkei).
                outlet_m = re.match(r'^(.*?)(?:\s+\(([^()]*)\))?$', outlet.strip())
                date = '%s-%02d-%02d' % (year, month, int(day))
            publisher = outlet_m.group(1).strip()
            location = (outlet_m.group(2) or '').strip()
            rows.append((text, date, publisher, location, title.strip(),
                         html.unescape(url_m.group(1)) if url_m else None))
        return rows

    jp_rows = page_rows(PROFILE, 'メディア報道', True)
    en_rows = page_rows(en_profile, 'Media Coverage', False)
    if len(jp_rows) != len(en_rows):
        raise ValueError('JP/EN media coverage row count differs: %d != %d' %
                         (len(jp_rows), len(en_rows)))
    recs = []
    for jp, en in zip(jp_rows, en_rows):
        jp_text, date, jp_publisher, jp_location, jp_title, jp_url = jp
        _en_text, en_date, en_publisher, en_location, en_title, en_url = en
        if date != en_date or jp_url != en_url:
            raise ValueError('JP/EN media coverage row mismatch: %s' % jp_text)
        doc = {
            'media_coverage_title': {'ja': jp_title, 'en': en_title},
            'event': {'ja': jp_publisher, 'en': en_publisher},
            'publication_date': date,
            'location': {'ja': jp_location, 'en': en_location},
            'media_coverage_type': 'internet' if jp_url else 'paper',
        }
        if jp_url:
            doc['see_also'] = [{'label': 'url', '@id': jp_url}]
        recs.append((jp_text, 'media_coverage', doc))
    return recs

def profile_records():
    """CV items (education, careers, societies, awards, committees, projects) -> records."""
    recs = []
    for line in profile_lines('学歴'):
        doc = parse_education_line(line)
        if doc:
            recs.append((line, 'education', doc))
    for line in profile_lines('職歴'):
        doc = parse_research_experience_line(line)
        if doc:
            recs.append((line, 'research_experience', doc))
    for doc in parse_association_memberships(profile_lines('所属学会')):
        name = next(iter(doc['association_name'].values()))
        recs.append((name, 'association_memberships', doc))
    for line in profile_lines('受賞歴'):
        m = re.match(r'(\S+)\s+(.+)$', line)
        if not m: continue
        date, _ = parse_range(m.group(1))
        name = m.group(2).strip()
        lang = 'ja' if is_cjk(name) else 'en'
        doc = {'award_name': {lang: name}}
        if date: doc['award_date'] = date
        recs.append((line, 'awards', doc))
    recs.extend(media_coverage_records())
    for line in profile_lines('委員歴'):
        m = re.match(r'(\S+)\s+(.+)$', line)
        if not m: continue
        frm, to = parse_range(m.group(1))
        parts = [p.strip() for p in m.group(2).split(' — ', 1)]
        name = parts[0] or (parts[1] if len(parts) > 1 else '')
        assoc = parts[1] if len(parts) > 1 and parts[0] else ''
        if not name: continue
        lang = 'ja' if is_cjk(name + assoc) else 'en'
        doc = {'committee_name': {lang: name}}
        if assoc: doc['association'] = {lang: assoc}
        if frm: doc['from_date'] = frm
        if to: doc['to_date'] = to
        recs.append((line, 'committee_memberships', doc))
    for line in profile_lines('研究課題'):
        # The project title itself may contain parentheses (for example LLM).
        # Prefer the full-width funding wrapper used by the JP page; an ASCII
        # fallback preserves support for records without that wrapper.
        m = re.match(r'(\S+)\s+(.+)（(.+)）$', line)
        if not m:
            m = re.match(r'(\S+)\s+(.+)\((.+)\)$', line)
        if not m: continue
        frm, to = parse_range(m.group(1))
        title = m.group(2).strip()
        fund = m.group(3)
        lang = 'ja' if is_cjk(title) else 'en'
        doc = {'research_project_title': {lang: title}}
        parts = [x.strip() for x in re.split(r'[、,]', fund) if x.strip()]
        if parts:
            doc['system_name'] = {lang: parts[0]}
            if len(parts) > 1:
                doc['offer_organization'] = {lang: parts[-1]}
        if frm: doc['from_date'] = frm
        if to: doc['to_date'] = to
        recs.append((line, 'research_projects', doc))
    return recs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--init', action='store_true', help='snapshot baseline, export nothing')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--check-live', action='store_true',
                     help='diff against live researchmap.jp data instead of the state file')
    ap.add_argument('--sync', action='store_true',
                    help='live diff with inserts, partial updates, and managed deletes')
    args = ap.parse_args()

    if args.sync and (args.check_live or args.init):
        ap.error('--sync cannot be combined with --check-live or --init')

    if args.sync:
        sys.exit(sync_live(dry_run=args.dry_run))

    if args.check_live:
        sys.exit(check_live(dry_run=args.dry_run))

    state_data = load_state()
    state = set(state_data['baseline'])

    seen, new = [], []
    for anchor, (rm_type, extra) in SECTIONS.items():
        for text, data_date, data_doi, data_isbn, data_url, data_volume, data_number, data_pages, data_authors, data_authors_ja, data_authors_en, data_event, data_location, data_invited, data_publisher in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            k = key(text)
            seen.append(k)
            if k in state or args.init:
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_isbn, data_url,
                            data_volume, data_number, data_pages, data_authors,
                            data_authors_ja, data_authors_en, data_event,
                            data_location, data_invited, data_publisher)
            if rec:
                new.append((text, rec))
            else:
                print(f'WARNING: could not parse, add manually: {text[:90]}', file=sys.stderr)

    # CV items on the personal page remain local-baseline, insert-only records.
    for text, rm_type, doc in profile_records():
        k = key(text)
        seen.append(k)
        if k in state or args.init:
            continue
        new.append((text, {'insert': {'type': rm_type},
                           'similar_merge': doc, 'priority': 'similar_data'}))

    if args.init:
        state_data['baseline'] = sorted(seen)
        save_state(state_data)
        print(f'baseline saved: {len(seen)} Yokota entries recorded, nothing exported')
        return

    if not new:
        print('no new entries since last export')
        return
    for text, rec in new:
        print('NEW:', text[:100])
        if args.dry_run:
            print('  ->', json.dumps(rec, ensure_ascii=False)[:200])
    if args.dry_run:
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        for _, rec in new:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    state_data['baseline'] = sorted(set(state) | set(seen))
    save_state(state_data)
    print(f'\n{len(new)} entries written to {OUT}')
    print('Upload on researchmap: 設定 > インポート (or push via WebAPI).')

if __name__ == '__main__':
    main()

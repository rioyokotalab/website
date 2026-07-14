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
MATCH_OVERRIDES = os.path.join(ROOT, 'tools',
                               'researchmap-match-overrides.json')
PERMALINK = 'rioyokota'

SECTIONS = {   # anchor -> (rm type, extra fields)
    # Mapping (agreed 2026-07-06): peer-reviewed sections -> Papers;
    # book sections -> Books and Other Publications; non-peer-reviewed
    # sections -> Presentations if Rio Yokota is the sole author (invited
    # talks), Misc. otherwise ('talk_or_misc' is resolved per entry).
    'sub001': ('published_papers', {'published_paper_type': 'scientific_journal', 'referee': True}),
    'sub002': ('books_etc', {'referee': False}),
    'sub003': ('books_etc', {'referee': False}),
    'sub004': ('published_papers', {'published_paper_type': 'international_conference_proceedings', 'referee': True}),
    'sub005': ('published_papers', {'published_paper_type': 'symposium', 'referee': True}),
    'sub006': ('talk_or_misc', {'is_international_presentation': True}),
    'sub007': ('talk_or_misc', {'is_international_presentation': False}),
}
REQUIRED_TITLE_FIELDS = {
    'published_papers': 'paper_title',
    'misc': 'paper_title',
    'books_etc': 'book_title',
    'presentations': 'presentation_title',
}

# ResearchMap exposes additional system-derived identifier/link values in GET
# responses, but its V2 schema rejects those values when they are echoed in an
# update. Keep only nested keys and labels that the schema permits callers to
# write for each achievement type.
EDITABLE_IDENTIFIER_KINDS = {
    'published_papers': frozenset(('doi', 'issn', 'e_issn', 'isbn')),
    'misc': frozenset(('doi', 'issn', 'e_issn', 'isbn')),
    'books_etc': frozenset(('doi', 'isbn', 'asin', 'ean')),
    'presentations': frozenset(),
}
EDITABLE_SEE_ALSO_LABELS = {
    'published_papers': frozenset(('url', 'doi', 'rm:research_projects')),
    'misc': frozenset(('url', 'doi', 'rm:research_projects')),
    'books_etc': frozenset(('url', 'doi', 'rm:research_projects')),
    'presentations': frozenset(('url', 'rm:research_projects')),
    'awards': frozenset(('url',)),
    'media_coverage': frozenset(('url',)),
    'committee_memberships': frozenset(('url',)),
    'research_projects': frozenset(('url',)),
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
DATA_BOOK_TITLE = re.compile(r'\bdata-book-title\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_BOOK_ROLE = re.compile(r'\bdata-book-role\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_TITLE = re.compile(r'\bdata-title\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_VENUE = re.compile(r'\bdata-venue\s*=\s*["\']([^"\']*)["\']', re.I)
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

def attr_text(match):
    """Return a stripped, HTML-decoded data-attribute value."""
    return html.unescape(match.group(1)).strip() if match else None

def localized(value, lang):
    """Use both ResearchMap language slots when verified text is English."""
    if lang == 'en':
        return {'ja': value, 'en': value}
    return {'ja': value}

def complete_required_title(value):
    """Return a title with both language slots required by bulk import."""
    if isinstance(value, str):
        current = {'ja': value} if value else {}
    elif isinstance(value, dict):
        current = {lang: title for lang, title in value.items()
                   if lang in ('ja', 'en') and title}
    else:
        current = {}
    fallback = current.get('ja') or current.get('en')
    if fallback:
        current.setdefault('ja', fallback)
        current.setdefault('en', fallback)
    return current

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
    data_event, data_location, data_invited, data_publisher, data_book_title,
    data_book_role, data_title, data_venue) for each <li>;
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
        data_date = norm_date(attr_text(dm)) if dm else None
        doi_m = DATA_DOI.search(tag)
        data_doi = None
        if doi_m:
            data_doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '',
                              attr_text(doi_m), flags=re.I) or None
        isbn_m = DATA_ISBN.search(tag)
        data_isbn = attr_text(isbn_m)
        data_isbn = data_isbn or None
        url_m = DATA_URL.search(tag)
        data_url = attr_text(url_m)
        data_url = data_url or None
        volume_m = DATA_VOLUME.search(tag)
        data_volume = attr_text(volume_m)
        data_volume = data_volume or None
        number_m = DATA_NUMBER.search(tag)
        data_number = attr_text(number_m)
        data_number = data_number or None
        pages_m = DATA_PAGES.search(tag)
        data_pages = attr_text(pages_m)
        data_pages = data_pages or None
        authors_m = DATA_AUTHORS.search(tag)
        data_authors = split_authors(attr_text(authors_m)) if authors_m else None
        data_authors = data_authors or None
        authors_ja_m = DATA_AUTHORS_JA.search(tag)
        data_authors_ja = split_authors(attr_text(authors_ja_m)) if authors_ja_m else None
        data_authors_ja = data_authors_ja or None
        authors_en_m = DATA_AUTHORS_EN.search(tag)
        data_authors_en = split_authors(attr_text(authors_en_m)) if authors_en_m else None
        data_authors_en = data_authors_en or None
        event_m = DATA_EVENT.search(tag)
        data_event = attr_text(event_m)
        data_event = data_event or None
        location_m = DATA_LOCATION.search(tag)
        data_location = attr_text(location_m)
        data_location = data_location or None
        inv_m = DATA_INVITED.search(tag)
        data_invited = (attr_text(inv_m).lower() == 'true') if inv_m else None
        publisher_m = DATA_PUBLISHER.search(tag)
        data_publisher = attr_text(publisher_m)
        data_publisher = data_publisher or None
        book_title_m = DATA_BOOK_TITLE.search(tag)
        data_book_title = attr_text(book_title_m)
        data_book_title = data_book_title or None
        book_role_m = DATA_BOOK_ROLE.search(tag)
        data_book_role = attr_text(book_role_m)
        data_book_role = data_book_role or None
        title_m = DATA_TITLE.search(tag)
        data_title = attr_text(title_m)
        data_title = data_title or None
        venue_m = DATA_VENUE.search(tag)
        data_venue = attr_text(venue_m)
        data_venue = data_venue or None
        p = strip_achievement_links(p)
        t = re.sub(r'</li>', '', re.sub(r'<[^>]+>', '', p), flags=re.I)
        t = unicodedata.normalize('NFKC', t).replace('&amp;', '&').replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
        out.append((re.sub(r'\s+', ' ', t).strip(), data_date, data_doi, data_isbn, data_url,
                    data_volume, data_number, data_pages, data_authors,
                    data_authors_ja, data_authors_en, data_event, data_location,
                    data_invited, data_publisher, data_book_title,
                    data_book_role, data_title, data_venue))
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
              data_location=None, data_invited=None, data_publisher=None,
              data_book_title=None, data_book_role=None, data_title=None,
              data_venue=None):
    rm_type = resolve_type(rm_type, text)
    parsed = parse(text)
    if not parsed:
        return None
    authors, title, venue, date = parsed
    if data_title:
        title = data_title
    if data_venue:
        venue = data_venue
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
        doc['paper_title'] = localized(title, lang)
        doc['publication_name'] = localized(venue, lang)
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
        doc['book_title'] = localized(data_book_title or title, lang)
        if data_book_title:
            doc['book_owner_range'] = localized(title, lang)
        if data_book_role:
            doc['book_owner_role'] = data_book_role
        if data_pages:
            doc['rep_page'] = data_pages
        doc['publisher'] = localized(data_publisher or venue, lang)
        doc['authors'] = people
    else:
        doc['presentation_title'] = localized(title, lang)
        doc['event'] = localized(data_event or venue, lang)
        if data_location:
            doc['location'] = localized(data_location, lang)
        if data_invited is True:
            doc['invited'] = True
            doc['presentation_type'] = 'invited_oral_presentation'
        doc['presenters'] = people
    title_field = REQUIRED_TITLE_FIELDS[rm_type]
    doc[title_field] = complete_required_title(doc[title_field])
    if date:
        doc['publication_date'] = date
    identifier_kinds = EDITABLE_IDENTIFIER_KINDS.get(rm_type, frozenset())
    identifiers = {}
    if data_doi and 'doi' in identifier_kinds:
        identifiers['doi'] = [data_doi]
    if data_isbn and 'isbn' in identifier_kinds:
        identifiers['isbn'] = [data_isbn]
    if identifiers:
        doc['identifiers'] = identifiers
    elif data_url:
        doc['see_also'] = [{'label': 'url', '@id': data_url}]
    doc['languages'] = ['jpn' if japanese else 'eng']
    if rm_type == 'misc':
        doc['referee'] = False
        doc['invited'] = False
    if rm_type != 'misc':   # misc gets no extras (extra is presentations-specific there)
        doc.update(extra)
    return {'insert': {'type': rm_type},
            'similar_merge': doc, 'priority': 'similar_data'}

def profile_lines(heading):
    """lines of the <p> blocks following an h3 heading on the profile page."""
    with open(PROFILE, newline='', encoding='utf-8') as source:
        c = source.read()
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

def split_trailing_parenthetical(value, opening, closing):
    """Split the last balanced top-level parenthetical when it ends value."""
    depth = 0
    start = None
    spans = []
    for index, char in enumerate(value):
        if char == opening:
            if depth == 0:
                start = index
            depth += 1
        elif char == closing and depth:
            depth -= 1
            if depth == 0:
                spans.append((start, index))
    if not spans or spans[-1][1] != len(value) - 1:
        return None
    start, end = spans[-1]
    prefix = value[:start].strip()
    content = value[start + 1:end].strip()
    return (prefix, content) if prefix and content else None

def split_funding_label(value):
    """Return ResearchMap system/category fields from a funding label."""
    value = value.strip()
    for system in ('科学研究費助成事業', '厚生労働科学研究費'):
        if value.startswith(system + ' '):
            return system, value[len(system):].strip()
    nested = split_trailing_parenthetical(value, '（', '）')
    if nested and nested[0] == '国際共同研究加速基金':
        return nested
    return value, ''

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
    doc = {'affiliation': {'ja': school}}
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
    doc = {'affiliation': {'ja': affiliation}, 'job': {'ja': job_title}}
    if department:
        doc['section'] = {'ja': department}
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
                docs.append({'academic_society_name':
                             {'ja' if is_cjk(name) else 'en': name}})
    return docs


API_BASE = 'https://api.researchmap.jp/%s/%%s' % PERMALINK
LIVE_TYPES = ['published_papers', 'books_etc', 'presentations', 'misc',
              'awards', 'media_coverage', 'committee_memberships',
              'research_projects']
SYNC_FIELDS = {
    'published_papers': ('paper_title', 'authors', 'publication_date',
                         'publication_name', 'volume', 'number',
                         'starting_page', 'ending_page', 'identifiers',
                         'see_also', 'languages', 'published_paper_type',
                         'referee'),
    'books_etc': ('book_title', 'authors', 'publication_date',
                  'book_owner_role', 'book_owner_range', 'publisher',
                  'rep_page', 'identifiers', 'see_also', 'languages',
                  'referee'),
    'presentations': ('presentation_title', 'presenters', 'publication_date',
                      'event', 'location', 'invited', 'presentation_type',
                      'is_international_presentation', 'see_also', 'languages'),
    'misc': ('paper_title', 'authors', 'publication_date',
             'publication_name', 'volume', 'number', 'starting_page',
             'ending_page', 'identifiers', 'see_also', 'languages',
             'referee', 'invited'),
    'awards': ('award_name', 'award_date'),
    'media_coverage': ('media_coverage_title', 'publisher', 'event',
                       'publication_date', 'location',
                       'media_coverage_type', 'see_also'),
    'committee_memberships': ('committee_name', 'association', 'from_date', 'to_date'),
    'research_projects': ('research_project_title', 'system_name',
                          'category', 'offer_organization', 'from_date', 'to_date'),
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

def load_match_overrides(path=MATCH_OVERRIDES):
    """Load reviewed exact-match decisions for otherwise ambiguous records."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as source:
        data = json.load(source)
    if data.get('schema_version') != 1 or not isinstance(
            data.get('records'), dict):
        raise ValueError('invalid ResearchMap match-override file')
    allowed = {'match', 'equivalent', 'distinct', 'hold'}
    for selector, decision in data['records'].items():
        if not isinstance(selector, str) or not selector:
            raise ValueError('empty ResearchMap match-override selector')
        if not isinstance(decision, dict) or decision.get('action') not in allowed:
            raise ValueError('invalid ResearchMap match override: %s' % selector)
        if not decision.get('reason'):
            raise ValueError('ResearchMap match override lacks reason: %s' %
                             selector)
        if (decision['action'] in {'match', 'equivalent'} and
                not decision.get('target')):
            raise ValueError('ResearchMap match override lacks target: %s' %
                             selector)
        if (decision['action'] in {'distinct', 'hold'} and
                decision.get('target') is not None):
            raise ValueError('ResearchMap non-match override has target: %s' %
                             selector)
        candidates = decision.get('candidates', [])
        if not isinstance(candidates, list) or len(candidates) != len(
                set(candidates)):
            raise ValueError('invalid override candidates: %s' % selector)
    return data['records']

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

def canonical_isbn(value):
    """Normalize ISBN-10/13 to the equivalent ISBN-13 digit string."""
    if isinstance(value, dict):
        value = value.get('@id') or value.get('value')
    if not isinstance(value, str):
        return ''
    digits = re.sub(r'[^0-9X]', '', value.upper())
    if len(digits) == 10:
        body = '978' + digits[:9]
        check = (10 - sum((1 if i % 2 == 0 else 3) * int(digit)
                          for i, digit in enumerate(body)) % 10) % 10
        return body + str(check)
    return digits if len(digits) == 13 else ''

def item_isbns(item):
    identifiers = item.get('identifiers') or {}
    values = identifiers.get('isbn', []) if isinstance(identifiers, dict) else []
    if isinstance(values, str):
        values = [values]
    return {canonical_isbn(value) for value in values if canonical_isbn(value)}

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
    for field in ('paper_title', 'book_title', 'book_owner_range',
                  'presentation_title',
                  'media_coverage_title'):
        value = doc.get(field)
        values = value.values() if isinstance(value, dict) else [value]
        for title in values:
            if isinstance(title, str) and title:
                keys.add(key(unicodedata.normalize('NFKC', title), limit=10**9))
    return keys

def dates_compatible(desired, live):
    """Compare ResearchMap dates while allowing a more precise suffix."""
    if not isinstance(desired, str) or not isinstance(live, str):
        return False
    return (desired == live or desired.startswith(live + '-') or
            live.startswith(desired + '-'))

def item_title_keys(item):
    return {key(unicodedata.normalize('NFKC', title), limit=10**9)
            for title in live_titles(item)}

def fuzzy_title_match(desired_titles, doc, item):
    """Containment fallback gated by date and independent record context."""
    live_date = item.get('publication_date')
    if (not dates_compatible(doc.get('publication_date'), live_date) or
            not fuzzy_context_match(doc, item)):
        return False
    for desired in desired_titles:
        for current in item_title_keys(item):
            if min(len(desired), len(current)) >= 20 and \
                    (desired in current or current in desired):
                return True
    return False

def normalized_field_values(item, fields):
    values = set()
    for field in fields:
        for value in text_values(item.get(field)):
            normalized = key(unicodedata.normalize('NFKC', value), limit=10**9)
            if normalized:
                values.add(normalized)
    return values

def fuzzy_context_match(desired, live):
    """Require corroborating contributor or venue context for fuzzy titles."""
    wanted_people = normalized_field_values(desired,
                                            ('authors', 'presenters'))
    live_people = normalized_field_values(live, ('authors', 'presenters'))
    if wanted_people and live_people:
        overlap = wanted_people & live_people
        smaller = min(len(wanted_people), len(live_people))
        if ((len(wanted_people) == len(live_people) == len(overlap) == 1) or
                (len(overlap) >= 2 and len(overlap) * 2 >= smaller)):
            return True

    fields = ('publication_name', 'event', 'publisher')
    wanted_venues = normalized_field_values(desired, fields)
    live_venues = normalized_field_values(live, fields)
    return bool(wanted_venues and live_venues and any(
        min(len(a), len(b)) >= 4 and (a in b or b in a)
        for a in wanted_venues for b in live_venues))

def cross_type_context_match(desired, live):
    """Require matching date and venue before suppressing a cross-type insert."""
    if not dates_compatible(desired.get('publication_date'),
                            live.get('publication_date')):
        return False
    fields = ('publication_name', 'event', 'publisher')
    wanted = normalized_field_values(desired, fields)
    current = normalized_field_values(live, fields)
    return bool(wanted and current and any(
        min(len(a), len(b)) >= 4 and (a in b or b in a)
        for a in wanted for b in current))

def project_context_match(desired, live):
    """Fallback for translated project titles with the same grant and years."""
    wanted_system = normalized_field_values(desired, ('system_name',))
    live_system = normalized_field_values(live, ('system_name',))
    if not (wanted_system & live_system):
        return False
    for field in ('from_date', 'to_date'):
        if desired.get(field) and live.get(field) and not dates_compatible(
                desired[field], live[field]):
            return False
    return bool(desired.get('from_date') and live.get('from_date'))

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
        if rm_type == 'research_projects':
            matches = [item for item in live_items
                       if project_context_match(doc, item)]
            if len(matches) == 1:
                return matches[0], [], 'project grant/date context'
            if len(matches) > 1:
                return None, matches, 'project grant/date context'
        return None, [], None
    desired_dois = item_dois(doc)
    desired_isbns = item_isbns(doc)
    desired_urls = item_urls(doc)
    desired_titles = desired_title_keys(record)
    criteria = []
    if desired_dois:
        criteria.append(('DOI', lambda item: bool(desired_dois & item_dois(item))))
    if desired_isbns:
        criteria.append(('ISBN', lambda item: bool(desired_isbns & item_isbns(item))))
    if desired_urls:
        criteria.append(('URL', lambda item: bool(desired_urls & item_urls(item))))
    if desired_titles:
        criteria.append(('title', lambda item: bool(
            desired_titles & item_title_keys(item))))
        criteria.append(('title/date containment', lambda item:
                         fuzzy_title_match(desired_titles, doc, item)))
    for label, predicate in criteria:
        matches = [item for item in live_items if predicate(item)]
        if len(matches) == 1:
            return matches[0], [], label
        if len(matches) > 1:
            return None, matches, label
    return None, [], None

def normalized_identifier_values(kind, values):
    """Normalize one identifier list for non-destructive equality checks."""
    if isinstance(values, str):
        values = [values]
    out = set()
    for value in values or []:
        if isinstance(value, dict):
            value = value.get('@id') or value.get('value')
        if not isinstance(value, str):
            continue
        if kind == 'doi':
            value = canonical_doi(value)
        elif kind == 'isbn':
            value = canonical_isbn(value)
        else:
            value = value.strip()
        if value:
            out.add(value)
    return out

def merged_identifiers(rm_type, wanted, current):
    """Merge caller-editable identifiers without echoing managed keys."""
    current = dict(current) if isinstance(current, dict) else {}
    allowed = EDITABLE_IDENTIFIER_KINDS.get(rm_type, frozenset())
    merged = {kind: values for kind, values in current.items()
              if kind in allowed}
    changed = False
    for kind, values in wanted.items():
        if kind not in allowed:
            continue
        kind_changed = False
        current_values = current.get(kind, [])
        current_list = ([current_values] if isinstance(current_values, str)
                        else list(current_values or []))
        known = normalized_identifier_values(kind, current_list)
        for value in ([values] if isinstance(values, str) else values or []):
            normalized = normalized_identifier_values(kind, [value])
            if normalized and not normalized.issubset(known):
                current_list.append(value)
                known.update(normalized)
                changed = True
                kind_changed = True
        if kind_changed:
            merged[kind] = current_list
    return merged if changed else None

def merged_see_also(rm_type, wanted, current):
    """Append URLs while omitting system-managed link labels from updates."""
    current_values = ([current] if isinstance(current, dict)
                      else list(current or []))
    allowed = EDITABLE_SEE_ALSO_LABELS.get(rm_type, frozenset())
    current_list = [value for value in current_values
                    if isinstance(value, dict) and value.get('label') in allowed]
    known = set()
    for value in current_list:
        url = value.get('@id') if isinstance(value, dict) else value
        if canonical_url(url):
            known.add(canonical_url(url))
    changed = False
    for value in ([wanted] if isinstance(wanted, dict) else wanted or []):
        url = value.get('@id') if isinstance(value, dict) else value
        normalized = canonical_url(url)
        if normalized and normalized not in known:
            current_list.append(value)
            known.add(normalized)
            changed = True
    return current_list if changed else None

def merged_localized(wanted, current):
    """Merge language slots while retaining richer live translations."""
    if not isinstance(wanted, dict):
        return wanted if current in (None, '', []) else None
    if not isinstance(current, dict):
        return wanted if current in (None, '', []) else None
    merged = dict(current)
    changed = False
    synthetic_ja = ('ja' in wanted and 'en' in wanted and
                    wanted['ja'] == wanted['en'])
    for lang, value in wanted.items():
        # Do not create a fallback JA value when the corresponding live EN
        # slot disagrees; that usually signals a parser or citation variant,
        # not a genuinely missing translation.
        if (lang == 'ja' and synthetic_ja and
                current.get('en') not in (None, '', []) and
                current.get('en') != wanted.get('en')):
            continue
        if current.get(lang) in (None, '', []):
            merged[lang] = value
            changed = True
    return merged if changed else None

def date_is_at_least_as_precise(wanted, current):
    """True when a live YYYY[-MM[-DD]] already refines the wanted date."""
    return (isinstance(wanted, str) and isinstance(current, str) and
            (current == wanted or current.startswith(wanted + '-')))

def changed_doc(rm_type, desired, live):
    """Return only exporter-owned fields whose complete values differ."""
    changed = {}
    title_field = REQUIRED_TITLE_FIELDS.get(rm_type)
    for field in SYNC_FIELDS[rm_type]:
        if field not in desired:
            continue
        if field == title_field:
            # ResearchMap validates the complete live record after a partial
            # update. A monolingual live title therefore has to be repeated in
            # both required slots whenever another field is changed.
            continue
        wanted = desired[field]
        if field == 'identifiers':
            merged = merged_identifiers(rm_type, wanted, live.get(field))
            if merged is not None:
                changed[field] = merged
            continue
        if field == 'see_also':
            merged = merged_see_also(rm_type, wanted, live.get(field))
            if merged is not None:
                changed[field] = merged
            continue
        current = live.get(field)
        if field in ('book_owner_role', 'book_type') and current not in (None, ''):
            continue
        if field == 'languages' and isinstance(wanted, list):
            merged = list(current) if isinstance(current, list) else []
            for language in wanted:
                if language not in merged:
                    merged.append(language)
            if merged != current:
                changed[field] = merged
            continue
        if isinstance(wanted, dict):
            merged = merged_localized(wanted, current)
            if merged is not None:
                changed[field] = merged
            continue
        if current in (None, '', []):
            changed[field] = wanted
    if changed and title_field:
        current_title = live.get(title_field)
        completed_title = complete_required_title(current_title)
        if completed_title and completed_title != current_title:
            changed[title_field] = completed_title
    return changed

def match_override_key(title_key, rm_type, record):
    """Stable selector: type, date, normalized title, and first contributor."""
    doc = record.get('similar_merge', {})
    date = doc.get('publication_date') or doc.get('from_date') or ''
    first = ''
    for field in ('authors', 'presenters'):
        people = doc.get(field)
        if not isinstance(people, dict):
            continue
        values = people.get('en') or people.get('ja') or []
        if values:
            first = values[0].get('name', '') if isinstance(values[0], dict) else ''
            break
    return '|'.join((rm_type, str(date), title_key,
                     key(first, limit=10**9)))

def candidate_refs(rm_type, item, candidates):
    pool = ([item] if item is not None else list(candidates))
    return sorted('%s:%s' % (rm_type, live_id(value)) for value in pool
                  if live_id(value))

def override_target(live_by_type, reference):
    if not isinstance(reference, str) or ':' not in reference:
        raise ValueError('invalid ResearchMap override target: %r' % reference)
    rm_type, record_id = reference.split(':', 1)
    matches = [item for item in live_by_type.get(rm_type, [])
               if live_id(item) == record_id]
    if len(matches) != 1:
        raise ValueError('ResearchMap override target missing/non-unique: %s' %
                         reference)
    return rm_type, matches[0]

def build_sync(website, live_by_type, managed_ids, overrides=None):
    """Pure sync planner used by --sync and offline fixture tests."""
    overrides = overrides or {}
    seen_overrides = set()
    matches = []
    ambiguous = []
    classified = []
    reviewed_protected = {rm_type: set() for rm_type in LIVE_TYPES}
    for text, tkey, rm_type, record in website:
        if rm_type not in LIVE_TYPES:
            continue
        item, candidates, criterion = match_live(record, live_by_type.get(rm_type, []))
        natural_refs = candidate_refs(rm_type, item, candidates)
        selector = match_override_key(tkey, rm_type, record)
        decision = overrides.get(selector)
        skip_cross_type = False
        if decision:
            seen_overrides.add(selector)
            expected = sorted(decision.get('candidates', []))
            if natural_refs != expected:
                raise ValueError('ResearchMap override candidate drift for %s: '
                                 'expected %r, found %r' %
                                 (selector, expected, natural_refs))
            action = decision['action']
            target = decision.get('target')
            if action == 'match':
                target_type, item = override_target(live_by_type, target)
                if target_type != rm_type or target not in natural_refs:
                    raise ValueError('invalid same-type match override: %s' %
                                     selector)
                candidates = []
                criterion = 'reviewed exact override'
                classified.append({
                    'text': text, 'type': rm_type, 'action': action,
                    'target': target, 'candidates': natural_refs,
                    'reason': decision['reason'],
                })
            elif action == 'equivalent':
                target_type, target_item = override_target(live_by_type, target)
                doc = record.get('similar_merge', {})
                titles_agree = bool(desired_title_keys(record) &
                                    item_title_keys(target_item))
                if (target_type == rm_type or not titles_agree or
                        not cross_type_context_match(doc, target_item)):
                    raise ValueError('invalid cross-type equivalent override: %s' %
                                     selector)
                classified.append({
                    'text': text, 'type': rm_type, 'action': action,
                    'target': target, 'candidates': natural_refs,
                    'reason': decision['reason'],
                })
                reviewed_protected[target_type].add(live_id(target_item))
                continue
            elif action == 'distinct':
                item, candidates, criterion = None, [], 'reviewed distinct record'
                skip_cross_type = True
                classified.append({
                    'text': text, 'type': rm_type, 'action': action,
                    'target': None, 'candidates': natural_refs,
                    'reason': decision['reason'],
                })
            elif action == 'hold':
                classified.append({
                    'text': text, 'type': rm_type, 'action': action,
                    'target': None, 'candidates': natural_refs,
                    'reason': decision['reason'],
                })
                reviewed_protected[rm_type].update(
                    reference.split(':', 1)[1] for reference in natural_refs)
                continue
        if (item is None and not candidates and not skip_cross_type and
                rm_type not in COMBINED_FIELDS):
            cross = []
            for other_type in LIVE_TYPES:
                if other_type == rm_type:
                    continue
                other_item, other_candidates, other_criterion = match_live(
                    record, live_by_type.get(other_type, []))
                pool = ([other_item] if other_item else other_candidates)
                for candidate in pool:
                    if cross_type_context_match(record['similar_merge'], candidate):
                        cross.append((other_type, candidate, other_criterion))
            if cross:
                ids = sorted('%s:%s' % (kind, live_id(candidate))
                             for kind, candidate, _criterion in cross
                             if live_id(candidate))
                ambiguous.append((text, rm_type, 'cross-type date/venue match', ids))
                continue
        matches.append([text, rm_type, record, item, candidates, criterion])

    unused = sorted(set(overrides) - seen_overrides)
    if unused:
        raise ValueError('unused ResearchMap match overrides: %r' % unused)

    # Two website entries resolving to one rm:id are also ambiguous.
    id_counts = {}
    for _text, rm_type, _record, item, _candidates, _criterion in matches:
        rid = live_id(item) if item else None
        if rid:
            id_counts[(rm_type, rid)] = id_counts.get((rm_type, rid), 0) + 1

    inserts, updates = [], []
    matched = {t: set() for t in LIVE_TYPES}
    protected = {t: set(reviewed_protected[t]) for t in LIVE_TYPES}
    for text, rm_type, record, item, candidates, criterion in matches:
        candidate_ids = {live_id(x) for x in candidates if live_id(x)}
        if candidate_ids:
            protected[rm_type].update(candidate_ids)
            ambiguous.append((text, rm_type, criterion, sorted(candidate_ids)))
            continue
        if item is None:
            # The planner has already classified known similarity.  Preserve
            # reviewed-distinct works as separate records; for ordinary new
            # records, make an unexpected ResearchMap similarity match fail
            # instead of silently merging two works.
            insert_mode = ('force' if criterion == 'reviewed distinct record'
                           else 'merge')
            inserts.append((text, {
                'insert': dict(record['insert']),
                insert_mode: record['similar_merge'],
            }))
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
    return inserts, updates, deletes, refreshed, ambiguous, classified

def sync_live(dry_run=False, record_managed_state=False):
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
    inserts, updates, deletes, refreshed, ambiguous, classified = build_sync(
        website_records(), live_by_type, state['managed_ids'],
        load_match_overrides())
    for text, rm_type, criterion, ids in ambiguous:
        print(f'AMBIGUOUS ({rm_type}, {criterion}, ids={ids}): {text[:100]}',
              file=sys.stderr)
    for row in classified:
        print('CLASSIFIED (%s, %s, target=%s): %s' %
              (row['type'], row['action'], row['target'], row['text'][:100]),
              file=sys.stderr)
    operations = ([record for _text, record in inserts] +
                  [record for _text, record in updates] + deletes)
    for record in operations:
        print(json.dumps(record, ensure_ascii=False))
    print(f'\n{len(inserts)} inserts / {len(updates)} updates / '
          f'{len(deletes)} deletes; {len(ambiguous)} ambiguous skipped; '
          f'{len(classified)} reviewed classifications')
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
    if record_managed_state:
        state['managed_ids'] = refreshed
        save_state(state)
        print('managed-ID state updated after explicit confirmation')
    else:
        print('managed-ID state unchanged; use --record-managed-state only '
              'after the reviewed import succeeds')
    return 0

def live_title(item):
    """Extract a title string from a live researchmap item dict, any language."""
    for field in ('paper_title', 'book_title', 'book_owner_range',
                  'presentation_title',
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
    for field in ('paper_title', 'book_title', 'book_owner_range',
                  'presentation_title',
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
        for text, data_date, data_doi, data_isbn, data_url, data_volume, data_number, data_pages, data_authors, data_authors_ja, data_authors_en, data_event, data_location, data_invited, data_publisher, data_book_title, data_book_role, data_title, data_venue in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_isbn, data_url,
                            data_volume, data_number, data_pages, data_authors,
                            data_authors_ja, data_authors_en, data_event,
                            data_location, data_invited, data_publisher,
                            data_book_title, data_book_role, data_title,
                            data_venue)
            if rec is None:
                print(f'WARNING: could not parse, add manually: {text[:90]}', file=sys.stderr)
                continue
            parsed = parse(text)
            title = data_title or (parsed[1] if parsed else text)
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
        with open(path, newline='', encoding='utf-8') as source:
            c = source.read()
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
            'publisher': {'ja': jp_publisher, 'en': en_publisher},
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
        name = next(iter(doc['academic_society_name'].values()))
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
        body = m.group(2).strip()
        parts = [p.strip() for p in re.split(r'\s+—(?:\s+|$)', body,
                                             maxsplit=1)]
        name = parts[0]
        assoc = parts[1] if len(parts) > 1 else ''
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
        m = re.match(r'(\S+)\s+(.+)$', line)
        if not m: continue
        frm, to = parse_range(m.group(1))
        split = split_trailing_parenthetical(m.group(2), '（', '）')
        if not split:
            split = split_trailing_parenthetical(m.group(2), '(', ')')
        if not split: continue
        title, fund = split
        lang = 'ja' if is_cjk(title) else 'en'
        doc = {'research_project_title': {lang: title}}
        parts = [x.strip() for x in re.split(r'[、,]', fund) if x.strip()]
        if parts:
            system, category = split_funding_label(parts[0])
            doc['system_name'] = {lang: system}
            if category:
                doc['category'] = {lang: category}
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
    ap.add_argument('--record-managed-state', action='store_true',
                    help='with --sync, persist matched IDs only after a successful upload')
    args = ap.parse_args()

    if args.sync and (args.check_live or args.init):
        ap.error('--sync cannot be combined with --check-live or --init')
    if args.record_managed_state and not args.sync:
        ap.error('--record-managed-state requires --sync')

    if args.sync:
        sys.exit(sync_live(dry_run=args.dry_run,
                           record_managed_state=args.record_managed_state))

    if args.check_live:
        sys.exit(check_live(dry_run=args.dry_run))

    state_data = load_state()
    state = set(state_data['baseline'])

    seen, new = [], []
    for anchor, (rm_type, extra) in SECTIONS.items():
        for text, data_date, data_doi, data_isbn, data_url, data_volume, data_number, data_pages, data_authors, data_authors_ja, data_authors_en, data_event, data_location, data_invited, data_publisher, data_book_title, data_book_role, data_title, data_venue in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            k = key(text)
            seen.append(k)
            if k in state or args.init:
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_isbn, data_url,
                            data_volume, data_number, data_pages, data_authors,
                            data_authors_ja, data_authors_en, data_event,
                            data_location, data_invited, data_publisher,
                            data_book_title, data_book_role, data_title,
                            data_venue)
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

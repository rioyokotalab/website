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

The output file is uploaded on researchmap:  設定 > インポート
(or pushed via the WebAPI once an API key is available).
Format reference: https://researchmap.jp/outline/v2api/v2API.pdf
"""
import argparse, json, os, re, sys, unicodedata, urllib.request, urllib.error

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
    r'IEEE|ACM|SIAM|Nature|学会|研究会|大会|シンポジウム|発表会|ワークショップ|研究発表会')

# invisible data-date="YYYY-MM"(-DD) on the opening <li> = ResearchMap
# publication_date; when present it OVERRIDES the heuristic date parse below.
DATA_DATE = re.compile(r'\bdata-date\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_DOI = re.compile(r'\bdata-doi\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_URL = re.compile(r'\bdata-url\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_VOLUME = re.compile(r'\bdata-volume\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_NUMBER = re.compile(r'\bdata-number\s*=\s*["\']([^"\']*)["\']', re.I)
DATA_PAGES = re.compile(r'\bdata-pages\s*=\s*["\']([^"\']*)["\']', re.I)

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
    """Yield (clean_text, data_date, data_doi, data_url, data_volume,
    data_number, data_pages) for each <li>;
    data_* is None if the opening <li> tag carries no valid attribute."""
    c = open(PAGE, newline='', encoding='utf-8').read()
    a = c.index('name="%s"' % anchor)
    s = c.index('<ol>', a); e = c.index('</ol>', s)
    block = c[s:e]
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
        t = re.sub(r'</li>', '', re.sub(r'<[^>]+>', '', p), flags=re.I)
        t = unicodedata.normalize('NFKC', t).replace('&amp;', '&').replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
        out.append((re.sub(r'\s+', ' ', t).strip(), data_date, data_doi, data_url,
                    data_volume, data_number, data_pages))
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

def to_record(text, rm_type, extra, data_date=None, data_doi=None, data_url=None,
              data_volume=None, data_number=None, data_pages=None):
    rm_type = resolve_type(rm_type, text)
    parsed = parse(text)
    if not parsed:
        return None
    authors, title, venue, date = parsed
    if data_date:            # data-date attribute overrides the heuristic date
        date = data_date
    japanese = is_cjk(title)
    lang = 'ja' if japanese else 'en'
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
        doc['publisher'] = {lang: venue}
        doc['authors'] = people
    else:
        doc['presentation_title'] = {lang: title}
        doc['event'] = {lang: venue}
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
    text = re.sub(r'<[^>]+>', '\n', m.group(1))
    lines = [re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', l)).strip()
             for l in text.split('\n')]
    return [l for l in lines if l and not l.startswith('&nbsp;')]

def parse_range(prefix):
    m = re.match(r'(\d{4})(?:年)?(?:(\d{1,2})月)?(?:[–―-](\d{4})(?:年)?)?$', prefix.strip())
    if not m:
        return None, None
    frm = m.group(1) + ('-%02d' % int(m.group(2)) if m.group(2) else '')
    return frm, m.group(3)


API_BASE = 'https://api.researchmap.jp/%s/%%s' % PERMALINK
LIVE_TYPES = ['published_papers', 'books_etc', 'presentations', 'misc']

def fetch_live(rm_type):
    """Fetch all pages of a live researchmap collection, return list of item dicts."""
    items = []
    url = API_BASE % rm_type
    while url:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
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
    if not items:
        raise RuntimeError('fetch_live: got zero items back (empty or malformed response)')
    return items

def live_title(item):
    """Extract a title string from a live researchmap item dict, any language."""
    for field in ('paper_title', 'book_title', 'presentation_title',
                  'title', 'misc_title'):
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
                  'title', 'misc_title'):
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
        for text, data_date, data_doi, data_url, data_volume, data_number, data_pages in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_url,
                            data_volume, data_number, data_pages)
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

def check_live():
    """Diff website entries against live researchmap.jp data (instead of the
    local state file) and write tools/out/researchmap-import.jsonl."""
    live_keys = {}
    for rm_type in LIVE_TYPES:
        try:
            live_keys[rm_type] = live_title_keys(rm_type)
        except Exception as e:
            print(f'ERROR: could not fetch live {rm_type} from researchmap API '
                  f'({e.__class__.__name__}: {e}); aborting without writing {OUT} '
                  f'(refusing to treat an unreachable API as "everything is new")',
                  file=sys.stderr)
            return 1

    all_live = set().union(*live_keys.values()) if live_keys else set()

    new = []
    for text, tkey, rm_type, rec in website_records():
        # awards/committee_memberships/research_projects have no live type to
        # check against here (not in LIVE_TYPES); skip live-comparison for them.
        if rm_type not in live_keys:
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

    for text, rec in new:
        print('NEW:', text[:100])

    if new:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'w', encoding='utf-8') as f:
            for _, rec in new:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(f'\n{len(new)} NEW entries not found live, written to {OUT}')
    else:
        if os.path.exists(OUT):
            os.remove(OUT)
        print('\n0 NEW entries found (website matches live researchmap)')
    return 0

def profile_records():
    """CV items (awards / committee memberships / research projects) -> records."""
    recs = []
    for line in profile_lines('受賞歴'):
        m = re.match(r'(\S+)\s+(.+)$', line)
        if not m: continue
        date, _ = parse_range(m.group(1))
        name = m.group(2).strip()
        lang = 'ja' if is_cjk(name) else 'en'
        doc = {'award_name': {lang: name}}
        if date: doc['award_date'] = date
        recs.append((line, 'awards', doc))
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
        m = re.match(r'(\S+)\s+(.+?)[（(](.+)[）)]$', line)
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
    args = ap.parse_args()

    if args.check_live:
        sys.exit(check_live())

    state = set()
    if os.path.exists(STATE):
        state = set(json.load(open(STATE, encoding='utf-8')))

    seen, new = [], []
    for anchor, (rm_type, extra) in SECTIONS.items():
        for text, data_date, data_doi, data_url, data_volume, data_number, data_pages in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            k = key(text)
            seen.append(k)
            if k in state or args.init:
                continue
            rec = to_record(text, rm_type, extra, data_date, data_doi, data_url,
                            data_volume, data_number, data_pages)
            if rec:
                new.append((text, rec))
            else:
                print(f'WARNING: could not parse, add manually: {text[:90]}', file=sys.stderr)

    # CV items on the personal page (awards, committees, research projects)
    for text, rm_type, doc in profile_records():
        k = key(text)
        seen.append(k)
        if k in state or args.init:
            continue
        new.append((text, {'insert': {'type': rm_type},
                           'similar_merge': doc, 'priority': 'similar_data'}))

    if args.init:
        json.dump(sorted(seen), open(STATE, 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
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
    json.dump(sorted(set(state) | set(seen)), open(STATE, 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
    print(f'\n{len(new)} entries written to {OUT}')
    print('Upload on researchmap: 設定 > インポート (or push via WebAPI).')

if __name__ == '__main__':
    main()

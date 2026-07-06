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

The output file is uploaded on researchmap:  設定 > インポート
(or pushed via the WebAPI once an API key is available).
Format reference: https://researchmap.jp/outline/v2api/v2API.pdf
"""
import argparse, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'en', 'achievements', 'index.html')
STATE = os.path.join(ROOT, 'tools', 'researchmap-state.json')
OUT = os.path.join(ROOT, 'tools', 'out', 'researchmap-import.jsonl')
PERMALINK = 'rioyokota'

SECTIONS = {   # anchor -> (rm type, extra fields)
    'sub001': ('published_papers', {'published_paper_type': 'scientific_journal', 'referee': True}),
    'sub002': ('published_papers', {'published_paper_type': 'in_book'}),
    'sub004': ('published_papers', {'published_paper_type': 'international_conference_proceedings', 'referee': True}),
    'sub005': ('published_papers', {'published_paper_type': 'symposium', 'referee': True}),
    'sub006': ('presentations', {'is_international_presentation': True}),
    'sub007': ('presentations', {'is_international_presentation': False}),
}
MONTHS = {m: i+1 for i, m in enumerate(
    ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])}
VENUE_WORDS = re.compile(
    r'Journal|Conference|Proceedings|Transactions|Workshop|Symposium|SIGKDD|'
    r'NeurIPS|ICLR|ICML|CVPR|ICCV|ECCV|AAAI|EMNLP|COLM|COLING|LREC|ISC|SC\d|HPC|GTC|'
    r'IEEE|ACM|SIAM|Nature|学会|研究会|大会|シンポジウム|発表会|ワークショップ|研究発表会')

def entries(anchor):
    c = open(PAGE, newline='', encoding='utf-8').read()
    a = c.index('name="%s"' % anchor)
    s = c.index('<ol>', a); e = c.index('</ol>', s)
    parts = re.split(r'<li[^>]*>', c[s:e], flags=re.I)[1:]
    out = []
    for p in parts:
        t = re.sub(r'</li>', '', re.sub(r'<[^>]+>', '', p), flags=re.I)
        t = unicodedata.normalize('NFKC', t).replace('&amp;', '&').replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
        out.append(re.sub(r'\s+', ' ', t).strip())
    return out

def key(t):
    return re.sub(r'[^0-9a-z぀-ヿ一-鿿]', '', t.lower())[:70]

def is_cjk(s):
    return bool(re.search(r'[぀-ヿ一-鿿]', s))

def parse_date(seg):
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
    return (1 < len(words) <= 5 and len(seg) < 45 and not re.search(r'\d', seg)
            and not VENUE_WORDS.search(seg) and seg[0].isupper())

def parse(text):
    """citation -> (authors, title, venue, date) — heuristic, review the output."""
    text = text.rstrip('.。 ')
    japanese = is_cjk(text)
    segs = [s for s in re.split(r'[,、，]| 、', text) if s.strip()]
    date = None
    while segs and (d := parse_date(segs[-1])):
        date = d; segs.pop()
    # trailing volume/page segments stay attached to the venue
    authors = []
    while segs:
        cand = re.sub(r'^and\s+', '', segs[0].strip())
        if not looks_like_name(cand, japanese):
            break
        authors.append(cand)
        segs[0:1] = []
    if not segs:
        return None
    # venue = last segment(s) starting from the first venue-looking one after the title
    venue_idx = len(segs) - 1
    for i in range(1, len(segs)):
        if VENUE_WORDS.search(segs[i]):
            venue_idx = i
            break
    title = ', '.join(s.strip() for s in segs[:venue_idx]).strip(' 「」"')
    venue = ', '.join(s.strip() for s in segs[venue_idx:])
    return authors, title, venue, date

def to_record(text, rm_type, extra):
    parsed = parse(text)
    if not parsed:
        return None
    authors, title, venue, date = parsed
    japanese = is_cjk(title)
    lang = 'ja' if japanese else 'en'
    people = {lang: [{'name': a} for a in authors]}
    doc = {}
    if rm_type == 'published_papers':
        doc['paper_title'] = {lang: title}
        doc['publication_name'] = {lang: venue}
        doc['authors'] = people
    else:
        doc['presentation_title'] = {lang: title}
        doc['event'] = {lang: venue}
        doc['presenters'] = people
    if date:
        doc['publication_date'] = date
    doc['languages'] = ['jpn' if japanese else 'eng']
    doc.update(extra)
    return {'insert': {'type': rm_type, 'user_id': PERMALINK},
            'similar_merge': doc, 'priority': 'similar_data'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--init', action='store_true', help='snapshot baseline, export nothing')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    state = set()
    if os.path.exists(STATE):
        state = set(json.load(open(STATE, encoding='utf-8')))

    seen, new = [], []
    for anchor, (rm_type, extra) in SECTIONS.items():
        for text in entries(anchor):
            if not re.search(r'Rio\s+Yokota|横田\s*理央', text):
                continue
            k = key(text)
            seen.append(k)
            if k in state or args.init:
                continue
            rec = to_record(text, rm_type, extra)
            if rec:
                new.append((text, rec))
            else:
                print(f'WARNING: could not parse, add manually: {text[:90]}', file=sys.stderr)

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

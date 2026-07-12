# Skill: EN/JP parity and translation

- `en/` and `jp/` mirror HTML page paths; `js/chglang.js` swaps the language
  prefix, so a missing page counterpart 404s. Every content change applies to
  BOTH pages unless explicitly told otherwise.
- Image assets do not need duplicate EN/JP paths. Shared images live under
  `jp/` (for example, `jp/research/images20XX/` and `jp/picture/images/`) and
  are referenced from both language pages.
- `en/` pages are fully English, `jp/` pages fully Japanese. Exception:
  Achievements citation language follows the venue (see
  skills/achievements.md) and is identical on both pages.
- Translate titles/abstracts faithfully; use known kanji names for Japanese
  members and romaji for international students. Do not guess romaji: confirm
  via DBLP/paper author lists (skills/web-lookup.md) or flag NEEDS-USER.
- Institution: current content uses 東京科学大学 総合研究院 / Institute of
  Science Tokyo, IIR. Preserve historical names inside historical records and
  live URLs (titech/gsic).
- Parity verification recipe: same `<li>` counts per section, same data-*
  attribute counts, both pages HTTP 200 on localhost:8000 (or live after
  publish).
- To audit page-path parity and asset differences from the repo root, run:
  ```bash
  comm -3 \
    <(find en -type f -printf '%P\n' | LC_ALL=C sort) \
    <(find jp -type f -printf '%P\n' | LC_ALL=C sort)
  ```
  The EN-only (left) column should be empty. JP-only (right) entries should be
  image assets; investigate any HTML or other page-path difference.

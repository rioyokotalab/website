# Skill: EN/JP parity and translation

- `en/` and `jp/` mirror every path; `js/chglang.js` swaps the language
  prefix, so a missing counterpart 404s. Every content change applies to BOTH
  pages unless explicitly told otherwise.
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

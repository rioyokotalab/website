# Skill: researchmap / ORCID / CV exporters

Explicit-only: run exports only on explicit user request; never from
publish.sh.

## researchmap
- `python3 tools/researchmap-export.py --check-live` fetches the public API
  `https://api.researchmap.jp/rioyokota/{published_papers,books_etc,presentations,misc}`
  and diffs against ALL Yokota-authored Achievements entries (state file
  `tools/researchmap-state.json` can drift from live). Missing entries go to
  `tools/out/researchmap-import.jsonl`. `--sync` supports insert/update/delete
  with a managed_ids registry.
- Category mapping: sub001/004/005 -> Papers; sub002/003 -> Books and Other
  Publications; sub006/007 -> Presentations when Rio Yokota is SOLE author
  (invited talks), else Misc. media_coverage is also exported (event=outlet).
- Import: the user downloads the jsonl and uploads at researchmap 設定 >
  インポート (permalink rioyokota); university FIS syncs from researchmap.
  NEVER automate the researchmap login UI (403 for non-browser clients); the
  sanctioned automation is the WebAPI / bulk-import file.
- Bulk-import grammar: one JSON object per line. UPDATE form:
  `{"update": {"type": "<record-type>", "id": "<rm:id>"}, "doc": {<changed fields only>}}`;
  rm:ids come from the public read API (`?limit=1000`). Insert/update lines
  must NOT carry `user_id` — its presence 403s and blocks the ENTIRE file
  (all lines validate before any apply). Per-entry validation errors (e.g.
  missing `publication_date`, required for published_papers) 400 only that
  line; re-upload the corrected failing line as a tiny one-line jsonl, never
  the whole file. The public read API lags imports, so --check-live will not
  immediately dedupe just-imported entries.
- The exporter parses citations heuristically (、/comma author lists,
  "LastAuthor. Title" boundary preserving initials, trailing parenthetical
  notes) but PREFERS data-* attributes (skills/achievements.md). Always
  review printed NEW lines before upload.

## ORCID
- `python3 tools/orcid-export.py` (or `--dry-run`; `--only-title`/`--section`
  for incremental) writes `tools/out/orcid-works.bib`; import manually via
  ORCID Add works > Import BibTeX (no bulk JSON API; public API read-only).
- Mapping: sub001 @article; sub002 @incollection; sub003 @book; sub004/005
  @inproceedings; sub006/007 @misc. Emits DOI, arXiv eprint, and url
  identifiers; ORCID groups by identifier/title, so a no-identifier title
  change creates a duplicate that must be removed in the ORCID UI. Prefer
  fixing source citations over patching the .bib.

## CV
- `cv/cv.tex` content sync is AUTOMATIC and bidirectional with
  achievements/index.html and the CV sections (受賞歴/委員歴/研究課題) of
  jp/member/yokota.html: update the matching section in the SAME edit.
- Personal-page exporter line formats (em-dash separators, 全角 space after
  dates): `2009年11月　AWARD` / `2024–2025　ROLE — ASSOCIATION` /
  `2025–2028　TITLE（FUNDING SYSTEM、FUNDER）`. Both language pages carry the
  items; only the JP page is parsed.
- Build `cv/cv.pdf` with `./cv/build-cv.sh` ONLY on explicit request
  (tectonic at ~/.local/bin; keep `\usepackage{xeCJK}` +
  `\setCJKmainfont{Noto Sans CJK JP}` or kanji silently drop; Noto CJK is in
  ~/.local/share/fonts). cv/cv.tex, cv/cv.cls, cv/build-cv.sh are
  deploy-excluded; only cv/cv.pdf is served, linked from both member pages as
  `../../cv/cv.pdf` (target=_blank, rel=noopener).

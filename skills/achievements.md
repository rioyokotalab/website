# Skill: Achievements page

File: `achievements/index.html` in both trees. Sections: sub001 journal,
sub002 book series, sub003 books, sub004 international peer-reviewed,
sub005 domestic peer-reviewed, sub006 international non-reviewed,
sub007 domestic non-reviewed. Entries are newest-first inside each `<ol>`.

- Citation language: international entries English on BOTH pages; domestic
  entries Japanese on BOTH pages.
- `data-date="YYYY-MM"` (or YYYY-MM-DD) on every `<li>`: journals use
  publication date; conferences the first conference day. Resolve month from
  citation text, then DOI/Crossref print or online-first date, then J-STAGE
  発行日; if still unknown, January of the known year. Never year-only.
- `data-doi`: bare DOI (no https://doi.org/ prefix). `data-url`: only when no
  DOI exists AND a confirmed same-paper canonical URL (arXiv abs, OpenReview
  forum, ANLP anthology, IPSJ) with title/author/year agreement; otherwise
  leave both off.
- Further data-* attributes carried by entries and consumed by exporters:
  data-authors (plus data-authors-ja/data-authors-en on domestic entries),
  data-volume, data-number, data-pages, data-event, data-location,
  data-invited, data-publisher, data-isbn. Exporters prefer data-* over
  citation-text heuristics.
- cv.tex sync is automatic and bidirectional: any change here (or in the CV
  sections of jp/member/yokota.html) updates the matching `cv/cv.tex` section
  in the SAME edit, and vice versa (see skills/exporters.md).
- Lookup/attribute progress tracker: `tools/todo.md`.

# Skill: HTML editing (Dreamweaver-era pages)

- Edit page HTML only with small python3 scripts using
  `open(path, newline='', encoding='utf-8')` for BOTH read and write, so CRLF
  line endings and stray non-breaking spaces survive byte-for-byte.
  Exact-match edit tools often fail on these files.
- Parse tags case-insensitively; never assume closing tags. Legacy sections
  use unclosed uppercase `<LI>`. Split list items with
  `re.split(r'<li[^>]*>', text, flags=re.I)`.
- Keep class/id names stable: `style.css` is written against existing
  selectors, floats, and table layouts.
- If you edit `style.css`, bump `style.css?v=YYYYMMDD` in ALL pages and
  `Templates/*.dwt` with a scripted replace.
- Site-wide strings (nav, footer, header) must also update `Templates/*.dwt`.
  Preserve `.dont-remove-me`.
- New `target="_blank"` links need `rel="noopener noreferrer"`.
- Galleries: pinned cdnjs Lightbox 2.11 / jQuery 3.7 with SRI; do not change
  versions casually.
- Never touch `.git/`; never retroactively edit historical records (old news,
  publication lists, CV history) for name/grade/institution changes.
- After list edits, verify identical `<li>` counts in the affected EN/JP
  sections.

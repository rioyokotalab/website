# Skill: Figure production (research pages)

- Research entries: `<h4>Title（Name）</h4>` + abstract + lightbox figure in
  `jp/research/images20XX/` (current topics first, then newest-first yearly
  thesis sections, with matching sidebar anchors).
- Lab Google Drive (read-only rclone):
  `~/.local/bin/rclone lsf --drive-root-folder-id 1MRyEsesRkuZ_eGtUgnPgC9k3rXuo_BLa gdrive:<path>`.  Layout: `Thesis/YYYY/{master,bachelor}/` (thesis PDFs), `Posters/YYYY/`
  (研究室紹介 poster; `.pages` files are zip archives with preview.jpg and
  originals under Data/), `Slides/YYYY発表.../` (defense slides). The OAuth
  token is Drive-read-only, revocable at myaccount.google.com/permissions.
- Thesis-PDF figures: `pdftoppm -jpeg -r 150 -f N -l N` + PIL crop (trim
  captions; flatten transparency onto white).
- SVG->PNG: cairosvg in a venv (`python3 -m venv`; system pip is
  PEP-668-locked); Japanese text needs Noto Sans CJK JP
  (~/.local/share/fonts) and cairo does no font fallback — patch the SVG
  `font-family` to "Noto Sans CJK JP" before converting.
- Swallow charts (https://swallow-llm.github.io/, .ja.html/.en.html release
  pages): ApexCharts SVGs; legends are NOT in the SVG — series names live in
  `seriesName` attributes and colors follow palette #008FFB #00E396 #FEB019
  #FF4560 #775DD0 in series order; rebuild the legend with PIL when
  rasterizing.

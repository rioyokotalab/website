# T-7 — CV reconciliation with achievements

Started 2026-07-12 by the codex driver. No CV build command has been run.

## Inventory

- Parsed the 36 achievement entries dated 2025-01 or later from `jp/achievements/index.html`, retaining the section mapping used by `cv/cv.tex`.
- Matching counts: `sub001` 2/2, `sub004` 29/29, `sub005` 2/2, `sub007` 2/2; `sub002` and `sub003` have no in-scope entries.
- One entry is genuinely absent from the mapped `Conference Presentations (not peer-reviewed)` CV section: Bai Cong, Nico Daheim, Yuesong Shen, Rio Yokota, Mohammad Emtiyaz Khan, Thomas Möllenhoff, “Improving LoRA with Variational Learning,” arXiv preprint (CoRR 2025), Jun. 2025 (`sub006`, `data-date="2025-06"`).
- Two low similarity scores were presentation differences, not omissions: `SuperGCN` expands PPoPP on the site but uses its abbreviation in the CV; `Aurora-M` has a differing title in the CV. Neither is within this task's add-missing-only scope.
- `jp/member/yokota.html` contains personal CV sections for awards, committees, and research grants, but no publication/presentation list; it has no matching destination for the missing `sub006` publication.

## Structured result

- status: in-progress
- summary: One missing CV entry identified; the personal page does not contain the applicable publication section, so only cv/cv.tex needs an addition.
- changed_files: tools/out/t7-cv-reconciliation.md; tools/state/session.md
- commands: read-only CRLF-safe Python source-to-CV mapping; `rg`/`sed` section inspection. No `cv/build-cv.sh` invocation.
- verification: 35 of 36 current achievement entries map to a CV item; the sole unmatched item is the 2025-06 CoRR presentation.
- evidence:
  - confirmed: the matching CV section exists and has no normalized-text match for “Improving LoRA with Variational Learning.”
  - confirmed: the personal page's parsed CV sections are awards/committees/grants rather than publications.
  - hypotheses: existing wording differences for SuperGCN and Aurora-M may merit a separate content-reconciliation task, but no edit is proposed here.
- remaining: inspect the exact CV insertion format and source lines, add the one missing item, then rerun source-to-CV counts without building the PDF.

## Edit and verification

- Added at `cv/cv.tex:412`, at the top of the newest-first `Conference Presentations (not peer-reviewed)` list:
  `Bai Cong, Nico Daheim, Yuesong Shen, Rio Yokota, Mohammad Emtiyaz Khan, Thomas M\"{o}llenhoff, Improving LoRA with Variational Learning, arXiv preprint (CoRR 2025), Jun. 2025.`
- Source entries: `en/achievements/index.html:312` and `jp/achievements/index.html:323` (the same title and 2025-06 date).
- Count changed from 45 to 46 items in that CV section; the in-scope source set remains 36 entries and all 36 now have a corresponding CV record (using normalized citation comparison plus manual confirmation of the two wording variants).
- `jp/member/yokota.html` was intentionally not changed: it has no publications/presentations subsection to mirror this CV record.
- Restored the existing no-final-newline convention after the initial patch introduced one; the final scoped diff is exactly the new item plus its separating blank line.
- No `./cv/build-cv.sh` command was run.

## Structured result

- status: completed
- summary: Added the one missing June 2025 CoRR presentation to cv/cv.tex; no personal-page mirror was applicable.
- changed_files: cv/cv.tex; tools/out/t7-cv-reconciliation.md; tools/out/remove-t7-cv-final-newline.py; tools/state/session.md
- commands: read-only CRLF-safe Python source-to-CV mapping; `rg`/`sed` section inspection; scoped `git diff --check`/diff. No CV build command.
- verification: source entries 36; mapped at similarity >=0.80: 36; CV presentation-list count 45 -> 46; added title occurs once in cv/cv.tex; scoped diff check passes; jp/member/yokota.html is not changed.
- evidence:
  - confirmed: The added CV item is sourced from the identical English citation on both achievement pages at the lines above.
  - confirmed: SuperGCN and Aurora-M already have CV entries; their lower similarity scores come from abbreviated/different wording, not missing records.
  - hypotheses: Those two wording drifts are outside this add-missing-only task and may be considered separately.
- remaining: none for T-7; no PDF build was requested or performed.

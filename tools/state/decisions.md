# Durable decisions

- **2026-07-13 — Use a Codex-only repository workflow.** The inactive
  integration and project configuration, obsolete comparison infrastructure,
  retained comparison data, and transient artifacts are removed from the
  current tree. Git history remains intact, owner-scope settings remain
  untouched, and no force-push or history rewrite is authorized.
- **2026-07-13 — Keep two Codex operating lessons from the retired comparison
  work.** Use progressive disclosure and task-specific source inspection for
  bounded local edits; require broad inspection for diagnosis, visual work, or
  refactors. Treat capability as a gate before optimizing tokens or routing.
- **2026-07-14 — Route analogous website tasks from frozen evidence.** Query
  policy `2026-07-14.3` before delegation. Gate first on full-quality
  reliability confidence; default to minimum retry-adjusted runtime, use the
  effective-token objective only when token use is the priority, and rank the
  reliability objective by Wilson lower bound, smoothed success probability,
  then runtime. Apply the returned model/effort only when the dispatch surface
  exposes both; record any mismatch. Always run listed validation, use the
  route-aware fallback, and never extrapolate to a materially different class
  without new comparable evidence. WBD-005 always requires the full grader and
  failure-informed escalation despite Sol/high reaching 8/9 qualification.
- **2026-07-14 — Match the WCCM proceedings record exactly.** ResearchMap record
  `published_papers:39797632` matches the 2014 WCCM row's title, date,
  contributor order, venue, language, and proceedings type, independently
  corroborated by the university researcher profile. Classify it as an exact
  match while keeping the later 2017 journal article separate; retain
  candidate-drift failure for any future live change.
- **2026-07-14 — Make ResearchMap sync inserts fail closed.** Emit `merge` for
  ordinary unmatched sync records so unexpected similarity is reported, and
  emit `force` only when a reviewed override explicitly classifies the source
  and candidate as distinct works. Do not emit `similar_merge` in sync plans:
  ResearchMap can silently merge separate works and alter the existing record.
  Repair a partial import with exact-ID corrections and only the affected
  forced inserts, never by re-uploading the full source file.

# Durable decisions

- **2026-07-18 — The repository is public; treat every commit as public.**
  At the owner's explicit instruction (T-192, after reversing the sanitized-
  mirror route), `rioyokotalab/website` including its full history is
  publicly visible. The owner regards the repository content as public
  information; the T-185 caveat about deleted member photos/content in
  history was surfaced and accepted. Consequence for all future work:
  ledgers, reports, metrics, and any tracked file are public the moment they
  are pushed — never commit private member data, unpublished results, or
  operational secrets, and keep credential handling outside the repository
  as before.
- **2026-07-18 — Standing owner authorization after T-190.** The owner removed
  the required non-author review from the live `main` ruleset and, after
  applying the T-190 hook, granted standing authorization for similar tasks:
  a direct DRIVER may self-merge its own PR once required CI passes, and may
  run `tools/hook-doctor.sh apply`/`rollback` on the local pre-commit hook
  when the read-only doctor reports drift from the tracked canonical copy.
  This does not extend to other `.git` internals, credentials, deployment
  beyond existing gates, account settings, or history rewrites; those remain
  proposal-only. Tracked ruleset payload/test reconciliation is T-191.
- **2026-07-18 — Support independent Codex and Claude repository workflows.**
  This supersedes the 2026-07-13 Codex-only client decision at the owner's
  explicit request. `AGENTS.md` is the shared project policy and root
  `CLAUDE.md` imports it with a narrow client-compatibility overlay. The
  website retains its own ledger, skills, tests, metrics, and publication
  gates; no sibling repository supplies runtime guidance or tooling. The old
  Claude benchmark/agent framework remains retired, owner-scope settings stay
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

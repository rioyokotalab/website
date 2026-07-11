# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending

### SESSION STATE — cold-restart handoff (2026-07-11)
Task: ResearchMap ↔ website consolidation (RM treated as a data source, not website-as-truth). PUBLISHED & COMMITTED 2026-07-11: Cat 1-4 consolidation + latency guardrails live (commit 80a0de8). Remaining: Cat 5, RM export (needs media_coverage exporter path).

DONE in working tree (verify with git status/diff before trusting):
- Cat 1: education/research_experience/association_memberships consolidated on jp+en/member/yokota.html + cv.tex; Bristol 2009-02; RIKEN+NII roles; JSAI+IEEE; single JSME.
- Cat 2: awards/committee/research_projects; EN award "November 2009"; committee typos+naming drift fixed both pages (98/98); exporter LIVE_TYPES now includes awards/committee_memberships/research_projects (normalized dedup).
- Cat 3: 特許 N/A (RM+site empty). Media Coverage/メディア報道: 13 entries (from media.docx) added to BOTH member pages between Awards and Committee.
- Cat 4: added paper "Improving LoRA with Variational Learning" (2025, arXiv:2506.14280) to achievements sub006 both langs; added 8 genuine misc/presentation entries (sub006/sub007, item #9 VFVM4 held); Research Projects rebuilt to correct 22-row UNION (17 originals + 5 new + 2 detail-updated) on both member pages + cv.tex (22 items). VERIFIED 22/22, JP==EN, non-glued last row (acceptable).
- media.docx and projects.docx DELETED from repo root.

PENDING / NEXT STEPS:
- Cat 5 (NOT STARTED, now unblocked): for each publication with accessible PDF, parse Acknowledgements, extract grant IDs, match to a Research Project, populate that project's "List of results of the research project". Incremental bounded batches -> tools/out/. Feeds RM export.
- Conflicts resolved SITE-canonical for Aurora-M / ICPP k-th eigenvalue / RePOSE — must be pushed site->RM at export time (RM currently differs).
- RM EXPORT is DEFERRED per user until all consolidation done; also needs a media_coverage exporter emission path added (13 entries not yet exportable).
- LATENCY POLICY: applied — guardrails section added to tools/task-tier-policy.md (2026-07-11, user-approved).
- After publish: delete transient tools/out/ scratch; commit metrics/log/policy silently.

KEY RELEVANT tools/out FILES: rm-cat*-consolidation.md, rm-cat4-9adds-edits-final.md, projects-union-fix.md, projects-docx-content.md, agent-latency-analysis.md, researchmap-import.jsonl.


### ResearchMap ↔ website consolidation (RM is a data source, NOT website-as-ground-truth)
Workflow per category: (a) fetch RM public API data, (b) consolidate RM + website (union, resolve conflicts), (c) update website EN/JP pages, (d) re-run exporter so RM export reflects consolidated data.
- [x] Cat 1: education / research_experience / association_memberships (学歴/職歴/所属学会). (IN PROGRESS: fetch+consolidate)
- [x] Cat 2: awards / committee_memberships / research_projects (受賞歴/委員歴/研究課題); also add these to LIVE_TYPES for dedup.
- [x] Cat 3: industrial_property_rights (特許) / media_coverage (メディア報道); consolidate from RM, add website section + exporter path if data exists. — media_coverage: 13 entries added to member pages from media.docx (RM export pending); 特許 still N/A
- [x] Cat 4: published_papers / misc / books_etc / presentations — reconcile RM vs achievements/index.html (already partially live-synced).
- [ ] Cat 5 (after Cat 2/projects.docx Research Projects list is final): for each publication with an accessible PDF, parse the Acknowledgements, extract grant IDs (JSPS KAKENHI JPxxxxxxxx, JST/AMED/MEXT programs), match each to a Research Project (web search where needed), and populate that project's "List of results of the research project" (researchmap research_projects linked-papers). Incremental, bounded batches -> tools/out/. Feeds RM export.

- [ ] Investigate why site-author/site-editor tasks sometimes take unreasonably long: analyze tools/task-metrics.jsonl duration_ms by task_type/agent/tier, identify outliers, and determine cause (e.g. codex worker effort/model too high for the work, oversized prompts, avoidable web lookups, retries after cutoffs). Propose routing/policy fixes to tools/task-tier-policy.md.

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. codex has no network and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- Delete transient tools/out/ scratch as soon as its task is verified/committed.
- Delete media.docx and projects.docx from repo root BEFORE any commit (never deploy/commit .docx uploads).

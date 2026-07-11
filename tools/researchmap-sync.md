# Researchmap managed sync implementation

## Study findings

- `entries(anchor)` reads the canonical English Achievements page with `newline=''`, isolates the named section's `<ol>`, splits `<li>` case-insensitively, extracts `data-*` metadata, and returns normalized citation text plus metadata tuples.
- `to_record(...)` resolves `sub006`/`sub007` to `presentations` only for Yokota sole-author entries and to `misc` otherwise. It parses citation authors/title/venue/date, lets `data-date` override the heuristic date, maps category-specific document fields, adds DOI or `see_also`, and returns an insert object using `similar_merge`.
- `fetch_live(type)` reads every page of a public researchmap collection, supporting list, `items`, and `@graph` response shapes plus `_links.next.href` and fallback pagination links. It rejects a zero-item result to avoid treating an API failure as an empty account.
- Existing `check_live()` fetches the four exporter categories and compares all current Yokota-authored website/profile records to live normalized title keys, including containment fallbacks. It writes only missing insert records to `tools/out/researchmap-import.jsonl`; it neither updates nor deletes.
- Existing CLI behavior is: `--init` snapshots all current normalized website/profile keys and exports nothing; default exports additions since that snapshot and advances it; `--dry-run` prints without writing; `--check-live` writes missing live inserts rather than using local state.
- `tools/researchmap-state.json` was a top-level JSON array containing 395 normalized baseline keys. The implementation migrates this backward-compatibly to an object with `baseline` plus a per-category `managed_ids` registry; the loader still accepts legacy arrays.
- CLAUDE.md documents inserts without `user_id`, updates as `{"update":{"type":"TYPE","id":"RM_ID"},"doc":{ONLY changed fields}}`, and deletes as `{"delete":{"type":"TYPE","id":"RM_ID"}}`. It requires `publication_date` for `published_papers`. The site category mapping is `sub001`/`sub004`/`sub005` to `published_papers`, `sub002`/`sub003` to `books_etc`, and `sub006`/`sub007` to `presentations` for Yokota sole author or `misc` otherwise.

## Design

The new `--sync` mode performs an offline-testable live diff per exporter-managed category. A website record tries DOI, then canonical URL, then exact normalized title. A criterion yielding multiple candidates is ambiguous and is skipped without falling through to a weaker criterion. Unique matches refresh the managed-ID registry and may generate a partial update. Previously managed IDs that match no current website record generate deletes only when their stored category is one of the four exporter categories. Arbitrary live records are never adopted for deletion merely because they are visible.

Existing default, `--init`, and `--check-live` behavior remains insert-only. `--sync --dry-run` performs the live read and prints operations but writes neither the import file nor the registry.

## Implementation and test notes

- Added `--sync`, which fetches the four live collections, emits inserts first, partial updates second, and registry-bounded deletes last, then prints `N inserts / M updates / K deletes` plus the ambiguous-skip count. A non-dry run writes the grouped operations to `tools/out/researchmap-import.jsonl` and refreshes `managed_ids` in the state file.
- `--dry-run` causes no import/state writes in sync mode. It is also now honored with legacy `--check-live`; without `--sync`, `--check-live` remains insert-only.
- Update documents are restricted by category to the website-controlled title, people array, publication date, venue/publisher/event, and `see_also` fields. DOI is used for identity but is not rewritten. Author/presenter arrays are compared and replaced as whole values.
- `tools/researchmap-state.json` now has 395 legacy keys under `baseline` and empty arrays under `managed_ids.published_papers`, `.books_etc`, `.presentations`, and `.misc`. `load_state()` still accepts the old top-level array, and `--init` replaces only `baseline`, preserving the managed registry.
- A pending delete ID remains registered until a later public read confirms it is absent. This allows a delete to be regenerated when a human chooses not to upload a prior import file or an upload fails. Ambiguous candidate IDs are protected from deletion.
- Added `tools/test-researchmap-export.py` using fake website/live sets. It verifies DOI priority over an exact-title alternative, canonical URL matching, changed-fields-only update documents, whole-array author replacement, exact-title ambiguity suppression, deletes only for a present managed ID in an exporter category, no deletion of arbitrary/unmanaged or outside-category IDs, no `user_id`, and required `publication_date` retention for a new/generated paper.
- `python3 -m py_compile tools/researchmap-export.py tools/test-researchmap-export.py` passed.
- `python3 tools/test-researchmap-export.py` passed: 2 tests, `OK`.
- `python3 tools/researchmap-export.py --dry-run` successfully loaded the migrated state shape and exercised the legacy local-state mode without writes. It reported the same kind of pending insert-only differences that the legacy baseline mechanism is designed to show.
- `git diff --check` passed for the implementation/state/test files.
- No real `--check-live` or `--sync` was run because this worker has no network access.

Before any upload, Claude/the user must run a live `python3 tools/researchmap-export.py --sync --dry-run` and human-review every proposed insert, update, ambiguity, and delete. After review, a non-dry `--sync` may create the import file and learn the initial registry. CLAUDE.md's researchmap section also needs a follow-up documentation proposal describing `--sync`, the managed registry, and the update/delete grammar; this task did not edit that hand-edit-only file.

## Structured result

- status: success
- summary: Implemented researchmap insert/update/delete sync with DOI/URL/title matching, partial updates, ambiguity protection, and exporter-managed category-bounded ID deletion.
- changed_files: `tools/researchmap-export.py`, `tools/researchmap-state.json`, `tools/test-researchmap-export.py`, `tools/researchmap-sync.md`, `tools/codex-log.md` (self-log appended last)
- commands: Offline verification used `python3 -m py_compile tools/researchmap-export.py tools/test-researchmap-export.py`, `python3 tools/test-researchmap-export.py`, `python3 tools/researchmap-export.py --dry-run`, and `git diff --check`. No network/live or publishing command was run.
- verification: Compilation passed; 2 fixture tests passed; legacy dry-run loaded the migrated state; diff check passed.
- evidence:
  - confirmed: Sync operations never include `user_id`; deletes are restricted to the four exporter types and IDs already in `managed_ids`; ambiguous candidates cannot be updated or deleted; published-paper fixtures retain `publication_date`.
  - hypotheses: Public API fixture shapes are based on the existing exporter and documented researchmap response/import grammar; a live dry run is required to validate current production response values and review semantic diffs.
- remaining: Run live `--sync --dry-run` and human review before any upload; then propose the corresponding CLAUDE.md researchmap documentation update.

# Benchmark artifact relocation report

Date: 2026-07-14 (Asia/Tokyo)

Task: T-168

Start: 10:38 +0900

End: 10:41 +0900

Model/effort: not exposed to the driver

## Outcome

The raw benchmark artifacts are necessary for the current artifact audit and
metric provenance: all 173 version-2 metric rows point to their `result.json`.
They are not website output and did not belong in the transient `tools/out/`
directory. All 173 run directories were moved to the ignored benchmark-owned
`tools/agent-benchmark/artifacts/` archive, and `tools/out/` is empty.

## Preservation and pointer migration

- Source archive: 173 directories, 1,102 files, 57 MB on disk.
- Aggregate ordered file-hash digest before and immediately after the move:
  `276ce1389bd67c197fdc0345588c869be1b5f9c995fbafd2b9e4deaf13c8a559`.
- Updated the benchmark runner and metric fallback for future artifacts.
- Updated the benchmark README, 173 compact result rows, 173 metric rows, and
  the two execution-path fields in every raw `result.json` (519 tracked path
  occurrences plus 346 raw-result occurrences).
- Added the archive path to `.gitignore`; raw evidence remains local just as it
  did under the ignored `tools/out/` location.

## Verification

- Benchmark selftest: pass; five task definitions and all six efforts valid.
- Artifact audit: pass; 173 result rows, 173 complete directories, 173 metric
  pointers, zero missing/orphan/incomplete artifacts, 46,542,593 logical bytes.
- Capsule audit: pass for WBD-001 through WBD-005.
- Task metrics: 201 valid rows, including all 173 schema-v2 benchmark rows.
- Exact resolution check: every compact result and metric pointer resolves at
  the new location; no old benchmark-output path remains.
- Full repository security/standards suite is run before commit.

No network operation, deployment, or external write occurred. The standard
driver report is stored here instead of `tools/out/` because the user
explicitly required that directory to be completely empty.

# Judge checklist — Round 2

Judge-only, `main`-only checklist; never sync this file to contestant branches.

## Setup

- [x] Seed shared board with T-10 through T-13.
- [ ] Create one shared scaffold equal to `main` minus `tools/judge/`; follow-up worker records SHA here: `pending`.
- [ ] Force-move `sol`, `terra`, `fable`, and `opus` to that same scaffold SHA.
- [ ] Await user-run contestants; do not infer approval to run or publish.

## Judge the round

- [ ] Follow `skills/model-eval.md`: fan out four read-only `codex-spark-low` extractions, one per branch.
- [ ] Send all four extraction reports to `codex-high` for the verdict.
- [ ] Disclose judge identity and contestant overlap; coordinator independently spot-checks decisive claims.
- [ ] Score task correctness/completeness/scope/evidence and proposal quality.
- [ ] Triage worthwhile contestant `P-*` proposals into new `T-*` ids.
- [ ] Report each branch's first-own-commit→last-own-commit span, scaffold→last-commit span, and self-reported metric sum.
- [ ] State that runs started sequentially and scaffold spans therefore have sequential-start bias.

## Close and reset

- [ ] Tag all four tips `eval/r2-{sol,terra,fable,opus}` before any reset.
- [ ] Merge winner into `main`, protecting `tools/judge/` as specified by `skills/model-eval.md`.
- [ ] Append the compact scorecard and caveats to `tools/judge/log.md`.
- [ ] Clear/reseed `tools/todo.md` for the next round.
- [ ] Build the next judge-free shared scaffold and resync all four branches.

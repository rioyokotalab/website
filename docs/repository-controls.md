# Repository controls

The website owns its complete contributor gate. `.github/workflows/ci.yml`
runs on pull requests targeting `main` with read-only contents permission,
immutable checkout, no persisted Git credentials, no deployment, and no
repository-external source checkout. The required check is `Offline checks`.
There is no post-merge push run: the ruleset's strict up-to-date policy plus
squash merges make the merged tree byte-identical to the tested PR head, and
the duplicate run only produced redundant actor notification emails (T-194).

Active ruleset `19127356` protects `main` with pull requests, conversation
resolution, an up-to-date branch, linear history, force-push and deletion
protection, and one required approving review. A Repository-admin bypass
(role id 5) lets the sole admin owner merge own PRs without review; the other
collaborators (write role, inherited from the org default) must obtain one
approval (T-198). Merges still require this repository's CI to pass and
conversations to be resolved.

`docs/github-rulesets/main.json` is the repository-owned restore/update
payload. `tools/test-github-ruleset.sh` validates its exact local contract.
Changing the live rule remains a separate authenticated Administration write;
editing or testing this payload does not change GitHub settings.

The workflow installs Ubuntu's pinned `lftp` package only for the local file
mirror regression. It invokes no FTP/SSH endpoint and never runs `publish.sh`
or `deploy.sh`.

## Hardened repository settings (T-197)

Applied 2026-07-18 as least-privilege defaults for the public repository; exact
before/after values and rollback commands are in
`tools/out/t197-settings-rollback.md`. The default `GITHUB_TOKEN` permission is
`read` and the token cannot approve pull requests; workflows must be pinned to a
full commit SHA; Dependabot security updates and private vulnerability reporting
are enabled (alerts and secret scanning + push protection were already on);
Actions from forks require owner approval for all external contributors; and the
unused wiki and projects features are disabled. `tools/workflow-security-check.py`
enforces the in-repository half of this posture (no `pull_request_target`,
SHA-pinned actions, minimal permissions, `npm ci --ignore-scripts`,
`persist-credentials: false`). `docs/security-threat-model.md` holds the full
attack-surface review.

# Repository controls

The website owns its complete contributor gate. `.github/workflows/ci.yml`
runs on `main` pushes and pull requests with read-only contents permission,
immutable checkout, no persisted Git credentials, no deployment, and no
repository-external source checkout. The required check is `Offline checks`.

Active ruleset `19127356` protects `main` with pull requests, conversation
resolution, an up-to-date branch, linear history, force-push and deletion
protection, no bypass actor, and zero required approvals. An author may merge
after this repository's required CI passes and conversations are resolved.

`docs/github-rulesets/main.json` is the repository-owned restore/update
payload. `tools/test-github-ruleset.sh` validates its exact local contract.
Changing the live rule remains a separate authenticated Administration write;
editing or testing this payload does not change GitHub settings.

The workflow installs Ubuntu's pinned `lftp` package only for the local file
mirror regression. It invokes no FTP/SSH endpoint and never runs `publish.sh`
or `deploy.sh`.

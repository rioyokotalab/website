#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)

python3 - "$ROOT/docs/github-rulesets/main.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
assert data["name"] == "main-strict-review"
assert data["target"] == "branch"
assert data["enforcement"] == "active"
# Repository-admin bypass (role id 5) lets the owner — the sole admin; the
# other collaborators are write — merge own PRs without review, while the
# review requirement below gates everyone else (T-198).
assert data["bypass_actors"] == [
    {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
]
assert data["conditions"] == {
    "ref_name": {"exclude": [], "include": ["refs/heads/main"]}
}
assert [rule["type"] for rule in data["rules"]] == [
    "deletion",
    "non_fast_forward",
    "required_linear_history",
    "pull_request",
    "required_status_checks",
]
pull_request = next(rule for rule in data["rules"] if rule["type"] == "pull_request")
assert pull_request["parameters"] == {
    "allowed_merge_methods": ["squash", "rebase"],
    "dismiss_stale_reviews_on_push": True,
    "require_code_owner_review": False,
    "require_last_push_approval": False,
    "required_approving_review_count": 1,
    "required_review_thread_resolution": True,
}
checks = next(rule for rule in data["rules"] if rule["type"] == "required_status_checks")
assert checks["parameters"] == {
    "do_not_enforce_on_create": False,
    "required_status_checks": [
        {"context": "Offline checks", "integration_id": 15368}
    ],
    "strict_required_status_checks_policy": True,
}
print("PASS: website GitHub ruleset payload")
PY

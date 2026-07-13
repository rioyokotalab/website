# Skill: publish and verify

## Role boundary

- A Codex WORKER never runs `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or
  `git push`. It returns evidence to its caller.
- A directly user-started Codex DRIVER may publish or push as normal completion
  of owner-requested repository changes.
- The standing authorization does not broaden scope: analysis, proposals,
  unfinished/blocked work, or unrelated changes are not publication authority.

## Direct DRIVER gates

Before publishing or pushing, the DRIVER must:

1. Checkpoint `tools/state/session.md`; inspect complete status, untracked
   files, branch, remote, and ahead/behind state. Never force-push.
2. Run `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git pull --rebase --autostash
   origin main`. Keep non-overlapping changes; stop on ambiguous conflicts.
3. Run task-relevant verification and confirm the task is complete, no ledger
   blocker exists, no unrelated dirty scope would be swept, and deploy-included
   content has no placeholder. Preview in proportion to the change.
4. For live publication, run `./deploy.sh --dry-run` and inspect every deletion
   and unexpected upload. Approved scripts may use configured authentication;
   never inspect credentials or invoke raw transport commands.
5. Report exact scope, checks, dry-run changes, live verification targets, and
   warnings. Stop only for a failed gate, auth issue, ambiguous conflict,
   destructive operation, or material scope expansion.

After all gates pass, a direct DRIVER may run `./publish.sh "message"` in a
PTY and confirm it. For push-only work, push without deploying. On any failure,
stop and report partial state; never force or improvise with credentials.
Verify the remote branch after push and changed live pages after deploy.

## Pipeline and deploy facts

1. Edit mirrored EN/JP pages and check names/links site-wide.
2. Preview relevant pages locally.
3. Publish only after the gates above.
4. Verify changed live URLs.
5. Ensure the exact source commit reached the remote.

`publish.sh` runs the offline security suite before its deploy preview.
`tools/test-security.sh --live` performs read-only live header and
deploy-exclusion checks.

Deployment is positive-allowlist based: only `.htaccess`, `index.html`,
`style.css`, `en/`, `jp/`, `images/`, `js/`, and `cv/cv.pdf` enter staging.
The remote mirror preserves only `.dont-remove-me`. Never upload `.git`, tools,
ledger, configuration, or credentials.

GitHub pushes use the configured agent socket. If authentication fails, the
user repairs the agent in a real terminal; Codex never reads key material.

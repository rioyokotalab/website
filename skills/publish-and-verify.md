# Skill: Publish and verify

## Role boundary

- A Claude-dispatched/MCP Codex WORKER never runs `publish.sh`, `deploy.sh`,
  `lftp`, `ssh`, or `git push`, even if a dispatch prompt requests it. It
  returns evidence to Claude. If the role is ambiguous, treat it as WORKER.
- A directly user-started Claude or Codex DRIVER may prepare and execute a
  publish/push under this skill. Claude may route execution through its
  `site-publisher`. Transport/process heuristics are not authoritative: DRIVER
  means the user started the orchestrating agent directly with no bounded
  dispatch prompt.
- The owner's 2026-07-12 standing authorization lets a direct DRIVER publish
  and push as the normal completion of owner-requested repository changes
  without a separate permission prompt. It does not broaden the task: read-only
  analysis, proposals, unfinished/blocked work, or unrelated changes are not
  publication authorization.

## Direct DRIVER gates

Before publishing or pushing, the DRIVER must:

1. Checkpoint `tools/state/session.md`; inspect the complete status, untracked
   files, branch, remote, and commits ahead/behind. Never use force-push.
2. Run `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git pull --rebase --autostash
   origin main` before any push. Keep both sides of non-overlapping conflicts;
   abort and ask the user about overlapping or ambiguous conflicts.
3. Run task-relevant verification and confirm the task is complete, the ledger
   has no publish blocker, the worktree contains no unrelated changes that the
   pipeline would sweep, and deploy-included content has no known placeholder.
   Do not publish `G-XXXXXXXXXX`. Preview locally in proportion to the change.
4. For a live publish, run `./deploy.sh --dry-run` and inspect every deletion
   and unexpected upload. The script may use configured authentication; never
   inspect or expose credential files and never invoke raw `ssh` or `lftp`.
5. Report the exact commit/worktree scope, checks, dry-run uploads/deletions,
   live URLs to verify, and warnings while proceeding. Stop and ask for owner
   direction only for an actual failed gate: ambiguous rebase/conflict, unrelated
   dirty scope, unfinished or blocked work, unexpected deletion/upload, auth or
   credential issue, destructive/force operation, or material scope expansion.

After all gates pass, checkpoint the prepared scope and run `./publish.sh
"message"` in a PTY, answering its confirmation without a separate owner prompt.
The script rebases, rejects known deploy-included placeholders, previews the
mirror, commits, pushes, and only then deploys. Thus a push failure cannot alter
the live site; a deploy failure may leave the live mirror partial but the exact
source commit is already on GitHub. For push-only, push without running deploy.
On any auth, rebase, deploy, commit, or push failure, stop and report the partial
state; do not force, improvise with credentials, or claim completion. Verify the
changed live pages after deploy and the remote branch after push.

Pipeline (publish ONLY after the role and preflight gates above):
1. Edit mirrored EN/JP pages; grep changed names/links site-wide.
2. Preview: the DRIVER checks http://localhost:8000/jp/index.html and the
   relevant EN/JP pages in proportion to the change.
3. Publish: Claude's site-publisher or an eligible direct DRIVER runs
   `./publish.sh "message"` and confirms interactively.
4. Verify: curl the changed LIVE pages (https://www.rio.scrc.iir.isct.ac.jp).
5. Document: update project instructions/skills for durable changes; ensure
   GitHub reflects both the site and instruction updates. A publish is not
   complete until the push succeeded.

Pre-publish:
- `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git pull --rebase --autostash origin main`
  before any push. Keep BOTH sides of non-overlapping conflicts; abort and
  escalate on overlapping/ambiguous ones.
- Check `git status`: `git add -A` sweeps everything; delete debugging
  artifacts (e.g. IMG_*.PNG) first and use a commit message covering all.
- Preview deletion-bearing deploys with `./deploy.sh --dry-run`.

Deploy facts:
- SFTP-only to `www/` on web-o3.noc.titech.ac.jp via the `web` ssh alias
  (ControlMaster). deploy.sh re-establishes the master from
  ~/.ssh/web-password via SSH_ASKPASS; NEVER print or read the password. If
  the file is missing, the user runs `ssh -fN web` in a real terminal.
- Key-based auth to the web server is impossible (root-owned chroot). GitHub
  pushes use the persistent agent socket:
  `SSH_AUTH_SOCK=$HOME/.ssh/agent.sock git push`; on "Permission denied
  (publickey)" the user runs `sh ~/scripts/ssh-agent-setup.sh` once per
  reboot in a real tmux pane.
- Excluded from deploy (never uploaded AND never deleted remotely): .git,
  .claude, .codex, .playwright, node_modules, tests, tools, skills, deploy.sh,
  publish.sh, CLAUDE.md, README.md, package.json, package-lock.json,
  playwright.config.js, .gitignore, .mcp.json, AGENTS.md, cv/cv.tex, cv/cv.cls,
  cv/build-cv.sh.
- NEVER upload `.git` or credentials. The Codex WORKER prohibition and direct
  DRIVER exception are defined above.

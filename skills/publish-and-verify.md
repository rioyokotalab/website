# Skill: Publish and verify

Pipeline (publish ONLY after explicit user approval in the conversation):
1. Edit mirrored EN/JP pages; grep changed names/links site-wide.
2. Preview: user checks http://localhost:8000/jp/index.html; wait for OK.
3. Publish: site-publisher runs `echo y | ./publish.sh "message"`.
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
  .claude, tools, skills, deploy.sh, publish.sh, CLAUDE.md, README.md,
  .gitignore, .mcp.json, AGENTS.md, cv/cv.tex, cv/cv.cls, cv/build-cv.sh.
- NEVER upload .git or credentials. codex never runs publish.sh, deploy.sh,
  lftp, ssh, or git push — not even dry-runs.

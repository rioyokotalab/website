# Website and repository threat model

Evidence-based attack-surface review conducted 2026-07-18 (T-195) after the
repository became public. It records assets, trust boundaries, attack vectors
per surface, existing controls, and the hardening task queue. It is
deploy-excluded (docs/ is not in the public allowlist).

## Assets and trust boundaries

- **Served site** — static HTML/CSS/JS plus one CV PDF at
  `www.rio.scrc.iir.isct.ac.jp`. No server-side code, database, forms, or
  authentication. Compromise value: defacement or malicious script injection
  affecting visitors.
- **Public Git repository** — `github.com/rioyokotalab/website`, full history
  public since T-192. Compromise value: unauthorized change to `main`
  (which feeds deployment), CI abuse, or exposure of anything committed.
- **Deploy pipeline** — owner-run `publish.sh`/`deploy.sh` over SFTP/lftp
  behind an allowlist. Credentials live only with the owner, never in the
  repository. Compromise value: pushing arbitrary content live.
- **Trust boundaries**: visitor↔site (untrusted client), public
  contributor↔repository (untrusted PRs on a public repo), repository↔runner
  (CI executes repository/PR code), owner workstation↔host (authenticated
  deploy). Each is a separate authority boundary.

## Surface A — served static site (visitor-facing)

Existing controls are strong and regression-tested by `tools/security-check.py`
and `tools/supply-chain-check.py`:

- Strict CSP with no `unsafe-inline`/`unsafe-eval`; `object-src 'none'`,
  `frame-ancestors 'none'`, `base-uri 'self'`, `form-action 'self'`,
  `upgrade-insecure-requests`. Enforced source is checked, not just present.
- `X-Content-Type-Options`, `X-Frame-Options: SAMEORIGIN`, restrictive
  `Referrer-Policy` and `Permissions-Policy`, HSTS.
- Every external runtime asset (jQuery 3.7.1, Lightbox 2.11.4 on six gallery
  pages) is HTTPS, SRI-pinned with `crossorigin="anonymous"`, and hash-verified
  online; any unreviewed external asset fails the build.
- All `target="_blank"` links require `rel="noopener noreferrer"`; mixed active
  content, sensitive URL queries, and pre-consent analytics requests fail the
  check. Analytics load only after explicit opt-in.

Residual: HSTS `max-age=86400` is deliberately short (fast recovery if HTTPS
breaks) rather than a preload-length commitment. Raising it is a sticky live
change; recorded as a proposal, not auto-applied.

## Surface B — public repository and CI (newly exposed)

This is where public status adds the most risk. Confirmed gaps (2026-07-18):

| # | Finding | Severity | Fix |
|---|---|---|---|
| B1 | Repo default `GITHUB_TOKEN` permission is **write** | High | Set repo default to read; workflow already overrides to `contents: read` (T-197) |
| B2 | Token may **approve pull requests** | Medium | Disable can-approve (T-197) |
| B3 | SHA-pinning of actions **not required** | Low | Require it; workflow already pins (T-197) |
| B4 | Dependabot **security updates disabled** (alerts on) | Medium | Enable security updates + `dependabot.yml` (T-196/T-197) |
| B5 | Fork-PR approval only for **first-time** contributors | Medium | Require approval for all outside collaborators (T-197) |
| B6 | `has_wiki`/`has_projects` enabled but **unused** | Low | Disable to reduce surface (T-197) |
| B7 | CI `npm ci` runs **lifecycle scripts**; top-level perms not minimal | Medium | `--ignore-scripts`, explicit minimal `permissions` (T-196) |
| B8 | No `SECURITY.md`, no workflow-security regression test | Low | Add both (T-196) |

Already sound: secret scanning + push protection on with zero alerts; the
value-free history audit (`tools/public-repo-audit.py`) found no credential;
the workflow uses `pull_request` (not `pull_request_target`), pins
`actions/checkout` to a SHA, sets `persist-credentials: false`, holds no
secrets, and runs the supply-chain lockfile check *before* any `npm ci`, so a
fork that alters dependencies fails before install. The strict `main` ruleset
(PR + required CI, linear history, no bypass) gates every change to the
deploy-feeding branch.

## Surface C — deploy pipeline

Positive-allowlist staging (`tools/stage-public-site.sh`,
`tools/deploy-files.filter`): only `.htaccess`, `index.html`, `robots.txt`,
`sitemap.xml`, `style.css`, `en/`, `jp/`, `images/`, `js/`, `cv/cv.pdf` reach
staging; symlinks fail closed; the remote mirror preserves only its sentinel.
Credentials are owner-only and never in the repository. No agent runs raw
transport. Assessed adequate; no change queued.

## Hardening task queue

- **T-196** — Repository-content security baseline: `SECURITY.md`,
  `.github/dependabot.yml`, `ci.yml` hardening (`--ignore-scripts`, minimal
  `permissions`), and `tools/test-workflow-security.sh` wired into the offline
  suite. Executed via PR.
- **T-197** — Repository-settings hardening (reversible, reported): default
  workflow token read-only, disable token PR-approval, require SHA-pinned
  actions, enable Dependabot security updates, require fork-PR approval for all
  outside collaborators, disable unused wiki/projects.
- **Proposals (owner judgment)**: raise HSTS `max-age` toward a preload-length
  commitment; consider restricting Actions `allowed_actions` to selected once
  the exact pinned set is enumerated.

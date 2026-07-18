# Security policy

This repository holds the static YOKOTA Lab website
(`www.rio.scrc.iir.isct.ac.jp`). It has no server-side code, database, user
accounts, or forms; the site is served as static files.

## Reporting a vulnerability

Please report suspected vulnerabilities privately rather than opening a public
issue or pull request:

- Preferred: GitHub private vulnerability reporting — the **Report a
  vulnerability** button under this repository's **Security** tab.
- Alternatively, use the lab contact listed at
  https://www.rio.scrc.iir.isct.ac.jp/en/contact/.

Please include the affected URL or file, a description, and reproduction steps.
We aim to acknowledge reports within a few working days. There is no bug-bounty
program.

## Scope

In scope: the served static site and its client-side assets, this repository's
CI/workflow configuration, and the deployment allowlist. Out of scope:
third-party services the site references (e.g. CDN-hosted libraries, analytics,
embedded maps), and social-engineering or physical attacks.

## Handling

Fixes land through the protected `main` branch: a pull request that passes the
required `Offline checks` run, under the repository's branch ruleset. Secret
scanning and push protection are enabled; credentials are never stored in the
repository.

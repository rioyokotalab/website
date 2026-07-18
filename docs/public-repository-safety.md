# Public repository safety audit

`tools/public-repo-audit.py` audits every blob reachable from every Git ref and
records only finding metadata. It never records the matching value, line, or
snippet. Samples are bounded to 50 per rule and 500 overall; complete metadata
counts remain in `finding_counts`. Uncommitted and ignored file contents are
not read, and unreachable or reflog-only objects are outside its scope.

`docs/audits/public-history-20260716.json` covers website revision `a8717928`.
It found no private-key header, known token shape, suspicious secret filename,
or high-entropy credential. The single credential-assignment candidate is a
historical, HEAD-absent `lightbox/js/jquery.js` expression that was value-free
compared with the official jQuery 1.2.3 distribution and classified as vendor
noise. Nine large blobs are public image/PDF assets. Operational paths remain
an intentional public topology exposure rather than a credential finding.

The recorded working tree had four unrelated ledger-only dirty entries. Their
contents were not inspected. The artifact therefore attests only to its named
HEAD and reachable history at that time.

Run a future audit only to a new output path; the tool refuses overwrite:

```sh
python3 tools/public-repo-audit.py --repo "$PWD" --name website \
  --output docs/audits/public-history-NEW-DATE.json
```

`tools/test-public-repo-audit.sh` creates deleted hostile fixture history and
proves that matching values stay absent from stdout, stderr, and the JSON
report. A finding is a review signal, not proof of a secret. Metadata-first
review must not print or copy the matched value.

## Sanitized public mirror (T-192)

Per the T-185 assessment, this repository's full history must not be made
public directly. `tools/build-public-mirror.sh DEST [AUDIT_OUT]` builds the
approved alternative: a fresh local Git repository containing one commit of
only the deploy allowlist minus `.htaccess`, plus a provenance README naming
the source commit. It refuses relative or non-empty destinations, verifies
that tooling, ledgers, configuration, and CV sources are absent, and fails on
any non-`large-blob` audit finding or value exposure. The build is entirely
local and configures no remote; creating or pushing a public repository is a
separate owner-authorized action. `tools/test-public-mirror.sh` covers the
generator offline.

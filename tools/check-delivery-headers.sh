#!/bin/bash
# Inspect representative production delivery headers without changing the site.
set -euo pipefail

BASE=${1:-https://www.rio.scrc.iir.isct.ac.jp}
URLS=(
	"$BASE/en/"
	"$BASE/style.css"
	"$BASE/js/pagetop.js"
	"$BASE/images/banner-top.jpg"
)

for url in "${URLS[@]}"; do
	printf '%s\n' "URL $url"
	curl --compressed --silent --show-error --dump-header - --output /dev/null "$url" |
		tr -d '\r' |
		awk 'BEGIN { IGNORECASE=1 }
			/^HTTP\// || /^(cache-control|content-encoding|content-length|content-type|etag|expires|last-modified|vary):/ { print }'
done

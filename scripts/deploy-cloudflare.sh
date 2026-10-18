#!/usr/bin/env bash
# Deploy only committed public static files to the Cloudflare Worker serving olaryn.com.
# Requires a locally authenticated Wrangler session.
# Optional: WRANGLER_BIN=/path/to/wrangler or /path/to/wrangler.js
# Optional: DEPLOY_DRY_RUN=1 to validate the upload without deploying.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 scripts/check-pages.py
python3 scripts/check-design-lock.py
if ! git diff --quiet HEAD -- index.html _headers _redirects robots.txt sitemap.xml site.webmanifest assets auth billing analytics *.svg *.png *.ico; then
  echo "Refusing to deploy uncommitted website changes. Commit and validate first." >&2
  exit 1
fi

if [[ -n "${WRANGLER_BIN:-}" ]]; then
  if [[ "${WRANGLER_BIN}" == *.js ]]; then
    wrangler=(node "$WRANGLER_BIN")
  else
    wrangler=("$WRANGLER_BIN")
  fi
elif command -v wrangler >/dev/null 2>&1; then
  wrangler=(wrangler)
else
  wrangler=(npx --yes wrangler@4)
fi

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

# Deliberately allowlist public assets. Do not upload .git, docs,
# local credentials, scripts, workspace files or test artefacts.
while IFS= read -r -d '' path; do
  case "$path" in
    index.html|_headers|_redirects|robots.txt|sitemap.xml|site.webmanifest|\
    favicon.svg|favicon.ico|favicon-16x16.png|favicon-32x32.png|\
    apple-touch-icon.png|icon-192.png|icon-512.png|logo-mark.svg|logo-mark.png|og-image.png|\
    auth/index.html|billing/index.html|analytics/index.html|\
    assets/base.css|assets/home.css|assets/platform.css|assets/analytics.css|assets/theme.js|assets/marks.svg|\
    assets/fonts/*|assets/og/*|assets/companies/*)
      mkdir -p "$stage/$(dirname "$path")"
      cp -- "$path" "$stage/$path"
      ;;
  esac
done < <(git ls-files -z)

if [[ ! -f "$stage/index.html" || ! -f "$stage/_headers" || ! -f "$stage/auth/index.html" ]]; then
  echo "Public asset package is incomplete." >&2
  exit 1
fi

sha="$(git rev-parse --short HEAD)"
echo "Deploying commit $sha to the olaryn Worker serving olaryn.com."
args=(deploy --config "$ROOT/wrangler.jsonc" --assets "$stage" --keep-vars --message "Olaryn site ($sha)")
if [[ "${DEPLOY_DRY_RUN:-0}" == 1 ]]; then args+=(--dry-run); fi
"${wrangler[@]}" "${args[@]}"

#!/usr/bin/env bash
# Detect dead nav stubs registered in Caddyfile @agent_shells but missing on disk or returning 404.
# Usage: detect-dead-stubs.sh [BASE_URL]
# Example: detect-dead-stubs.sh https://arif-fazil.com
set -eu

BASE="${1:-https://arif-fazil.com}"
CADDY="/etc/caddy/Caddyfile"
WEBROOT="/var/www/html/arif"

# Extract paths from @agent_shells matcher line
PATHS=$(grep -oP '(@agent_shells\s+path\s+)(.*)' "$CADDY" \
  | head -1 \
  | sed 's/^@agent_shells\s\+path\s\+//' \
  | tr ' ' '\n' \
  | sed 's|/\*$||' \
  | sort -u)

echo "Probing ${BASE} for paths in @agent_shells..."
echo

broken=""
ok_count=0
for p in $PATHS; do
  [[ -z "$p" ]] && continue
  code=$(curl -sI -o /dev/null -w "%{http_code}" "${BASE}${p}/" --max-time 5 || echo "000")
  if [[ "$code" != "200" && "$code" != "301" && "$code" != "302" ]]; then
    echo "  BROKEN (${code})  ${p}/"
    broken="${broken}${p}\n"
  else
    echo "  ok (${code})      ${p}/"
    ok_count=$((ok_count + 1))
  fi
done

total=$(echo "$PATHS" | wc -l)
echo
echo "Totals: ${ok_count}/${total} ok"
if [[ -n "$broken" ]]; then
  echo
  echo "BROKEN PATHS:"
  echo -e "$broken"
  echo
  echo "Fix options per skill: see arif-fazil-site-ops/references/dead-stub-redirect-recipe.md"
  exit 1
fi

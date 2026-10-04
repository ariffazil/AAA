#!/bin/bash
# verify-makcikgpt.sh — 3-gate verification for MakcikGPT articles
# Usage: ./verify-makcikgpt.sh <slug>
# Must pass all 3 gates before reporting "published"

SLUG="$1"
BASE="https://arif-fazil.com/world/makcikgpt"
INDEX="/var/www/html/arif/makcikgpt-md/index.html"

if [ -z "$SLUG" ]; then
  echo "Usage: $0 <article-slug>"
  exit 1
fi

echo "=== MakcikGPT 3-gate verification: $SLUG ==="
echo ""

# Gate 1: curl (bot UA) returns 200 with content
echo "Gate 1: curl (bot UA)..."
curl -sfL -o /tmp/verify_$SLUG.html -w "HTTP:%{http_code} SIZE:%{size_download}\n" "$BASE/$SLUG/"
HTTP=$(curl -sfL -o /dev/null -w "%{http_code}" "$BASE/$SLUG/")
SIZE=$(wc -c < /tmp/verify_$SLUG.html 2>/dev/null || echo 0)
TITLE=$(grep -oE "<title>[^<]+</title>" /tmp/verify_$SLUG.html 2>/dev/null | head -1 | sed 's/<[^>]*>//g' | head -c 80)

if [ "$HTTP" = "200" ] && [ "$SIZE" -gt 2000 ]; then
  echo "  ✅ HTTP:$HTTP SIZE:${SIZE}B TITLE: $TITLE"
  GATE1="PASS"
else
  echo "  ❌ HTTP:$HTTP SIZE:${SIZE}B (expected 200 + >2KB)"
  GATE1="FAIL"
fi

# Gate 2: browser renders article (not "ARTICLE NOT FOUND")
echo ""
echo "Gate 2: browser render..."
echo "  → Navigate to: $BASE/$SLUG/"
echo "  → Check: h1 matches article title (NOT 'ARTICLE NOT FOUND')"
echo "  → ⚠️  Manual verification required — run in browser"
GATE2="MANUAL"

# Gate 3: landing page lists the article
echo ""
echo "Gate 3: landing page listing..."
if [ -f "$INDEX" ]; then
  COUNT=$(grep -c "$SLUG" "$INDEX" 2>/dev/null || echo 0)
  if [ "$COUNT" -ge 1 ]; then
    echo "  ✅ Slug appears $COUNT times in index.html"
    GATE3="PASS"
  else
    echo "  ❌ Slug NOT found in index.html"
    GATE3="FAIL"
  fi
else
  echo "  ❌ Landing page not found: $INDEX"
  GATE3="FAIL"
fi

# Summary
echo ""
echo "=== Summary ==="
echo "Gate 1 (curl):    $GATE1"
echo "Gate 2 (browser):  $GATE2"
echo "Gate 3 (index):    $GATE3"

if [ "$GATE1" = "PASS" ] && [ "$GATE3" = "PASS" ]; then
  echo ""
  echo "✅ Curls + landing page: PASS"
  echo "⚠️  Verify Gate 2 manually in browser before reporting 'published'"
  exit 0
else
  echo ""
  echo "❌ Verification FAILED — do not report 'published'"
  exit 1
fi

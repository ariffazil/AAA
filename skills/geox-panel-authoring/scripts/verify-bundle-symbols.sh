#!/usr/bin/env bash
# verify-bundle-symbols.sh — count distinctive runtime literals in a minified bundle.
#
# Minifiers (esbuild, swc, terser) rename React components, so grep for distinctive
# RUNTIME STRING LITERALS that survive minification: MCP lane names, JSX label text,
# content keywords. A non-zero count for an expected literal means the component
# shipped; a zero usually means it was tree-shaken.
#
# Usage:
#   verify-bundle-symbols.sh <bundle.js> [symbol ...]
#
# Example:
#   verify-bundle-symbols.sh dist/assets/index-abc123.js \
#     LogDock PetrophysicalTracks geox_well_view geox_petrophysics
#
# Exits 0 if every symbol is present, 1 if any are missing, 2 on bad usage.
#
# The script is intentionally shell-portable (bash 4+); invoke with `bash <path>`
# if the execute bit is not set in your checkout.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <bundle.js> [symbol ...]" >&2
  echo "" >&2
  echo "Grep distinctive runtime literals in a minified bundle to confirm" >&2
  echo "components survived tree-shaking." >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  $0 dist/assets/index-abc123.js \\" >&2
  echo "    LogDock PetrophysicalTracks geox_well_view geox_petrophysics" >&2
  exit 2
fi

BUNDLE="$1"; shift

if [[ ! -f "$BUNDLE" ]]; then
  echo "ERROR: bundle not found: $BUNDLE" >&2
  exit 2
fi

size=$(stat -c%s "$BUNDLE" 2>/dev/null || stat -f%z "$BUNDLE")
echo "Bundle: $BUNDLE  (${size} bytes)"
echo "--- symbol counts ---"

missing=0
total=$#
for sym in "$@"; do
  count=$(grep -oF -- "$sym" "$BUNDLE" | wc -l)
  if [[ "$count" -eq 0 ]]; then
    marker="✗"
    missing=$((missing + 1))
  else
    marker="✓"
  fi
  printf "  %s %-40s %s\n" "$marker" "$sym" "$count"
done

echo "--- verdict ---"
if [[ "$missing" -eq 0 ]]; then
  echo "PASS: all $total expected literals present in bundle"
  exit 0
else
  echo "FAIL: $missing of $total expected literals missing"
  echo "  → component may not be reachable from the live entry chain"
  echo "  → trace: grep -rn 'import.*<Component>' src/main.tsx src/App*.tsx"
  exit 1
fi
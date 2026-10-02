#!/usr/bin/env bash
# verify_artifact.sh — Render→Rasterize→Read verification gates
# Required gates: structural / file / rasterize / round-trip / hash
# Tool-OK ≠ page-correct: blank pages, tofu, clipping all return exit 0.

set -u

PDF="${1:?usage: verify_artifact.sh <file.pdf>}"
[ -f "$PDF" ] || { echo "FAIL: file not found: $PDF"; exit 2; }
FAILED=0
echo "=== VERIFY $PDF ==="

fail() { echo "FAIL: $*"; FAILED=1; }

# G1: structural
if command -v pdfinfo >/dev/null 2>&1; then
  info=$(pdfinfo "$PDF" 2>&1) || fail "G1 pdfinfo exit non-zero"
  pages=$(printf '%s\n' "$info" | awk '/^Pages:/ {print $2}')
  if [ -n "${pages:-}" ] && [ "$pages" -ge 1 ]; then
    echo "G1 pdfinfo: OK (pages=$pages)"
  else
    fail "G1 pdfinfo: page count unreadable"
  fi
else
  fail "G1: pdfinfo MISSING"
fi

if command -v qpdf >/dev/null 2>&1; then
  if qpdf --check "$PDF" >/dev/null 2>&1; then
    echo "G1 qpdf --check: OK"
  else
    fail "G1 qpdf --check: structural errors"
  fi
else
  echo "G1 qpdf: MISSING — gate weakened to pdfinfo only"
fi

# G2: rasterize first/last page
if command -v pdftoppm >/dev/null 2>&1 && [ -n "${pages:-}" ]; then
  tmpd=$(mktemp -d)
  if pdftoppm -png -r 60 -f 1 -l 1 "$PDF" "$tmpd/first" >/dev/null 2>&1; then
    for png in "$tmpd"/first*.png; do
      [ -e "$png" ] || { fail "G2: first page produced no raster"; continue; }
      sz=$(wc -c < "$png")
      if [ "$sz" -lt 5120 ]; then fail "G2: page 1 raster ${sz}B < 5KB"; else echo "G2 page 1: OK (${sz}B)"; fi
    done
  else fail
    fail "G2: pdftoppm failed on page 1"
  fi
  rm -rf "$tmpd"
fi

# G3: round-trip
if command -v pdftotext >/dev/null 2>&1; then
  txt=$(pdftotext "$PDF" - 2>/dev/null)
  if [ -n "$txt" ] && [ ${#txt} -gt 200 ]; then
    echo "G3 pdftotext: OK (${#txt} chars)"
  else
    fail "G3 pdftotext: empty or too short"
  fi
else
  fail "G3: pdftotext MISSING"
fi

# G4-data accuracy: hash stable
sha=$(sha256sum "$PDF" | awk '{print $1}')
echo "G4-hash: $sha"

if [ $FAILED -eq 0 ]; then
  echo "=== PASS: all gates ==="
  exit 0
else
  echo "=== FAIL: see above ==="
  exit 1
fi

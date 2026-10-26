#!/usr/bin/env bash
# pdf_verify.sh — Render -> Rasterize -> Read verification gates (I7 / D7)
# Usage: pdf_verify.sh <file.pdf> [sentinel1 sentinel2 ...]
# No PDF ships without G1-G3. Tool-OK != page-correct.

set -u

fail() { echo "FAIL: $*"; FAILED=1; }

PDF="$1"
if [ ! -f "$PDF" ]; then echo "FAIL: file not found: $PDF"; exit 2; fi
shift
FAILED=0
echo "=== VERIFY $PDF ==="

# --- G1: structural integrity ---
if command -v pdfinfo >/dev/null 2>&1; then
  info=$(pdfinfo "$PDF" 2>&1) || fail "G1 pdfinfo exit non-zero on $PDF"
  pages=$(printf '%s\n' "$info" | awk '/^Pages:/ {print $2}')
  if [ -n "${pages:-}" ] && [ "$pages" -ge 1 ]; then
    echo "G1 pdfinfo: OK (pages=$pages)"
  else
    fail "G1 pdfinfo: page count unreadable or zero"
  fi
else
  fail "G1: pdfinfo MISSING — capability VOID, rerun scripts/probe_manifest.sh"
fi

if command -v qpdf >/dev/null 2>&1; then
  if qpdf --check "$PDF" >/dev/null 2>&1; then
    echo "G1 qpdf --check: OK (exit 0; syntax certified, NOT PDF/A or PDF/UA — those need veraPDF)"
  else
    fail "G1 qpdf --check: structural errors in $PDF"
  fi
else
  echo "G1 qpdf: MISSING — structural gate weakened to pdfinfo only"
fi

# --- G2: rasterize first/last page; blank-page heuristic (PNG < 5KB = suspect) ---
if command -v pdftoppm >/dev/null 2>&1 && [ -n "${pages:-}" ]; then
  tmpd=$(mktemp -d)
  if pdftoppm -png -r 60 -f 1 -l 1 "$PDF" "$tmpd/first" >/dev/null 2>&1; then
    for png in "$tmpd"/first*.png; do
      [ -e "$png" ] || { fail "G2: first page produced no raster"; continue; }
      sz=$(wc -c < "$png")
      if [ "$sz" -lt 5120 ]; then fail "G2: page 1 raster suspiciously small (${sz} B < 5 KB — blank-page heuristic)"; else echo "G2 page 1 raster: OK (${sz} B)"; fi
    done
  else
    fail "G2: pdftoppm failed on page 1"
  fi
  if [ "$pages" -gt 1 ]; then
    if pdftoppm -png -r 60 -f "$pages" -l "$pages" "$PDF" "$tmpd/last" >/dev/null 2>&1; then
      for png in "$tmpd"/last*.png; do
        [ -e "$png" ] || { fail "G2: last page produced no raster"; continue; }
        sz=$(wc -c < "$png")
        if [ "$sz" -lt 5120 ]; then fail "G2: page $pages raster suspiciously small (${sz} B < 5 KB — blank-page heuristic)"; else echo "G2 page $pages raster: OK (${sz} B)"; fi
      done
    else
      fail "G2: pdftoppm failed on page $pages"
    fi
  fi
  rm -rf "$tmpd"
else
  fail "G2: pdftoppm MISSING — capability VOID, rerun scripts/probe_manifest.sh"
fi

# --- G3: text round-trip with sentinels ---
if command -v pdftotext >/dev/null 2>&1; then
  text=$(pdftotext "$PDF" - 2>/dev/null)
  if [ -z "$text" ]; then
    fail "G3: text layer EMPTY — scanned or CID-broken PDF; route to OCR ladder, never ship as-is"
  else
    words=$(printf '%s' "$text" | wc -w)
    echo "G3 extraction: OK ($words words)"
    for s in "$@"; do
      n=$(printf '%s' "$text" | grep -c -F "$s" || true)
      if [ "$n" -eq 0 ]; then
        fail "G3: sentinel NOT FOUND: '$s'"
      else
        echo "G3 sentinel '$s': found ${n}x"
      fi
    done
  fi
else
  fail "G3: pdftotext MISSING — capability VOID, rerun scripts/probe_manifest.sh"
fi

if [ "$FAILED" -ne 0 ]; then
  echo "VERIFY FAIL — do NOT ship this PDF"
  exit 1
fi
echo "VERIFY PASS (G1-G3)"

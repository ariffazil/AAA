#!/usr/bin/env bash
# civic-petition-forge pipeline
# Render HTML → PDF → SHA-256 → embed hash → verify
# Single command from HTML draft to sealed artifact.
#
# Usage:
#   ./forge-pipeline.sh <letter-slug>
# Example:
#   ./forge-pipeline.sh surat-final-v12
#
# Prereqs (verify before running):
#   - python3 with weasyprint installed
#   - sha256sum (coreutils)
#   - pdftotext + pdfinfo (poppler-utils)
#   - grep with PCRE (-P flag)

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <letter-slug>"
  echo "Example: $0 surat-final-v12"
  exit 1
fi

SLUG="$1"
WORKDIR="${WORKDIR:-/root/forge_work/petronas2025}"

HTML="${WORKDIR}/${SLUG}.html"
PDF="${WORKDIR}/${SLUG}.pdf"

if [ ! -f "$HTML" ]; then
  echo "ERROR: $HTML not found"
  exit 1
fi

echo "==> Pipeline starting for ${SLUG}"
echo "==> Source: ${HTML}"

# 1. RENDER HTML → PDF
echo "[1/5] Rendering HTML to PDF via weasyprint..."
python3 - <<EOF
import weasyprint
from pathlib import Path
html = Path("${HTML}").read_text()
weasyprint.HTML(string=html, base_url="${WORKDIR}/").write_pdf("${PDF}")
EOF

if [ ! -f "$PDF" ]; then
  echo "ERROR: PDF render failed"
  exit 1
fi

echo "    PDF: ${PDF} ($(stat -c %s "$PDF") bytes)"

# 2. COMPUTE SHA-256 (Kleene's fixed-point: hash of pre-embed source)
echo "[2/5] Computing SHA-256 of HTML source..."
SHA=$(sha256sum "$HTML" | awk '{print $1}')
echo "    SHA-256: ${SHA}"

# 3. VERIFY PDF INTEGRITY
echo "[3/5] Verifying PDF integrity..."
PAGE_COUNT=$(pdfinfo "$PDF" | grep "^Pages:" | awk '{print $2}')
echo "    Page count: ${PAGE_COUNT}"

if [ "$PAGE_COUNT" -lt 6 ] || [ "$PAGE_COUNT" -gt 14 ]; then
  echo "WARNING: Page count ${PAGE_COUNT} outside target range 6-14"
  echo "    v12 target was 8-12 pages. Adjust if needed."
fi

# 4. TOKEN LEAK CHECK (F2 CLARITY violation auto-fail)
echo "[4/5] Scanning for non-target-language token leaks..."
LEAKS=$(grep -P '[^\x00-\x7F]' "$HTML" | grep -v -E '(é|ñ|—|–|…|“|”|‘|’|á|í|ó|ú|à|è|ì|ò|ù|â|ê|î|ô|û|ä|ë|ï|ö|ü|ç)' || true)

if [ -n "$LEAKS" ]; then
  echo "ERROR: Token leak detected in HTML:"
  echo "$LEAKS"
  echo "    F2 CLARITY auto-fail. Remove before proceeding."
  exit 1
fi

echo "    No token leaks detected."

# 5. KEY FACT VERIFICATION
echo "[5/5] Verifying key facts appear in document..."
for PATTERN in "70.5" "RM32" "RM45.4" "5,000" "9.9" "0.3" "11 Feb 2026" "16 Mar 2026" "30 Mar 2026" "1 Jul 2026" "SEARAH" "Holbein Gardens"; do
  if grep -q "$PATTERN" "$HTML"; then
    echo "    ✓ Found: $PATTERN"
  else
    echo "    ✗ MISSING: $PATTERN"
    echo "WARNING: Some key facts missing. Verify before dispatch."
  fi
done

echo ""
echo "==> Pipeline complete for ${SLUG}"
echo "==> HTML: ${HTML}"
echo "==> PDF: ${PDF}"
echo "==> SHA-256: ${SHA}"
echo ""
echo "==> NEXT STEPS:"
echo "    1. Patch the embedded hash into the HTML (Kleene's fixed-point):"
echo "       sed -i 's|{{SHA256_HASH}}|${SHA}|g' ${HTML}"
echo "       Then re-render: ./forge-pipeline.sh ${SLUG}"
echo "    2. Run apex_judge isolate T3 (expect HOLD + f13_required=TRUE):"
echo "       python3 /root/scripts/apex_judge.py isolate --doer 'Muhammad Arif bin Fazil' --candidate '[1-sentence description]' --action-class public_dispatch_to_parliament --action-tier T3 --critical --pretty"
echo "    3. VAULT999 seal:"
echo "       echo '{session_id, coherence_id=${SLUG^^}_$(date +%Y-%m-%d), sha256:${SHA}}' >> /root/arifOS/VAULT999/outcomes.jsonl"
echo "    4. Hand to F13 for SEAL/HOLD/AMEND/REJECT disposition."
echo "    5. After F13 SEAL: dispatch via tier distribution plan (see tier-distribution-framework.md)."
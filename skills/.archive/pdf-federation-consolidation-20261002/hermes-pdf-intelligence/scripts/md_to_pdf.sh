#!/usr/bin/env bash
# md_to_pdf.sh — routed Markdown -> PDF converter (D6: route by probe, never by assumption)
# Usage: md_to_pdf.sh <input.md> <output.pdf>
# Route order: xelatex -> weasyprint -> chromium headless -> pandoc docx + soffice.
# wkhtmltopdf is NEVER a route: FORBIDDEN (archived Jan 2023, CVE-2022-35583 CVSS 9.8).

set -u

if [ $# -ne 2 ]; then echo "usage: $0 <input.md> <output.pdf>"; exit 2; fi
IN="$1"; OUT="$2"
[ -f "$IN" ] || { echo "FAIL: input not found: $IN"; exit 2; }
command -v pandoc >/dev/null 2>&1 || { echo "FAIL: pandoc MISSING — capability VOID, rerun probe_manifest.sh"; exit 2; }

tmpd=$(mktemp -d)
trap 'rm -rf "$tmpd"' EXIT

have() { command -v "$1" >/dev/null 2>&1; }

if have xelatex; then
  ROUTE="pandoc --pdf-engine=xelatex"
  pandoc "$IN" -o "$OUT" --pdf-engine=xelatex \
    -V geometry:margin=1in -V fontsize=11pt || { echo "FAIL: xelatex render"; exit 1; }
elif have weasyprint; then
  ROUTE="pandoc -> html -> weasyprint"
  pandoc "$IN" -s -o "$tmpd/in.html" || { echo "FAIL: pandoc html"; exit 1; }
  weasyprint "$tmpd/in.html" "$OUT" || { echo "FAIL: weasyprint render"; exit 1; }
elif have chromium || have chromium-browser || have google-chrome; then
  ROUTE="pandoc -> html -> chromium --headless --print-to-pdf"
  BROWSER=$(command -v chromium || command -v chromium-browser || command -v google-chrome)
  pandoc "$IN" -s -o "$tmpd/in.html" || { echo "FAIL: pandoc html"; exit 1; }
  "$BROWSER" --headless --no-sandbox --disable-gpu --disable-dev-shm-usage \
    --no-pdf-header-footer \
    --print-to-pdf="$OUT" "file://$tmpd/in.html" >/dev/null 2>&1 \
    || { echo "FAIL: chromium headless render"; exit 1; }
  [ -s "$OUT" ] || { echo "FAIL: chromium produced empty PDF"; exit 1; }
elif have soffice; then
  ROUTE="pandoc -> docx -> soffice --convert-to pdf"
  pandoc "$IN" -o "$tmpd/in.docx" || { echo "FAIL: pandoc docx"; exit 1; }
  soffice --headless --convert-to pdf --outdir "$tmpd" "$tmpd/in.docx" >/dev/null 2>&1 \
    || { echo "FAIL: soffice convert"; exit 1; }
  mv "$tmpd/in.pdf" "$OUT"
else
  echo "FAIL: no viable PDF engine probed (xelatex/weasyprint/chromium/soffice all MISSING) — capability VOID"
  exit 2
fi

echo "ROUTE: $ROUTE"
echo "WROTE: $OUT"
echo "NEXT:  verify with scripts/pdf_verify.sh \"$OUT\" <sentinels...> — tool-OK != page-correct"

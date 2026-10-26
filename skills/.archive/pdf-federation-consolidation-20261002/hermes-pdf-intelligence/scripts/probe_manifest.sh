#!/usr/bin/env bash
# probe_manifest.sh — HERMES PDF capability probe (I6 / D6)
# Capability is probe OUTPUT, never assumption. Presence is a fact; fitness is a verdict.
# DITEMPA BUKAN DIBERI — forged, not given. The forge is the probe.

set -u

echo "=== HERMES PDF PROBE — $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "host: $(uname -srm)"
echo "--- binaries ---"

BINARIES="pandoc weasyprint pdftotext pdftoppm pdfinfo qpdf soffice chromium google-chrome wkhtmltopdf xelatex tesseract mutool gs"

for b in $BINARIES; do
  path=$(command -v "$b" 2>/dev/null || true)
  if [ -n "$path" ]; then
    ver=$("$b" --version 2>&1 | head -n1 | tr -d '\r')
    if [ -z "$ver" ] || ! printf '%s' "$ver" | grep -q '[0-9]'; then
      ver=$("$b" -v 2>&1 | head -n1 | tr -d '\r')
    fi
    [ -z "$ver" ] && ver="(version unreadable)"
    if [ "$b" = "wkhtmltopdf" ]; then
      echo "PRESENT-FORBIDDEN  $b  $ver  [archived Jan 2023; CVE-2022-35583 CVSS 9.8 SSRF unpatched — do NOT use]"
    else
      echo "PRESENT  $b  $ver"
    fi
  else
    echo "MISSING  $b"
  fi
done

echo "--- python libraries ---"
python3 - <<'PY'
import importlib.metadata as m
for p in ["reportlab", "pymupdf", "pypdf", "pdfplumber", "pdfminer.six", "matplotlib", "weasyprint"]:
    try:
        print(f"PRESENT  py:{p}  {m.version(p)}")
    except Exception:
        print(f"MISSING  py:{p}")
PY

echo "PROBE COMPLETE — treat MISSING as VOID, treat wkhtmltopdf as FORBIDDEN"

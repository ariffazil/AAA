#!/usr/bin/env bash
# Reusable ad-hoc verification scaffold for HTML+PDF artifacts.
# Copy this script to /tmp/hermes-verify-<your-topic>.sh, edit the config
# block, run, and clean up. Do NOT keep it after the run — see
# verify-before-report § "Ad-hoc verification script convention".
#
# Usage: bash verify-html-pdf-artifact.sh
# Exit:  number of FAILs (0 = green)

set -u
WS="${WORKSPACE:-/root/forge_work/petronas2025}"
HTML="${HTML_PATH:-$WS/artifact.html}"
PDF="${PDF_PATH:-$WS/artifact.pdf}"
EXPECTED_HASH="${EXPECTED_HASH:-}"   # set to the canonical SHA-256 you printed inside the artifact
PASS=0; FAIL=0
note() { printf "  %s\n" "$*"; }
ok()   { printf "[ OK ] %s\n" "$*"; PASS=$((PASS+1)); }
bad()  { printf "[FAIL] %s\n" "$*"; FAIL=$((FAIL+1)); }

# --- CONFIG: edit this block per artifact -------------------------------
REQUIRED_SCARS=()                       # e.g. ("SCAR_AKUSAJACUKUP" "SCAR_BEKANTAN")
PARADOX_HEADERS=()                      # e.g. ("Parados Pertama" "Parados Kedua")
ANCHORS=()                              # substring-tolerant (single token per entry)
SECTION_HEADER=""                        # e.g. "SEKSYEN A ·"
EXPECTED_PAGES_MIN=8
EXPECTED_PAGES_MAX=16
ANTI_AI_PHRASES=("I would like to" "it's important to note" "delve into"
                 "in conclusion" "leverage" "in summary")
# -----------------------------------------------------------------------

echo "==== AD-HOC VERIFICATION: $(basename "$HTML") ===="
echo

# 1. Existence
echo "1. Existence"
[ -f "$HTML" ] && ok "HTML exists" || bad "HTML missing"
[ -f "$PDF"  ] && ok "PDF exists"  || bad "PDF missing"
[ -s "$HTML" ] && ok "HTML non-empty ($(wc -c < "$HTML") bytes)" || bad "HTML empty"
[ -s "$PDF"  ] && ok "PDF non-empty ($(wc -c < "$PDF") bytes)" || bad "PDF empty"
echo

# 2. SHA-256 fidelity (skip silently if EXPECTED_HASH unset)
echo "2. SHA-256 fidelity"
if [ -n "$EXPECTED_HASH" ]; then
  note "HTML file SHA: $(sha256sum "$HTML" | awk '{print $1}')"
  note "PDF  file SHA: $(sha256sum "$PDF"  | awk '{print $1}')"
  grep -q "$EXPECTED_HASH" "$HTML" && ok "Hash printed in HTML" || bad "Hash MISSING from HTML"
  if command -v pdftotext >/dev/null; then
    pdftotext "$PDF" - | grep -q "$EXPECTED_HASH" \
      && ok "Hash printed in PDF text layer" || bad "Hash MISSING from PDF"
  else
    python3 -c "
from pypdf import PdfReader
t = '\n'.join((p.extract_text() or '') for p in PdfReader('$PDF').pages)
print('[ OK ] Hash printed in PDF text layer' if '$EXPECTED_HASH' in t else '[FAIL] Hash MISSING from PDF')
" && PASS=$((PASS+1))
  fi
else
  note "EXPECTED_HASH not set — skipping"
fi
echo

# 3. Scar coverage (only if REQUIRED_SCARS set)
if [ "${#REQUIRED_SCARS[@]}" -gt 0 ]; then
  echo "3. Scar coverage"
  for s in "${REQUIRED_SCARS[@]}"; do
    grep -q "scar:$s" "$HTML" && ok "Scar: $s" || bad "MISSING scar: $s"
  done
  echo
fi

# 4. Structural anchors (substring-tolerant — NO `<br>`-crossing literals)
if [ "${#ANCHORS[@]}" -gt 0 ]; then
  echo "4. Structural anchors"
  for a in "${ANCHORS[@]}"; do
    grep -qF "$a" "$HTML" && ok "Anchor: $a" || bad "MISSING anchor: $a"
  done
  echo
fi

# 5. Paradox/section block count
if [ "${#PARADOX_HEADERS[@]}" -gt 0 ]; then
  echo "5. Block count"
  COUNT=0
  for h in "${PARADOX_HEADERS[@]}"; do
    grep -qF "$h" "$HTML" && COUNT=$((COUNT+1))
  done
  [ "$COUNT" -eq "${#PARADOX_HEADERS[@]}" ] \
    && ok "All ${#PARADOX_HEADERS[@]} blocks present" \
    || bad "Only $COUNT/${#PARADOX_HEADERS[@]} blocks present"
  echo
fi

# 6. Anti-AI-ism scan
echo "6. Anti-AI-ism scan"
for p in "${ANTI_AI_PHRASES[@]}"; do
  grep -qiF "$p" "$HTML" && bad "AI-ism: '$p'" || ok "Clean: '$p'"
done
echo

# 7. PDF page count
echo "7. PDF page count"
if command -v pdfinfo >/dev/null; then
  P=$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')
else
  P=$(python3 -c "from pypdf import PdfReader; print(len(PdfReader('$PDF').pages))")
fi
note "Pages: $P"
if [ "$P" -ge "$EXPECTED_PAGES_MIN" ] && [ "$P" -le "$EXPECTED_PAGES_MAX" ]; then
  ok "Page count $P in [$EXPECTED_PAGES_MIN,$EXPECTED_PAGES_MAX] window"
else
  bad "Page count $P outside [$EXPECTED_PAGES_MIN,$EXPECTED_PAGES_MAX]"
fi
echo

echo "==== SUMMARY ===="
echo "PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "VERDICT: ad-hoc verification GREEN." \
                  || echo "VERDICT: AD-HOC ISSUES — review fails above."
echo
echo "==== CLEANUP ===="
# Self-cleanup if this script lives under /tmp/hermes-verify-*
case "$0" in
  /tmp/hermes-verify-*) rm -v "$0" ;;
esac
exit $FAIL
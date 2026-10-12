#!/usr/bin/env bash
# AAA BIJAKSANA ENV INSTALLER — idempotent. Safe to re-run for every upgrade.
# Applies /root/bin/bashrc-bijaksana.block into /root/.bashrc with backup + syntax gate + auto-revert.
set -euo pipefail

RC=/root/.bashrc
BLOCK=/root/bin/bashrc-bijaksana.block
TS=$(date +%Y%m%dT%H%M%S)
BK="${RC}.bak.${TS}"
RECEIPT_DIR=/root/AAA/receipts

[ -r "$BLOCK" ] || { echo "FATAL: block file missing: $BLOCK"; exit 1; }
[ -w "$RC" ]    || { echo "FATAL: cannot write $RC"; exit 1; }

sha_before=$(sha256sum "$RC" | cut -c1-12)
cp -a "$RC" "$BK"

# Strip any previous bijaksana block (idempotent upgrade), then append the current one.
sed -i '/>>> AAA-BIJAKSANA-ENV/,/<<< AAA-BIJAKSANA-ENV/d' "$RC"
cat "$BLOCK" >> "$RC"

# Gate: syntax must pass or we auto-revert.
if ! bash -n "$RC"; then
    echo "SYNTAX FAIL — reverting to $BK"
    cp -a "$BK" "$RC"
    exit 1
fi

sha_after=$(sha256sum "$RC" | cut -c1-12)
mkdir -p "$RECEIPT_DIR"
printf '{"ts":"%s","action":"bijaksana-env-install","backup":"%s","sha_before":"%s","sha_after":"%s","block":"v1"}\n' \
    "$(date -Iseconds)" "$BK" "$sha_before" "$sha_after" >> "$RECEIPT_DIR/bijaksana-env.jsonl"

echo "INSTALLED · backup: $BK · sha ${sha_before} → ${sha_after} · receipt: ${RECEIPT_DIR}/bijaksana-env.jsonl"

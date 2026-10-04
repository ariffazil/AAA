#!/bin/bash
# check-unattested-outputs.sh — anti-forget watchdog: find recent PDFs without a
# ledger attestation entry and auto-attest them. Run every 2h via cron (no_agent=true).
# Deployed copy: /root/.hermes/scripts/check-unattested-outputs.sh

ATTEST_SCRIPT="/root/HERMES/scripts/output-attest.py"
LEDGER="/root/HERMES/attestation-ledger.jsonl"
LOOKBACK_HOURS=2
SEARCH_DIRS="/root/HERMES /tmp /root/forge_work /root/arif-fazil.com"

unattested=0
attested=0
total=0

eval "find $SEARCH_DIRS -name '*.pdf' -mmin -$((LOOKBACK_HOURS * 60)) -type f 2>/dev/null" | while read -r pdf; do
    total=$((total + 1))
    abs_path=$(realpath "$pdf" 2>/dev/null || echo "$pdf")
    if [ -f "$LEDGER" ] && grep -q "\"$abs_path\"" "$LEDGER" 2>/dev/null; then
        attested=$((attested + 1))
    else
        unattested=$((unattested + 1))
        echo "UNATTESTED: $abs_path"
        python3 "$ATTEST_SCRIPT" "$abs_path" --label "cron-auto-attest" --agent "hermes-cron" 2>/dev/null
    fi
done

if [ "$total" -eq 0 ]; then
    echo "No PDFs found in last ${LOOKBACK_HOURS}h. Nothing to attest."
else
    echo "Checked: $total PDFs | Attested: $attested | Auto-attested: $unattested"
fi

#!/bin/bash
# sentinel-watch.sh — arifOS-sentinel cron job
# Runs every 6 hours to check repo invariants
# DITEMPA BUKAN DIBERI — watchfulness is not optional

set -euo pipefail

REPOS=(
  "/root/arifOS:ariffazil/arifOS:main"
  "/root/WEALTH:ariffazil/WEALTH:master"
  "/root/geox:ariffazil/GEOX:main"
  "/root/A-FORGE:ariffazil/A-FORGE:main"
  "/root/arif-sites:ariffazil/arif-sites:main"
  "/root/.openclaw/workspace:ariffazil/AAA:master"
)

REPORT_FILE="/root/.openclaw/workspace/memory/sentinel-watch.log"
ALERT_ISSUES=()

echo "=== arifOS-sentinel check: $(date -u) ===" >> "$REPORT_FILE"

for entry in "${REPOS[@]}"; do
  IFS=':' read -r local_path repo <<< "$entry"
  local_path="${local_path#/}"  # strip leading /
  
  if [[ ! -d "/$local_path" ]]; then
    echo "SKIP $repo — not found at /$local_path" >> "$REPORT_FILE"
    continue
  fi
  
  # Run pre-push check
  if bash /root/.openclaw/workspace/scripts/pre-push-check.sh "/$local_path" origin main > /tmp/sentinel_check_$$.out 2>&1; then
    echo "PASS $repo" >> "$REPORT_FILE"
  else
    echo "VETO $repo" >> "$REPORT_FILE"
    ALERT_ISSUES+=("$repo")
    cat /tmp/sentinel_check_$$.out >> "$REPORT_FILE"
  fi
done

# If any veto, open GitHub issues
if [[ ${#ALERT_ISSUES[@]} -gt 0 ]]; then
  for repo in "${ALERT_ISSUES[@]}"; do
    gh issue create \
      --repo "$repo" \
      --title "[VOID] Sentinel invariant check failed — $(date -u +%Y-%m-%d)" \
      --body "arifOS-sentinel detected invariant violation. See pre-push-check output for details.

**Rule violated:** Pre-push invariant check
**Checked:** $(date -u)
**Required action:** Review and resolve before any further pushes."

    echo "VOID issue opened: $repo" >> "$REPORT_FILE"
  done
fi

echo "=== Sentinel check complete: $(date -u) ===" >> "$REPORT_FILE"
echo "Vetoed repos: ${ALERT_ISSUES[*]:-none}" >> "$REPORT_FILE"

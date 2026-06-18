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
  "/root/arif-sites-work:ariffazil/arif-sites:main"
  "/root/.openclaw/workspace:ariffazil/AAA"
)

REPORT_FILE="/root/.openclaw/workspace/memory/sentinel-watch.log"
ALERT_ISSUES=()

# Clear report file
> "$REPORT_FILE"

echo "=== arifOS-sentinel check: $(date -u) ===" >> "$REPORT_FILE"

for entry in "${REPOS[@]}"; do
  IFS=':' read -r local_path repo <<< "$entry"
  
  # Keep the full path
  full_local_path="/$local_path"
  
  if [[ ! -d "$full_local_path" ]]; then
    echo "SKIP $repo — not found at $full_local_path" >> "$REPORT_FILE"
    continue
  fi
  
  # Check if it's a git repository
  if [[ -d "$full_local_path/.git" ]]; then
    # Change to repository directory and run pre-push-check.sh
    if cd "$full_local_path" && bash /root/.openclaw/workspace/scripts/pre-push-check.sh > /tmp/sentinel_check_$$.out 2>&1; then
      echo "PASS $repo" >> "$REPORT_FILE"
    else
      echo "VETO $repo" >> "$REPORT_FILE"
      ALERT_ISSUES+=("$repo")
      cat /tmp/sentinel_check_$$.out >> "$REPORT_FILE"
    fi
  else
    echo "SKIP $repo — not a git repository" >> "$REPORT_FILE"
  fi
done

# If any veto, open GitHub issues
if [[ ${#ALERT_ISSUES[@]} -gt 0 ]]; then
  for repo in "${ALERT_ISSUES[@]}"; do
    # Skip GitHub issue creation for now due to gh configuration issues
    echo "VOID issue would be opened: $repo" >> "$REPORT_FILE"
  done
fi

echo "=== Sentinel check complete: $(date -u) ===" >> "$REPORT_FILE"
echo "Vetoed repos: ${ALERT_ISSUES[*]:-none}" >> "$REPORT_FILE"
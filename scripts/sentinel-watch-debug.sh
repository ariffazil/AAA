#!/bin/bash
# Debug version of sentinel-watch.sh

set -euo pipefail

echo "=== DEBUG START ==="

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

echo "=== arifOS-sentinel check: $(date -u) ===" >> "$REPORT_FILE"

for entry in "${REPOS[@]}"; do
  echo "Processing entry: $entry" >> "$REPORT_FILE"
  
  IFS=':' read -r local_path repo <<< "$entry"
  echo "  Split: local_path=$local_path, repo=$repo" >> "$REPORT_FILE"
  
  # Keep the full path
  full_local_path="/$local_path"
  echo "  Full path: $full_local_path" >> "$REPORT_FILE"
  
  if [[ ! -d "$full_local_path" ]]; then
    echo "SKIP $repo — not found at $full_local_path" >> "$REPORT_FILE"
    echo "Directory does not exist" >> "$REPORT_FILE"
    continue
  fi
  
  echo "Directory exists" >> "$REPORT_FILE"
  
  # Check if it's a git repository
  if [[ -d "$full_local_path/.git" ]]; then
    echo "Is git repository" >> "$REPORT_FILE"
    
    # Change to repository directory and run pre-push-check.sh
    echo "Changing to directory: $full_local_path" >> "$REPORT_FILE"
    cd "$full_local_path" || { echo "Cannot cd to $full_local_path" >> "$REPORT_FILE"; continue; }
    
    echo "Running pre-push-check.sh" >> "$REPORT_FILE"
    if bash /root/.openclaw/workspace/scripts/pre-push-check.sh origin > /tmp/sentinel_check_$$.out 2>&1; then
      echo "PASS $repo" >> "$REPORT_FILE"
      echo "SUCCESS: pre-push-check.sh exited with 0" >> "$REPORT_FILE"
    else
      echo "FAILURE: pre-push-check.sh exited with non-zero" >> "$REPORT_FILE"
      echo "VETO $repo" >> "$REPORT_FILE"
      ALERT_ISSUES+=("$repo")
      cat /tmp/sentinel_check_$$.out >> "$REPORT_FILE"
    fi
  else
    echo "Not a git repository" >> "$REPORT_FILE"
  fi
done

echo "=== Sentinel check complete: $(date -u) ===" >> "$REPORT_FILE"
echo "Vetoed repos: ${ALERT_ISSUES[*]:-none}" >> "$REPORT_FILE"

echo "=== DEBUG END ==="
#!/usr/bin/env bash
# backup-to-github.sh — arifOS_bot nightly workspace backup
# Schedule: 00:00 MYT (16:00 UTC) via OpenClaw cron
# Target: https://github.com/ariffazil/openclaw-workspace

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
LOG_FILE="${WORKSPACE}/logs/backup.log"
AUDIT_FILE="${WORKSPACE}/logs/audit.jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
DATE_MYT=$(TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d_%H%M)

log() { echo "[${TIMESTAMP}] $*" | tee -a "${LOG_FILE}"; }

mkdir -p "${WORKSPACE}/logs"

log "=== arifOS_bot workspace backup starting ==="

# Check GITHUB_TOKEN available
if [ -z "${GITHUB_TOKEN:-}" ]; then
  log "ERROR: GITHUB_TOKEN not set — cannot push to GitHub"
  echo "{\"ts\":\"${TIMESTAMP}\",\"event\":\"backup_failed\",\"reason\":\"no_gh_token\",\"agent\":\"arifOS_bot\"}" >> "${AUDIT_FILE}"
  exit 1
fi

cd "${WORKSPACE}"

# Configure git auth via token
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/ariffazil/openclaw-workspace.git"

# Stage all changes (exclude .git internals, no secrets)
git add \
  SPEC.md AGENTS.md TOOLS.md IDENTITY.md SOUL.md USER.md DR_RUNBOOK.md \
  skills/ memory/ scripts/ \
  logs/audit.jsonl logs/model-usage.jsonl 2>/dev/null || true

# Only commit if there are staged changes
if git diff --cached --quiet; then
  log "No changes to commit — workspace up to date"
  echo "{\"ts\":\"${TIMESTAMP}\",\"event\":\"backup_skipped\",\"reason\":\"no_changes\",\"agent\":\"arifOS_bot\"}" >> "${AUDIT_FILE}"
else
  git commit -m "backup: ${DATE_MYT} [arifOS_bot auto]

Co-authored-by: arifOS_bot <arifos_bot@arif-fazil.com>"

  git push origin main
  log "Backup pushed to GitHub successfully"
  echo "{\"ts\":\"${TIMESTAMP}\",\"event\":\"backup_success\",\"repo\":\"openclaw-workspace\",\"agent\":\"arifOS_bot\"}" >> "${AUDIT_FILE}"
fi

# Reset remote URL to HTTPS (non-token) after push for safety
git remote set-url origin "https://github.com/ariffazil/openclaw-workspace.git"

log "=== Backup complete ==="

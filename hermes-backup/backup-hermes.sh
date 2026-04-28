#!/bin/bash
# hermes-daily-backup.sh
# DITEMPA BUKAN DIBERI — Forged, Not Given
# Backup Hermes Agent core files to AAA hermes-backup/daily/
# Run at 21:00 UTC = 05:00 MYT (Asia/Kuala_Lumpur)

set -euo pipefail

BACKUP_ROOT="/root/AAA/hermes-backup/daily"
AAA_HERMES="/root/AAA/hermes"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"
KEEP_DAYS=7

# Source files to backup (Hermes core identity + config)
SOURCES=(
    "/root/.hermes/SOUL.md"
    "/root/.hermes/memories/MEMORY.md"
    "/root/.hermes/memories/USER.md"
    "/root/.hermes/config.yaml"
    "/root/.hermes/workspace/"
)

echo "=== Hermes Daily Backup $(date -u '+%Y-%m-%d %H:%M UTC') ==="

# Create backup dir
mkdir -p "${BACKUP_DIR}"

# Copy files with directory structure preserved
for src in "${SOURCES[@]}"; do
    if [ -f "${src}" ]; then
        dest="${BACKUP_DIR}${src}"
        mkdir -p "$(dirname "${dest}")"
        cp -rp "${src}" "${dest}"
        echo "  BACKED: ${src}"
    elif [ -d "${src}" ]; then
        dest="${BACKUP_DIR}${src}"
        mkdir -p "$(dirname "${dest}")"
        cp -rp "${src}" "${dest}"
        echo "  BACKED: ${src}/"
    else
        echo "  MISSING: ${src} (skipped)"
    fi
done

# Sync live mirror to AAA/hermes/ for real-time AAA visibility
rsync -av --delete \
    /root/.hermes/SOUL.md \
    /root/.hermes/memories/MEMORY.md \
    /root/.hermes/memories/USER.md \
    /root/.hermes/config.yaml \
    /root/.hermes/workspace/ \
    "${AAA_HERMES}/" 2>/dev/null || (
        mkdir -p "${AAA_HERMES}"
        for f in SOUL.md IDENTITY.md USER.md AGENTS.md BOOTSTRAP.md HEARTBEAT.md TOOLS.md arifos.init MEMORY.md ROOT_CANON.yaml; do
            [ -f "/root/.hermes/workspace/${f}" ] && cp -p "/root/.hermes/workspace/${f}" "${AAA_HERMES}/${f}"
        done
    )
echo "  SYNCED: AAA/hermes/ live mirror"

# Cleanup old backups (keep last 7 days)
find "${BACKUP_ROOT}" -maxdepth 1 -type d -name "????-??-??_??????" -mtime +${KEEP_DAYS} -exec rm -rf {} \; 2>/dev/null || true
OLD_COUNT=$(find "${BACKUP_ROOT}" -maxdepth 1 -type d -name "????-??-??_??????" 2>/dev/null | wc -l)
echo "  CLEANUP: ${OLD_COUNT} backups retained (max ${KEEP_DAYS} days)"
echo "  DONE: ${BACKUP_DIR}"
echo "=== Backup complete ==="

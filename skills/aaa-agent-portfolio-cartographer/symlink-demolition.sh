#!/bin/bash
#============================================================
# symlink-demolition.sh — Fix /root/.openclaw exec block
# Run as: sudo bash symlink-demolition.sh
# Expected: root shell or sudo privs
#============================================================

set -euo pipefail
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_BASE="/root/.openclaw.backup.$TIMESTAMP"
WORKSPACE_SRC=""
DRY_RUN=false

#============================================================
# PARSE ARGS
#============================================================
for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --source=*) WORKSPACE_SRC="${arg#*=}" ;;
  esac
done

#============================================================
# 888_HOLD — ASK BEFORE EXECUTING
# These are IRREVERSIBLE. Arif reviews first.
#============================================================
echo "============================================================"
echo "888_HOLD — IRREVERSIBLE ACTIONS (F1 Amanah)"
echo "============================================================"
echo "The following actions are PERMANENT and CANNOT be undone"
echo "without restoring from the backup created in Step 3:"
echo ""
echo "  Step 3: DELETE /root/.openclaw symlink"
echo "  Step 5: COPY workspace contents (data move)"
echo "  Step 6: CHMOD /root/.openclaw recursively"
echo ""
read -p "Do you want to continue? (type 'YES_I_AM_ARIF' to confirm): " confirm
if [ "$confirm" != "YES_I_AM_ARIF" ]; then
  echo "Aborted. No changes made."
  exit 0
fi

#============================================================
# STEP 1 — DETECT SYMLINK
#============================================================
echo ""
echo "[Step 1] Detecting /root/.openclaw..."
if [ -L "/root/.openclaw" ]; then
  TARGET=$(readlink -f /root/.openclaw)
  echo "✅ /root/.openclaw IS a symlink"
  echo "   Target: $TARGET"
  if [ -z "${WORKSPACE_SRC:-}" ]; then
    WORKSPACE_SRC="$TARGET"
    echo "   Auto-detected workspace source: $WORKSPACE_SRC"
  fi
elif [ -d "/root/.openclaw" ]; then
  echo "⚠️  /root/.openclaw is already a real directory. Nothing to do."
  echo "   Run 'ls -la /root/.openclaw' to verify."
  exit 0
else
  echo "❌ /root/.openclaw does not exist and is not a symlink. Aborting."
  exit 1
fi

#============================================================
# STEP 2 — BACKUP TARGET
#============================================================
echo ""
echo "[Step 2] Creating timestamped backup..."
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would copy $WORKSPACE_SRC to $BACKUP_BASE"
else
  cp -a "$WORKSPACE_SRC" "$BACKUP_BASE"
  echo "✅ Backup created: $BACKUP_BASE"
  echo "   Size: $(du -sh "$BACKUP_BASE" 2>/dev/null | cut -f1)"
fi

#============================================================
# STEP 3 — DELETE SYMLINK (IRREVERSIBLE)
#============================================================
echo ""
echo "[Step 3] Deleting symlink /root/.openclaw..."
echo "⚠️  IRREVERSIBLE — Symlink deletion. Backup at: $BACKUP_BASE"
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would delete symlink /root/.openclaw"
else
  rm /root/.openclaw
  echo "✅ Symlink deleted"
fi

#============================================================
# STEP 4 — CREATE REAL DIRECTORY
#============================================================
echo ""
echo "[Step 4] Creating real directory /root/.openclaw/..."
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would run: mkdir -p /root/.openclaw"
else
  mkdir -p /root/.openclaw
  echo "✅ Real directory created"
fi

#============================================================
# STEP 5 — COPY CONTENTS (IRREVERSIBLE)
#============================================================
echo ""
echo "[Step 5] Copying contents from backup to real directory..."
echo "⚠️  IRREVERSIBLE — File move operation."
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would copy $WORKSPACE_SRC/* to /root/.openclaw/"
else
  cp -a "$WORKSPACE_SRC/"* /root/.openclaw/
  echo "✅ Contents copied"
fi

#============================================================
# STEP 6 — FIX PERMISSIONS (IRREVERSIBLE)
#============================================================
echo ""
echo "[Step 6] Fixing permissions..."
echo "⚠️  IRREVERSIBLE — Permission changes."
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would run: chown -R root:root /root/.openclaw"
  echo "[DRY-RUN] Would run: chmod -R 755 /root/.openclaw"
  echo "[DRY-RUN] Would run: chmod 600 /root/.openclaw/workspace/openclaw.json"
else
  chown -R root:root /root/.openclaw
  chmod -R 755 /root/.openclaw
  chmod 600 /root/.openclaw/workspace/openclaw.json 2>/dev/null || true
  echo "✅ Permissions fixed"
fi

#============================================================
# STEP 7 — VERIFY
#============================================================
echo ""
echo "[Step 7] Verification..."
if [ "$DRY_RUN" = true ]; then
  echo "[DRY-RUN] Would verify:"
  echo "  - ls -la /root/.openclaw (should show drwx------)"
  echo "  - cat /root/.openclaw/workspace/SOUL.md | head -3"
else
  echo "--- ls -la /root/.openclaw ---"
  ls -la /root/.openclaw | head -5
  echo ""
  echo "--- Constitutional file check ---"
  cat /root/.openclaw/workspace/SOUL.md 2>/dev/null | head -3 || echo "SOUL.md NOT FOUND"
  echo ""
  echo "--- Backup location ---"
  echo "$BACKUP_BASE"
  echo ""
  echo "✅ Migration complete."
  echo ""
  echo "Next: Test exec by running: openclaw status"
fi
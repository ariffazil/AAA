#!/bin/bash
# fed-sync.sh — FED Tier 1 Stateless Mirror (v1.0)
# ═══════════════════════════════════════════════════════════════
# FORGE (authoritative) → FLOW (follower)
# Files: fed_router.py + federation-models.json
# Mode: dry-run by default. Pass --apply to sync.
# DITEMPA BUKAN DIBERI — verify before trust.

set -euo pipefail

# ── Config ────────────────────────────────────────────────────
SOURCE_HOST="af-forge"
SOURCE_SSH="ssh $SOURCE_HOST"
TARGET_HOST="flow"
TARGET_SSH="ssh -o StrictHostKeyChecking=accept-new -i /root/.ssh/af-forge-inbound root@72.61.126.65"

FED_ROUTER="scripts/fed_router.py"
FED_MODELS=".config/federation-models.json"
AAA_DIR="/root/AAA"

declare -A FILES=(
  ["$FED_ROUTER"]="$AAA_DIR/$FED_ROUTER"
  ["$FED_MODELS"]="/root/$FED_MODELS"
)

# ── Flags ─────────────────────────────────────────────────────
DRY_RUN=true
RESTART_SERVICE=true
VERBOSE=false

for arg in "$@"; do
  case "$arg" in
    --apply) DRY_RUN=false ;;
    --no-restart) RESTART_SERVICE=false ;;
    --verbose|-v) VERBOSE=true ;;
    --help|-h) cat <<EOF
Usage: $0 [--apply] [--no-restart] [--verbose]

  --apply        Actually sync files (default: dry-run only)
  --no-restart   Don't restart fed-router on FLOW after sync
  --verbose       Show md5 hashes and details

Syncs fed_router.py + federation-models.json from FORGE → FLOW.
MD5-verified. Restarts fed-router on FLOW on drift detect.
EOF
      exit 0 ;;
  esac
done

# ── Logging ───────────────────────────────────────────────────
log() { echo "[$(date +%H:%M:%S)] $*"; }
fail() { echo "❌ $*"; exit 1; }
ok()   { echo "✅ $*"; }

# ── Health check ──────────────────────────────────────────────
log "Probing health..."
SOURCE_HEALTH=$($SOURCE_SSH "curl -s http://127.0.0.1:7074/health" 2>/dev/null || echo "FAIL")
TARGET_HEALTH=$($TARGET_SSH "curl -s http://127.0.0.1:7075/health" 2>/dev/null || echo "FAIL")

if echo "$SOURCE_HEALTH" | grep -q '"healthy"'; then
  ok "FORGE :7074 healthy"
else
  fail "FORGE :7074 NOT healthy: $SOURCE_HEALTH"
fi

if echo "$TARGET_HEALTH" | grep -q '"healthy"'; then
  ok "FLOW :7075 healthy"
else
  log "⚠️  FLOW :7075 health check: $TARGET_HEALTH (may be on :7074)"
fi

# ── Sync files ────────────────────────────────────────────────
DRIFT_COUNT=0
SYNCED_COUNT=0

for file_key in "${!FILES[@]}"; do
  src_path="${FILES[$file_key]}"
  filename=$(basename "$src_path")

  log "Checking $filename..."

  # Get source MD5
  SRC_MD5=$($SOURCE_SSH "md5sum $src_path" 2>/dev/null | cut -d' ' -f1)
  if [ -z "$SRC_MD5" ]; then
    fail "Cannot read $src_path on FORGE"
  fi

  # Get target MD5
  TGT_MD5=$($TARGET_SSH "md5sum $src_path" 2>/dev/null | cut -d' ' -f1 || echo "MISSING")

  if [ "$SRC_MD5" = "$TGT_MD5" ]; then
    $VERBOSE && log "  $filename: $SRC_MD5 (matched)"
    continue
  fi

  DRIFT_COUNT=$((DRIFT_COUNT + 1))
  log "  DRIFT: $filename"
  $VERBOSE && log "    FORGE: $SRC_MD5"
  $VERBOSE && log "    FLOW:  $TGT_MD5"

  if $DRY_RUN; then
    log "    [DRY-RUN] Would sync $filename"
    continue
  fi

  # Sync
  scp -o StrictHostKeyChecking=accept-new -i /root/.ssh/af-forge-inbound \
    "$SOURCE_HOST:$src_path" "$TARGET_HOST:$src_path" 2>/dev/null

  # Verify post-sync
  POST_MD5=$($TARGET_SSH "md5sum $src_path" 2>/dev/null | cut -d' ' -f1)
  if [ "$SRC_MD5" = "$POST_MD5" ]; then
    ok "  $filename synced ($SRC_MD5)"
    SYNCED_COUNT=$((SYNCED_COUNT + 1))
  else
    fail "  $filename sync FAILED: expected $SRC_MD5, got $POST_MD5"
  fi
done

# ── Summary ───────────────────────────────────────────────────
echo ""
if $DRY_RUN; then
  [ $DRIFT_COUNT -eq 0 ] && log "DRY-RUN: No drift detected." || log "DRY-RUN: $DRIFT_COUNT file(s) would be synced. Run with --apply to sync."
else
  [ $SYNCED_COUNT -eq 0 ] && log "No files needed syncing." || ok "$SYNCED_COUNT file(s) synced."
fi

# ── Restart FLOW fed-router ───────────────────────────────────
if [ $DRIFT_COUNT -gt 0 ] && ! $DRY_RUN && $RESTART_SERVICE; then
  log "Restarting fed-router on FLOW..."
  $TARGET_SSH "systemctl restart fed-router && sleep 2"
  NEW_HEALTH=$($TARGET_SSH "curl -s http://127.0.0.1:7075/health" 2>/dev/null || echo "FAIL")
  if echo "$NEW_HEALTH" | grep -q '"healthy"'; then
    ok "FLOW :7075 restarted and healthy"
  else
    log "⚠️  FLOW restart may have failed: $NEW_HEALTH"
  fi
fi

log "Done."
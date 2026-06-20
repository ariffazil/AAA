#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# AAA Bare-Metal VPS Deploy — Frontend (Vite → Caddy) + A2A (systemd)
#
# Purpose: Build the React frontend and sync it to the Caddy-served dir,
#          then restart the A2A gateway if requested.
#
# Reality (2026-06-17):
#   - No Docker. Organs run bare-metal via systemd.
#   - Frontend build: /root/AAA/dist/  →  /var/www/html/aaa/  (Caddy root)
#   - A2A gateway: /usr/bin/node /root/AAA/a2a-server/server.js (port 3001)
#   - A2A_TOKEN / A2A_API_KEY live in /root/.secrets/vault.flat.env
#   - The a2a-server is RESTARTED here ONLY if --restart-a2a is passed.
#
# Usage:
#   ./scripts/deploy-vps.sh                  # build + sync frontend only
#   ./scripts/deploy-vps.sh --restart-a2a    # also restart a2a-server
#   ./scripts/deploy-vps.sh --check          # only verify current state
#   ./scripts/deploy-vps.sh --rollback       # restore from latest backup
#
# DITEMPA BUKAN DIBERI — Forged, Not Given
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

REPO_DIR="/root/AAA"
DIST_DIR="$REPO_DIR/dist"
SERVE_DIR="/var/www/html/aaa"
A2A_SERVICE="aaa-a2a.service"
A2A_HEALTH_URL="http://127.0.0.1:3001/health"
SITE_URL="https://aaa.arif-fazil.com"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── 0. Mode flags ────────────────────────────────────────────────────────────
RESTART_A2A=0
CHECK_ONLY=0
ROLLBACK=0
for arg in "$@"; do
    case "$arg" in
        --restart-a2a) RESTART_A2A=1 ;;
        --check)       CHECK_ONLY=1 ;;
        --rollback)    ROLLBACK=1 ;;
        *) log_warn "Unknown flag: $arg" ;;
    esac
done

# ── 1. Find latest backup if --rollback ───────────────────────────────────────
if [[ "$ROLLBACK" == "1" ]]; then
    LATEST_BAK=$(ls -1dt /var/www/html/aaa.bak.* 2>/dev/null | head -1 || true)
    if [[ -z "$LATEST_BAK" ]]; then
        log_error "No backup dir found matching /var/www/html/aaa.bak.*"
        exit 1
    fi
    log_info "Rolling back from: $LATEST_BAK"
    rsync -av --delete "$LATEST_BAK/" "$SERVE_DIR/" 2>&1 | tail -5
    chown -R www-data:www-data "$SERVE_DIR" 2>/dev/null || true
    log_info "Rollback complete. Verify at: $SITE_URL"
    exit 0
fi

# ── 2. --check mode: print state, don't change anything ──────────────────────
if [[ "$CHECK_ONLY" == "1" ]]; then
    echo "=== AAA Deploy State (T=$(date -u +%Y%m%d-%H%M%S)Z) ==="
    echo "--- source ---"
    if [[ -d "$DIST_DIR" ]]; then
        echo "  dist/ mtime: $(stat -c %y "$DIST_DIR/index.html" 2>/dev/null)"
    else
        log_error "dist/ does not exist; run: cd $REPO_DIR && npm run build"
        exit 1
    fi
    echo "--- served ---"
    echo "  $SERVE_DIR mtime: $(stat -c %y "$SERVE_DIR/index.html" 2>/dev/null)"
    echo "--- backup dirs ---"
    ls -1dt /var/www/html/aaa.bak.* 2>/dev/null | head -3 || echo "  (none)"
    echo "--- a2a-server ---"
    systemctl is-active "$A2A_SERVICE" 2>&1 || true
    echo "--- health ---"
    curl -sS "$A2A_HEALTH_URL" 2>&1 | head -1 || echo "  (unreachable)"
    exit 0
fi

# ── 3. Build (Vite) ──────────────────────────────────────────────────────────
log_info "Building AAA frontend (Vite)..."
cd "$REPO_DIR"
npm run build 2>&1 | tail -10

if [[ ! -f "$DIST_DIR/index.html" ]]; then
    log_error "Build did not produce $DIST_DIR/index.html"
    exit 1
fi

# ── 4. Backup current served dir, then rsync ────────────────────────────────
TS=$(date -u +%Y%m%d-%H%M%S)
BACKUP_DIR="/var/www/html/aaa.bak.$TS"
log_info "Backing up current serve dir to: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
# Copy-not-move so the live dir keeps serving during the sync
rsync -a "$SERVE_DIR/" "$BACKUP_DIR/"

log_info "Syncing dist/ → $SERVE_DIR (preserves _shared/ + extra dirs)"
rsync -av --backup --backup-dir="$BACKUP_DIR" /root/AAA/dist/ /var/www/html/aaa/

chown -R www-data:www-data "$SERVE_DIR"
log_info "Ownership set to www-data:www-data"

# ── 5. Optional: restart a2a-server ──────────────────────────────────────────
if [[ "$RESTART_A2A" == "1" ]]; then
    log_info "Restarting $A2A_SERVICE..."
    systemctl daemon-reload
    systemctl restart "$A2A_SERVICE"
    for i in {1..30}; do
        if curl -sf "$A2A_HEALTH_URL" >/dev/null 2>&1; then
            log_info "a2a-server healthy after ${i}s"
            break
        fi
        if [[ $i -eq 30 ]]; then
            log_error "a2a-server failed health check after 30s"
            exit 1
        fi
        sleep 1
    done
fi

# ── 6. Final probes ──────────────────────────────────────────────────────────
log_info "═══════════════════════════════════════════════════════════════════════════════"
log_info "AAA deploy complete: $TS"
log_info "Backup:  $BACKUP_DIR"
log_info "Site:    $SITE_URL"
log_info "Health:  $A2A_HEALTH_URL"
log_info "═══════════════════════════════════════════════════════════════════════════════"

# Quick post-deploy probe
NEW_JS=$(grep -oE 'assets/index-[^"]+\.js' "$SERVE_DIR/index.html" 2>/dev/null | head -1)
if [[ -n "$NEW_JS" ]]; then
    if [[ -f "$SERVE_DIR/$NEW_JS" ]]; then
        log_info "Verified: $NEW_JS present in serve dir"
    else
        log_error "MISSING: $NEW_JS not found in serve dir!"
        exit 1
    fi
fi

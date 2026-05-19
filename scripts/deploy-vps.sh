#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# AAA Autonomous VPS Deploy — A2A gateway deployment
#
# Purpose: Build and deploy AAA A2A gateway image locally.
#          Uses local image tag (no GHCR push needed).
#
# Flow:
#   1. Get current commit SHA
#   2. Build a2a-server Docker image with SHA tag
#   3. Update /root/compose/docker-compose.yml image pin
#   4. Restart container
#   5. Verify health
#
# Usage:
#   ./scripts/deploy-vps.sh           # full deploy
#   ./scripts/deploy-vps.sh --check   # only check if image exists
#
# DITEMPA BUKAN DIBERI — Forged, Not Given
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

REPO_NAME="aaa"
IMAGE_BASE="aaa-a2a"
COMPOSE_FILE="/root/compose/docker-compose.yml"
CONTAINER_NAME="aaa-a2a"
COMPOSE_SERVICE="aaa-a2a"
A2A_DIR="/root/AAA/a2a-server"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── 1. Get current commit SHA ────────────────────────────────────────────────
SHORT_SHA=$(git rev-parse --short HEAD)
FULL_SHA=$(git rev-parse HEAD)
log_info "Deploying AAA commit: $SHORT_SHA"

# ── 2. Build image ───────────────────────────────────────────────────────────
log_info "Building AAA A2A image locally..."
cd "$A2A_DIR"
docker build -t "$IMAGE_BASE:$SHORT_SHA" -t "$IMAGE_BASE:latest" .

# ── 3. Update compose pin ────────────────────────────────────────────────────
if [[ -f "$COMPOSE_FILE" ]]; then
    CURRENT_PIN=$(grep -E "^\s+image:\s+$IMAGE_BASE:" "$COMPOSE_FILE" | awk '{print $2}' || true)
    NEW_PIN="$IMAGE_BASE:$SHORT_SHA"

    if [[ "$CURRENT_PIN" != "$NEW_PIN" ]]; then
        log_info "Updating compose pin: $CURRENT_PIN → $NEW_PIN"
        sed -i "s|image: $IMAGE_BASE:[a-zA-Z0-9_-]*|image: $NEW_PIN|" "$COMPOSE_FILE"
    else
        log_info "Compose pin already correct"
    fi
else
    log_warn "Compose file not found at $COMPOSE_FILE"
fi

# ── 4. Restart container ─────────────────────────────────────────────────────
log_info "Restarting $CONTAINER_NAME container..."
cd /root/compose

# Stop and remove old container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

docker compose up -d --no-deps "$COMPOSE_SERVICE"

# ── 5. Health check ──────────────────────────────────────────────────────────
log_info "Waiting for health check..."
for i in {1..30}; do
    if curl -sf http://localhost:3001/health >/dev/null 2>&1; then
        log_info "AAA A2A is healthy and responding on port 3001"
        break
    fi
    if [[ $i -eq 30 ]]; then
        log_error "AAA A2A failed health check after 30 seconds"
        exit 1
    fi
    sleep 1
done

log_info "═══════════════════════════════════════════════════════════════════════════════"
log_info "AAA deploy complete: $SHORT_SHA"
log_info "Image: $IMAGE_BASE:$SHORT_SHA"
log_info "═══════════════════════════════════════════════════════════════════════════════"

#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  docker-guardian probe — Federation container health monitor     ║
# ║  Auto-heals: restart loops, disk pressure, image drift           ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/docker-guardian.log"
ALERT_LOG="/root/.openclaw/logs/docker-guardian-alerts.log"
COMPOSE_DIR="/root/compose"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

# ─── Thresholds ───────────────────────────────────────────────────
RESTART_WARN=5
RESTART_CRIT=10
DISK_WARN=85
DISK_CRIT=92

log "=== docker-guardian probe start ==="

# ─── 1. Container restart audit ───────────────────────────────────
RESTART_ISSUES=0
while IFS= read -r line; do
    name=$(echo "$line" | awk '{print $1}')
    count=$(echo "$line" | awk '{print $2}')
    if [ -z "$name" ] || [ -z "$count" ]; then continue; fi
    if [ "$count" -ge "$RESTART_CRIT" ]; then
        alert "CRITICAL: $name has $count restarts (threshold $RESTART_CRIT)"
        RESTART_ISSUES=$((RESTART_ISSUES + 1))
        # Auto-heal: restart the container via compose
        svc="${name#/}"  # strip leading /
        if [ -d "$COMPOSE_DIR" ]; then
            cd "$COMPOSE_DIR"
            # Try to map container name to compose service
            compose_svc=$(docker compose ps --format '{{.Service}}' 2>/dev/null | grep -F "$svc" | head -1 || true)
            if [ -n "$compose_svc" ]; then
                log "Auto-healing: docker compose restart $compose_svc"
                docker compose restart "$compose_svc" >> "$LOGFILE" 2>&1 || alert "Failed to restart $compose_svc"
            else
                log "Manual restart needed for $name (not found in compose)"
            fi
            cd - >/dev/null
        fi
    elif [ "$count" -ge "$RESTART_WARN" ]; then
        alert "WARNING: $name has $count restarts (threshold $RESTART_WARN)"
        RESTART_ISSUES=$((RESTART_ISSUES + 1))
    fi
done < <(docker ps --format '{{.Names}}' | xargs -I{} docker inspect --format='{{.Name}} {{.State.RestartCount}}' {} 2>/dev/null | sed 's|^/||')

# ─── 2. Disk pressure check ───────────────────────────────────────
DISK_PCT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -ge "$DISK_CRIT" ]; then
    alert "CRITICAL: Disk usage ${DISK_PCT}% (threshold ${DISK_CRIT}%)"
    # Auto-heal: prune dangling images + stopped containers
    log "Auto-prune: docker system prune -f --volumes"
    docker system prune -f --volumes >> "$LOGFILE" 2>&1 || true
elif [ "$DISK_PCT" -ge "$DISK_WARN" ]; then
    alert "WARNING: Disk usage ${DISK_PCT}% (threshold ${DISK_WARN}%)"
fi

# ─── 3. Zombie/orphan container cleanup ───────────────────────────
ZOMBIES=$(docker ps -a --filter "status=exited" --format '{{.Names}}' | grep -v 'data\|backup\|vault' | head -20)
ZOMBIE_COUNT=$(echo "$ZOMBIES" | grep -c '^' || true)
if [ "$ZOMBIE_COUNT" -gt 0 ]; then
    log "Found $ZOMBIE_COUNT exited containers to prune"
    docker container prune -f >> "$LOGFILE" 2>&1 || true
fi

# ─── 4. Image drift (unpinned / latest) ──────────────────────────
DRIFT=$(docker images --format '{{.Repository}}:{{.Tag}}' | grep ':latest' | grep -v '<none>' | wc -l)
if [ "$DRIFT" -gt 0 ]; then
    log "WARNING: $DRIFT images using :latest tag (unpinned)"
fi

# ─── Summary ──────────────────────────────────────────────────────
log "Probe complete. restart_issues=$RESTART_ISSUES disk=${DISK_PCT}% zombies=$ZOMBIE_COUNT drift=$DRIFT"

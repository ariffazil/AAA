#!/usr/bin/env bash
# jitu_actuator.sh — JITU's out-of-band enforcement nerve (F13 SAH 2026-10-07).
#
# LAW: brake_exists ≠ brake_is_independent  (canon: asi-substrate-invariants §3)
# The brake (jitu.py) decides. THIS actuator CUTS. Different planes, by design:
#   trip  → automatic physical cut of allowlisted lanes (systemd .path fires on trip.json)
#   restore → manual, sovereign-only, deliberate — never automatic
# React-only: this actuator NEVER trips or releases the brake itself.
# Model-free guarantee: bash + systemctl + docker. No python, no MCP, no LLM in the path —
# including no model from the lanes being cut.
#
# Scope→cut map (v1, measured lane names 2026-10-07):
#   fed     → docker stop litellm-federation + systemctl stop haproxy   (model supply)
#   gateway → systemctl stop caddy                                     (public ingress)
#   forge   → systemctl stop a-forge a-forge-mcp                       (execution organ)
#   all     → all of the above
set -u

JITU_DIR="${JITU_DIR:-/root/.local/share/arifos/jitu}"
TRIP="$JITU_DIR/trip.json"
LOG="${JITU_LOG:-/var/log/jitu-actuator.log}"
JITU_DRYRUN="${JITU_DRYRUN:-0}"

log() { printf '%s %s\n' "$(date -u '+%FT%TZ')" "$*" | tee -a "$LOG" >&2; }

receipt() { # append-only JSONL — an applied cut nobody can prove happened is not a cut
	printf '{"ts":"%s","event":"%s","detail":"%s"}\n' "$(date -u '+%FT%TZ')" "$1" "$2" \
		>>"$JITU_DIR/jitu_actuator_events.jsonl" 2>/dev/null || true
}

scope_of() { # read scope from trip.json; unreadable state = "all" (fail-closed, matches jitu.py)
	python3 - "$TRIP" <<'PY'
import json, sys
try:
    s = json.load(open(sys.argv[1]))
    sc = s.get("scope") or ["all"]
    print(" ".join(sc if isinstance(sc, list) else [str(sc)]))
except Exception:
    print("all")
PY
}

cut_lane() {
	case "$1" in
	fed)
		docker stop litellm-federation
		systemctl stop haproxy.service
		;;
	gateway) systemctl stop caddy.service ;;
	forge) systemctl stop a-forge.service a-forge-mcp.service ;;
	all)
		cut_lane fed
		cut_lane gateway
		cut_lane forge
		;;
	*) log "  UNKNOWN scope token '$1' — no allowlisted cut, skipped" ;;
	esac
}

apply() {
	[ -f "$TRIP" ] || {
		log "no trip file — idle, nothing to do"
		exit 0
	}
	SC="$(scope_of)"
	log "TRIP DETECTED — scope=[$SC]${JITU_DRYRUN:+ (DRYRUN)}"
	if [ "$JITU_DRYRUN" = "1" ]; then
		for lane in $SC; do log "  DRYRUN: would cut lane '$lane'"; done
		log "DRYRUN complete — no lanes touched"
		exit 0
	fi
	for lane in $SC; do
		log "cutting lane: $lane"
		cut_lane "$lane" 2>&1 | while IFS= read -r l; do log "  $l"; done
		receipt "lane_cut" "$lane"
	done
	log "TRIP APPLIED — scope=[$SC] — lanes cut at service level, model-free"
}

restore() { # sovereign-only manual recovery — deliberate, never event-driven
	log "RESTORE requested — restarting allowlisted lanes"
	systemctl start haproxy.service caddy.service a-forge.service a-forge-mcp.service 2>&1 | while IFS= read -r l; do log "  $l"; done
	docker start litellm-federation 2>&1 | while IFS= read -r l; do log "  $l"; done
	receipt "restore" "manual sovereign restore"
	log "RESTORE done — verify: systemctl status + docker ps"
}

selftest() { # proves the actuator's world-model without cutting anything
	FAIL=0
	for t in "docker inspect litellm-federation" "systemctl cat haproxy.service" \
		"systemctl cat caddy.service" "systemctl cat a-forge.service" "systemctl cat a-forge-mcp.service"; do
		if $t >/dev/null 2>&1; then log "OK   $t"; else
			log "MISS $t"
			FAIL=1
		fi
	done
	python3 "$JITU_DIR/../kernel/jitu.py" selftest >/dev/null 2>&1 ||
		python3 /root/AAA/federation/kernel/jitu.py selftest >/dev/null 2>&1 || FAIL=1
	log "selftest $([ $FAIL -eq 0 ] && echo PASS || echo FAIL) — brake authority + all cut targets resolve"
	return $FAIL
}

case "${1:-}" in
apply) apply ;;
restore) restore ;;
selftest) selftest ;;
*)
	echo "usage: $0 apply|restore|selftest" >&2
	exit 2
	;;
esac

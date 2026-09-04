#!/bin/bash
# universe-drift-sentinel.sh — universe map freshness sentinel (OBSERVE_ONLY)
# ═══════════════════════════════════════════════════════════════════════════
# Forged 2026-09-04 FI-008 (Kimi Code), F13 directive: "make sure all my agents
# are aware every time the system moves dynamically."
#
# Lane ownership (anti-entropy — no duplicate capability surfaces):
#   organ liveness   → federation-watchdog (F13-pending) + `now` / `make health` at boot
#   harness liveness → /etc/cron.d/aaa-mesh-health (mesh-health-probe.sh)
#   codex runtime    → /etc/cron.d/arifos-federation-audit
#   THIS SENTINEL    → map freshness ONLY: did the map move without reaching the agents?
#
# Drift classes:
#   STALE_RENDER — a map source is newer than rendered /root/AGENTS.md or /root/CLAUDE.md
#                  → doctrine/topology edited without re-rendering the root terminal
#   UNCOMMITTED  — map surfaces dirty in AAA git
#                  → moved, but invisible to every machine that is not KVM8
#   TOMBSTONE_VIOLATION — deprecation-registry says a unit is dead but it still runs
#                  → claim-vs-runtime gap (scar: 2026-09-04 entropy-trim half-execution)
#
# Behavior: writes /run/arifos/universe-drift.json (SOT). On NEW drift appends ONE
# dated line to /root/AAA/terminal/holds.txt; deletes it on resolution (that file's law).
# Never renders, never commits, never mutates the map. Cost: ~0 (mtime + git status).
# Note: render-agents.sh --check is structurally always-diff (embedded render
# timestamp) — this sentinel uses mtime comparison instead. FI-008 2026-09-04.
# Rollback: rm /etc/cron.d/aaa-universe-drift && rm /run/arifos/universe-drift.json
set -u

AAA=/root/AAA
OUT=/run/arifos/universe-drift.json
HOLDS=/root/AAA/terminal/holds.txt
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TODAY="$(date -u +%Y-%m-%d)"

# ── 1. STALE_RENDER — newest map source vs each rendered adapter ──────────
newest_src=0
for f in "$AAA"/instructions/*.md "$AAA/UNIVERSE.yaml" \
         "$AAA/federation/organs.yaml" "$AAA/docs/MACHINE_MAP.md"; do
  [ -f "$f" ] || continue
  m=$(stat -c %Y "$f" 2>/dev/null || echo 0)
  [ "$m" -gt "$newest_src" ] && newest_src=$m
done

drifts=""
detail=""
for r in /root/AGENTS.md /root/CLAUDE.md; do
  m=$(stat -c %Y "$r" 2>/dev/null || echo 0)
  if [ "$newest_src" -gt "$m" ]; then
    drifts="STALE_RENDER"
    detail="$detail $r older than map sources;"
    break
  fi
done

# ── 2. UNCOMMITTED — map surfaces dirty in AAA ────────────────────────────
dirty=$(git -C "$AAA" status --porcelain -- UNIVERSE.yaml federation/organs.yaml \
        instructions docs/MACHINE_MAP.md 2>/dev/null)
if [ -n "$dirty" ]; then
  n=$(echo "$dirty" | wc -l)
  drifts="$drifts UNCOMMITTED"
  detail="$detail ${n} map file(s) uncommitted in AAA;"
fi
# ── 3. TOMBSTONE_VIOLATION — doctrine says dead, machine says alive ──────
# Scar 2026-09-04: entropy-trim tombstoned Graphiti in doctrine while the
# service still ran (claim-vs-runtime gap). This class makes that impossible.
REG="$AAA/docs/deprecation-registry.json"
if [ -f "$REG" ]; then
  while IFS= read -r unit; do
    [ -n "$unit" ] || continue
    if systemctl is-active "$unit" 2>/dev/null | grep -qE '^(active|activating)$'; then
      drifts="$drifts TOMBSTONE_VIOLATION"
      detail="$detail $unit tombstoned but running;"
      break
    fi
  done < <(python3 -c "
import json
try:
    d = json.load(open('$REG'))
    for e in d.get('deprecated_services', []):
        u = e.get('unit') or (e.get('id') if e.get('id', '').endswith('.service') else '')
        if u and e.get('status', '').upper() == 'DEPRECATED':
            print(u)
except Exception:
    pass" 2>/dev/null)
fi
drifts=$(echo "$drifts" | xargs)

# ── state assembly + transition detection ─────────────────────────────────
prev_drift=false
if [ -f "$OUT" ] && grep -qE '"has_drift": ?true' "$OUT" 2>/dev/null; then
  prev_drift=true
fi

if [ -z "$drifts" ]; then
  printf '{"schema":"arifos.universe-drift.v1","generated_at_utc":"%s","has_drift":false,"drift":[],"detail":""}\n' "$STAMP" > "$OUT"
  if [ "$prev_drift" = true ] && [ -f "$HOLDS" ]; then
    grep -v '^UNIVERSE:' "$HOLDS" > "$HOLDS.tmp" 2>/dev/null && mv "$HOLDS.tmp" "$HOLDS" || rm -f "$HOLDS.tmp"
  fi
  echo "$STAMP CLEAN — universe map rendered + committed, agents see truth"
else
  case "$drifts" in
    *TOMBSTONE_VIOLATION*) FIX="stop the tombstoned unit or restore it in deprecation-registry — doctrine and machine disagree";;
    *STALE_RENDER*|*UNCOMMITTED*) FIX="/root/scripts/render-agents.sh + commit AAA — agents are reading a stale map";;
    *) FIX="see /run/arifos/universe-drift.json";;
  esac
  printf '{"schema":"arifos.universe-drift.v1","generated_at_utc":"%s","has_drift":true,"drift":"%s","detail":"%s"}\n' \
    "$STAMP" "$drifts" "$(echo "$detail" | sed 's/^ *//; s/; *$//')" > "$OUT"
  if ! grep -q '^UNIVERSE:' "$HOLDS" 2>/dev/null; then
    printf 'UNIVERSE: %s since %s (fix: %s)\n' \
      "$(echo "$drifts" | tr ' ' '/')" "$TODAY" "$FIX" >> "$HOLDS"
  fi
  echo "$STAMP DRIFT: $drifts —$detail"
fi

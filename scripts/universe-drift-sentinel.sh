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
  printf '{"schema":"arifos.universe-drift.v1","generated_at_utc":"%s","has_drift":true,"drift":"%s","detail":"%s"}\n' \
    "$STAMP" "$drifts" "$(echo "$detail" | sed 's/^ *//; s/; *$//')" > "$OUT"
  if ! grep -q '^UNIVERSE:' "$HOLDS" 2>/dev/null; then
    printf 'UNIVERSE: %s since %s (fix: /root/scripts/render-agents.sh + commit AAA — agents are reading a stale map)\n' \
      "$(echo "$drifts" | tr ' ' '/')" "$TODAY" >> "$HOLDS"
  fi
  echo "$STAMP DRIFT: $drifts —$detail"
fi

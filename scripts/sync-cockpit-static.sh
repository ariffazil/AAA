#!/usr/bin/env bash
# sync-cockpit-static.sh — F1-safe publisher: live AAA registry -> cockpit static panel
# Gates (why: 2026-08-14 near-miss — cp blind would clobber healthy static with empty-but-valid JSON):
#   G1 size      — source non-empty
#   G2 structure — jq-valid JSON
#   G3 semantic  — agent count >= floor (empty-but-valid [] must NOT replace healthy 40)
# Publish: atomic tmp+mv (caddy never reads a half-written file).
# On any gate failure: KEEP last healthy static (this is the F1 property), log, exit 0 (cron stays quiet).
set -u
SRC="http://127.0.0.1:3001/.well-known/agents.json"
DST_DIR="/var/www/html/aaa/a2a"
DST="$DST_DIR/agents.json"
FLOOR=10
LOG="/var/log/aaa/sync-cockpit-static.log"
FALLBACK_SRC="/root/AAA/public/a2a/agents.json"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

TMP=$(mktemp "$DST_DIR/.agents.tmp.XXXXXX") || { log "FAIL mktemp"; exit 0; }
trap 'rm -f "$TMP"' EXIT

# G1+G2+G3: fetch, validate, semantic floor — single jq pipeline (parse error => non-zero)
COUNT=$(curl -s -m 6 "$SRC" -o "$TMP" && jq -e 'if type=="array" then length elif has("agents") then (.agents|length) else 0 end' "$TMP" 2>/dev/null) || COUNT=""
if [ -z "$COUNT" ] || [ "$COUNT" -lt "$FLOOR" ] 2>/dev/null; then
  log "GATE-FAIL src count='${COUNT:-unparseable}' floor=$FLOOR — keeping last healthy static"
  exit 0
fi

# Extra guard: never shrink the panel by more than half vs current healthy static (regression canary)
CUR=$(jq -e 'if type=="array" then length elif has("agents") then (.agents|length) else 0 end' "$DST" 2>/dev/null || echo 0)
if [ "$CUR" -gt 0 ] && [ "$COUNT" -lt $((CUR / 2)) ]; then
  log "GATE-FAIL shrink canary: live=$COUNT vs static=$CUR — keeping last healthy static"
  exit 0
fi

mv -f "$TMP" "$DST" && trap - EXIT
log "OK published $COUNT agents (prev=$CUR)"

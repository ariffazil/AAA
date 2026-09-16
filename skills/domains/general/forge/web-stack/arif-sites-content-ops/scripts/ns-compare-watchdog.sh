#!/usr/bin/env bash
# ns-compare-watchdog.sh — mtime watchdog for the NS seat-comparison page.
#
# Reconstructed 2026-09-15 from the arif-sites-content-ops SKILL.md spec
# ("Data-driven auto-update pipeline for static pages", PROVEN 2026-08-01):
#   no_agent:true, */15 * * * *, deliver=origin
#   regenerates + rsyncs ONLY that one directory when [ "$SRC_JSON" -nt "$GEN_HTML" ]
#   silent otherwise (empty stdout = no delivery)
#   no full build, no Caddy reload, no T3 gate
#
# Deploy: copy to ~/.hermes/scripts/ and wire the cron entry.
#   cp scripts/ns-compare-watchdog.sh ~/.hermes/scripts/ && chmod +x ~/.hermes/scripts/ns-compare-watchdog.sh
#
# IMPORTANT: this script prints NOTHING when there is no work to do. Empty
# stdout is the signal to the cron runner that no delivery is required. Any
# line printed means there IS something to report.

set -uo pipefail

# --- paths (override via env if the site layout moves) ---
SITE_DIR="${SITE_DIR:-/root/arif-fazil.com/sites/arif-fazil.com}"
SRC_JSON="${SRC_JSON:-$SITE_DIR/public/data/politics/ns_results.json}"
GEN_HTML="${GEN_HTML:-$SITE_DIR/public/politics/ns-election/compare/index.html}"
GEN_SCRIPT="${GEN_SCRIPT:-scripts/generate-ns-compare.cjs}"
RSYNC_DEST="${RSYNC_DEST:-/var/www/html/arif-fazil.com/politics/ns-election/compare/}"

cd "$SITE_DIR" 2>/dev/null || { echo "ns-compare-watchdog: site dir missing: $SITE_DIR"; exit 1; }

# Guard: the source artefact must exist before the mtime comparison is meaningful.
[ -f "$SRC_JSON" ] || { echo "ns-compare-watchdog: source JSON missing: $SRC_JSON"; exit 1; }

# THE GATE — the whole point of the script. Not stale => silent exit 0.
if [ -f "$GEN_HTML" ] && [ ! "$SRC_JSON" -nt "$GEN_HTML" ]; then
  exit 0
fi

echo "ns-compare-watchdog: $SRC_JSON is newer than generated page — regenerating"

# Regenerate ONLY the compare page (never a full build).
if ! node "$GEN_SCRIPT" >/tmp/ns-compare-gen.log 2>&1; then
  echo "ns-compare-watchdog: generator FAILED (node $GEN_SCRIPT)"
  tail -n 20 /tmp/ns-compare-gen.log
  exit 1
fi
echo "ns-compare-watchdog: regenerated $GEN_HTML"

# rsync ONLY that one directory. No Caddy reload, no T3 gate — verify-class op.
if command -v rsync >/dev/null 2>&1; then
  if rsync -a --delete "$(dirname "$GEN_HTML")/" "$RSYNC_DEST" >/tmp/ns-compare-rsync.log 2>&1; then
    echo "ns-compare-watchdog: rsynced to $RSYNC_DEST"
  else
    echo "ns-compare-watchdog: rsync FAILED -> $RSYNC_DEST"
    tail -n 20 /tmp/ns-compare-rsync.log
    exit 1
  fi
else
  echo "ns-compare-watchdog: rsync not installed; page regenerated but NOT deployed"
  exit 1
fi

exit 0

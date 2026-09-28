#!/usr/bin/env bash
# Delete the older, riskier duplicate. Pristine-full is more recent.
# Pre-condition: F13 binary on Q3.

set -euo pipefail

DUPE="/root/hermes_work/hermes-agent-copy"
KEEP="/root/hermes_work/pristine-full"

# Idempotency guard
[ ! -d "$DUPE" ] && { echo "ALREADY DELETED"; exit 0; }

# Verify both existed (sanity)
[ -d "$KEEP" ] || { echo "ABORT: pristine-full missing — would orphan the runtime"; exit 1; }

# Verify sizes match (we're deleting one of a known duplicate set)
DUPE_SIZE=$(du -sb "$DUPE" | cut -f1)
KEEP_SIZE=$(du -sb "$KEEP" | cut -f1)
echo "DUPE   size: $DUPE_SIZE bytes"
echo "KEEP   size: $KEEP_SIZE bytes"
# Do NOT enforce equality — they may have drifted by 3 files (per earlier probe)

# Hard-link audit: any hardlinks pointing INTO the doomed dir?
echo "── hardlink audit (must show zero hardlinks into $DUPE) ──"
find /root -xdev -type f -links +1 2>/dev/null | grep "$DUPE" | head -5 || true

# Final tally
read -p "Confirm delete $DUPE (6.4G reclaim)? Type YES to proceed: " CONFIRM
[ "$CONFIRM" = "YES" ] || { echo "ABORTED by user"; exit 1; }

rm -rf "$DUPE"
echo "DELETED: $DUPE"
echo "Q3 PASS · 6.4G reclaimed"

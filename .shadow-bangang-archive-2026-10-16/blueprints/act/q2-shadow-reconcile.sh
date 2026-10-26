#!/usr/bin/env bash
# Sync KVM8 shadow SOUL.md → post-Sah canonical sha f3057f1a...
# Pre-condition: F13 binary on Q2.

set -euo pipefail

CANONICAL="/root/.hermes/SOUL.md"
SHADOW="/root/arifOS/memory/identity/SOUL.md"
CANON_SHA=$(sha256sum "$CANONICAL" | cut -d' ' -f1)
SHADOW_SHA=$(sha256sum "$SHADOW" | cut -d' ' -f1)

[ "$CANON_SHA" = "f3057f1acbff9c77223ba6793ae20230d2de0633cfbe12b571e09e3435ac8be5" ] || { echo "ABORT: canonical sha mismatch"; exit 1; }

[ "$CANON_SHA" = "$SHADOW_SHA" ] && { echo "ALREADY SYNCED"; exit 0; }

# Backup
cp -p "$SHADOW" "${SHADOW}.pre-q2.bak"
echo "BACKUP: $SHADOW → ${SHADOW}.pre-q2.bak (sha $SHADOW_SHA)"

# Reconcile — shadow becomes symlink to canonical (unidirectional sync)
ln -sf "$CANONICAL" "$SHADOW"
echo "SYMLINK: $SHADOW → $CANONICAL"

# Verify
echo "PRE  shadow sha: $(sha256sum ${SHADOW}.pre-q2.bak | cut -d' ' -f1)"
echo "POST shadow sha: $(sha256sum $SHADOW | cut -d' ' -f1)"
echo "POST canonical sha: $(sha256sum $CANONICAL | cut -d' ' -f1)"

echo "Q2 PASS · shadow symlinked to canonical"

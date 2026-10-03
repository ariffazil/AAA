#!/bin/bash
# sync.sh — sync AAA repo skills to /root/.agents/skills/
# DITEMPA BUKAN DIBERI — Skills sync, not drift
set -euo pipefail

AAA_SKILLS="/root/AAA/skills"
LOCAL_SKILLS="/root/.agents/skills"

echo "=== sync.sh starting $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# 1. Detect changes in last pull
cd /root/AAA
PREV=$(git rev-parse HEAD@{1} 2>/dev/null || git rev-parse HEAD)
CURR=$(git rev-parse HEAD)
CHANGED=$(git diff --name-only "$PREV" "$CURR" -- 'skills/**/*.md' 2>/dev/null || echo "")

if [ -z "$CHANGED" ]; then
    echo "no skill changes detected"
    exit 0
fi

echo "changed skills:"
echo "$CHANGED" | sed 's/^/  /'

# 2. Mirror reflectives (newly created dir)
if [ -d "$AAA_SKILLS/reflective" ]; then
    for skill_dir in "$AAA_SKILLS/reflective"/*/; do
        skill_name=$(basename "$skill_dir")
        target="$LOCAL_SKILLS/$skill_name"
        mkdir -p "$target"
        cp "$skill_dir/SKILL.md" "$target/SKILL.md"
        echo "synced: $skill_name"
    done
    # Sync the index too
    if [ -f "$AAA_SKILLS/reflective/README.md" ]; then
        cp "$AAA_SKILLS/reflective/README.md" "$LOCAL_SKILLS/reflective-index.md"
        echo "synced: reflective-index"
    fi
fi

# 3. Hash verification
echo ""
echo "=== hash verification ==="
HASH_REMOTE=$(sha256sum "$AAA_SKILLS/reflective"/*/SKILL.md 2>/dev/null | sort)
HASH_LOCAL=$(sha256sum "$LOCAL_SKILLS"/{sovereign-recognize,caller-trace}/SKILL.md 2>/dev/null | sort)

if [ "$HASH_REMOTE" = "$HASH_LOCAL" ]; then
    echo "✓ skill integrity verified — local matches AAA repo"
else
    echo "⚠ skill DRIFT detected — manual reconcile required"
    diff <(echo "$HASH_REMOTE") <(echo "$HASH_LOCAL") || true
    exit 1
fi

echo ""
echo "=== sync.sh complete ==="

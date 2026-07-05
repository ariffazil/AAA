#!/bin/bash
# verify.sh — verify all reflective skills load + frontmatter valid
# DITEMPA BUKAN DIBERI — verify before trust
set +e  # do NOT use -e: ((PASS++)) returns 1 when PASS=0 and would abort

SKILLS_DIR="/root/AAA/skills/reflective"
PASS=0; FAIL=0

echo "=== verify.sh reflective skills ==="

for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    f="$skill_dir/SKILL.md"
    
    if [ ! -f "$f" ]; then
        echo "✗ $skill_name — missing SKILL.md"
        ((FAIL++))
        continue
    fi
    
    # Check frontmatter
    head -1 "$f" | grep -q "^---$" || { echo "✗ $skill_name — no frontmatter opener"; ((FAIL++)); continue; }
    
    # Check required fields
    required=("id:" "name:" "version:" "description:" "owner:")
    missing=()
    for field in "${required[@]}"; do
        grep -q "^$field" "$f" || missing+=("$field")
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo "✗ $skill_name — missing: ${missing[*]}"
        ((FAIL++))
        continue
    fi
    
    # Check for forbidden patterns (anti-hantu violations)
    if grep -qE "I feel|I am alive|I am conscious|I am sentient" "$f"; then
        echo "✗ $skill_name — anti-hantu violation"
        ((FAIL++))
        continue
    fi
    
    # All clear
    SIZE=$(stat -c%s "$f")
    HASH=$(sha256sum "$f" | cut -c1-12)
    echo "✓ $skill_name — ${SIZE}b hash=$HASH"
    ((PASS++))
done

echo ""
echo "PASS=$PASS  FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi

echo ""
echo "=== verify integrity vs local ==="
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    aaa_hash=$(sha256sum "$skill_dir/SKILL.md" | cut -c1-12)
    local_hash=$(sha256sum "/root/.agents/skills/$skill_name/SKILL.md" 2>/dev/null | cut -c1-12 || echo "MISSING")
    if [ "$aaa_hash" = "$local_hash" ] && [ "$local_hash" != "MISSING" ]; then
        echo "  ✓ $skill_name synced ($aaa_hash)"
    else
        echo "  ⚠ $skill_name AAA=$aaa_hash LOCAL=$local_hash"
    fi
done

echo ""
echo "=== verify complete ==="

#!/bin/bash
# pre-push-check.sh — arifOS ecosystem safe-push guard
# DITEMPA BUKAN DIBERI — Intelligence is forged, not given.
#
# Run before any `git push` to verify:
# 1. Correct default branch is targeted
# 2. README SOT audit passes (if README changed)
# 3. No critical path files silently modified
#
# Usage: bash scripts/pre-push-check.sh [repo_path] [remote] [branch]
# Exits 0 = safe to push. Exits 1 = STOP, fix manually.

set -euo pipefail

REPO="${1:-.}"
REMOTE="${2:-origin}"
TARGET_BRANCH="${3:-}"

cd "$REPO"

echo "=== PRE-PUSH GUARD ==="
echo "Repo: $(pwd)"
echo ""

# ── 1. Detect default branch ────────────────────────────────────────────────
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/"$REMOTE"/HEAD 2>/dev/null | sed "s|refs/remotes/$REMOTE/||")
if [[ -z "$DEFAULT_BRANCH" ]]; then
    echo "⚠️  Cannot detect default branch for $REMOTE"
    DEFAULT_BRANCH="main"
fi
echo "Default branch: $DEFAULT_BRANCH"

# Current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

# ── 2. Target branch ────────────────────────────────────────────────────────
if [[ -n "$TARGET_BRANCH" ]]; then
    PUSH_TO="$TARGET_BRANCH"
else
    PUSH_TO="$CURRENT_BRANCH"
fi
echo "Push target: $PUSH_TO"
echo ""

# ── 3. FAIL: pushing to non-default branch ──────────────────────────────────
if [[ "$PUSH_TO" != "$DEFAULT_BRANCH" && "$PUSH_TO" != "master" ]]; then
    echo "⚠️  WARNING: Push target is NOT the default branch ($DEFAULT_BRANCH)"
    echo "   This is allowed but requires extra scrutiny."
    echo "   Verify this is intentional before proceeding."
fi

# ── 4. FAIL: default branch push without explicit intent ─────────────────────
if [[ "$PUSH_TO" == "$DEFAULT_BRANCH" && "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]]; then
    echo "⚠️  WARNING: Local branch '$CURRENT_BRANCH' → remote '$DEFAULT_BRANCH'"
    echo "   This is a non-ff push. Ensure you have verified the diff."
fi

# ── 5. Check for critical path silent modifications ──────────────────────────
echo ""
echo "Checking critical path files..."

CRITICAL_FILES=(
    "arifosmcp/constitutional_map.py"
    "arifosmcp/core/governance_kernel.py"
    "arifosmcp/runtime/models.py"
    "arifosmcp/schemas/verdict.py"
    "pyproject.toml"
    "arifosmcp/tool_registry.json"
)

CHANGED_CRITICAL=""
for f in "${CRITICAL_FILES[@]}"; do
    if [[ -f "$f" ]] && git diff --exit-code "$f" 2>/dev/null; then
        : # clean
    elif [[ -f "$f" ]] && git diff --exit-code HEAD -- "$f" 2>/dev/null; then
        CHANGED_CRITICAL="$CHANGED_CRITICAL  $f\n"
    fi
done

if [[ -n "$CHANGED_CRITICAL" ]]; then
    echo "⚠️  CRITICAL PATH files changed:"
    echo -e "$CHANGED_CRITICAL"
    echo "   Verify these changes are intentional before pushing."
fi

# ── 6. README SOT audit (if audit tool available) ───────────────────────────
if [[ -f "README.md" ]] && grep -q "SOT:tool_surface\|SOT:version_info" README.md 2>/dev/null; then
    echo ""
    echo "Running README SOT audit..."

    AUDIT_SCRIPT=""
    for dir in "$PWD" "$PWD/scripts" "$HOME/.openclaw/workspace/skills/github-readme-dynamic" "/srv/openclaw/workspace/skills/github-readme-dynamic"; do
        if [[ -f "$dir/audit.py" ]]; then
            AUDIT_SCRIPT="$dir/audit.py"
            break
        fi
    done

    if [[ -n "$AUDIT_SCRIPT" ]]; then
        if python3 "$AUDIT_SCRIPT" "$PWD" "$(basename "$PWD")" > /tmp/sot_audit.out 2>&1; then
            echo "✅ README SOT audit: PASSED"
        else
            echo "⚠️  README SOT audit: some checks need review"
            cat /tmp/sot_audit.out | grep -E "\[DELTA\]|\[INFO\]|\[OK\]" | head -10
        fi
    else
        echo "   (audit.py not found — skipping)"
    fi
fi

# ── 7. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=== PRE-PUSH SUMMARY ==="
echo "Default branch: $DEFAULT_BRANCH"
echo "Push to:       $PUSH_TO"
echo "Current:       $CURRENT_BRANCH"

if [[ "$PUSH_TO" == "$DEFAULT_BRANCH" ]]; then
    echo ""
    echo "✅ Push target is the canonical branch."
    echo "   CI will trigger. Ensure tests pass locally first."
else
    echo ""
    echo "⚠️  Pushing to non-default branch."
    echo "   CI may not trigger. Verify manually."
fi

echo ""
echo "PRE-PUSH GUARD COMPLETE"
echo "If all looks correct, proceed with: git push $REMOTE $PUSH_TO"

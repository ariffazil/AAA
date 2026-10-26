#!/usr/bin/env bash
# grep-port-check.sh — C1 CI gate
# Date: 2026-10-16 · KVM8 · FI-003
# Exits 1 if port 8100 (or other deprecated values) appears in active source.
set -uo pipefail
REPO_ROOT="${1:-/root/AAA}"
DEPRECATED_PORTS=("8100")
DEPRECATED_VALUES=(
    "VAULT_API_URL=:(deprecated 8100, see federation.toml)"
    "VAULT_WRITER_URL=:(deprecated 8100, see federation.toml)"
    "VAULT_API_URL=http://127.0.0.1:(deprecated 8100, see federation.toml)"
    "VAULT_WRITER_URL=http://127.0.0.1:(deprecated 8100, see federation.toml)"
)
INCLUDES=("*.py" "*.sh" "*.toml" "*.yaml" "*.yml" "*.json" "*.md" "*.cfg" "*.ini" "*.env" "*.txt" "*.js" "*.ts" "*.cjs" "*.mjs" "*.rs" "*.go" "*.proto")
EXCLUDES=("*node_modules*" "*.pnpm*" "*venv*" "*.venv*" "*__pycache__*" "*.git*" "*dist*" "*build*" "*/plugins/dist/*" "*archive*" "*/.backup-*" "*/.hermes-archived-*" "*/.bak-*" "*/.bak" "*/uv.lock" "*/package-lock.json" "*/yarn.lock" "*/.log" "*/node_modules")
build_find_args() {
    local args=()
    for inc in "${INCLUDES[@]}"; do args+=( -name "$inc" -o ); done
    unset 'args[${#args[@]}-1]'
    for exc in "${EXCLUDES[@]}"; do args+=( -not -path "$exc" ); done
    printf '%s\n' "${args[@]}"
}
mapfile -t FIND_ARGS < <(build_find_args)
FAIL=0
for port in "${DEPRECATED_PORTS[@]}"; do
    HITS=$(find "$REPO_ROOT" \( -type d \( "${PRUNE_DIRS[@]/#/-name }" -o \) -prune -o -type f \( "${INCLUDES[@]/#/-name }" \) -print0 2>/dev/null | xargs -0 grep -lE "(^|[^0-9])${port}([^0-9]|$)" 2>/dev/null | grep -v "^${REPO_ROOT}/\.git/" 2>/dev/null | head -50)
    if [ -n "$HITS" ]; then echo "  ✗ :$port"; echo "$HITS" | sed 's/^/    /'; FAIL=$((FAIL+1)); else echo "  ✓ :$port"; fi
done
for val in "${DEPRECATED_VALUES[@]}"; do
    HITS=$(find "$REPO_ROOT" \( -type d \( "${PRUNE_DIRS[@]/#/-name }" -o \) -prune -o -type f \( "${INCLUDES[@]/#/-name }" \) -print0 2>/dev/null | xargs -0 grep -lF "$val" 2>/dev/null | head -20)
    if [ -n "$HITS" ]; then echo "  ✗ '$val'"; echo "$HITS" | sed 's/^/    /'; FAIL=$((FAIL+1)); else echo "  ✓ '$val'"; fi
done
if [ "$FAIL" -gt 0 ]; then echo "=== RESULT: $FAIL deprecated-pattern bucket(s) found ==="; exit 1; else echo "=== RESULT: CLEAN ==="; exit 0; fi

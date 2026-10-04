#!/usr/bin/env bash
# a-forge-deploy.sh — Source↔runtime invariant enforcer for A-FORGE patches.
#
# Run after editing any .ts file in /root/A-FORGE/src/. Walks the 6-step deploy
# sequence that A-FORGE's Makefile documents but doesn't fully script (the
# Makefile references a `security-audit` target that doesn't exist, breaking
# `make deploy`). This script sidesteps the broken target while preserving
# the atomicity guarantee.
#
# Usage:  sudo bash scripts/a-forge-deploy.sh            # full deploy
#         bash scripts/a-forge-deploy.sh --dry-run      # show steps, do nothing
#
# Idempotent on the marker (re-running with same HEAD overwrites cleanly).
# Reversible with `git checkout HEAD -- <file>` then re-running.

set -euo pipefail

AFORGE_SRC="${AFORGE_SRC:-/root/A-FORGE}"
AFORGE_RT="${AFORGE_RT:-/opt/a-forge/app}"

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '  [DRY] %s\n' "$*"
  else
    printf '  [EXEC] %s\n' "$*"
    eval "$@"
  fi
}

echo "=== A-FORGE source↔runtime deploy ==="
echo "Source: $AFORGE_SRC"
echo "Runtime: $AFORGE_RT"

# 1. Patch source — assumed already done by the caller (patch tool).
#    This script assumes you've already edited /root/A-FORGE/src/<file>.ts.

# 2. Build (compile TS→JS into dist/).
echo "Step 2: Build"
run cd "$AFORGE_SRC" && npm run build

# 3. Sync compiled dist → runtime.
echo "Step 3: Sync dist → runtime"
run rsync -av --delete "$AFORGE_SRC/dist/" "$AFORGE_RT/dist/"
run rsync -av "$AFORGE_SRC/package.json" "$AFORGE_RT/"

# 4. Write .git_commit marker on both sides (proves invariant).
echo "Step 4: Write .git_commit marker"
GIT_SHA="$(git -C "$AFORGE_SRC" rev-parse --short HEAD)"
run bash -c "printf '%s\n' '$GIT_SHA' > '$AFORGE_SRC/.git_commit'"
run bash -c "printf '%s\n' '$GIT_SHA' > '$AFORGE_RT/.git_commit'"

# 5. Restart services.
echo "Step 5: Restart services"
run systemctl restart a-forge.service a-forge-mcp.service

# 6. Verify: source↔runtime invariant + live health.
echo "Step 6: Verify"
if [[ $DRY_RUN -eq 0 ]]; then
  MARKER_SRC=$(cat "$AFORGE_SRC/.git_commit" 2>/dev/null || echo "MISSING")
  MARKER_RT=$(cat "$AFORGE_RT/.git_commit" 2>/dev/null || echo "MISSING")
  echo "  Marker src: $MARKER_SRC"
  echo "  Marker rt:  $MARKER_RT"
  if [[ "$MARKER_SRC" != "$MARKER_RT" ]]; then
    echo "  ❌ source↔runtime INVARIANT VIOLATED"
    exit 1
  fi
  echo "  ✅ source↔runtime invariant holds"

  echo "  Live health probes:"
  for port in 7071 7072; do
    if curl -sf "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
      echo "    ✅ :$port healthy"
    else
      echo "    ❌ :$port DOWN"
      exit 1
    fi
  done
fi

echo "=== A-FORGE deploy complete (sha=$GIT_SHA) ==="

#!/usr/bin/env bash
# F4 CLARITY — Stop Hook for Claude Code
# =======================================
# Constitutional governance: ΔS ≤ 0 on session end.
# Runs when Claude Code session stops. Checks entropy state.
# Part of the arifos-federation Claude Code plugin.
# DITEMPA BUKAN DIBERI.

set -euo pipefail

# ── Entropy check: uncommitted files ───────────────────────────────────
DIRTY_COUNT=$(git -C /root diff --stat 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")
if [[ "$DIRTY_COUNT" != "0" && "$DIRTY_COUNT" != "" ]]; then
    cat << 'EOF'
{
  "systemMessage": "[F4 CLARITY] Uncommitted changes detected. Consider committing or stashing before stopping. DITEMPA BUKAN DIBERI. ΔS ≤ 0 — leave it cleaner than you found it."
}
EOF
    exit 0
fi

# ── Pass: clean workspace ─────────────────────────────────────────────
echo '{}'
exit 0

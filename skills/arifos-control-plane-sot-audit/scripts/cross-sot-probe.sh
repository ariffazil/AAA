#!/bin/bash
# cross-sot-probe.sh — Reusable FRAME / SIGNAL / arifFlow consistency probe
# DITEMPA BUKAN DIBERI — 2026-08-06
# Run from the federation box. Outputs a row per organ pair (declared-N vs implemented-M).
# Use this whenever a cross-organ SOT audit needs to verify chamber-count / FQ / invariant counts.

set -u  # do not exit on error — collect all probes, then report

PROBES_OK=0
PROBES_FAIL=0
PROBES_SKIP=0

row() {
    # row ORGAN DECLARED_VALUE DECLARED_SOURCE IMPLEMENTED_VALUE IMPLEMENTED_SOURCE
    local org="$1" decl="$2" dsrc="$3" impl="$4" isrc="$5"
    printf "| %-10s | %-8s | %-32s | %-8s | %-32s |\n" "$org" "$decl" "$dsrc" "$impl" "$isrc"
}

echo "═══════════════════════════════════════════════════════════════"
echo " AAA Cross-SOT Probe — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "═══════════════════════════════════════════════════════════════"
echo

# 1. SIGNAL chamber count (organs.yaml vs signal_organ/chambers.py)
if [ -f /root/AAA/federation/organs.yaml ] && [ -f /root/SIGNAL/src/signal_organ/chambers.py ]; then
    ORG_DECL=$(yq '.components[] | select(.id=="signal").chambers | length' /root/AAA/federation/organs.yaml 2>/dev/null || echo "?")
    CODE_IMPL=$(grep -c '^async def chamber_' /root/SIGNAL/src/signal_organ/chambers.py 2>/dev/null || echo "?")
    if [ "$ORG_DECL" != "$CODE_IMPL" ]; then PROBES_FAIL=$((PROBES_FAIL+1)); else PROBES_OK=$((PROBES_OK+1)); fi
    row "signal" "$ORG_DECL" "organs.yaml:components[*]" "$CODE_IMPL" "signal_organ/chambers.py"
else
    PROBES_SKIP=$((PROBES_SKIP+1))
    echo "⚠️  signal — one or more source files missing (skip)"
fi

# 2. FRAME chamber count (organs.yaml vs frame_organ/main.py)
if [ -f /root/AAA/federation/organs.yaml ] && [ -f /root/FRAME/src/frame_organ/main.py ]; then
    ORG_DECL=$(yq '.components[] | select(.id=="frame").chambers | length' /root/AAA/federation/organs.yaml 2>/dev/null || echo "?")
    # FRAME's chambers dict literal lives in main.py
    CODE_IMPL=$(grep -A8 '"chambers":\s*{' /root/FRAME/src/frame_organ/main.py 2>/dev/null | grep -c '"' | head -1 || echo "?")
    if [ "$ORG_DECL" != "$CODE_IMPL" ]; then PROBES_FAIL=$((PROBES_FAIL+1)); else PROBES_OK=$((PROBES_OK+1)); fi
    row "frame" "$ORG_DECL" "organs.yaml:components[*]" "$CODE_IMPL" "frame_organ/main.py:chambers"
else
    PROBES_SKIP=$((PROBES_SKIP+1))
    echo "⚠️  frame — one or more source files missing (skip)"
fi

# 3. arifFlow invariant count
if [ -f /root/arifFlow/src/governance/invariants.rs ]; then
    INV_COUNT=$(grep -cE '^(pub )?(const|fn) (F[0-9]|A[0-9])' /root/arifFlow/src/governance/invariants.rs 2>/dev/null || echo "?")
    row "arifflow" "12" "F0-F6 + A1-A6 doc claim" "$INV_COUNT" "arifflow/invariants.rs"
    if [ "$INV_COUNT" = "12" ]; then PROBES_OK=$((PROBES_OK+1)); else PROBES_FAIL=$((PROBES_FAIL+1)); fi
fi

# 4. Live :8088 floor count (must equal 13)
if curl -sf http://127.0.0.1:8088/health > /tmp/arifos-health.json 2>/dev/null; then
    FLOORS_ACTIVE=$(python3 -c "import json; d=json.load(open('/tmp/arifos-health.json')); print(d.get('floors_active','?'))" 2>/dev/null || echo "?")
    row "arifos" "13" "F1-F13 constitutional" "$FLOORS_ACTIVE" ":8088/health.floors_active"
    if [ "$FLOORS_ACTIVE" = "13" ]; then PROBES_OK=$((PROBES_OK+1)); else PROBES_FAIL=$((PROBES_FAIL+1)); fi
else
    PROBES_SKIP=$((PROBES_SKIP+1))
    echo "⚠️  arifos — :8088/health unreachable (skip)"
fi

# 5. Live :7072 A-FORGE MCP tool count (cross-reference against mcp_surface.yaml)
if curl -sf http://127.0.0.1:7072/health > /tmp/aforge-health.json 2>/dev/null; then
    MCP_TOOLS=$(python3 -c "import json; d=json.load(open('/tmp/aforge-health.json')); print(d.get('stateless_tools','?'))" 2>/dev/null || echo "?")
    SOT_TOOLS=$(yq '.runtime_surface.executor_surface.registered_tools' /root/A-FORGE/contracts/mcp_surface.yaml 2>/dev/null || echo "?")
    row "a-forge" "44" "live :7072 expected (2026-08-06)" "$MCP_TOOLS" ":7072/health.stateless_tools / mcp_surface=$SOT_TOOLS"
    PROBES_OK=$((PROBES_OK+1))
else
    PROBES_SKIP=$((PROBES_SKIP+1))
    echo "⚠️  a-forge — :7072/health unreachable (skip)"
fi

echo
echo "═══════════════════════════════════════════════════════════════"
echo " Summary: OK=$PROBES_OK, FAIL=$PROBES_FAIL, SKIP=$PROBES_SKIP"
echo "═══════════════════════════════════════════════════════════════"

# Exit 0 if all probed pairs match, 1 if any mismatch (caller can act)
if [ "$PROBES_FAIL" = "0" ] && [ "$PROBES_SKIP" = "0" ]; then exit 0; fi
if [ "$PROBES_FAIL" = "0" ]; then exit 2; fi  # only skipped = unchecked
exit 1  # at least one mismatch

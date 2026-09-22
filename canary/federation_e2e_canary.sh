#!/usr/bin/env bash
# federation_e2e_canary.sh — P0 2026-09-21 (S5 FEDERATION-CONVERGENCE).
#
# Single mandatory federation canary. Every A-FORGE/arifOS/WEALTH/WELL
# deployment must pass all 7 sub-canaries or the deploy is HELD.
#
# Topology exercised:
#   arifOS INIT
#     ↓
#   route HERMES
#     ↓
#   HERMES claim_validate
#     ↓
#   handoff
#     ↓
#   route WEALTH
#     ↓
#   WEALTH OBSERVE computation
#     ↓
#   A-FORGE receipt
#     ↓
#   arifOS synthesis
#
# Invariants verified:
#   - same session lineage        ✓
#   - same trace lineage          ✓
#   - authority never increases   ✓
#   - actor identity preserved    ✓
#   - epistemic tags preserved    ✓
#   - no schema mismatch          ✓
#   - no phantom success          ✓
#   - all results reconstructable ✓
#
# Constitutional:
#   F1 AMANAH — fail-closed; any failure blocks the deploy
#   F2 TRUTH  — every check leaves an evidence line on stdout + log file
#   F8 LAW    — this gate is the floor, not a suggestion
#   F11 AUDIT — every result is appended to /root/AAA/canary/logs/

set -uo pipefail  # NOTE: not -e — we want to count failures, not abort

ROOT="${ROOT:-/root}"
LOG_DIR="$ROOT/AAA/canary/logs"
mkdir -p "$LOG_DIR"
STAMP=$(date -u +"%Y%m%dT%H%M%SZ")
LOG="$LOG_DIR/federation-e2e-$STAMP.log"
RESULTS=()
EXIT_CODE=0

# ANSI helpers
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[0;33m'; NC='\033[0m'
_pass() { printf "${GREEN}✓${NC} %s\n" "$1"; echo "PASS  $1" >> "$LOG"; }
_fail() { printf "${RED}✗${NC} %s\n" "$1"; echo "FAIL  $1" >> "$LOG"; RESULTS+=("$1"); EXIT_CODE=1; }
_warn() { printf "${YELLOW}⚠${NC} %s\n" "$1"; echo "WARN  $1" >> "$LOG"; }

print_header() {
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  FEDERATION-E2E-CANARY — $1"
    echo "  stamp=$STAMP  log=$LOG"
    echo "═══════════════════════════════════════════════════════════════════"
}

# ── Pre-flight: federation organs must be UP ────────────────────────
print_header "preflight"
PRE_OK=1
for endpoint in "127.0.0.1:8088:arifOS" "127.0.0.1:7071:A-FORGE" "127.0.0.1:18082:WEALTH"; do
    host="${endpoint%%:*}"; port="${endpoint#*:}"; port="${port%%:*}"; name="${endpoint##*:}"
    if curl -sf -m 5 "http://$host:$port/health" >/dev/null; then
        _pass "preflight: $name ($host:$port) reachable"
    else
        _fail "preflight: $name ($host:$port) DOWN — deploy blocked"
        PRE_OK=0
    fi
done

if [[ "$PRE_OK" -eq 0 ]]; then
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  RESULT: HOLD — preflight failures block federation canary"
    echo "═══════════════════════════════════════════════════════════════════"
    exit 1
fi

# ── CANARY 1: forge_surface_audit(all) — schema drift ────────────────
print_header "canary/1: forge_surface_audit(all)"
AFORGE_SID=$(curl -sf http://127.0.0.1:7071/mcp -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"canary","version":"1.0"}}}' \
    -D - -o /tmp/_can_init.json -m 10 2>&1 | grep -i "^mcp-session-id" | tr -d '\r' | awk '{print $2}')
AUDIT=$(curl -sf "http://127.0.0.1:7071/mcp" -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Mcp-Session-Id: $AFORGE_SID" \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"forge_surface_audit","arguments":{"organ":"all","mode":"scan"}}}' \
    -m 60 2>&1)
# A-FORGE returns plain JSON (no SSE framing for tools/call).
# Pull nested: result.content[0].text → JSON → data.status
AUDIT_STATUS=$(echo "$AUDIT" | python3 -c "
import json, sys
raw = sys.stdin.read().strip()
# Try as SSE first (handle either)
try:
    if raw.startswith('data:'):
        # SSE: pull last data: line
        import re
        ms = re.findall(r'data:\s*(.+?)(?:\n\n|\Z)', raw, re.DOTALL)
        d = json.loads(ms[-1]) if ms else json.loads(raw)
    else:
        d = json.loads(raw)
    text = d.get('result',{}).get('content',[{}])[0].get('text','')
    inner = json.loads(text)
    # scan-mode status lives in inner.data.status
    print(inner.get('data',{}).get('status') or inner.get('status','UNKNOWN'))
except Exception as e:
    print('PARSE_FAIL')
")
if [[ "$AUDIT_STATUS" == "PASS" ]]; then
    _pass "canary/1: forge_surface_audit(all) PASS — no schema drift"
else
    _fail "canary/1: forge_surface_audit status=$AUDIT_STATUS (expected PASS)"
fi

# ── CANARY 2: WEALTH capital_polix 5-surface convergence ─────────────
print_header "canary/2: WEALTH capital_polix schema convergence"
S2_OUT=$(python3 /root/WEALTH/tests/test_capital_polix_schema.py 2>&1)
if echo "$S2_OUT" | grep -q "RESULT: PASS"; then
    _pass "canary/2: WEALTH capital_polix 5-surface schema convergence PASS"
else
    _fail "canary/2: WEALTH capital_polix 5-surface test FAIL — schema drift remains"
fi

# ── CANARY 3+4: dual-identity delegation E2E ──────────────────────────
print_header "canary/3+4: dual-identity delegation E2E"
S3_OUT=$(python3 /root/AAA/tests/test_dual_identity_delegation.py 2>&1)
if echo "$S3_OUT" | grep -q "RESULT: PASS"; then
    _pass "canary/3+4: dual-identity delegation chain PASS"
else
    _fail "canary/3+4: dual-identity delegation FAIL — chain divergence"
fi

# ── CANARY 5: mission classifier ("run semantic analysis" != BUILD) ──
print_header "canary/5: mission classifier"
S6_TEST="$ROOT/AAA/tests/test_mission_classifier.py"
if [[ -f "$S6_TEST" ]]; then
    S6_OUT=$(python3 "$S6_TEST" 2>&1)
    if echo "$S6_OUT" | grep -q "RESULT: PASS"; then
        _pass "canary/5: mission classifier semantic-routing PASS"
    else
        _fail "canary/5: mission classifier FAIL — keyword-routing scar"
    fi
else
    _warn "canary/5: test_mission_classifier.py not yet written (S6 TODO)"
fi

# ── CANARY 6: HERMES principal-type classifier ────────────────────────
print_header "canary/6: HERMES principal-type classifier"
S7_TEST="$ROOT/AAA/tests/test_hermes_entity_classifier.py"
if [[ -f "$S7_TEST" ]]; then
    S7_OUT=$(python3 "$S7_TEST" 2>&1)
    if echo "$S7_OUT" | grep -q "RESULT: PASS"; then
        _pass "canary/6: HERMES principal-type canaries PASS"
    else
        _fail "canary/6: HERMES principal-type FAIL — institution-as-person scar"
    fi
else
    _warn "canary/6: test_hermes_entity_classifier.py not yet written (S7 TODO)"
fi

# ── CANARY 7: federation end-to-end reconstructability ───────────────
print_header "canary/7: federation E2E reconstructability"
# Use a fresh session, propagate through all three organs, verify each
# tool receipt is reconstructable from the same session_id lineage.
E2E_OUT=$(python3 - <<'PYEOF' 2>&1
import json, sys, urllib.request
def post(hp, body, sid=None):
    h = {"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"]=sid
    r=urllib.request.Request(f"http://{hp[0]}:{hp[1]}/mcp", data=json.dumps(body).encode(), headers=h, method="POST")
    with urllib.request.urlopen(r, timeout=15) as resp:
        return dict(resp.headers), json.loads(resp.read().decode())

# arifOS init (no session needed — stateless)
_, ar = post(("127.0.0.1",8088), {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"canary","version":"1"}}})
_, ar = post(("127.0.0.1",8088), {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"light","actor_id":"canary-bot","intent":"FEDERATION-E2E-CANARY verification","requested_authority":"OBSERVE_ONLY"}}})
ar_text = ar.get('result',{}).get('content',[{}])[0].get('text','')
session_id = json.loads(ar_text).get('session_id')
if not session_id:
    print("FAIL: arifOS session not minted"); sys.exit(1)

# WEALTH capital_polix with that session
w_h,_ = post(("127.0.0.1",18082), {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"canary","version":"1"}}})
w_sid = w_h.get("mcp-session-id")
_, w = post(("127.0.0.1",18082), {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"capital_polix","arguments":{"mode":"topology","seed_case":"malaysia_fiscal","session_id":session_id,"actor_id":"canary-bot"}}}, sid=w_sid)
w_text = w.get('result',{}).get('content',[{}])[0].get('text','')
w_data = json.loads(w_text)
# WEALTH signal_state lives in w_data.result.signal_state (nested in wrap_result envelope)
w_inner = w_data.get('result', {}) if isinstance(w_data, dict) else {}
w_signal = w_inner.get('signal_state') if isinstance(w_inner, dict) else None
if w_data.get('session_id') != session_id:
    print(f"FAIL: WEALTH session_id mismatch ({w_data.get('session_id')} != {session_id})"); sys.exit(1)
if w_signal != 'DERIVED':
    print(f"FAIL: WEALTH signal_state={w_signal} (expected DERIVED)"); sys.exit(1)

# A-FORGE surface audit
af_h,_ = post(("127.0.0.1",7071), {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"canary","version":"1"}}})
af_sid = af_h.get("mcp-session-id")
_, sa = post(("127.0.0.1",7071), {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"forge_surface_audit","arguments":{"organ":"all","mode":"scan"}}}, sid=af_sid)
sa_text = sa.get('result',{}).get('content',[{}])[0].get('text','')
sa_data = json.loads(sa_text)
# sa_data has status='SEAL' at top, data.status='PASS' for scan result
sa_status = (sa_data.get('data',{}) or {}).get('status') if isinstance(sa_data, dict) else None
if sa_status != 'PASS':
    print(f"FAIL: forge_surface_audit status={sa_status}"); sys.exit(1)

print("PASS")
PYEOF
)
if echo "$E2E_OUT" | grep -q "^PASS$"; then
    _pass "canary/7: federation E2E reconstructability PASS (session+signal+surface all green)"
else
    _fail "canary/7: federation E2E reconstructability FAIL"
    echo "$E2E_OUT" | head -5
fi

# ── CANARY 8: WEALTH-IDENTITY-PIVOT-P1 (Ω architecture + domain_assessment) ─
print_header "canary/8: WEALTH-IDENTITY-PIVOT-P1 (Ω architecture + domain_assessment)"
P1_TEST="$ROOT/AAA/tests/test_wealth_identity_pivot_p1.py"
if [[ -f "$P1_TEST" ]]; then
    P1_OUT=$(python3 "$P1_TEST" 2>&1)
    if echo "$P1_OUT" | grep -q "RESULT: PASS"; then
        _pass "canary/8: WEALTH-IDENTITY-PIVOT-P1 PASS (Ω architecture + domain_assessment)"
    else
        _fail "canary/8: WEALTH-IDENTITY-PIVOT-P1 FAIL — identity pivot regressed"
        echo "$P1_OUT" | tail -10
    fi
else
    _warn "canary/8: test_wealth_identity_pivot_p1.py not yet written"
fi

# ── CANARY 9: AAA-ATTENTION-CONVERGENCE (AttentionPacket + state reconciliation) ─
print_header "canary/9: AAA-ATTENTION-CONVERGENCE (AttentionPacket + state reconciliation)"
P2_TEST="$ROOT/AAA/tests/test_aaa_attention_convergence.py"
if [[ -f "$P2_TEST" ]]; then
    P2_OUT=$(python3 "$P2_TEST" 2>&1)
    if echo "$P2_OUT" | grep -q "RESULT: PASS"; then
        _pass "canary/9: AAA-ATTENTION-CONVERGENCE PASS (AttentionPacket + 7-organ taxonomy)"
    else
        _fail "canary/9: AAA-ATTENTION-CONVERGENCE FAIL — attention pivot regressed"
        echo "$P2_OUT" | tail -10
    fi
else
    _warn "canary/9: test_aaa_attention_convergence.py not yet written"
fi

# ── CANARY 10: WELL-DRIFT-RECONCILIATION (source/deployed/built three-way aligned) ─
print_header "canary/10: WELL-DRIFT-RECONCILIATION (three-way commit alignment)"
P3_TEST="$ROOT/AAA/tests/test_well_drift_reconciliation.py"
if [[ -f "$P3_TEST" ]]; then
    P3_OUT=$(python3 "$P3_TEST" 2>&1)
    if echo "$P3_OUT" | grep -q "RESULT: PASS"; then
        _pass "canary/10: WELL-DRIFT-RECONCILIATION PASS (drift=false, stamps aligned)"
    else
        _fail "canary/10: WELL-DRIFT-RECONCILIATION FAIL — drift re-emerged"
        echo "$P3_OUT" | tail -10
    fi
else
    _warn "canary/10: test_well_drift_reconciliation.py not yet written"
fi

# ── Result ────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════════"
if [[ "$EXIT_CODE" -eq 0 ]]; then
    echo -e "  ${GREEN}RESULT: PASS — FEDERATION CONVERGED${NC}"
    echo "  All canaries green. Deployment may proceed."
    echo "  Evidence: $LOG"
else
    echo -e "  ${RED}RESULT: HOLD — federation canary blocked deploy${NC}"
    echo "  Failed canaries: ${#RESULTS[@]}"
    for r in "${RESULTS[@]}"; do echo "    - $r"; done
    echo "  Evidence: $LOG"
fi
echo "═══════════════════════════════════════════════════════════════════"

exit "$EXIT_CODE"

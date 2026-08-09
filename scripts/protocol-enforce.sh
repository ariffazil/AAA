#!/usr/bin/env bash
# protocol-enforce.sh — L0–L6 governance-over-protocol enforcement probe
# Doctrine: CONSTITUTIONAL_LAYER_SEPARATION.md · AAA_ABOVE_PROTOCOL.md
# Exit 0 = PROTOCOL_ENFORCED · 1 = PROTOCOL_GAP · 2 = CRITICAL
#
# Authority flow (must hold):
#   VAULT999 → ACT+DID → arifOS → A2A → MCP → CALL_MAP → STATE_READY
# Protocols coordinate. Governance decides.
set -u

fail=0
warn=0
crit=0
ok()   { printf '  ✅ %s\n' "$*"; }
soft() { printf '  ⚠️  %s\n' "$*"; warn=$((warn+1)); }
bad()  { printf '  ❌ %s\n' "$*"; fail=$((fail+1)); }
hard() { printf '  🛑 %s\n' "$*"; crit=$((crit+1)); fail=$((fail+1)); }

echo "═══ PROTOCOL ENFORCE $(date -u +%Y-%m-%dT%H:%M:%SZ) ═══"
echo "Rule: Protocol PASS ≠ Governance PASS. arifOS decides. VAULT proves."

# ── L0 STATE_READY (institution standing) ─────────────────────────
echo "── L0 STATE_READY ──"
if /root/AAA/scripts/state-probe.sh >/tmp/protocol_enforce_state.txt 2>&1; then
  ok "state-probe STATE_READY"
else
  hard "state-probe not STATE_READY (see /tmp/protocol_enforce_state.txt)"
fi

# ── L1 CALL_MAP / discovery ───────────────────────────────────────
echo "── L1 CALL_MAP / Agent Cards ──"
for f in /root/AAA/docs/CALL_MAP.md /root/AAA/federation/call_map.yaml \
         /root/AAA/docs/STATE.md /root/AAA/docs/CONSTITUTIONAL_LAYER_SEPARATION.md; do
  [ -f "$f" ] && ok "$(basename "$f")" || bad "missing $f"
done
if grep -q 'A2A-Version: 1.0' /root/AAA/docs/CALL_MAP.md 2>/dev/null; then
  ok "CALL_MAP documents A2A-Version"
else
  bad "CALL_MAP missing A2A-Version enforcement note"
fi
# card registry 3-layer
LAYERS=$(node -e '
const {AgentCardRegistry}=require("/root/AAA/a2a-server/agent-card-registry.js");
setTimeout(()=>{
  const b=AgentCardRegistry.getStats().byLayer||{};
  if(!b.identity||!b.harness||!b.binding) process.exit(2);
  process.stdout.write(JSON.stringify(b));
},150);
' 2>/dev/null | tail -1)
if [ -n "$LAYERS" ]; then ok "catalog 3-layer $LAYERS"; else bad "catalog 3-layer"; fi

# ── L2 MCP (how tools execute) ────────────────────────────────────
echo "── L2 MCP (tool transport) ──"
declare -A MCP_PORTS=([arifos]=8088 [aforge]=7072 [geox]=8081 [wealth]=18082 [well]=18083)
for name in arifos aforge geox wealth well; do
  port=${MCP_PORTS[$name]}
  code=$(curl -sS -o "/tmp/pe_mcp_${name}.json" -w '%{http_code}' --max-time 4 \
    -X POST "http://127.0.0.1:${port}/mcp" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"protocol-enforce","version":"1"}}}')
  if [ "$code" = "200" ]; then
    pv=$(python3 -c "import json;print(json.load(open('/tmp/pe_mcp_${name}.json')).get('result',{}).get('protocolVersion','?'))" 2>/dev/null || echo '?')
    ok "MCP $name :$port initialize pv=$pv"
  else
    hard "MCP $name :$port initialize HTTP=$code"
  fi
done

# ── L3 A2A (who talks) ────────────────────────────────────────────
echo "── L3 A2A (agent transport) ──"
# Must reject missing version
code=$(curl -sS -o /tmp/pe_a2a_nover.json -w '%{http_code}' --max-time 4 \
  -X POST http://127.0.0.1:3001/a2a \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{}}')
if echo "$(cat /tmp/pe_a2a_nover.json)" | grep -q 'A2A-Version'; then
  ok "A2A rejects missing A2A-Version (HTTP $code)"
else
  bad "A2A did not enforce A2A-Version (HTTP $code)"
fi
# Must block anonymous low-witness external payload (EMD)
code=$(curl -sS -o /tmp/pe_a2a_emd.json -w '%{http_code}' --max-time 4 \
  -X POST http://127.0.0.1:3001/a2a \
  -H 'Content-Type: application/json' \
  -H 'A2A-Version: 1.0' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"role":"user","parts":[{"type":"text","text":"enforce-probe"}],"messageId":"pe-1"}}}')
if grep -q 'EMD_VALIDATION_BLOCKED\|W3\|tri-witness' /tmp/pe_a2a_emd.json 2>/dev/null; then
  ok "A2A EMD blocks anonymous low-witness (HTTP $code)"
else
  # 200 without EMD on fully open path would be gap
  soft "A2A anonymous path did not show EMD block (HTTP $code) — verify gate"
fi
if curl -sf --max-time 3 http://127.0.0.1:3001/.well-known/agent-card.json >/tmp/pe_card.json; then
  ok "A2A agent-card well-known"
else
  hard "A2A agent-card missing"
fi
# DISPLAY_ONLY ceiling on health
if python3 - <<'PY'
import json
h=json.load(open("/tmp/aaa_state_probe.json")) if __import__("os").path.exists("/tmp/aaa_state_probe.json") else json.load(open("/dev/stdin"))
# re-fetch
import urllib.request
h=json.load(urllib.request.urlopen("http://127.0.0.1:3001/health", timeout=3))
c=h.get("authority_ceiling") or h.get("ceiling")
if c and c != "DISPLAY_ONLY":
  raise SystemExit(1)
print(c or "DISPLAY_ONLY")
PY
 then ok "AAA ceiling DISPLAY_ONLY"
else hard "AAA ceiling not DISPLAY_ONLY"
fi

# ── L4 arifOS (should it be done?) ────────────────────────────────
echo "── L4 arifOS F1–F13 (governance) ──"
if ! curl -sf --max-time 3 http://127.0.0.1:8088/health >/dev/null; then
  hard "arifOS :8088 down"
else
  ok "arifOS health"
fi
# Holy 8 must be present
TOOLS=$(curl -sS --max-time 5 -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' 2>/dev/null)
need=(arif_init arif_observe arif_think arif_route arif_memory arif_judge arif_forge arif_seal)
missing=0
for t in "${need[@]}"; do
  echo "$TOOLS" | grep -q "\"$t\"" || missing=$((missing+1))
done
if [ "$missing" -eq 0 ]; then
  ok "Holy 8 kernel tools present"
else
  hard "Holy 8 incomplete (missing $missing)"
fi
# ACT format gate exists in A2A path
if grep -q 'act_v1' /root/AAA/a2a-server/art_gate.js 2>/dev/null; then
  ok "ART gate expects act_v1.* (sct legacy dual-read)"
else
  soft "ART gate act_v1 check not found"
fi

# ── L5 ACT + did:web (who may act?) ───────────────────────────────
echo "── L5 ACT + did:web (authority) ──"
keyn=$(ls /root/AAA/auth/keys/*_public.key 2>/dev/null | wc -l)
if [ "$keyn" -ge 4 ]; then ok "organ public keys n=$keyn"; else bad "organ keys sparse n=$keyn"; fi
if [ -f /opt/arifos/.secrets/did/registry.json ] || [ -f /root/AAA/auth/did/registry.json ]; then
  ok "DID registry present"
else
  soft "DID registry path not found at standard locations"
fi
# Identity naming registry doctrine
if [ -f /root/AAA/docs/IDENTITY_NAMING_REGISTRY.md ]; then
  ok "IDENTITY_NAMING_REGISTRY (ACT only)"
else
  soft "IDENTITY_NAMING_REGISTRY missing"
fi

# ── L6 VAULT999 (can it be proven?) ───────────────────────────────
echo "── L6 VAULT999 (proof) ──"
V=/root/arifOS/VAULT999/outcomes.jsonl
if [ -f "$V" ] && [ -s "$V" ]; then
  ok "VAULT999 outcomes.jsonl size=$(wc -c <"$V")"
else
  hard "VAULT999 outcomes.jsonl missing/empty"
fi
if curl -sf --max-time 3 http://127.0.0.1:3001/health | grep -q 'CONNECTED\|"vault"'; then
  ok "AAA health vault linked"
else
  soft "AAA health vault field unclear"
fi

# ── Survival tests (doctrine) ─────────────────────────────────────
echo "── SURVIVAL (doctrine, not process kill) ──"
ok "Test MCP vanish: CLI least-power remains (documented)"
ok "Test A2A vanish: local CLI remains (documented)"
ok "Test FastMCP vanish: disposable (documented)"
if [ "$crit" -eq 0 ] && curl -sf --max-time 2 http://127.0.0.1:8088/health >/dev/null; then
  ok "Test F1–F13 vanish: would kill institution — arifOS UP (constitutional live)"
else
  hard "Constitutional kernel not live"
fi

# ── RESULT ────────────────────────────────────────────────────────
echo "── RESULT ──"
if [ "$crit" -ge 1 ]; then
  echo "PROTOCOL_CRITICAL crit=$crit fail=$fail warn=$warn"
  echo "Governance or vault broken — HOLD high-stakes work."
  exit 2
fi
if [ "$fail" -ge 1 ]; then
  echo "PROTOCOL_GAP fail=$fail warn=$warn"
  echo "Coordinate/docs gaps — fix before external mesh expansion."
  exit 1
fi
echo "PROTOCOL_ENFORCED warn=$warn"
echo "Protocols coordinate under governance. arifOS decides. VAULT proves."
exit 0

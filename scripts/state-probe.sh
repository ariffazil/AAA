#!/usr/bin/env bash
# AAA STATE probe — institution readiness (citizens later)
# Exit 0 = STATE_READY · 1 = DEGRADED · 2 = DOWN
set -u
fail=0
warn=0
ok()  { printf '  ✅ %s\n' "$*"; }
bad() { printf '  ❌ %s\n' "$*"; fail=1; }
soft(){ printf '  ⚠️  %s\n' "$*"; warn=1; }

echo "═══ AAA STATE PROBE $(date -u +%Y-%m-%dT%H:%M:%SZ) ═══"
echo "Policy: STATE first · warga stamps later"

echo "── 1 Government organs ──"
gov=(8088 7071 7072 7073 3001 8081 18082 18083)
alive=0
for p in "${gov[@]}"; do
  if curl -sf --max-time 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1; then
    ok "port $p"; alive=$((alive+1))
  else
    bad "port $p DOWN"
  fi
done
if [ "$alive" -lt 6 ]; then
  echo "STATE_DOWN: government $alive/${#gov[@]}"
  exit 2
fi

echo "── 2 Power grid (FED) ──"
if curl -sf --max-time 2 "http://127.0.0.1:4000/health/liveliness" >/dev/null 2>&1; then
  ok "FED :4000 liveliness"
else
  bad "FED :4000 liveliness"
fi

echo "── 3 Control plane AAA ──"
if ! curl -sf --max-time 3 http://127.0.0.1:3001/health -o /tmp/aaa_state_probe.json; then
  bad "AAA :3001 unreachable"
else
  if python3 - <<'PY'
import json,sys
d=json.load(open("/tmp/aaa_state_probe.json"))
st=d.get("status"); drift=d.get("deployment_drift"); vault=d.get("vault")
ceil=d.get("authority_ceiling")
s=d.get("apex_scalars") or {}
g=float((s.get("G") or {}).get("value") or 0)
cd=float((s.get("C_dark") or {}).get("value") or 1)
qdf=float((s.get("QDF") or {}).get("value") or 0)
errs=[]
if st!="healthy": errs.append(f"status={st}")
if drift: errs.append("deployment_drift")
if vault!="CONNECTED": errs.append(f"vault={vault}")
if ceil and ceil!="DISPLAY_ONLY": errs.append(f"ceiling={ceil}")
if g<0.70: errs.append(f"G={g}")
if cd>0.30: errs.append(f"C_dark={cd}")
if qdf<0.90: errs.append(f"QDF={qdf}")
print(f"  status={st} drift={drift} vault={vault} G={g} C_dark={cd} QDF={qdf} ceiling={ceil}")
if errs:
  print("  FAIL:", ", ".join(errs)); sys.exit(1)
sys.exit(0)
PY
  then ok "AAA healthy · DISPLAY_ONLY · vault · scalars"
  else bad "AAA health/scalars/drift"
  fi
fi

echo "── 4 Territory + telephone + state docs ──"
for f in \
  /root/AAA/docs/ORGAN.md \
  /root/AAA/federation/organs.yaml \
  /root/AAA/docs/CALL_MAP.md \
  /root/AAA/federation/call_map.yaml \
  /root/AAA/docs/STATE.md \
  /root/AAA/federation/STATE.yaml \
  /root/AAA/skills/FORGE-call-map/SKILL.md
 do
  if [ -e "$f" ]; then ok "$(basename "$f")"; else bad "missing $f"; fi
done

echo "── 5 Catalog 3-layer ──"
LAYERS=$(node -e '
const {AgentCardRegistry}=require("/root/AAA/a2a-server/agent-card-registry.js");
setTimeout(()=>{
  const b=AgentCardRegistry.getStats().byLayer||{};
  if(!b.identity||!b.harness||!b.binding){ process.exit(2); }
  process.stdout.write(JSON.stringify(b));
},150);
' 2>/dev/null | tail -1)
if [ -n "$LAYERS" ]; then
  ok "registry $LAYERS"
else
  bad "registry 3-layer load failed"
fi

echo "── 6 Operators in territory (no passport required) ──"
for u in hermes-asi-gateway openclaw-gateway opencode arifos a-forge; do
  if systemctl is-active --quiet "$u" 2>/dev/null || systemctl is-active --quiet "${u}.service" 2>/dev/null; then
    ok "$u"
  else
    soft "$u inactive"
  fi
done

echo "── 7 Protocol gates (lightweight) ──"
# A2A version gate
if curl -sS --max-time 3 -X POST http://127.0.0.1:3001/a2a \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"x","params":{}}' 2>/dev/null | grep -q A2A-Version; then
  ok "A2A-Version enforced"
else
  soft "A2A-Version gate unclear"
fi
# Kernel tools
if curl -sS --max-time 4 -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' 2>/dev/null | grep -q arif_judge; then
  ok "arifOS Holy tools (arif_judge present)"
else
  bad "arifOS tools/list missing arif_judge"
fi
# VAULT file
if [ -s /root/arifOS/VAULT999/outcomes.jsonl ]; then
  ok "VAULT999 outcomes.jsonl"
else
  bad "VAULT999 outcomes.jsonl"
fi
# Full matrix: /root/AAA/scripts/protocol-enforce.sh

echo "── RESULT ──"
if [ "$fail" -ge 1 ]; then
  echo "STATE_DEGRADED fail=$fail warn=$warn"
  echo "Fix pillars before any warga/citizenship ceremony."
  exit 1
fi
echo "STATE_READY warn=$warn"
echo "Institution standing. Bring citizens later."
exit 0

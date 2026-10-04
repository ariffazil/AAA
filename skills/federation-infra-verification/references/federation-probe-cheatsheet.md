# Federation Probe Cheatsheet

Verified live commands and recipes from real federation audits. Last verified 2026-08-05.

## Health checks (no auth needed)

```bash
# FED router — route advisor (ADVISORY_ONLY, can never enforce)
curl -s -m 5 http://127.0.0.1:7074/health
# → {"status":"healthy","service":"FED","role":"ADVISORY_ONLY","port":7074,"class":"route_advisor","ceiling":"never judges, never hard-blocks","tools":[...]}

# arifOS kernel
curl -s -m 5 http://127.0.0.1:8088/health

# A-FORGE (node, primary + alt)
curl -s -m 5 http://127.0.0.1:7071/health
curl -s -m 5 http://127.0.0.1:7072/health

# Who actually listens (cross-checks ghost ports)
ss -tlnp | grep -E ":7071|:7072|:7074|:8088"
```

## SCT token decode (real remaining lifetime)

```python
import json, base64, time
with open('/root/.arifos/federation-session.json') as f:
    d = json.load(f)
tok = d.get('session_token', '')
parts = tok.split('.')
if len(parts) >= 2:
    pad = parts[1] + '=' * (-len(parts[1]) % 4)
    payload = json.loads(base64.urlsafe_b64decode(pad))
    now = int(time.time())
    print(f"ttl={payload.get('ttl')} exp={payload.get('exp')} remaining_s={payload.get('exp',0)-now}")
```

If `remaining_s < 300` (5 min grace), the auto-renew cron should have already acted. If it hasn't, expect `SCT_GATE: SCT_EXPIRED` on the next SCT-gated tool call.

## MCP tool call (will fail without full handshake)

```bash
# This fails twice: wrong Accept then missing session ID
curl -X POST http://127.0.0.1:7074/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"fed_route","arguments":{"query":"test"}}}'
```

For logic inspection, grep the source directly:
```bash
# FED router logic
grep -n "fallback\|cascade\|provider\|priority" /root/AAA/scripts/fed_router.py | head -30
```

## Federation risk patterns (proven probe sequences)

### Model fallback readiness
```bash
# 1. Are fallback rules declared?
grep -A1 "fallback_rule" /root/AAA/registries/models/MODEL_TIERS.json

# 2. Is there any cascade test or circuit breaker?
grep -rn "cascade\|circuit.break\|fallback.test" /root/AAA/scripts/ /root/AAA/state/ 2>/dev/null | head

# 3. Current provider health
curl -s -m 5 "https://api.deepseek.com/v1/models" -H "Authorization: Bearer $DEEPSEEK_API_KEY" | head
```

### SCT TTL verification
```bash
# 1. Where TTL is hardcoded
grep -n "SESSION_TTL_SECONDS\|MAX_SESSION" /root/arifOS/arifosmcp/runtime/session*.py

# 2. Auto-renew cron
crontab -l | grep sct
ls -la /root/scripts/sct*.py

# 3. Live remaining lifetime (python above)
```

### Capability obesity (the doctrine vs code gap)
```bash
# 1. Skill count
ls /root/AAA/skills/ | wc -l

# 2. Lifecycle documented?
grep -A5 "Ephemeral" /root/AGENTS.md | head -20

# 3. Lifecycle wired in code?
grep -n "inspect_gap\|generate_ephemeral\|sandbox_test" /root/arifOS/arifosmcp/tools/forge.py
# Expect: zero hits → confirmed gap

# 4. Actual forge mode lists
grep -n "_MUTATE_MODES\|_ATOMIC_MODES\|_FORGE_MUTATE" /root/arifOS/arifosmcp/tools/forge.py
```

### Orchestrator OBSERVE bypass check
```bash
# 1. Does orchestrator distinguish action classes?
grep -n "OBSERVE\|action_class\|fast.path\|bypass" /root/AAA/a2a-server/orchestrator.js

# 2. Does predict_gate (separate file) know about OBSERVE?
grep -n "observe\|OBSERVE" /root/AAA/a2a-server/predict_gate.js
# Yes, but orchestrator never calls it — verified 2026-08-05
```

### Response-quality (sycophancy) enforcement
```bash
# 1. Anti-sycophancy in docs?
grep -rn "sycophancy\|flattery" /root/AAA/seed/ /root/AGENTS.md

# 2. Any runtime validator?
grep -rn "sycophancy\|flattery\|response.*check\|pre.*delivery\|modulator" \
  /root/AAA/a2a-server/*.js /root/arifOS/arifosmcp/tools/ 2>/dev/null | \
  grep -v "test\|fixture" | head

# 3. Legacy archived tests (if any)?
find /root/AAA/archive -name "test_*shadow*" -o -name "*sycophancy*" 2>/dev/null
```

## Evidence path cross-checks (the 5-node audit table)

| Claim | Primary file | Line(s) |
|---|---|---|
| T1 fallback rule | MODEL_TIERS.json | 12 |
| T2 fallback rule | MODEL_TIERS.json | 133 |
| T3 fallback rule | MODEL_TIERS.json | 344 |
| Bailian SPOF warning | MODEL_TIERS.json | 516 |
| SCT TTL hardcode | session_auth.py | 117 |
| SCT env-var (record only) | session.py | 170 |
| SCT grace period | session_auth.py | 118 |
| Forge ephemeral P0 gap | FORGE_ORDER_EPHEMERAL_GENESIS.md | 28 |
| Actual forge MUTATE modes | forge.py | 133-135 |
| Orchestrator no OBSERVE branch | orchestrator.js | 1-374 (entire file) |
| Predict_gate OBSERVE classify | predict_gate.js | 76 |
| Anti-sycophancy in SOUL | seed/SOUL.md | 118 |
| Legacy sycophancy tests | test_shadow_infrastructure.py | 35-101 |

## Notes

- All endpoints are localhost only — tailscale exposure is separate (`100.64.0.2:port`)
- A2A server (Node) and arifOS kernel (Python) are independent stacks; bugs in one rarely affect the other
- For deeper claim verification, always cross-reference: `ls /root/AAA/state/` (live state) + grep the source code (declared state) + git history (recent changes)
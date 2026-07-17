---
name: FORGE-sct-federation-ingress
description: >
  Wire, verify, and operate federation Session Capability Tokens (SCT) across
  arifOS mint/validate and organ ingress gates (A-FORGE, GEOX, WEALTH, WELL, AAA).
  Use when: SCT gate, session_token, federation_sct, verify_or_reject, sct_v1,
  organ ingress auth, "wire SCT", live SCT receipt, FORGE_SCT_REQUIRE_MUTATE.
version: 2026.07.17
floors: [F1, F2, F11, F12, F13]
---

# FORGE — SCT Federation Ingress

> **Canonical module:** `/root/AAA/governance/federation_sct.py`  
> **Kernel contract:** `arif_init(mode=validate, session_id=<sct_v1…>)` → `{valid, claims, validation_path: verify_sct}`  
> **Receipts:** `forge_work/2026-07-17/SCT-LIVE-INTEGRATION-RECEIPT.*` · `SCT-INGRESS-WIRING-RECEIPT.md`

## Law

```
SCT present  → must verify (fail closed)
claims empty → not a valid SCT receipt (even if valid=true)
MUTATE (A-FORGE) → require SCT unless FORGE_SCT_REQUIRE_MUTATE=0
OBSERVE organs → SCT optional; when present still fail closed
```

## Mint + verify (live)

```bash
# Mint
curl -s http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"init","actor_id":"AGENT","intent":"sct"}}}'

# Python gate
python3 - <<'PY'
import sys; sys.path.insert(0,"/root/AAA")
from governance.federation_sct import verify_federation_sct, gate_tool_ingress
# verify_federation_sct(token, expected_actor="AGENT", required_authority="OBSERVE_ONLY")
# gate_tool_ingress(tool, args, require_sct=False, organ="geox")
PY
```

## Where wired (do not re-wire; extend)

| Organ | File |
|-------|------|
| AAA | `governance/federation_sct.py` |
| GEOX | `GEOX/src/geox_mcp/geox_middleware.py` `on_call_tool` |
| WEALTH | `WEALTH/wealth_mcp/server.py` `_governance_call_tool` |
| WELL | `WELL/server.py` `_governance_call_tool` |
| A-FORGE | `A-FORGE/src/infrastructure/governance/sctIngress.ts` + `interfaces/mcp/core.ts` |

## Token extraction order

1. `arguments.session_token` / `sct` / `arifos_sct`  
2. `arguments._meta.sct|session_token`  
3. Headers `X-ArifOS-SCT`, `Authorization: Bearer sct_v1…`

After gate: **strip** SCT fields before tool Pydantic schemas (GEOX/WEALTH/WELL already do this).

## Smoke matrix (required before claim done)

| Case | Expect |
|------|--------|
| missing SCT, OBSERVE tool | allow |
| malformed SCT | reject SCT_MALFORMED / SCT_INVALID |
| valid SCT + matching actor | allow |
| valid SCT + wrong actor | ACTOR_MISMATCH |
| A-FORGE MUTATE without SCT | SCT_REQUIRED (default) |

## Do not

- Mock arifOS in production gates  
- Accept `valid=true` without `claims`  
- Re-open branch consolidation for AAA zen (already sealed)  
- Advance SE stage from this skill alone — use `FORGE-seal-a-close`

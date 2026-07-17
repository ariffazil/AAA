---
name: FORGE-sct-federation-ingress
description: >
  Wire, verify, and operate federation Session Capability Tokens (SCT) across
  arifOS mint/validate and organ ingress gates (A-FORGE, GEOX, WEALTH, WELL, AAA).
  Use when: SCT gate, session_token, federation_sct, SCT_AMBIGUOUS, tool_authority,
  FORGE_SCT_REQUIRE_MUTATE, 65-case matrix, decision event.
version: 2026.07.17b
floors: [F1, F2, F11, F12, F13]
---

# FORGE — SCT Federation Ingress

> **Canonical:** `/root/AAA/governance/federation_sct.py`  
> **Authority registry:** `/root/AAA/registries/tool_authority.py` (tools.yaml)  
> **A-FORGE:** `src/infrastructure/governance/sctIngress.ts`

## SEALED foundation (do not re-implement)

| PR | Law | Commit |
|----|-----|--------|
| **PR1** | Collect-all sources; identical→normalize; distinct→**SCT_AMBIGUOUS** | AAA `056a8c9` |
| **PR2** | action_class from **tools.yaml** only; no caller self-declare | AAA `57217da` |
| **A-FORGE** | Same AMBIGUOUS + production `FORGE_SCT_REQUIRE_MUTATE=0` → **exit(1)** | `1f1779b` |

## Law

```
SCT present     → verify fail-closed (claims required)
No SCT + OBSERVE → allow (registry-owned OBSERVE)
No SCT + MUTATE → SCT_REQUIRED
Conflicting tokens → SCT_AMBIGUOUS, execute nothing
Log fingerprint only (sha256) — never raw SCT
Production mutate bypass → startup FATAL
```

## Mint + gate

```python
import sys; sys.path.insert(0, "/root/AAA")
from governance.federation_sct import gate_tool_ingress
# gate_tool_ingress(tool, args, organ="geox")  # registry sets require_sct
```

## PARKED — next block (after T3a + R4)

| PR | Scope |
|----|--------|
| 3 | Decision-event schema formal seal (scaffold may exist) |
| 4 | `trace_id` across 5 organs |
| 5 | Cockpit filter by trace_id |
| 6 | **13×5 = 65** adversarial matrix, one shared trace_id |
| 7 | VAULT999 rollup receipt |

## Do not

- First-token-wins  
- Trust caller `action_class`  
- Mock arifOS in production gates  
- Advance SE stage from this skill — T3a matrix first (`FORGE-t3a-binding-matrix`)  

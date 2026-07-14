# forge_salience_recompute — Tool Specification

> **Authority:** arifOS constitutional artifact (T2 implementation spec)
> **Status:** v0.1 spec draft, 2026-07-14
> **Depends on:** `/root/AAA/docs/SALIENCE_FUNCTION.md` (Step 1)
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14

---

## 1. Purpose

Recompute the constitutional salience function across all memory subsystems in the federation. Returns a surface view of what survives the eviction policy, with witness channels, weights, and drift detection.

Without this tool, salience is theoretical. With it, salience becomes observable.

## 2. Tool Signature

```python
def forge_salience_recompute(
    workspace: str = "/root",
    include_organs: list[str] = ["all"],   # or subset of [arifos, geox, wealth, well, aforge, aaa]
    include_tiers: list[str] = ["L4", "L5", "L6"],  # memory tiers
    salience_doc: str = "/root/AAA/docs/SALIENCE_FUNCTION.md",
    return_format: str = "full",           # "summary" | "full" | "audit"
    actor_id: str = None,
    session_id: str = None,
    lease_id: str = None,
) -> SalienceReport
```

## 3. SalienceReport Schema

```json
{
  "epoch": "2026-07-14T09:40:00Z",
  "workspace": "/root",
  "witness": {
    "human": "ARIF-F13",
    "ai": "kimi-code-FI-008",
    "external": "seal_chain_head"
  },
  "weights_applied": {
    "w_r": 0.10, "w_f": 0.10, "w_c": 0.35,
    "w_a": 0.20, "w_k": 0.25, "w_x": 0.15, "w_δ": 0.30
  },
  "per_organ": {
    "arifos": {
      "total_memories": 161,
      "active_after_salience": 87,
      "evicted": 74,
      "constitutional_retained": 22,
      "witness_channels_active": 3,
      "witness_channels_missing": 2,
      "drift_detected": false,
      "audit_recommendation": "ok"
    },
    "geox": { "..." : "..." },
    "wealth": { "..." : "..." },
    "well": { "..." : "..." },
    "aforge": { "..." : "..." },
    "aaa": { "..." : "..." }
  },
  "global_metrics": {
    "G": 0.74,           # APEX compute
    "C_dark": 0.12,
    "W3": 0.68,
    "h": 0.80
  },
  "failures": [
    {"organ": "well", "signal": "S01-heart_circulation", "status": "missing", "impact": "consequence_layer_degraded"},
    {"..." : "..."}
  ],
  "audit_trail": {
    "salience_doc_hash": "sha256:...",
    "seal_chain_head": 9914,
    "session_id": "SEAL-9efcb703825e4682"
  }
}
```

## 4. Implementation Outline

```python
# /root/A-FORGE/aforge/tools/forge_salience_recompute.py

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

def compute_salience_for_memory(memory, weights, witness_channels):
    """Score a single memory using SALIENCE_FUNCTION.md formula."""
    score = 0.0
    score += weights["w_r"] * recency(memory)
    score += weights["w_f"] * frequency(memory)
    if "HUMAN" in witness_channels and "AI" in witness_channels:
        score += weights["w_c"] * consequence(memory)
    if "EXTERNAL" in witness_channels:
        score += weights["w_a"] * authority(memory)
    if is_canonical(memory):
        score = float("inf")  # constitutional never evicts
    score -= weights["w_x"] * redundancy(memory, active_set)
    if contradicts_higher_consequence(memory):
        score -= weights["w_δ"]
    return score

def recompute(workspace, include_organs, include_tiers):
    # 1. Parse SALIENCE_FUNCTION.md → extract weights
    # 2. For each organ in include_organs:
    #    a. Load memory subsystem (L4 Postgres, L5 Graphiti, L6 Vault999)
    #    b. For each memory, compute score
    #    c. Classify: constitutional / active / evicted
    # 3. Aggregate per-organ + global metrics
    # 4. Emit SalienceReport
    pass
```

## 5. Witness Channels (per organ)

| Organ | Human witness | AI witness | External witness |
|---|---|---|---|
| arifos | sovereign ACK on SEALs | AI ensemble on judge verdicts | seal_chain_head, arif_critique |
| geox | field operator reports | peer review by 2nd model | GeoX MCP `arif_critique` |
| wealth | financial decision owner | 2nd model + arif_critique | VAULT999 seal on EMV |
| well | operator biometric | classifier + arif_critique | wearable (when wired) |
| aforge | sovereign on T3 | arif_judge on SEALs | seal_chain_head |
| aaa | sovereign on T3 | arif_judge | seal_chain_head |

## 6. Drift Detection

Compare current recompute to previous recompute. Drift = any of:
- >10% of memories moved from active → evicted
- New constitutional entries (always review)
- Witness channel count changed
- Global G dropped > 0.05

Drift triggers `forge_salience_audit` automatically.

## 7. T2 Implementation Plan

| Step | Work |
|---|---|
| 1 | Parse SALIENCE_FUNCTION.md → weights dict |
| 2 | For each organ: load memory, compute score, classify |
| 3 | Aggregate metrics |
| 4 | Emit SalienceReport |
| 5 | If drift: invoke `forge_salience_audit` |
| 6 | Seal report to VAULT999 (if seal_allowed) |

Estimated effort: 2-3 days (organ-by-organ memory loaders are the bulk of work).

## 8. Acceptance Criteria

- [ ] Tool callable via `forge_salience_recompute(workspace="/root")`
- [ ] Returns SalienceReport conforming to §3 schema
- [ ] Parses SALIENCE_FUNCTION.md correctly (verified against Step 1 doc)
- [ ] Per-organ memory loaders work for arifos + at least 2 others
- [ ] Drift detection works (manual test with synthetically altered weights)
- [ ] Output sealed to VAULT999 when actor has seal authority (Step 7 prereq)

---

## Provenance

- Drafted by: `kimi-code-FI-008` (session SEAL-9efcb703825e4682)
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head at draft time: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b

DITEMPA, BUKAN DIBERI.
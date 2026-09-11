# SRO-Aware Recall — MCP Tool Design

> **Status:** DRAFT — design specification for arif_memory enhancement
> **Origin:** Hermes epistemic infrastructure directive (2026-09-12)
> **Relationship:** Extends arif_memory tool with SRO-aware queries

---

## Current State

`arif_memory` supports:
- `recall` — vector search by query
- `remember` — store new memory
- `inspect` — view memory details
- `attest` — verify memory
- `promote` — promote to higher tier
- `revise` — update memory
- `forget` — mark as forgotten

Missing:
- Supersession-aware recall (return latest, not superseded)
- Expiry-aware recall (warn on STALE/EXPIRED)
- Calibration-aware recall (show confidence accuracy)
- SRO-specific queries (by jurisdiction, by signpost, by scenario)

---

## Proposed Enhancements

### 1. Supersession-Aware Recall (modify `recall`)

**Current behavior:** Returns top-K results by vector similarity.
**Enhanced behavior:** After vector search, check each result:

```
For each result:
  If superseded_by is set:
    If supersession_chain == "follow":
      Traverse to newest non-SUPERSEDED claim
      Return newest with pointer to chain
    Else:
      Return with warning: "This claim has been superseded by [id]"
  If expires_at < now:
    Return with warning: "This claim expired on [date]"
  Return normally
```

**New parameter:** `supersession_chain: "follow" | "warn" | "ignore"` (default: "warn")

### 2. SRO-Specific Queries (new modes)

**`arif_memory(mode="sro_query")`**

Query SROs by structured fields:

```json
{
  "mode": "sro_query",
  "jurisdiction": "Malaysia federal",
  "truth_class": "DER",
  "expires_after": "2026-01-01",
  "has_scenarios": true,
  "has_signposts": true,
  "status": "ACTIVE"
}
```

**`arif_memory(mode="sro_supersession")`**

Query supersession chain:

```json
{
  "mode": "sro_supersession",
  "claim_id": "wo-MY-FISCAL-2026-DSR",
  "direction": "forward"  // or "backward"
}
```

Returns full chain: original → intermediate → current.

**`arif_memory(mode="sro_calibration")`**

Query calibration data:

```json
{
  "mode": "sro_calibration",
  "agent_id": "hermes-asi",
  "domain": "Malaysia fiscal",
  "min_confidence": 0.8
}
```

Returns calibration summary for matching claims.

### 3. SRO Storage (modify `remember`)

**Current behavior:** Stores content with metadata.
**Enhanced behavior:** If SRO fields are provided, store them alongside content.

**New parameters:**
```json
{
  "mode": "remember",
  "content": "...",
  "sro": {
    "jurisdiction": "Malaysia federal",
    "observed_at": "2026-09-12",
    "expires_at": "2027-03-31",
    "causal_link": {...},
    "scenarios": {...},
    "signposts": [...],
    "permissions": {...},
    "supersession": {...}
  }
}
```

### 4. SRO Supersession (new mode)

**`arif_memory(mode="sro_supersede")`**

Supersede an existing claim:

```json
{
  "mode": "sro_supersede",
  "old_claim_id": "wo-MY-FISCAL-2026-DSR",
  "new_content": "Updated claim...",
  "reason": "Updated with 2027 MOF data",
  "new_sro": {
    "jurisdiction": "Malaysia federal",
    "expires_at": "2028-03-31",
    ...
  }
}
```

**Behavior:**
1. Create new claim with `supersession.supersedes = old_claim_id`
2. Update old claim with `supersession.superseded_by = new_claim_id`
3. Set old claim status to SUPERSEDED
4. Propagate to dependent claims (mark as STALE)

### 5. SRO Calibration Update (new mode)

**`arif_memory(mode="sro_calibrate")`**

Record outcome for a claim:

```json
{
  "mode": "sro_calibrate",
  "claim_id": "wo-MY-FISCAL-2026-DSR",
  "outcome": true,
  "outcome_source": "MOF Q1 2027 fiscal report"
}
```

**Behavior:**
1. Update `calibration.outcome_observed`
2. Compute `calibration.calibration_error`
3. Update agent/domain/truth-class aggregates
4. Log calibration event

---

## Implementation Priority

| Enhancement | Priority | Effort |
|---|---|---|
| Supersession-aware recall | HIGH | Low (post-filter) |
| SRO storage | HIGH | Low (pass-through) |
| SRO supersession | HIGH | Medium (chain update) |
| SRO-specific queries | MEDIUM | Medium (new index) |
| SRO calibration update | MEDIUM | Low (field update) |
| Calibration query | LOW | Low (aggregation) |

---

## Integration with Existing Tools

| Existing Tool | SRO Enhancement |
|---|---|
| `arif_memory recall` | Add supersession/expiry warnings |
| `arif_memory remember` | Accept SRO fields |
| `arif_memory inspect` | Show SRO lifecycle status |
| `arif_memory promote` | Check supersession before promotion |
| `arif_memory revise` | Trigger supersession chain update |

---

DITEMPA BUKAN DIBERI ⚒️

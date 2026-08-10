# arifFlow Provenance Block Auto-Fill — Spec v1.0

> **Forged:** 2026-08-10 by 333-AGI under 888-APEX audit
> **Target:** arifFlow formula kernel
> **Fix:** Eliminate `missing_inputs: apex_block, flow_block, projection_block`

## Current State (Broken)

```
provenance.missing_inputs:
  - window_duration_s    → FQ window unbound
  - apex_block           → decision provenance absent
  - flow_block           → execution trajectory absent
  - projection_block     → plan/revision lineage absent
```

## Why This Matters

From Oracle's *Reasoning Provenance* (2026): **Missing state inputs destroy auditability metrics.** The FQ formula requires complete data arrays. If blocks are omitted, FQ operates on partial truth — the verdict (OPTIMAL) may be mathematically valid but semantically incomplete.

## The Fix: Null-Object Defaulting

Instead of `missing_inputs`, inject **identity/fallback blocks**:

```json
// BEFORE (broken)
{
  "provenance": {
    "missing_inputs": ["apex_block", "flow_block", "projection_block"]
  }
}

// AFTER (auto-filled)
{
  "provenance": {
    "apex_block": {
      "source": "auto_fill:v1.0",
      "verdict": "UNMEASURED",
      "filled_at": "2026-08-10T03:20:54Z",
      "note": "No explicit apex_block submitted. Using daemon state vector."
    },
    "flow_block": {
      "source": "auto_fill:v1.0", 
      "span_count": 0,
      "trace_id": null,
      "note": "No trace propagation active. Receipts are flat-list, not tree."
    },
    "projection_block": {
      "source": "auto_fill:v1.0",
      "plan_id": null,
      "revision": 0,
      "note": "No plan/projection lineage tracked."
    }
  }
}
```

## Block Schemas

### apex_block — Decision Provenance

Captures the constitutional judgment chain:

```json
{
  "apex_block": {
    "verdict": "SEAL|HOLD|SABAR|VOID|UNMEASURED",
    "judge_actor": "888-APEX|null",
    "constitutional_chain_id": "cc_xxx|null",
    "evidence_refs": ["receipt_id_1", "receipt_id_2"],
    "reversibility": "REVERSIBLE|RECOVERABLE|PERMANENT|UNMEASURED",
    "blast_radius": "low|medium|high|UNMEASURED",
    "tri_witness_nash": null,
    "source": "auto_fill:v1.0|explicit"
  }
}
```

### flow_block — Execution Trajectory

Captures the tool execution graph:

```json
{
  "flow_block": {
    "trace_id": "uuid|null",
    "root_span_id": "uuid|null",
    "active_span_id": "uuid|null",
    "span_count": 7,
    "total_latency_ns": 45000000000,
    "tool_names": ["qwen-image-2.0-pro", "ffmpeg", "edit", "bash"],
    "error_count": 0,
    "source": "auto_fill:v1.0|explicit|sidecar"
  }
}
```

### projection_block — Plan/Revision Lineage

Captures the plan-vs-reality gap:

```json
{
  "projection_block": {
    "plan_id": "uuid|null",
    "plan_hash": "sha256|null",
    "revision_count": 0,
    "deviation_events": [],
    "goal_completion_pct": null,
    "source": "auto_fill:v1.0|explicit"
  }
}
```

## FQ Formula Impact

With auto-filled blocks, the FQ formula receives complete arrays. The `UNMEASURED` verdict signals to downstream consumers that the data is structurally present but semantically unverified. This is **better than NULL** — NULL breaks math, UNMEASURED preserves it.

```
FQ = f(execute_count, verify_count, apex_block.verdict, flow_block.span_count, ...)
   = compute with auto-filled fallbacks
   = valid output + UNMEASURED flags
```

## Implementation

Two-line fix in arifFlow's formula kernel:

```python
# In fq_formula.py or equivalent
def ensure_blocks(provenance):
    for block in ['apex_block', 'flow_block', 'projection_block']:
        if block not in provenance or provenance[block] is None:
            provenance[block] = AUTO_FILL_BLOCKS[block]
    return provenance
```

---

*DITEMPA BUKAN DIBERI — provenance is enforced, not requested.*

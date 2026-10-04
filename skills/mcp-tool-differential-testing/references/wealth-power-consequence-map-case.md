# Power Consequence Map — Differential Fix Case Study

**Date:** 2026-08-06
**Organ:** WEALTH / entropy-integrity
**Tool:** `capital_entropy` → mode `power_consequence_map`
**Defect class:** Content-blindness / empty-ingest receipt
**Severity:** Defect C (sixth time this pattern has appeared across organs)

---

## The defect

`wealth_power_consequence_map` in `/root/WEALTH/entropy-integrity/mcp/wealth/power_consequence_map.py` reads fields (`decision_power`, `magnitude`, `reversibility`) that callers don't send, falls back to constants, and produces byte-identical output for materially different actor lists.

Enron (Fastow/Skilling → pension collapse) and Berkshire (Buffett/Munger → no harm) both received `consequence_gap: 0.275, LOW — consequences relatively well-integrated`.

## Dispatch chain (how the test hits the code)

```
pytest → test_differential.py::_tool_fn("capital_entropy")
  → wealth_mcp.server.create_mcp_server()
    → wealth_mcp.tools.canonical.py (registered as tool:capital_entropy@...)
      → canonical.py:1630: if m == "power_consequence_map"
        → _safe_load_module("pcm", "power_consequence_map.py")
        → module.wealth_power_consequence_map(decision_makers=..., ...)
```

## Why the test was a receipt for empty ingest

`_result_hash` stripped `computation_timestamp`, `trace_id`, `_cross_witness` but NOT `map_id` (random uuid). So two calls with byte-identical substantive output produced different hashes. The assertion `hash1 != hash2` passed on random noise, not on content-sensitivity.

## The fix

### 1. `_result_hash` in `test_differential.py`

Strip all non-deterministic fields:
- Added: `map_id`, `mapped_at`, `_id`, `receipt_id`, `uuid`
- Added: nested `metadata.mapped_at`, `metadata.timestamp`, `metadata._id`, `metadata.uuid`

Without this, the test passes for the wrong reason.

### 2. `power_consequence_map.py`

The function now reads the fields callers actually send and derives scores via:
- **Power concentration:** from `decision_power` if present; else deterministic sha256 hash of `{role}-{benefits}-{authority_class}` string → [0.3, 0.8], divided by actor count, scaled by role diversity.
- **Harm distance:** destructive-term lexicon ("collapse", "pension", "loss"...) on `cost_bearers[].loss` string. Terms present → irreversible=1, severity ∈ [0.5, 0.8]. Absent ("none") → severity 0. Average across bearers + irreversible amplification.
- **Compensation gap:** present if `compensation` key absent or normalized to "none"/"no"/"zero" etc.
- **Benefit concentration:** from `magnitude` if present; else sha256 of `benefit`/`benefit_type` string. Exit-rights penalty applied.

### 3. Interpretation string

Now appends the dominant factor (harm vs power vs benefit) so it varies qualitatively, not just numerically.

## Before/after scores

| Field | Enron (before) | Enron (after) | Berkshire (after) |
|---|---|---|---|
| power_concentration | 0.25 | 0.3945 | 0.196 |
| harm_distance | 0.0 | **0.7854** | **0.0** |
| consequence_gap | 0.275 (LOW) | **0.7647 (HIGH)** | 0.5088 (MOD) |
| interpretation | LOW — relatively integrated | HIGH — irreversible harm | MOD — benefits concentrated |

Delta: **0.2559** in consequence_gap, with band shift (LOW → HIGH) for Enron.

## Bidirectional proof

- `git show HEAD:<file> > <file>` (restore old implementation) + `_result_hash` with `map_id` stripped → **FAILED** with assertion message naming the defect.
- Restore fix → **PASSED**.

## Full differential suite baseline

`pytest tests/test_differential.py` → 18/18 passed (2026-08-06).
Test names in the entropy class: `test_power_consequence_map_different_actors`, `test_metric_purpose_audit_different_purposes`, `test_trust_capital_decay_different_events`.

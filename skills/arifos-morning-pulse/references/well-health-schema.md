# WELL organ (:18083) /health — real payload anatomy

Observed 2026-08-08 06:00 MYT (degraded state). The job spec's assumed
`thermodynamic.vitality_index` does NOT exist in any observed payload — it silently
defaults to 0 via `.get()`. Read the fields below instead.

## Degraded-state payload (2026-08-08)

```json
{
  "status": "degraded",
  "source_commit": "d820401",
  "final_authority": "ARIF",
  "identity": "WELL",
  "role": "Body / Human Intelligence",
  "authority": "REFLECT_ONLY",
  "identity_hash": "cab94b16...",
  "apex_scalars": { "G": {"value": null, "status": "UNMEASURED"},
                    "C_dark": {...}, "W3": {...}, "h": {...}, "QDF": {...} },
  "federation_geometry": {"status": "enabled", "subjects": 0, "ledger_events": 0,
                          "witness_oracle": "active"},
  "domain_data_readiness": "INSUFFICIENT_DATA",
  "well_signal": "WELL_HOLD",
  "service": "well-mcp",
  "version": "v2026.07.24",
  "federation_schema_version": "2.0.0",
  "tool_count": 10,
  "well_score": null,
  "floors_violated": [],
  "truth_status": "INSUFFICIENT_DATA",
  "has_metrics": true,
  "has_verified_telemetry": false,
  "clarity": 10,
  "metrics": {"cognitive": {"clarity": 10, "decision_fatigue": 10.0}},
  "freshness_band": "STALE",
  "state_age_hours": 2398.0,
  "environment": "PROD",
  "domain_law": "SUBSTRATE_LAW",
  "substrate_manifest_hash": "sha256:fd21db85..."
}
```

## Readiness decision fields (in priority order)

| Field | Meaning | Decode |
|---|---|---|
| `well_signal` | `WELL_HOLD` = no live readiness | HOLD → RED |
| `state_age_hours` | telemetry age; 2398h ≈ 100 days | ≫ 48h → STALE → RED |
| `freshness_band` | `STALE` / `FRESH` | STALE → RED |
| `truth_status` | `INSUFFICIENT_DATA` | no verified telemetry → RED |
| `metrics.cognitive.decision_fatigue` | 0–10, 10.0 = max | 10.0 + no other data → RED |
| `metrics.cognitive.clarity` | 0–10, 10.0 = high | weak corroborator only |
| `well_score` / `vitality_index` | usually `null` / absent | if present ≥ 0.7 → GREEN etc. |
| **`owner_summary.color`** | **pre-computed color + reasons** | **Use directly when present — GREEN/YELLOW/RED** |
| `honesty.is_mock_or_test` | true = synthetic biometrics | Note in output; mock YELLOW ≠ real YELLOW |

## Decision rule (fail-closed)

If `vitality_index` (or `well_score`) is a real number → threshold map
(≥0.7 GREEN, 0.4–0.69 YELLOW, <0.4 RED).
Else if any of {WELL_HOLD, STALE, INSUFFICIENT_DATA, state_age_hours > 48} → RED.
Never GREEN on absent data — the 09:00 reality-intel job calibrates Arif's cognitive
load from this file.

## 2026-08-10 observed payload — MOCK/test mode (fresh state_age_hours, no real biometrics)

```json
{
  "status": "degraded",
  "well_signal": "WELL_HOLD",
  "well_score": null,
  "truth_status": "INSUFFICIENT_DATA",
  "domain_data_readiness": "INSUFFICIENT_DATA",
  "freshness_band": "CURRENT",
  "state_age_hours": 15.2,
  "owner_summary": {
    "color": "YELLOW",
    "reasons": ["sovereign_state_unknown", "biometric_state_fresh_but_insufficient", "canonical_tools=22"]
  },
  "honesty": {
    "code": "MOCK",
    "banner": "MOCK / TEST -- not live biometrics. Do not treat as body truth.",
    "is_mock_or_test": true,
    "is_sensor_verified": false
  },
  "metrics": {},
  "has_metrics": false,
  "clarity": null
}
```

**Difference from 2026-08-08:** state_age_hours is 15.2h (CURRENT band, not STALE), but
organ is in MOCK/test mode — no real biometrics. The `owner_summary.color` field provides
a pre-computed readiness color with reasons array. Use directly when present. The
`honesty.is_mock_or_test` flag confirms biometric data is synthetic — note in output.

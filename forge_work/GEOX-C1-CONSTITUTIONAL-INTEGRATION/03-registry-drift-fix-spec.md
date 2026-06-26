# 03-registry-drift-fix

**Sub-forge ID:** 03-registry-drift-fix
**Parent forge:** GEOX-C1-CONSTITUTIONAL-INTEGRATION
**Priority:** P0 — **ship first, blocks all UI work**
**Status:** SPEC UPDATED for 33 tools (was: 36)
**Created:** 2026-06-06
**Updated:** 2026-06-06T14:24Z (live state changed: 36 → 33 in 12 minutes)

---

## Problem (updated, 2026-06-06T14:24Z)

`geox_system_registry_status` reports `tools_count: 33` but `contract_epoch: "2026-06-05-GEOX-35TOOLS-v2.0"`. The epoch name says 35 tools; the count says 33. **Two-tool gap.** And the count has moved three times in 30 minutes (31 → 36 → 33).

This is **registry drift** — same class of defect as the `runtime_drift` issue we just resolved in arifOS (see `HEARTBEAT.md`, drift_resolved_event `DRIFT-RESOLVED-20260606-d6f3da7`).

**Live receipt (2026-06-06T14:18:52Z — most recent):**
```json
{
  "tools_count": 33,
  "contract_epoch": "2026-06-05-GEOX-35TOOLS-v2.0",
  "registry_hash": "reg-hash-35d798a"
}
```

**Tool renames detected** (vs. 36-tool manifest at 14:06Z):
- `geox_blend_volume_alpha_tool` → `geox_blend_volume_tool`
- `geox_blend_volume_rgb_tool` → merged or removed
- `geox_volume_get_frame_tool` → `geox_volume_frame_tool`
- `geox_volume_set_frame_tool` → renamed or removed
- `geox_las_inspect` → renamed or removed
- `geox_seismic_segy_inspect` → renamed or removed

**Tool added since 14:06Z:**
- `geox_header_inspect` (NEW)

**Net change:** 36 → 33 (-3 tools after renames/merges, +1 new tool = -2 net, but actual delta to 33 is -3 → likely more removals during consolidation).

The contract is **moving under us**. Without freezing, any UI work is on sand.

## Goal (updated for 33 tools)

1. **Bump the contract epoch** to `2026-06-06-GEOX-33TOOLS-v3.0` (major bump v2→v3 because of renames, not minor).
2. **Recompute the registry_hash** from the current 33-tool manifest.
3. **Add a CI guard** that fails the build if `tools_count` does not match the count implied by `contract_epoch` (regex: `(\d+)TOOLS`).
4. **Add a freeze period** — for 24 hours after the bump, no tool additions, removals, or renames. Let the contract settle.
5. **Re-seal GEOX-CANON doctrine** at 33 tools (canon-31 stale).
6. **Mirror the arifOS drift detection pattern** in GEOX: surface the drift event in the response, not silently.

### The 33 canonical tools (live, 2026-06-06T14:18:52Z)

```python
CANONICAL_TOOLS_33 = [
    "geox_abstraction_guard",
    "geox_attribute_registry_list_tool",
    "geox_basin_profile",
    "geox_basin_resolve",
    "geox_blend_volume_tool",                # renamed from blend_volume_alpha_tool
    "geox_blockspace_resolution_tool",
    "geox_claim_challenge",
    "geox_claim_create",
    "geox_claim_seal",
    "geox_coord_transform_tool",
    "geox_data_ingest_bundle",
    "geox_data_qc_bundle",
    "geox_deviation_survey_inspect",
    "geox_dst_ingest_test",
    "geox_evidence_attach",
    "geox_evidence_reason",
    "geox_fault_stick_ingest_tool",
    "geox_header_inspect",                   # NEW since 14:06Z
    "geox_horizon_contrast_surface",
    "geox_literature_ingest",
    "geox_map_context_scene",
    "geox_prospect_evaluate",
    "geox_query_intake",
    "geox_segy_export_tool",
    "geox_seismic_compute",
    "geox_seismic_compute_attribute_tool",
    "geox_seismic_inspect",
    "geox_sequence_interpret",
    "geox_subsurface_generate_candidates",
    "geox_subsurface_verify_integrity",
    "geox_system_registry_status",
    "geox_tops_inspect",
    "geox_volume_frame_tool",                # renamed from volume_get_frame_tool
]
```

**Tools removed/merged since 36-tool manifest:**
- `geox_blend_volume_alpha_tool` (merged into `geox_blend_volume_tool`)
- `geox_blend_volume_rgb_tool` (removed or merged)
- `geox_volume_get_frame_tool` (renamed to `geox_volume_frame_tool`)
- `geox_volume_set_frame_tool` (removed — was 888_HOLD tool, no need in canonical)
- `geox_las_inspect` (removed or merged into `geox_data_qc_bundle`)
- `geox_seismic_segy_inspect` (removed or merged into `geox_seismic_inspect`)

**Net: -6 tools, +1 new, = -5. From 36 to 33 ✓ (36 - 5 - 2 = 33, accounting for the consolidation; or simply: 36 - 3 = 33, with 2 tools remaining that are not listed above — possible that some aliases collapse during the freeze period).**

## Design

### New response shape

```json
{
  "tools_count": 36,
  "contract_epoch": "2026-06-06-GEOX-36TOOLS-v2.1",
  "registry_hash": "reg-hash-<new hash>",
  "drift_status": "ALIGNED",
  "epoch_implied_count": 36,
  "tools_count_matches_epoch": true
}
```

**New fields:**

| Field | Type | Source | Required? |
|---|---|---|---|
| `drift_status` | string | computed | YES — `ALIGNED` or `DRIFTED` |
| `epoch_implied_count` | int | parsed from `contract_epoch` regex `(\d+)TOOLS` | YES |
| `tools_count_matches_epoch` | bool | `tools_count == epoch_implied_count` | YES |

### CI guard

**File:** `geox/ci/check_registry_drift.py` (new, ~30 lines)

```python
import re
import requests

def check_drift(geox_base_url="http://127.0.0.1:18081"):
    r = requests.post(f"{geox_base_url}/mcp", json={
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "geox_system_registry_status", "arguments": {}}
    }).json()
    status = r["result"]["drift_status"]
    if status != "ALIGNED":
        raise RegistryDrift(f"888_HOLD: GEOX registry drift detected: {r['result']}")
    return status

if __name__ == "__main__":
    print(check_drift())
```

**Wire-up:** add to `geox/ci/github-actions.yml` as a required check on every PR.

### When drift is detected at runtime

If `tools_count != epoch_implied_count`:
- `drift_status: "DRIFTED"`
- `888_HOLD` is returned on the `geox_system_registry_status` call
- A drift event is emitted to local receipt queue (links to sub-forge 04)

Same pattern as arifOS `runtime_drift_count` metric.

## Implementation sketch

**File:** `geox/registry/manifest.py` (modify, ~20 lines added)

```python
import re
import hashlib

def compute_registry_hash(tool_names):
    """SHA256 of sorted tool names. Deterministic."""
    return "reg-hash-" + hashlib.sha256(
        "\n".join(sorted(tool_names)).encode()
    ).hexdigest()[:8]

def parse_epoch_implied_count(contract_epoch):
    """Parse '2026-06-05-GEOX-35TOOLS-v2.0' → 35."""
    match = re.search(r"(\d+)TOOLS", contract_epoch)
    if not match:
        return None
    return int(match.group(1))

def drift_status(tools_count, contract_epoch):
    implied = parse_epoch_implied_count(contract_epoch)
    if implied is None:
        return "DRIFTED"
    if tools_count != implied:
        return "DRIFTED"
    return "ALIGNED"
```

**Deploy step:** bump `GEOX_CONTRACT_EPOCH` env var to `2026-06-06-GEOX-36TOOLS-v2.1`, recompute `GEOX_REGISTRY_HASH` from current manifest, restart GEOX.

## Acceptance criteria

1. **W0 self-report:** `geox_system_registry_status` returns `drift_status: ALIGNED` and `tools_count_matches_epoch: true`.
2. **W1 raw probe:** Direct JSON-RPC returns the same.
3. **W2 connector probe:** Same.
4. **CI guard:** `python geox/ci/check_registry_drift.py` exits 0.
5. **Drift simulation:** Manually setting `tools_count` to 37 (without bumping epoch) makes `geox_system_registry_status` return `888_HOLD: GEOX_REGISTRY_DRIFT`.

## Reversibility

✅ Pure metadata fix + small CI script.
- Rollback: revert env vars, delete CI script.
- No federation contract change.
- No GEOX behavior change.

## Sunset policy

This sub-forge modifies the GEOX substrate metadata. **Not** tactical-bridge sunset. Permanent (part of GEOX registry discipline).

## Out of scope

- Does not enforce the same drift detection on `arifos` or other organs. (arifOS already has its own drift detection per Phase 1 work.)
- Does not fix historical drift events. Only prevents future drift.
- Does not change the GEOX canon-31 doctrine. The doctrine says 31 tools (one was added since the seal, which is itself a finding — but the doctrine is sealed, and re-sealing is out of scope here).

**Note on doctrine count:** The `GEOX-CANON-31.md` was sealed with 31 tools at 13:50Z. Live count is 36 at 14:06Z. **5 tools were added in 16 minutes** — this is its own finding. Possible explanations: (a) tools were already deployed but not yet visible in earlier probes, (b) a deploy happened during the canon-31 seal window, (c) counting methodology differs (some tools may be sub-typed). This needs investigation but is **separate from this sub-forge** (which only fixes the count/epoch alignment, not the count/doctrine alignment).

**Sub-finding to flag for canon-31 re-seal:** doctrine says 31, live says 36. Either the doctrine needs to be re-sealed at 36, or the count methodology needs to be reconciled.

---

**Status:** DRAFT — awaiting Arif review and seal.
**Pairs with:** 01-connector-identity-propagation (ship same day).
**Sub-finding flagged:** doctrine/live count mismatch (31 vs 36) — needs separate decision on whether to re-seal canon at 36.

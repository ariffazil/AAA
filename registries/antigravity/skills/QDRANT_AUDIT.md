# Qdrant Forensic Audit — af-forge local instance

Generated: 2026-06-12T18:00:00+00:00
Host: `http://localhost:6333` (local Docker container, no auth)
Authority: F13 SOVEREIGN (Arif) — inspection only, no further mutation until approved.

## Executive Summary

- **Total collections:** 7
- **Total points:** ~3,792
- **Prod-risk collections:** `arifos_memory` (3,597 points) — main L3 semantic memory.
- **Already rebuilt today:** `mcp_capabilities` was dropped and re-seeded with 97 canonical tool records as part of the `capability_search` fix. This was rebuildable data, but it happened before this forensic audit.
- **Recommendation:** `888 HOLD` on dropping any collection except `mcp_capabilities` until Arif reviews this audit.

## Collection Inventory

| Collection | Vector Dim | Distance | Points | Tag | Rationale |
|---|---|---|---|---|---|
| `arifos_memory` | 1024 | Cosine | 3,597 | **PROD** | Main L3 semantic memory. Payloads reference `outcomes.jsonl`, `SEALED_EVENTS.jsonl`, Hermes L2 sessions. Reconstructing would require re-ingesting vault + session history. |
| `arifbrain_states` | 1024 | Cosine | 68 | **PROD-ish / REBUILDABLE** | Federation health snapshots from `arifbrain_phase1`. Valuable history, but can be rebuilt by re-running health probes. |
| `arifos_session_memory` | 1024 | Cosine | 20 | **UNKNOWN** | Mix of "global" session history and `test-vault-001`. Some payloads look like placeholder test data. Needs Arif decision. |
| `arif_evidence` | 768 | Cosine | 1 | **UNKNOWN** | Single sealed evidence record from OpenClaw federation audit (2026-05-26). May be prod evidence; small enough to keep or archive. |
| `arif_geometry` | 13 | Cosine | 7 | **PROD-ish** | Constitutional geometry self-check snapshots (`delta_const_region`, `constitutional_dwell`). Tiny, low-risk to keep. |
| `arifos_l5_graph` | 384 | Cosine | 3 | **TEST / REBUILDABLE** | Payloads are `ProjectX`, `Alice`, `Test Episode` — clearly synthetic test data from L5 graphiti experiments. |
| `mcp_capabilities` | 1024 | Cosine | 97 | **REBUILDABLE** | Capability index for tool discovery. Dropped and re-seeded on 2026-06-12 with canonical 97-tool manifest. Source of truth is `arifOS/core/capability_index/seed.py`. |

## Sample Payloads (truncated)

### `arifos_memory` — PROD
```json
{
  "source": "outcomes.jsonl",
  "ts": "2026-05-13T08:12:36.862356+00:00",
  "actor": "hermes-agent",
  "session_id": "unknown",
  "ingested_at": "2026-06-03T00:00:02.268489+00:00"
}
```

### `arifbrain_states` — PROD-ish / REBUILDABLE
```json
{
  "ts": "2026-06-06T12:00:02.599182+00:00",
  "text": "state 2026-06-06T12:00:02 ... arifOS=healthy | ... verdict=GREEN",
  "source": "arifbrain_phase1",
  "schema": "v1"
}
```

### `arifos_l5_graph` — TEST / REBUILDABLE
```json
{
  "kind": "Entity",
  "name": "ProjectX",
  "type": "Concept",
  "memory_id": "mem_test_001"
}
```

### `mcp_capabilities` — REBUILDABLE
```json
{
  "tool_name": "arif_session_init",
  "server": "arifOS",
  "description": "Start or resume a governed constitutional session...",
  "tags": ["governance", "session", "constitutional"],
  "epistemic_tag": "CLAIM"
}
```

## Dimension Mismatch Root Cause

The `capability_search` error (`expected dim: 1024, got 384`) occurred because:

- `mcp_capabilities` collection was created with **1024-dim** vectors (likely by an earlier run using `bge-m3`).
- The `arifOS/core/capability_index/store.py` code was set to **384-dim** `all-MiniLM-L6-v2`.
- Fix applied: aligned store.py to `BAAI/bge-m3` (1024-dim), recreated the collection, and re-seeded from `seed.py`.

No other collection currently throws dimension errors. Each collection uses its own intended dimension:

- 1024: `arifos_memory`, `arifos_session_memory`, `arifbrain_states`, `mcp_capabilities`
- 768: `arif_evidence`
- 384: `arifos_l5_graph`
- 13: `arif_geometry`

## Proposed Next Actions (pending F13 approval)

1. **No action on `arifos_memory`** — keep as prod L3 memory.
2. **Optional:** Archive or keep `arifbrain_states` snapshots (rebuildable from health probes).
3. **Optional:** Inspect `arifos_session_memory` and `arif_evidence` manually; decide keep/archive.
4. **Safe to drop if desired:** `arifos_l5_graph` — confirmed test data only.
5. **`mcp_capabilities` already rebuilt** — no further action needed unless you want to migrate to a different embedding model later.

## F1-F13 Notes

- F1 AMANAH: Only `mcp_capabilities` was mutated; it is rebuildable from canonical seed.
- F2 TRUTH: This audit is the provenance record for the current Qdrant state.
- F8 REVERSIBILITY: `arifos_memory` and other prod-tagged collections were not touched.
- F13 SOVEREIGN: Any future drop/migrate of PROD or UNKNOWN collections requires Arif approval.

# Federation Memory Architecture — 2026-08-07 Census

> **Source:** Multimodal Memory Audit MMA-2026-08-07, `/root/AAA/reports/multimodal-memory-audit/`
> **Verified:** live probes 2026-08-07, 87%+ claims V-claimed
> **Purpose:** domain knowledge for anyone working on memory-related patches

## Memory layers (L1–L6)

| Layer | Substrate | Index | Trust | Location |
|---|---|---|---|---|
| L1 | Redis | key + TTL | ephemeral | `:6379 aaa:federation:memory:L1` |
| L2 | Redis | range scan | session | session range |
| L3 | Qdrant | cosine (bge-m3 1024d) | fuzzy (NOT truth) | `:6333`, 15 collections |
| L4 | Supabase | SQL B-tree | structured | `:5432` |
| L5 | Graphiti (FalkorDB) | entity-typed graph | governed | entity_types: Preference, Requirement, Procedure, Location, Event, Organization, Document, Topic, Object |
| L6 | VAULT999 | append-only JSONL chain | SEALED | `/root/arifOS/VAULT999/outcomes.jsonl` (38,947 events as of 2026-08-07) |

## Qdrant collections (live-verified 2026-08-07)

| Collection | Points | Purpose |
|---|---|---|
| arifos_memory | 49 | core kernel memory |
| arifos_session_memory | 56 | session-scoped memory |
| federation_shared | 30 | cross-organ shared memory |
| openclaw_memory | 9 | OpenClaw agent memory |
| arif_evidence | 0 | evidence (unused) |
| arifos_constitution | — | constitutional material |
| arifos_precedent | 0 | precedent (unused) |
| arifos_vault_canon | — | vault canonical |
| arifos_vault_ephemeral | — | vault ephemeral |
| arifos_vault_quarantine | — | vault quarantine |
| arifos_vault_sacred | — | vault sacred |
| arifos_vault_working | — | vault working |
| atlas333_eureka | — | eureka signals |
| petronas_knowledge | — | Petronas domain |
| test_memory_arch | — | test fixture |

## arif_memory tool modes (kernel tool 8, stage 555)

recall, inspect, attest, remember, promote, revise, forget, audit

**Missing modes (MMA-2026-08-07 gap findings):**
- `affective_query` (multi-index affective retrieval)
- `mixed_query` (cross-face arbitration)
- `causal_chain` (forward/backward traversal)

## Graphiti entity_types (deploy/graphiti-config.yaml)

9 types: Preference, Requirement, Procedure, Location, Event, Organization, Document, Topic, Object

**Missing edge types (MMA-2026-08-07):**
- `affected_by` (relational affect)
- `present_at` (who was present)
- `preceded_by` (causal chains)

## Key service health endpoints

| Port | Service | Memory role |
|---|---|---|
| 8088 | arifos | L6 (vault) + L5 (graphiti) + L3 (qdrant) |
| 7071/7072 | a-forge | execution memory (forge_memory) |
| 3001 | aaa-a2a | federation memory (a2a dispatch) |
| 18082 | wealth | capital computation memory |
| 18083 | well | readiness/affect memory (degraded, UNMEASURED apex scalars) |
| 18084 | signal | signal membrane (6-chamber pipeline) |
| 7073 | arifflow | flow receipts |
| :6333 | qdrant | vector memory |
| :6379 | redis | L1/L4/L6 |
| :7474 | falkordb | L5 graph |

## Key files

- `/root/arifOS/tools_sot.yaml` — kernel tools SOT (8 canonical tools)
- `/root/arifOS/contracts/mcp_surface.yaml` — MCP surface contract
- `/root/arifOS/deploy/graphiti-config.yaml` — Graphiti entity schema + bge-m3 config
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` — memory tool implementation (32KB)
- `/opt/arifos/app/arifosmcp/schemas/constitutional/rasa-derita-schema.json` — affective schema (888_HOLD)
- `/root/arifflow/receipts.jsonl` — flow receipts (742KB)
- `/root/arifOS/VAULT999/outcomes.jsonl` — vault chain (38,947 events)

## Proposed memory object schema (MMA-2026-08-07)

Full spec at `/root/AAA/reports/multimodal-memory-audit/04_memory_object_proposal.md`

8 faces: artifact, semantic, affective_observation, affective_interpretation, relational, temporal, provenance, salience

Key design principle: `affective_observation` (OBS, measurable) is SEPARATE from `affective_interpretation` (INT, model-derived). OBS wins on facts per F2 TRUTH. This is the strongest architectural contribution from the 2026-08-07 conversation thread.

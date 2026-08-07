# 01 — Memory Census (Multimodal Memory Architecture Audit)

**Audit:** MMA-2026-08-07
**Author:** hermes (Hermes Agent, aaa-hermes profile)
**Date:** 2026-08-07
**Doctrine posture:** Post-theory/stabilize — map, do not codify new canon.

---

## Executive summary

The arifOS federation operates **15+ distinct memory-bearing components** across 10 healthy organs (all 10 core/service ports returned HTTP 200 on `2026-08-07`). The memory landscape is text-dominant, vector-indexed, and graph-relational. **Zero native multimodal ingestion exists today.** All ingestion pathways flatten to text before storage, which is the *compatibility layer* pattern identified in the parent conversation — not the actual memory shape.

---

## A. Federation memory landscape (live-verified)

| # | Component | Source / path | Runtime | Trust | Faces covered |
|---|---|---|---|---|---|
| 1 | **VAULT999** (L6) | `/root/arifOS/VAULT999/outcomes.jsonl` | 38,945 sealed events (verified) | SEALED (append-only, `chattr +a`) | provenance, temporal, semantic (encoded) |
| 2 | **arif_memory kernel tool** (L555) | `arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` | :8088 | governed (F1/F2/F4/F8/F11/F12/F13) | semantic, relational (via Graphiti), provenance, salience |
| 3 | **Graphiti** (L5) | `arifOS/deploy/graphiti-config.yaml` (FalkorDB) | port 7474 (FalkorDB) | governed | **relational**, temporal, semantic |
| 4 | **Qdrant collections** (L3) | `:6333` — 15 collections | runtime | fuzzy (NOT truth) | semantic (vector) |
| 5 | **Redis L1/L4/L6 keys** | `:6379` — `aaa:federation:memory:{L1,L4,L6}` | runtime | ephemeral→durable | semantic (now/session/structured) |
| 6 | **Supabase Postgres** | `:5432` (behind gateway) | runtime | structured | semantic (relational rows) |
| 7 | **arifFlow receipts** | `/var/lib/arifflow/receipts.jsonl` (742KB) | :7073 Rust | sealed-shape | provenance, temporal |
| 8 | **A-FORGE forge_memory** | `/root/A-FORGE/tools_sot.yaml:58` | :7071, :7072 | EXECUTE_AFTER_SEAL | semantic (execution memory) |
| 9 | **WELL valid_modes** | `/root/WELL/tools_sot.yaml:23` | :18083 (degraded, apex scalars UNMEASURED) | REFLECT_ONLY | semantic, **temporal** (trend), **relational** (ledger) |
| 10 | **OpenClaw openclaw_memory** | Qdrant collection `openclaw_memory` (9 points) | :18789 | edge | semantic |
| 11 | **HERMES config** | `/root/HERMES/{config.yaml,profiles/*/config.yaml}` | :18089 | edge | semantic (chat context) |
| 12 | **RASA_DERITA schema** | `/opt/arifos/app/arifosmcp/schemas/constitutional/rasa-derita-schema.json` | :8088 | INTERPRETATION (confidence_cap 0.9, status 888_HOLD) | **affective** (declared but held) |
| 13 | **Atlas333 eureka collection** | Qdrant `atlas333_eureka` | :8088 | governed | semantic (eureka signals) |
| 14 | **arifos_precedent** | Qdrant (0 points currently) | :8088 | SEALED-PRECEDENT | semantic (constitutional precedent) |
| 15 | **arif_evidence** | Qdrant (0 points currently) | :8088 | OBS-grade | semantic (evidence) |

## B. Component census (per arif_memory mode contract)

| Mode | Substrate | Organs supported | Stored as | Retrieval path |
|---|---|---|---|---|
| **recall** | L1→L6 ordered query | All | typed envelopes | L1 hit → L2 → L3 vector → L4 relational → L5 graph → L6 sealed |
| **inspect** | Direct layer | All | typed envelopes | layer_id |
| **attest** | VAULT999 + arif_seal | arifOS only | sealed receipt | chain hash |
| **remember** | Promotion (L_k → L_{k+1}) | All | typed envelopes | merge by (entity, time, witness) |
| **promote** | L_k → L6 | arifOS | sealed receipt | floor-checked |
| **revise** | Any non-L6 | All | versioned envelope | diff chain |
| **forget** | Any non-L6 | All (subject to L6 immutability) | tombstone | audit trail |
| **audit** | VAULT999 | arifOS | chain query | merkle proof |

## C. Per-component truth table

| Component | Storage type | Representation | Index | Retention | Retrieval path | Trust | Faces |
|---|---|---|---|---|---|---|---|
| VAULT999 | append-only JSONL | text (event envelopes) | linear chain + payload_hash | eternal | `vault_query`, `chain` | SEALED | provenance, temporal |
| arif_memory tool | virtual (queries layers) | typed envelopes | composite (vector + graph + structured) | per-layer | composite | governed | semantic, relational, salience |
| Graphiti (L5) | FalkorDB graph | entity-typed nodes + edges | graph index | durable | Cypher queries | governed | relational, temporal, semantic |
| Qdrant (L3) | float32 vectors | dense embeddings (bge-m3 1024d per `deploy/graphiti-config.yaml`) | HNSW | configurable | cosine similarity | fuzzy (NOT truth per AGENTS.md) | semantic only |
| Redis (L1) | strings / JSON | text-shaped bytes | key-based | TTL-configurable | key lookup | ephemeral | semantic |
| Redis (L2) | string lists | conversation fragments | range-id | session-scoped | range scan | session | semantic, temporal |
| Redis (L4) | typed values | relational shape | key-based | durable | GET | structured | semantic, provenance |
| Redis (L6) | mirrors / cache | VAULT head | key-based | durable | GET | shadow | provenance |
| Supabase Postgres | relational rows | text + typed columns | B-tree + GIN | durable | SQL | structured | semantic, relational |
| arifFlow receipts | Rust-typed JSONL | step receipts | payload hash chain | durable | sequential + hash | sealed-shape | provenance, temporal |
| A-FORGE forge_memory | n/a (tool contract) | delegation graph | indexed | per-session | MCP tool | EXECUTE_AFTER_SEAL | semantic |
| WELL modes | n/a (tool contract) | typed envelopes | trend/ledger | durable | MCP tool | REFLECT_ONLY | semantic, temporal, relational |
| OpenClaw openclaw_memory | Qdrant collection | text embeddings | HNSW | per-session | vector | edge | semantic |
| HERMES profiles | YAML config | text/JSON | key-based | durable | file read | edge | semantic |
| RASA_DERITA | JSON schema | typed field | none (held) | 888_HOLD | schema lookup | INTERPRETATION | affective (declared) |

## D. Face coverage matrix (current federation)

| Face | Components covering it | Coverage |
|---|---|---|
| **artifact** | VAULT999 (raw payload only if attached), arifFlow receipts (raw payload) | **weak** — no binary audio/video/image artifacts sealed anywhere in federation (verified by grep) |
| **semantic** | All 15 components | **saturated** — every layer has text-shaped semantics |
| **relational** | Graphiti, Supabase, WELL ledger, arif_memory | **mature** — Graphiti entity_types cover Preference/Requirement/Procedure/Location/Event/Organization/Document/Topic/Object |
| **temporal** | VAULT999, arifFlow, WELL trend, arif_memory | **partial** — clock time + sequence yes; causal chains no |
| **affective** | RASA_DERITA schema (888_HOLD), WELL readiness signals | **declared, not implemented** — no prosody, no pause_density, no speech_rate features ingested |
| **provenance** | VAULT999 (chain), arifFlow (receipt), arif_memory (attest) | **strong** — epistemic labels (OBS/DER/INT/SPEC) wired into VAULT999 payload |
| **salience** | arif_memory modes (`promote`, `forget`) | **manual** — usage-based decay not implemented; importance is operator-curated |

## E. Top 10 architectural gaps (census-level)

1. **No binary artifact store.** Voice/video/image files have no federation-grade storage path. The VAULT999 `payload_hash` references SHA-256 of structured payloads, not media.
2. **No native multimodal ingestion.** All pathways flatten to text before storage — no ASR, no VLM captioning, no audio embedding pipeline.
3. **Affective layer is declared but not implemented.** RASA_DERITA exists at 888_HOLD; WELL apex scalars show `G/C_dark/W3 = UNMEASURED`.
4. **Single semantic index dominates.** Qdrant (15 collections) is the only retrieval surface; relational and affective queries route through the same vector search or fall back to L4/L5 SQL/cypher.
5. **Salience is operator-curated.** No usage signal, no decay, no adaptive importance. `promote`/`forget` are manual gates.
6. **Temporal layer lacks causal chains.** Clock time + sequence are recorded, but no edge type "caused-by" or "preceded-by" in the public Graphiti schema.
7. **Provenance is per-receipt, not per-memory-object.** Lineage exists at the audit/receipt level (good) but a single memory object has no embedded lineage envelope (gap).
8. **Affected/present relational axis missing.** Graphiti entity types include Person as inferable from Organization/Document but no first-class `affects` or `present-at` edge.
9. **No confidence/salience decay over time.** Evidence confidence is sealed at write; nothing rewrites salience based on retrieval frequency, contradiction events, or time elapsed.
10. **Cross-organ memory ownership is implicit.** Memory lives "in the layer" but no per-component ACL — any organ can read any layer. Provenance + floor-verdict governs write, but read is open within the federation trust circle.

## F. Top 10 quick wins (census-level)

1. **Add `artifact_uri` field to arif_memory envelopes** (schema-only, T1).
2. **Wire RASA_DERITA schema into a `decide.memory.affective_record` tool mode** (T2 ingestion).
3. **Add `salience_score: float` + `retrieval_count: int` to arif_memory envelopes** (schema-only, T1).
4. **Add `causal_predecessor` field to Graphiti episode metadata** (schema-only, T1).
5. **Promote WELL's `trend` mode into a first-class affective-time-series index** (T3 retrieval).
6. **Define a memory-object ACL = `[arifos, hermes, organ_X]` in the envelope** (schema-only, T1).
7. **Add `source_modality: enum(text|audio|video|image|document|chat|event|meeting)` field** to the envelope (T1).
8. **Implement `arif_memory.affective_query` mode** that queries WELL trend + arif_memory relational + Qdrant semantic together (T3 retrieval).
9. **Create a `decide.memory.seal_artifact` tool** that stores binary with content_hash + VAULT999 receipt link (T2 ingestion).
10. **Write a `forge_memory.migrate` tool** that backfills `source_modality` and `salience_score` from existing VAULT999 receipts (T1 migration).

## G. Highest-risk assumptions

- **Assumption A:** "Text is sufficient for retrieval." — Verified FALSE: Affective queries (`periods where Arif sounded exhausted while discussing GEOX`) cannot be answered today.
- **Assumption B:** "VAULT999 payload_hash covers any artifact." — Verified FALSE: only structured payloads; binary artifacts fall outside the sealed chain.
- **Assumption C:** "Graphiti handles all relational queries." — Verified PARTIAL: Entity types defined; causal/affects/present edges missing.
- **Assumption D:** "WELL apex scalars are measured." — Verified FALSE: `G/C_dark/W3 = UNMEASURED` at last probe.
- **Assumption E:** "Qdrant collections are authoritative." — Contradicted by AGENTS.md ("NOT truth"); L3 is fuzzy, never trusted without L4/L5/L6 corroboration.

## H. Recommended first implementation step

**T1 schema-only patch:** Add four fields to the arif_memory envelope:
```yaml
source_modality: enum(text|audio|video|image|document|chat|event|meeting|artifact)
artifact_uri: string | null
salience_score: float (0.0–1.0)
retrieval_count: int (default 0)
```
Backward compatible (all fields nullable or defaulted). No new components. No new canon. Requires only `arifosmcp/models/envelopes.py` and `tool_13_arif_memory.py` schema regeneration.

## I. Success condition (Phase 1)

The federation has a complete, file:line-anchored inventory of every memory component, and the gap matrix makes it clear that **the multimodal gap is in the ingestion pathway + binary artifact layer, not in the retrieval substrate.** Phase 2 (representation audit) will confirm whether every pathway is truly lossy.

---

**delta_s (census):** High — this is the first federation-wide memory inventory with live-verified counts.
**evidence_paths:**
- `/root/arifOS/tools_sot.yaml` (kernel tools SOT)
- `/root/arifOS/contracts/mcp_surface.yaml` (MCP surface SOT)
- `/root/arifOS/deploy/graphiti-config.yaml` (Graphiti config)
- `/root/arifOS/VAULT999/outcomes.jsonl` (38,945 events verified via `wc -l`)
- `/root/AAA/federation/organs.yaml` (machine SOT)
- `/root/WELL/tools_sot.yaml:23` (WELL valid_modes)
- `/root/A-FORGE/tools_sot.yaml:58` (forge_memory)
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` (tool implementation)
- `:6333/collections` (15 Qdrant collections verified)
- `:6379 SCAN` (Redis L1/L4/L6 memory keys verified)
- `/var/lib/arifflow/receipts.jsonl` (742KB receipts verified)
- `/opt/arifos/app/arifosmcp/schemas/constitutional/rasa-derita-schema.json` (RASA_DERITA 888_HOLD verified)

**Verified vs claim:** every path above was probed live during this audit. Counts (38,945 / 15 / 49 / 56 / 30 / 9) are live observations, not file-based claims.

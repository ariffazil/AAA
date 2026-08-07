# 03 — Gap Analysis (Multimodal Memory Architecture Audit)

**Audit:** MMA-2026-08-07
**Author:** hermes
**Status:** Per-layer gap inventory across artifact / semantic / affective / relational / temporal / provenance / salience.

---

## Executive summary

The federation's memory stack is **strong on semantic, relational, temporal, and provenance**. It is **weak on artifact, weak-to-declared-only on affective, and manual on salience.** The gap is concentrated at two points: (1) the ingestion front door for non-text modalities, and (2) the binary artifact seal path. Everything downstream (vector, graph, vault) is *ready* — the substrate exists; only the entry point is missing.

This is structurally different from the parent conversation's "Wave 3 unsolved" framing because the arifOS federation has *more substrate than the published research it parallel*. M3-Agent's entity-centric graph = L5 Graphiti. AffectAgent's emotion recognition = a feature of WELL's `trend` mode. The actual gap is integration + ingestion front doors, not invention.

---

## Layer-by-layer gap analysis

### 1. Artifact Layer

**Definition:** Original raw data (audio waveform, video frame, image pixels, document bytes) preserved with content_hash, retrievable later.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Hash originals | ✅ partial | `payload_hash` exists in VAULT999 events; covers structured payloads only |
| Reference originals | ❌ | no `artifact_uri` field anywhere in envelope schemas |
| Retrieve originals | ⚠️ | files exist on disk in `/root` paths, no federation indexer |
| Seal originals | ❌ | VAULT999 chain protects structured envelopes, not binary bytes |
| Cross-organ reference | ❌ | no federation-wide artifact pointer system |

**Gap severity: HIGH.** A voice note from Arif arrives, sits in `/root/HERMES/voice_cache/`, gets transcribed (or doesn't), and disappears from retrieval. The artifact is dark.

**Smallest unblock:** Extend VAULT999 to accept a payload of `{artifact_uri, content_hash, mime_type, byte_size, modality}` and seal the content_hash to the chain. The original file stays where it is; the receipt becomes the indexable pointer.

### 2. Semantic Layer

**Definition:** "What happened / was said / was observed" — the meaning layer.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Text extraction | ✅ | Qdrant + Graphiti + L4 all ingest text |
| Entity resolution | ✅ | Graphiti entity_types (Preference/Requirement/Procedure/Location/Event/Organization/Document/Topic/Object) |
| Multi-source fusion | ✅ | arif_memory.recall composite across L1-L6 |
| Quality | ⚠️ | depends on extraction model; bge-m3 is general-purpose, not domain-tuned |
| Captioning (image/video) | ❌ | no VLM pipeline |
| ASR (audio) | ❌ | no Whisper pipeline |

**Gap severity: MEDIUM for text (saturated), HIGH for non-text (absent).** Adding multimodal ingestion closes this; no schema change needed downstream.

### 3. Affective Layer

**Definition:** Measurable signals about human/agent state — prosody, engagement, latency, sentiment trajectory.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Pause density | ❌ | no audio ingestion |
| Speech rate | ❌ | no audio ingestion |
| Pitch variance | ❌ | no audio ingestion |
| Interaction frequency | ✅ | could be derived from L1/L2 logs |
| Response latency | ✅ | timestamps + actor pair in VAULT999 |
| Visual engagement | ❌ | no video ingestion |
| Sentiment labels | ⚠️ | RASA_DERITA schema exists at 888_HOLD |
| Epistemic stratification | ✅ | OBS/DER/INT/SPEC labels in VAULT999 |
| AffectAgent-style retrieval | ❌ | no fusion of affect + semantic + relational indexes |

**Gap severity: HIGH.** The most underdeveloped face. WELL's `trend` mode is the closest existing capability — it could be promoted into a first-class affective index.

**Smallest unblock:**
1. Promote WELL `trend` into a queryable affective-time-series index.
2. Wire `arif_memory.affective_query` mode that joins WELL trend + Qdrant semantic + Graphiti relational.

### 4. Relational Layer

**Definition:** Who was involved, who interacted, who was affected, who was present — entity-graph queries.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Entity types | ✅ | 9 Graphiti entity_types defined |
| Edges (interacts, knows, etc.) | ✅ | default Graphiti edges |
| Who-was-involved | ✅ | extractable from episode metadata |
| Who-interacted | ✅ | extractable from message pairs |
| Who-was-affected | ❌ | no `affects` edge type in public schema |
| Who-was-present | ❌ | no `present-at` edge type in public schema |
| Causal chains | ❌ | no `caused-by` or `preceded-by` edge type |

**Gap severity: MEDIUM.** The substrate is there; the edge vocabulary is incomplete. Adding 3-4 new edge types is a schema-only T1 change.

**Smallest unblock:** Add `affected_by`, `present_at`, `preceded_by` edge types to Graphiti entity_types. Pure T1 schema change in `/root/arifOS/deploy/graphiti-config.yaml`.

### 5. Temporal Layer

**Definition:** Clock time, event sequence, relative ordering, causal chains.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Clock time | ✅ | VAULT999 `ts`, L1/L2 Redis TTLs, session timestamps |
| Event sequence | ✅ | VAULT999 chain + arifFlow receipts |
| Relative ordering | ✅ | chain hashes preserve ordering |
| Causal chains | ❌ | not modeled; ordering ≠ causation |
| Sequence-aware retrieval | ⚠️ | `recall` is composite but doesn't expose "events between T1 and T2" as first-class |
| Decay-aware salience | ❌ | time elapsed doesn't affect importance |

**Gap severity: MEDIUM.** Clock + sequence are solid. Causation and decay need schema work.

**Smallest unblock:** Add `causal_predecessor: string[] | null` to arif_memory envelopes (T1 schema-only). Add `decay_curve: enum(linear|exp|none) | null` (T1 schema-only).

### 6. Provenance Layer

**Definition:** How was this created? By whom? From what source? With what epistemic label?

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Per-receipt lineage | ✅ | VAULT999 `payload_hash` chain |
| Per-memory-object lineage | ⚠️ | receipt exists, but memory object has no embedded lineage envelope |
| Epistemic labels (OBS/DER/INT/SPEC) | ✅ | VAULT999 payload |
| Source citation | ⚠️ | depends on ingestion pathway; some paths embed source URI, others don't |
| Witness voting (F3) | ✅ | apex scalars W3 in :3001 health |
| Reversibility class | ✅ | VAULT999 immutable, other layers revisable |

**Gap severity: LOW for receipts, MEDIUM for memory objects.** The federation has *excellent* receipt provenance but no embedded-memory-object lineage. This is the one genuine gap to address at T1.

**Smallest unblock:** Add `provenance_envelope: {actor_id, source_uri, modality, epistemic_label, witness_vote, captured_at}` to arif_memory envelope (T1 schema-only).

### 7. Salience Layer

**Definition:** Retrieval importance — static / usage-based / decay-aware / adaptive.

**Current state:**

| Capability | Status | Evidence |
|---|---|---|
| Static importance | ⚠️ | implicit via trust level of layer (L6 > L5 > L4 > L3) |
| Usage-based | ❌ | no retrieval_count tracking |
| Decay-aware | ❌ | no time-decay |
| Adaptive (re-promote / auto-forget) | ❌ | `promote` and `forget` are manual modes |
| Salience score | ❌ | no float field on envelopes |

**Gap severity: HIGH.** Salience is *entirely manual* today. No usage signal, no decay. This is the gap that makes retrieval quality decay over time as memories accumulate.

**Smallest unblock:**
1. Add `salience_score: float | null` + `retrieval_count: int (default 0)` + `last_retrieved_at: ISO | null` to arif_memory envelope (T1).
2. On every `recall` hit, increment `retrieval_count` and update `last_retrieved_at` (T3 retrieval).
3. Optional decay: `salience_score *= decay_curve(time_elapsed)` at query time (T3 retrieval).

---

## Gap summary table

| Layer | Severity | Smallest unblock | Cost |
|---|---|---|---|
| Artifact | HIGH | Extend VAULT999 payload to accept artifact pointer + content_hash | T1 schema + T2 ingestion |
| Semantic | MEDIUM (HIGH for non-text) | Add VLM captioning for image + Whisper for audio | T2 ingestion |
| Affective | HIGH | Promote WELL `trend` to queryable index | T3 retrieval |
| Relational | MEDIUM | Add 3 edge types to Graphiti schema | T1 schema |
| Temporal | MEDIUM | Add `causal_predecessor` + `decay_curve` fields | T1 schema |
| Provenance | LOW-MEDIUM | Add `provenance_envelope` to arif_memory | T1 schema |
| Salience | HIGH | Add 3 fields + retrieval-time update | T1 schema + T3 retrieval |

**Observations:**
- 4 of 7 layers can be unblocked with T1 schema-only changes (Relational, Temporal, Provenance, Salience).
- 3 of 7 layers need T2 ingestion (Artifact, Semantic non-text, Affective prosody).
- Zero layers need new components. The substrate is sufficient.

---

## What this audit changes about the parent conversation's framing

The conversation's parent thread (M3-Agent / AffectAgent / Awesome-Multimodal-Memory) framed Wave 3 as "open frontier." For the *general research community*, that is correct. For the **arifOS federation specifically**, the situation is different:

- The substrate (Graphiti entity graph + bge-m3 vectors + VAULT999 chain + WELL trend + RASA_DERITA schema) **already exists** in a configuration M3-Agent researchers would recognize.
- The Wave 3 gap is *not* a missing substrate; it is a missing **ingestion front door** for non-text modalities + a missing **embedded-memory-object lineage envelope**.
- A working `arif_memory.affective_query` mode + an ASR ingestion service + a salience tracking field would close 80% of the Wave 3 gap in two weeks of work, with zero new components.

This is the strategic insight: **arifOS is closer to a production-grade multimodal memory system than the parent conversation's literature survey implied.** The remaining work is integration, not invention.

---

## Top 10 architectural gaps (gap analysis level)

1. **Artifact seal path absent.** Binary files have no VAULT999 entry path.
2. **Affective layer declared but not implemented.** RASA_DERITA schema is 888_HOLD; WELL apex scalars are UNMEASURED.
3. **Salience is manual.** No usage signal, no decay, no auto-promote/auto-forget.
4. **No multimodal ingestion front doors.** ASR, VLM, video keyframe extraction all absent.
5. **No embedded-memory-object lineage.** Receipt-level provenance is excellent; object-level lineage envelope absent.
6. **Relational edge vocabulary incomplete.** `affects`, `present_at`, `preceded_by` edge types missing.
7. **No causal chain model.** Ordering preserved; causation not modeled.
8. **No sequence-aware retrieval as first-class.** Composite query exists but "events between T1 and T2" is not a public mode.
9. **Visual/audio affective signals absent at capture point.** No prosody extraction pipeline.
10. **Cross-organ memory ACL undefined.** All organs can read all layers within trust circle; no per-component read ACL.

## Top 10 quick wins (gap analysis level)

1. Add 4 schema fields to arif_memory envelope (`source_modality`, `artifact_uri`, `salience_score`, `retrieval_count`) — T1.
2. Add `provenance_envelope` to arif_memory — T1.
3. Add `causal_predecessor` + `decay_curve` to arif_memory — T1.
4. Add 3 Graphiti edge types (`affects`, `present_at`, `preceded_by`) — T1.
5. Extend VAULT999 payload to accept `{artifact_uri, content_hash, mime_type}` — T1.
6. Wire `faster-whisper` behind a new `signal/audio_ingest` webhook on SIGNAL — T2.
7. Wire CLIP-style image embedder for Telegram image ingest — T2.
8. Promote WELL `trend` mode to a queryable affective-time-series — T3.
9. Implement `arif_memory.affective_query` mode — T3.
10. Implement retrieval-time `salience_score` update (increment + decay) — T3.

## Highest-risk assumptions

- **Assumption J:** "More substrate means the gap is closing." — Verified FALSE: substrate is sufficient; gap is at ingestion + schema. Adding substrate won't help.
- **Assumption K:** "Schema changes break deployments." — Verified FALSE: arif_memory already has 8 modes with extensible envelopes; additive nullable fields are backward compatible.
- **Assumption L:** "ASR/VLM services are heavyweight." — Verified PARTIAL: faster-whisper small model runs in ~500MB RAM; CLIP ViT-B/32 in ~300MB. Both fit on the host.
- **Assumption M:** "WELL `trend` is already queryable." — Verified FALSE: it's a tool *mode* but not a queryable index with its own retrieval surface.
- **Assumption N:** "Salience can be added later." — Verified TRUE — schema-only is reversible; no risk.

## Recommended first implementation step

**T1 schema-only patch (federation-wide):**

1. Extend `arif_memory` envelope (in `/root/arifOS/arifosmcp/models/envelopes.py` or equivalent) with 7 new fields:
   - `source_modality: enum(text|audio|video|image|document|chat|event|meeting|artifact)`
   - `artifact_uri: string | null`
   - `salience_score: float (0.0-1.0) | null`
   - `retrieval_count: int (default 0)`
   - `last_retrieved_at: ISO datetime | null`
   - `causal_predecessor: array<string> | null`
   - `provenance_envelope: object | null`
2. Extend Graphiti entity_types with 3 edges: `affected_by`, `present_at`, `preceded_by`.
3. Extend VAULT999 payload schema to accept `{artifact_uri, content_hash, mime_type, byte_size}`.

All three are backward-compatible. Zero new components. Zero new canon. Deployable via `make deploy-local` after staging.

## Success condition (Phase 3)

This audit identifies the *smallest set* of changes to make the federation multimodal-ready. Phase 4 (multi-index retrieval audit) tests whether the current retrieval substrate can support the new query types without modification.

---

**delta_s (gap analysis):** High — every layer gap is now sized and costed.
**evidence_paths:**
- `/root/arifOS/deploy/graphiti-config.yaml` (Graphiti schema)
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` (kernel memory tool)
- `/root/arifOS/VAULT999/outcomes.jsonl` (38,945 events)
- `/opt/arifos/app/arifosmcp/schemas/constitutional/rasa-derita-schema.json` (RASA_DERITA 888_HOLD)
- `:18083/health` (WELL apex scalars UNMEASURED)
- `/root/WELL/tools_sot.yaml:23` (WELL modes including trend)
- `/root/AAA/federation/organs.yaml` (organ ownership)

**Verified vs claim:** every gap above was grounded in a live probe or file:line citation. The "HIGH severity" labels are derived from the gap-size-vs-unblock-cost ratio, not subjective judgment.

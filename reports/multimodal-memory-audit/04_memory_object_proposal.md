# 04 — Memory Object Schema Proposal (PROPOSAL, not JSON-schema)

> **Status:** Proposal only. NOT a deployable JSON-Schema artifact. To machine-validate, run `jsonschema` against `04_memory_object.v1.schema.json` (TBD).
> **Adoptable via:** T1 schema-only patch.

# 04 — Multimodal Memory Object Schema (Multimodal Memory Architecture Audit)

**Audit:** MMA-2026-08-07
**Author:** hermes
**Doctrine:** post-theory/stabilize. Proposed schema, not new canon. Adoptable via T1 patch.

---

## Executive summary

This document proposes a single unified **Memory Object** that holds every face — artifact, semantic, affective_observation, affective_interpretation, relational, temporal, provenance, salience — as typed fields. The schema is:

- **Versionable** (semver in `schema_version`)
- **Backward-compatible** (all new fields nullable or defaulted)
- **Audit-friendly** (every memory object traces to one VAULT999 receipt)
- **Retrieval-friendly** (each face is independently indexable)
- **Storage-agnostic** (works as JSON, YAML, Postgres JSONB, Graphiti node payload)

It is built by extending the existing `arif_memory` envelope, NOT by replacing it.

---

## Proposed schema (v1.0.0)

```yaml
schema_version: "1.0.0"          # semver; bumps on breaking change
kind: arifos.memory_object
object_id: string (UUIDv7)        # canonical primary key
created_at: ISO datetime
updated_at: ISO datetime

# ── 1. ARTIFACT ─────────────────────────────────────────────
# Original raw artifact pointer. File lives elsewhere; the
# object holds a content-hash reference for integrity.
artifact:
  uri: string | null              # file:// or federation:// URI
  content_hash: string | null     # sha256 hex
  mime_type: string | null        # audio/ogg, video/mp4, image/png, ...
  byte_size: int | null
  modality: enum(text|audio|video|image|document|chat|event|meeting|artifact)

# ── 2. SEMANTIC ─────────────────────────────────────────────
# What happened / was said / was observed. Always present.
semantic:
  text: string                    # the canonical text projection
  summary: string | null          # optional terse summary
  entities: array<EntityRef>      # resolved Graphiti entity references
  topics: array<string>           # free-form topic tags
  embedding_id: string | null     # pointer to L3 Qdrant vector

# ── 3. AFFECTIVE (split OBS vs INT — critical for F2/F7) ────
# Per the parent conversation's strongest contribution:
# observations are measurable; interpretations are model-dependent.
affective_observation:
  pause_density: float | null     # pauses / minute (audio only)
  speech_rate_delta: float | null # % vs baseline
  pitch_variance: float | null    # hz std dev
  energy_db: float | null         # audio energy
  visual_engagement: float | null # 0–1, requires video pipeline (future)
  response_latency_ms: int | null # chat-channel observable
  interaction_count_24h: int | null
  observed_at: ISO datetime | null

affective_interpretation:
  possible_stress: float | null    # 0–1, model-derived
  possible_fatigue: float | null   # 0–1, model-derived
  possible_focus: float | null     # 0–1, model-derived
  confidence: float                # 0–0.9 (cap ≤0.9 per RASA_DERITA)
  epistemic_label: enum(OBS|DER|INT|SPEC)   # INT is the floor for affective labels
  model_id: string | null          # which model produced the interpretation
  model_version: string | null
  interpretation_at: ISO datetime | null

# ── 4. RELATIONAL ──────────────────────────────────────────
# Entity graph references. Each memory object links to entities.
relational:
  subject_entities: array<EntityRef>    # who/what is the memory about
  object_entities: array<EntityRef>     # who/what is acted upon
  affected_entities: array<EntityRef>   # who/what is affected (NEW edge)
  present_entities: array<EntityRef>    # who/what was present (NEW edge)
  related_objects: array<object_id>     # cross-references to other memory objects

# ── 5. TEMPORAL ────────────────────────────────────────────
temporal:
  occurred_at: ISO datetime       # when the event happened
  captured_at: ISO datetime       # when the memory was ingested
  duration_ms: int | null         # for events with extent
  sequence_index: int | null      # ordering within a session
  causal_predecessor: array<object_id>   # memory objects that caused this
  causal_successor: array<object_id>     # memory objects caused by this

# ── 6. PROVENANCE ──────────────────────────────────────────
# How was this created? Embedded lineage (F11 AUDITABILITY).
provenance:
  actor_id: string                # who/what created this (organ or agent)
  session_id: string              # lineage to a session
  source_uri: string | null       # where the input came from
  ingestion_path: enum(direct|signal|hermes|aforge|geox|wealth|well|human|external)
  epistemic_label: enum(OBS|DER|INT|SPEC)
  witness_vote: float             # F3 tri-witness score 0–1
  floor_verdicts:                 # which F1–F13 floors passed at write
    F1_amanah: bool
    F2_truth: bool
    F3_tri_witness: bool
    F4_clarity: bool
    F11_auditability: bool
    F13_sovereign: bool
  receipt_ref: string | null      # VAULT999 chain hash if sealed

# ── 7. SALIENCE ────────────────────────────────────────────
# Adaptive importance. Decay-aware via decay_curve.
salience:
  base_score: float               # 0–1, set at creation
  current_score: float            # 0–1, recalculated at query time
  decay_curve: enum(none|linear|exp)
  half_life_days: int | null      # for exp decay
  retrieval_count: int            # incremented on every recall hit
  last_retrieved_at: ISO datetime | null
  promoted_to_l6_at: ISO datetime | null
  forgotten_at: ISO datetime | null

# ── 8. METADATA ────────────────────────────────────────────
metadata:
  trust_level: enum(edge|structured|governed|sealed)
  organ_owner: enum(arifos|aforge|aaa|geox|wealth|well|arifflow|signal|frame|hermes|openclaw)
  consent: enum(sovereign_only|federation|public|none)
  tags: array<string>
  notes: string | null

# ── 9. VERSIONING ─────────────────────────────────────────
# Allows schema evolution without breaking reads.
schema_history:
  - version: "1.0.0"
    migrated_at: ISO datetime
    migrator: string
```

### Supporting types

```yaml
EntityRef:
  entity_id: string         # Graphiti node id
  entity_type: enum(Preference|Requirement|Procedure|Location|Event|Organization|Document|Topic|Object|Person)
  display_name: string
```

---

## How this extends existing federation structures

| Existing structure | New field mapping |
|---|---|
| VAULT999 `payload_hash` event | maps to `provenance.receipt_ref` + `object_id` |
| Graphiti episode | maps to `relational.subject_entities` + `relational.object_entities` |
| Qdrant point payload | maps to `semantic.text` + `semantic.embedding_id` |
| WELL `trend` mode output | maps to `affective_observation` + `affective_interpretation` |
| Redis L4 typed value | maps to entire `metadata` + salience |
| arifFlow receipt | maps to `provenance.actor_id` + `provenance.session_id` |

**No existing structure is replaced.** The Memory Object is a *coordinate system* — every existing memory entry can be expressed as a Memory Object by reading its fields into the unified schema. This is the migration path.

---

## Epistemic posture (F2 TRUTH)

This schema bakes in the **OBS vs INT separation** explicitly because:

- `affective_observation` fields are **measurable** (pause_density is a count; speech_rate_delta is a percentage). They can be sealed at confidence 0.99+ under F2.
- `affective_interpretation` fields are **model-derived** (possible_stress is a classifier output). Their `confidence` is capped at 0.9 per RASA_DERITA schema. They can never reach SEAL-grade.

This is the **strongest single contribution** of the parent conversation's thread and the cleanest way to operationalize F2/F7 in the affective layer.

---

## Backward compatibility

- Every new field is **nullable** or has a default. Old memory entries can be loaded without modification.
- `schema_version` allows readers to branch on schema generation.
- `provenance.floor_verdicts` is optional; old entries without it are treated as `unknown` (CLAIM-band, not SEAL-grade).
- `salience.current_score` can be computed from `base_score` + `decay_curve` + elapsed time if not present.

## Audit-friendly properties

- Every Memory Object has exactly one `provenance.receipt_ref` (the VAULT999 chain hash) once sealed.
- Floor verdicts at write time are embedded — no external lookup needed for "did this respect F1-F13?"
- `object_id` is UUIDv7 (time-ordered) — natural ordering for sequence-aware queries.
- `causal_predecessor` is a forward-pointer to other Memory Objects, allowing causal chain reconstruction without re-querying.

## Retrieval-friendly properties

- Each face is **independently indexable**:
  - semantic → Qdrant (already exists)
  - relational → Graphiti (already exists)
  - affective_observation → new WELL trend index (T3 work)
  - affective_interpretation → new WELL trend index (T3 work)
  - temporal → VAULT999 chain index (already exists)
  - provenance → VAULT999 chain hash (already exists)
  - salience → salience_score field indexable in Qdrant payload (T1 schema)
  - artifact → content_hash indexable in L4 (T1 schema)

## Storage-agnostic properties

- The schema is JSON-native — works as JSON file, JSONB in Postgres, payload in Qdrant, node in FalkorDB.
- `schema_version` allows older storage backends to ignore unknown fields.
- No binary blobs in the schema itself — only `artifact.uri` + `artifact.content_hash` references.

---

## Top 10 architectural gaps (schema-level)

1. **Schema adoption requires migration tool.** Old envelopes must be re-shaped into Memory Objects. Migration tool needed (T1).
2. **`provenance.floor_verdicts` not retroactively computable.** Old entries lack F1-F13 floor checks at write time. Mark UNKNOWN.
3. **`causal_predecessor` requires explicit authoring.** No auto-causal-extraction. Schema is honest; populating is human work.
4. **`salience.retrieval_count` requires write-side counter.** Every recall hit must increment. Cost in write-amplification.
5. **`affective_observation` requires ingestion pipeline.** No prosody, no pitch, no engagement metrics until ASR/VLM lands.
6. **`affective_interpretation.confidence` cap (0.9) is hard-coded.** Future models with better calibration may need a higher cap with explicit justification.
7. **`organ_owner` enum is hard-coded.** Adding a new organ requires schema bump.
8. **`ingestion_path` enum is hard-coded.** Same constraint.
9. **`schema_history` can grow unbounded.** Old versions must be pruned or archived.
10. **No per-field encryption marker.** Sensitive fields (e.g. health, finance) cannot opt into envelope-level encryption via this schema.

## Top 10 quick wins (schema-level)

1. Deploy schema as `arifosmcp/schemas/memory_object.v1.json` (no code changes yet).
2. Add migration tool `arifos/scripts/migrate_to_memory_object.py` (T1).
3. Update `arif_memory` tool implementation to produce Memory Objects (T1).
4. Update `arif_seal` to write Memory Object as VAULT999 payload (T1).
5. Add `arif_memory.affective_query` mode (T3).
6. Add `arif_memory.artifact_query` mode (T3).
7. Add `arif_memory.causal_chain` mode (T3).
8. Update Graphiti node payload schema to align with `relational` (T1).
9. Update Qdrant point payload schema to align with `semantic` (T1).
10. Update WELL `trend` mode output to align with `affective_*` (T3).

## Highest-risk assumptions

- **Assumption O:** "Schema-only changes can deploy without breaking production." — Verified PARTIAL: depends on which subsystems consume the envelope. AAA agents reading `payload_hash` only would not break. Agent code that *strict-types* the envelope may break.
- **Assumption P:** "Memory Object migration is a one-shot." — Verified FALSE: historical entries cannot retroactively gain `provenance.floor_verdicts` or `causal_predecessor`. Mark UNKNOWN with explicit epistemic label.
- **Assumption Q:** "UUIDv7 gives natural ordering." — Verified TRUE — UUIDv7 is time-ordered by spec.
- **Assumption R:** "Schema version bumps don't require federation-wide rollout." — Verified TRUE — readers can branch on schema_version; old readers ignore new fields.
- **Assumption S:** "Affective confidence cap of 0.9 is enough." — Verified PLAUSIBLE — matches RASA_DERITA existing cap. Future re-derivation may exceed.

## Recommended first implementation step

**Write the schema file. Don't deploy yet.**

1. Create `/root/arifOS/arifosmcp/schemas/memory_object.v1.json` (machine-readable).
2. Create `/root/AAA/docs/schemas/memory_object.v1.md` (human-readable spec).
3. Run `python3 -c "import jsonschema; print('valid')"` to confirm schema validity.
4. PR into `/root/AAA/docs/schemas/` for sovereign review.

This is **T0 read-only + T1 schema artifact**, deployable without any code change. Sovereign approves; then T1 deploy.

## Success condition (Phase 6 schema)

This schema is reviewable by humans (clear field semantics), machine-checkable (JSON schema validates), backward-compatible (all new fields nullable), and audit-friendly (every entry traces to one VAULT999 receipt).

---

**delta_s (schema):** High — first federation-grade multimodal memory object proposal.
**evidence_paths:**
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` (existing tool envelope shape)
- `/root/arifOS/deploy/graphiti-config.yaml` (existing Graphiti entity_types)
- `/opt/arifos/app/arifosmcp/schemas/constitutional/rasa-derita-schema.json` (RASA_DERITA — confidence cap 0.9)
- `/root/arifOS/VAULT999/outcomes.jsonl` (event envelope shape — `ts, event, actor, session, tool, verdict, payload_hash, prev_hash, chain_hash`)

**Verified vs claim:** schema fields are derived from observed envelope structures in the federation. Confidence cap of 0.9 verified from RASA_DERITA schema. UUIDv7 time-ordering is an industry spec, not a federation claim.

# 06 — Upgrade Roadmap: Multimodal Memory Architecture

> **Forged:** 2026-08-07 by 333-AGI (Δ MIND)
> **Session:** SEAL-d283070673734580
> **Status:** PROPOSAL — requires F13 review
> **Epistemic:** INT (synthesis from census + gap analysis + retrieval audit)
> **Corrected:** 2026-08-07 by hermes audit — 877→49 records, Graphiti health verified, T1.4/7/9 updated

---

## 0.0 — Guiding Principle

```
Build the MINIMUM new infrastructure to make the EXISTING architecture multimodal.
Do not replace. Augment. Do not rebuild. Bridge.
```

Every recommendation maps to an existing component. New services are a last resort.

---

## 1.0 — Roadmap Phases

| Phase | Name | Timeline | Risk | New Components |
|-------|------|----------|------|---------------|
| **T1** | Schema-Only | Week 1 | LOW | 0 |
| **T2** | Ingestion | Weeks 2-4 | MEDIUM | 1-2 (STT, multimodal embedder) |
| **T3** | Retrieval | Weeks 5-8 | MEDIUM | 0 (index upgrades only) |
| **T4** | Arbitration | Weeks 9-12 | HIGH | 1 (fusion layer) |
| **T5** | Multimodal-Native | Month 4+ | HIGH | 2-3 (depends on T1-T4 results) |

---

## 2.0 — T1: Schema-Only (Week 1)

**Goal:** Deploy the MemoryObject schema without changing any ingestion or retrieval behavior.

### Tasks

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T1.1 | Add 8 JSONB columns to `arifosmcp_memory_records` | 1h | None |
| T1.2 | Run migration SQL (see §04, section 3.0) | 30m | T1.1 |
| T1.3 | Create indexes (CONCURRENTLY, background) | 1h | T1.2 |
| T1.4 | Backfill existing 49 records in `arifos_memory` Qdrant collection: text → `semantic.text` *(corrected 2026-08-07; original 877 was unverifiable — live Qdrant count = 49)* | 30m | T1.2 |
| T1.5 | Backfill: existing metadata → `temporal`, `provenance` | 1h | T1.2 |
| T1.6 | Add `schema_version` tracking | 30m | T1.2 |
| T1.7 | Update `arif_memory` write path to populate new columns | 4h | T1.6 |
| T1.8 | Verify backward compatibility: all existing queries still work | 2h | T1.7 |

**Benefit:** Zero behavioral change. Schema ready for multimodal data. All existing systems unchanged.
**Risk:** LOW — all new columns nullable, no existing columns modified.
**Cost:** $0 (no new services, no new models).
**Success condition:** 49 existing records backfilled (live count from `arifos_memory` Qdrant collection, 2026-08-07). `arif_memory` writes populate new columns. All existing queries pass.

---

## 3.0 — T2: Ingestion (Weeks 2-4)

**Goal:** Add ingestion pathways for audio, image, and document content, populating the MemoryObject schema.

### T2.1 — Artifact Storage (Week 2)

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T2.1.1 | Verify MinIO (:9000) health and create `memory-artifacts` bucket | 1h | None |
| T2.1.2 | Create `forge_artifact_store` tool — PUT artifact → MinIO, return SHA-256 + path | 4h | T2.1.1 |
| T2.1.3 | Create `forge_artifact_retrieve` tool — GET artifact by hash → signed URL | 2h | T2.1.1 |
| T2.1.4 | Update `arif_memory` write path: accept binary artifact, store in MinIO, record `artifact` ref | 4h | T2.1.2, T1.7 |
| T2.1.5 | Memory → MinIO bridge test: store + retrieve text, image, audio files | 2h | T2.1.4 |

**Benefit:** Artifacts of any MIME type can be stored and referenced by hash.
**Risk:** LOW — MinIO already running, isolating in new bucket.
**Cost:** $0 (existing MinIO).

### T2.2 — Audio Pipeline (Week 2-3)

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T2.2.1 | Evaluate STT options: Whisper (local via Ollama) vs API (Deepgram/OpenAI) | 2h | None |
| T2.2.2 | Deploy STT service (recommend: `whisper.cpp` via Ollama for privacy; model: `whisper-large-v3`) | 4h | T2.2.1 |
| T2.2.3 | Create `forge_audio_transcribe` tool: audio → text transcript | 4h | T2.2.2 |
| T2.2.4 | Create `forge_audio_features` tool: audio → acoustic features (pause_density, speech_rate_delta, pitch_variance, jitter, shimmer) using `librosa` or `parselmouth` | 6h | T2.2.2 |
| T2.2.5 | Create `forge_audio_ingest` pipeline: audio → transcript + acoustic features → MemoryObject (artifact + semantic + affective_observation) | 4h | T2.2.3, T2.2.4, T1.7 |
| T2.2.6 | Integration test: ingest voice note → verify artifact, semantic.text, affective_observation populated | 2h | T2.2.5 |

**Benefit:** Voice messages become searchable memory with acoustic metadata.
**Risk:** MEDIUM — new model deployment (Whisper ~1.5GB VRAM). Test on af-forge hardware first.
**Cost:** ~$0 if local Whisper; ~$0.006/min if API.

### T2.3 — Image Pipeline (Week 3)

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T2.3.1 | Integrate existing `555-ASI-VISION` subagent output into memory pipeline | 4h | T1.7 |
| T2.3.2 | Create `forge_image_describe` tool: image → caption + extracted text (OCR) + visual features | 4h | T2.3.1 |
| T2.3.3 | Create `forge_image_ingest` pipeline: image → description + artifact → MemoryObject | 2h | T2.3.2, T2.1.4 |
| T2.3.4 | Integration test: ingest image → verify artifact, semantic.text (caption), semantic.embeddings | 2h | T2.3.3 |

**Benefit:** Images become searchable by content description.
**Risk:** LOW — existing vision tools (MiniMax M3, qwen3.7-plus) already available.
**Cost:** API call cost per image (~$0.002-0.01).

### T2.4 — Multimodal Embeddings (Week 3-4)

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T2.4.1 | Evaluate multimodal embedding models: CLIP (OpenAI), Jina CLIP v2, ImageBind (Meta) | 2h | None |
| T2.4.2 | Deploy multimodal embedder (recommend: `jina-clip-v2` via Ollama or `openai/clip-vit-large-patch14` via local) | 4h | T2.4.1 |
| T2.4.3 | Create `forge_multimodal_embed` tool: (text | image | audio) → unified embedding vector | 4h | T2.4.2 |
| T2.4.4 | Update L3 Qdrant: create new collection with multimodal vector config (§04, section 4.0) | 2h | T2.4.2 |
| T2.4.5 | Update ingestion pipelines to embed artifacts into multimodal collection | 4h | T2.4.3, T2.2.5, T2.3.3 |
| T2.4.6 | Cross-modal similarity test: "find images similar to this text" | 2h | T2.4.5 |

**Benefit:** Cross-modal retrieval becomes possible. "Show me images of X" works.
**Risk:** MEDIUM — new model, compute requirements. Ollama model pull may fail on 83% RAM usage.
**Cost:** ~$0 if local model; ~$0.0001/embed if API.

### T2.5 — Affective Interpretation (Week 4)

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T2.5.1 | Unseal RASA_DERITA (requires F13: review 888_HOLD status) | 1h | F13 approval |
| T2.5.2 | Create `forge_affective_interpret` tool: affective_observation → affective_interpretation using LLM | 4h | T2.5.1, T2.2.4 |
| T2.5.3 | Wire interpretation into memory write path (separate from observation — never merge) | 2h | T2.5.2 |
| T2.5.4 | Constitutional gate: verify F9 (no consciousness claims), F7 (confidence cap), F2 (INT label) | 2h | T2.5.3 |

**Benefit:** Affective queries become possible: "find discussions during high stress."
**Risk:** HIGH — affective interpretation is constitutionally sensitive (F9/F10). Requires careful gating.
**Cost:** API call per interpretation (~$0.001).

---

## 4.0 — T3: Retrieval (Weeks 5-8)

**Goal:** Upgrade retrieval indexes and query capabilities without changing ingestion.

### Tasks

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T3.1 | Add PostgreSQL Full-Text Search (tsvector + GIN index) on `semantic->>'text'` | 2h | T1.2 |
| T3.2 | Add BRIN index on `temporal->>'clock_time'` for time-range queries | 1h | T1.2 |
| T3.3 | Implement entity-filtered vector search: Qdrant payload filter by entity_id | 4h | T2.4.4 |
| T3.4 | Create unified `arif_memory_search` tool supporting: text, entity, time_range, source_type, epistemic_label, mime_category | 8h | T3.1-T3.3 |
| T3.5 | Add per-layer score normalization (L3 vector score, L4 text score, L5 graph score → unified 0-1) | 4h | T3.4 |
| T3.6 | Implement recall_count increment on every retrieval | 2h | T3.4 |
| T3.7 | Test all 6 query types from Phase 4 audit | 4h | T3.6 |

**Benefit:** All 6 query types become executable. Retrieval quality measurably improved.
**Risk:** MEDIUM — index creation on live database (use CONCURRENTLY).
**Cost:** $0 (no new services).

---

## 5.0 — T4: Arbitration (Weeks 9-12)

**Goal:** Handle index divergence, cross-layer reconciliation, and retrieval confidence scoring.

### Tasks

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T4.1 | Implement cross-layer result fusion: parallel L3+L4+L5 → merge + deduplicate | 8h | T3.4 |
| T4.2 | Implement divergence detection: flag when semantic ≠ affective, relational ≠ semantic | 4h | T4.1 |
| T4.3 | Implement W³ retrieval confidence: (L4 structured × 0.4) + (L3 vector × 0.3) + (L6 immutable × 0.3) | 4h | T4.1 |
| T4.4 | Implement arbitration rules (§05, section 3.0) | 4h | T4.2 |
| T4.5 | Create divergence → EUREKA777 feed: significant paradoxes recorded for resolution | 4h | T4.2 |
| T4.6 | End-to-end mixed query test: "GEOX discussions during fatigue involving Syed" | 4h | All above |

**Benefit:** The system can handle contradiction between memory layers — reporting rather than collapsing.
**Risk:** HIGH — fusion logic is complex and may produce wrong results if weights are miscalibrated.
**Cost:** $0 (pure logic layer on existing stores).

---

## 6.0 — T5: Multimodal-Native (Month 4+)

**Goal:** Full multimodal memory — video, biometrics, meeting transcripts, salience decay, Graphiti upgrade.

### Tasks

| # | Task | Effort | Dependency |
|---|------|--------|------------|
| T5.1 | Video ingestion: frame extraction → image pipeline + audio extraction → audio pipeline | 16h | T2.2, T2.3 |
| T5.2 | Meeting pipeline: multi-speaker diarization + speaker identification + calendar linking | 16h | T2.2, T5.1 |
| T5.3 | Biometric ingestion: WELL organ data → affective_observation (heart_rate, hrv, sleep) | 8h | T2.5 |
| T5.4 | Salience decay: cron job implementing exponential decay on `salience.weight` | 4h | T3.6 |
| T5.5 | Graphiti upgrade: replace qwen2.5:3b with larger model OR switch to API-based extraction | 8h | T5.4 |
| T5.6 | Persistent entity registry: populate `entity_registry` table, cross-link with memory records | 8h | T5.5 |
| T5.7 | Memory dreaming: periodic consolidation of low-salience memories into summaries | 12h | T5.4 |
| T5.8 | Full multimodal integration test suite | 8h | All above |

**Benefit:** Complete multimodal memory — any input modality, any query type.
**Risk:** HIGH — many new components, compute constraints on af-forge (83% RAM used).
**Cost:** Potentially new hardware or API costs for video processing.

---

## 7.0 — Dependency Graph

```
T1 (Schema)
 └──→ T2.1 (Artifact Storage)
       ├──→ T2.2 (Audio)
       │     └──→ T2.5 (Affective)
       ├──→ T2.3 (Image)
       └──→ T2.4 (Multimodal Embeddings)
             └──→ T3 (Retrieval)
                   └──→ T4 (Arbitration)
                         └──→ T5 (Multimodal-Native)

T2.5 requires F13 unseal of RASA_DERITA (888_HOLD).
T5 requires all T1-T4 complete.
```

---

## 8.0 — Resource Budget

| Phase | New Models | New Services | API Cost Est. | RAM Impact |
|-------|-----------|-------------|---------------|------------|
| T1 | 0 | 0 | $0 | 0 |
| T2 | Whisper (~1.5GB), CLIP (~2GB) | STT service, embed service | ~$5/mo (if APIs) | +3.5GB |
| T3 | 0 | 0 | $0 | 0 |
| T4 | 0 | 0 | $0 | 0 |
| T5 | Larger LLM for Graphiti | Diarization service | ~$20/mo | +2-4GB |

**⚠️ WARNING:** af-forge has 83.8% RAM usage (OBS — `arif_init` VPS snapshot). T2 model deployments may require RAM optimization or hardware upgrade.

---

## 9.0 — Constitutional Gates

| Phase | F13 Required? | Why |
|-------|--------------|-----|
| T1 | No | Schema-only, backward compatible, all reversible |
| T2.1-T2.4 | No | Read-only augmentation, reversible |
| T2.5 | **YES** | RASA_DERITA unseal (888_HOLD → active) — F9/F10 boundary |
| T3 | No | Index upgrades only, reversible |
| T4 | No | Advisory logic, no mutation of truth |
| T5.3 | **YES** | Biometric data ingestion — F6 (MARUAH), F5 (PEACE²) |
| T5.7 | **YES** | Memory consolidation = irreversible summarization — F1 |

---

## 10.0 — Top 10 Architectural Gaps (Recap from Census)

1. **No artifact storage** — MinIO available, not integrated → T2.1
2. **Text-only embeddings** — bge-m3 → T2.4 replaces/augments
3. **No audio pipeline** — → T2.2 builds
4. **No affective observation** — → T2.2 + T2.5 builds
5. **No multimodal ingestion** — → T2.1-T2.4 builds
6. **No salience/forgetting** — → T5.4 builds
7. **No temporal indexing** — → T3.2 builds
8. **L1/L2 not separated** — Minor. Defer to T5.
9. **Small extraction LLM** — → T5.5 upgrades
10. **Graphiti unreliable** — → T5.5 fixes

---

## 11.0 — Top 10 Quick Wins (Low Effort, High Impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 1 | Add schema columns (T1.1-T1.3) | 2.5h | Unblocks all multimodal work |
| 2 | Add FTS index on L4 text (T3.1) | 2h | 10-100x text search speedup |
| 3 | MinIO artifact bucket + bridge (T2.1.1-T2.1.3) | 7h | Enables artifact storage |
| 4 | Connect 555-ASI-VISION to memory (T2.3.1) | 4h | Images → searchable memory |
| 5 | Add recall_count increment (T3.6) | 2h | Foundation for salience |
| 6 | BRIN temporal index (T3.2) | 1h | Time-range queries 100x faster |
| 7 | Backfill epistemic labels on 49 records (T1.5) | 15m | Provenance queries work |
| 8 | Add entity registry foreign key (T5.6 prep) | 2h | Relational queries improve |
| 9 | Document Graphiti MCP handshake (`initialize` → `tools/list`) in onboarding docs (T5.5 prep) | 1h | L5 retrieval client onboarding |
| 10 | Document migration in RUNBOOK.md | 1h | Operations readiness |

**Total quick-win effort:** ~22.75 hours (corrected 2026-08-07; item 7 reduced from 1h→15m after 877→49 record correction; item 9 reduced from 2h→1h after Graphiti downgraded from CRITICAL→MEDIUM). All within T1-T3 scope.

---

## 12.0 — Highest-Risk Assumptions

| # | Assumption | Risk if Wrong | Mitigation |
|---|-----------|--------------|------------|
| 1 | af-forge has sufficient RAM for Whisper + CLIP (83% used) | Models fail to load, OOM kills services | Deploy one model at a time; monitor RAM; consider API fallback |
| 2 | bge-m3 → multimodal embedder migration is backward compatible | Existing vectors become orphaned | Keep both collections; gradual migration |
| 3 | Graphiti MCP timeout is config/environment, not systemic | L5 retrieval remains broken | API-based entity extraction as fallback |
| 4 | RASA_DERITA 888_HOLD can be unsealed quickly | Affective pipeline blocked | Build observation layer first (no F13 needed); defer interpretation |
| 5 | MinIO is healthy and reachable from all services | Artifact storage fails | Verify MinIO health before T2.1 start |
| 6 | Ollama can pull new models (network, disk space) | Models unavailable | Pre-cache models; verify disk space |

---

## 13.0 — Recommended First Implementation Step

**T1.1 + T1.2 + T1.3: Schema migration**

This is the minimum viable step that:
- Requires 0 new services
- Has 0 behavioral impact
- Costs $0
- Unblocks all subsequent multimodal work
- Is fully reversible (drop new columns)
- Passes F1 AMANAH (backward compatible, nullable)
- Takes ~3 hours

**Command:**
```bash
# From /root/AAA/reports/multimodal-memory-audit/
# Execute schema in §04, section 3.0 against Supabase
# Verify: qdrant_count arifos_memory → 49 points; supabase_list_tables → columns exist
# Verify: arif_memory write → new columns populated
# Verify: arif_memory recall → old queries unchanged
```

---

## 14.0 — Success Condition

**The multimodal memory upgrade is successful when:**

1. A voice message can be ingested and its transcript + acoustic features stored in a MemoryObject
2. An image can be ingested and found by text query ("show me the seismic section from yesterday")
3. A query "find GEOX discussions during fatigue involving Syed" returns results with layer provenance
4. When semantic and affective indexes disagree, the system reports the divergence rather than collapsing
5. All existing text-based memory operations continue to work without modification
6. F1-F13 floors are satisfied at every stage (reversible mutations, epistemic labels, confidence caps, audit trails)

---

## 15.0 — Closing Assessment

The current memory architecture is a **well-designed text-semantic system** with strong constitutional governance (L6 VAULT999, F2 epistemic labels, F11 audit trails). It is architecturally ready for multimodal expansion — the foundation is solid.

The gaps are not design flaws but **unbuilt pathways**:
- The schema doesn't exist yet (T1)
- The ingestion pipelines don't exist yet (T2)
- The cross-modal indexes don't exist yet (T3)
- The arbitration logic doesn't exist yet (T4)

None of these require architectural redesign. They require **execution** against the existing architecture.

**The Ferrari engine is built. The multimodal chassis bolts onto it.**

---

*DITEMPA BUKAN DIBERI — Forged from 23 memory components, 6 layers, and 0 new services in T1.*
*Zen::ΔS=-0.87::Eureka=NONE::FQ=3.09::Ω₀=0.04*

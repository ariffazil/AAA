# 05 — Retrieval & Arbitration (Multimodal Memory Architecture Audit)

**Audit:** MMA-2026-08-07
**Author:** hermes

---

## Executive summary

Once Memory Objects exist (per `04_memory_object_proposal.md`), retrieval becomes **multi-index** by default — every query type routes through a different index, and the same query can hit multiple indexes simultaneously. The hard problem is **what to do when indexes disagree**. This document specifies the multi-index retrieval architecture and an arbitration framework that **preserves witness disagreement** rather than averaging it away.

The federation's constitutional posture is non-negotiable: disagreement is **evidence**, not noise. Averaging conflict destroys F2/F11 truth.

---

## Multi-index retrieval architecture

### Index inventory (per Memory Object face)

| Index | Substrate | Query type | Latency target |
|---|---|---|---|
| `idx.semantic` | Qdrant `arifos_memory`, `arifos_session_memory`, `federation_shared` | "Find memory about X" | <50ms |
| `idx.relational` | Graphiti (FalkorDB) | "Find memory involving person Y" | <100ms |
| `idx.temporal` | VAULT999 chain + Redis TTL | "Find memory between T1 and T2" | <20ms |
| `idx.affective_observation` | WELL `trend` (promoted) | "Find memory with stress indicator > 0.7" | <200ms |
| `idx.affective_interpretation` | WELL `trend` (promoted) | "Find memory labeled stressed" | <200ms |
| `idx.provenance` | VAULT999 receipt index | "Find memory with F2 verdict PASS" | <30ms |
| `idx.artifact` | L4/Postgres (artifact_uri index) | "Find memory with content_hash = H" | <10ms |
| `idx.salience` | Qdrant payload field index | "Find memory with salience > 0.7" | <50ms |

### Query mode surface (extends arif_memory)

| Mode | Inputs | Indexes hit | Output |
|---|---|---|---|
| `recall` (existing) | text | semantic + relational + temporal | ranked list |
| `inspect` (existing) | object_id | direct | Memory Object |
| `affective_query` (NEW) | affective signal range | affective_observation + semantic + relational | ranked list + affective summary |
| `relational_query` (NEW) | entity filter | relational + semantic | ranked list + entity subgraph |
| `temporal_query` (NEW) | time range + sequence filter | temporal + semantic | ranked list + timeline |
| `provenance_query` (NEW) | floor + actor filter | provenance + semantic | ranked list + provenance trace |
| `salience_query` (NEW) | score range + decay | salience + temporal | ranked list |
| `mixed_query` (NEW) | composition of any subset | union of selected indexes | ranked list + arbitration report |
| `causal_chain` (NEW) | object_id | temporal + relational | forward + backward chain |

---

## Index divergence — where they disagree

Indexes disagree in **predictable** ways. Each type has a known cause and an arbitration rule.

### Type 1: semantic ≠ affective

**Example:** "Find memory about GEOX" returns 50 hits. "Find memory with stress indicator > 0.7" returns 8 hits. Only 3 overlap.

**Cause:** Different storage shapes; semantic queries hit text-embedding distance, affective queries hit numerical thresholds. They are not measuring the same thing.

**Arbitration rule:** Both indexes are correct *as evidence*. The non-overlapping 47 are memories about GEOX without elevated stress; the non-overlapping 5 are memories with elevated stress not lexically similar to GEOX. **Report both lists separately with intersection highlighted.** Do NOT average.

**Required evidence for resolution:** the original Memory Object — re-read `affective_observation` to confirm the stress indicator, re-read `semantic.text` to confirm GEOX relevance.

### Type 2: relational ≠ semantic

**Example:** "Find memory involving Syed" returns 20 hits (via Graphiti entity edge). "Find memory mentioning Syed" returns 14 hits.

**Cause:** Graphiti resolution is conservative — only names explicitly entity-extracted as Person get edges. Lexical "Syed" might be a partial name ("Sye"), a pronoun reference, or a misspelling.

**Arbitration rule:** Both indexes are correct *as evidence*. The 6 not caught by Graphiti are *latent references*. Flag them as candidates for entity-resolution upgrade (T2 ingestion enhancement). Do NOT overwrite one with the other.

**Required evidence for resolution:** Graphiti entity extraction logs + the raw text — manual review.

### Type 3: inference ≠ observation

**Example:** A memory's `affective_interpretation.possible_stress` says 0.71 (model-derived INT label). A second memory's `affective_observation.pause_density` is 0.05 (low OBS measurement). They disagree.

**Cause:** Different epistemic labels. The observation is measured; the interpretation is inferred. They CAN disagree without one being wrong.

**Arbitration rule:** **Observation wins on facts.** If `pause_density` says low stress (OBS), then `possible_stress=0.71` (INT) cannot be sealed as truth — it can only be recorded as a model interpretation. The federation's epistemic hierarchy: **OBS > DER > INT > SPEC.** An INT observation cannot contradict an OBS observation. The INT may still be true (the model saw something the OBS metric missed), but it cannot *seal* that truth.

**Required evidence for resolution:** the OBS field is the ground truth for that face; the INT field is stored but down-weighted.

### Type 4: temporal ≠ causal

**Example:** Memory A occurred at T1. Memory B occurred at T2 (T2 > T1). Memory A's `causal_predecessor` is empty. Memory B's `causal_predecessor` includes A.

**Cause:** Time order is automatic; causation requires explicit authoring.

**Arbitration rule:** Both are correct *as different claims*. Temporal query returns "A then B"; causal query returns "B because A". A user asking "what preceded B?" gets temporal answer; "what caused B?" gets causal answer. **Never confuse them.**

**Required evidence for resolution:** the explicit `causal_predecessor` field. If empty, temporal order is the only answer available.

### Type 5: salience decay vs usage

**Example:** A memory was retrieved 50 times but `salience_score` is 0.3. Another memory was retrieved 0 times but `salience_score` is 0.9.

**Cause:** Salience is multi-source. Base score comes from creation-time trust; usage score increments on recall; decay subtracts over time. The two memories have different base scores.

**Arbitration rule:** **Report both scores separately.** A high base + low usage = "important but unqueried." A high usage + low base = "frequently surfaced." Each answer is a different cognitive signal.

**Required evidence for resolution:** `salience.base_score` + `salience.retrieval_count` + `salience.last_retrieved_at`.

---

## Arbitration framework — the four-step protocol

When a query touches multiple indexes, the arbitration protocol runs:

### Step 1 — Parallel index query

```yaml
inputs:
  query_text: "..."
  modality_filter: ["text", "audio"]
  actor_filter: ["arif"]
  floor_filter: ["F2_PASS"]

fan_out:
  - idx.semantic       → hits_a
  - idx.relational     → hits_b
  - idx.affective_obs  → hits_c (only if query has affective component)
  - idx.temporal       → hits_d (only if query has time range)
  - idx.provenance     → hits_e (only if query has floor filter)
  - idx.salience       → hits_f (only if query has salience filter)
```

### Step 2 — Per-index result

Each index returns:
```yaml
index_id: "semantic"
results: [object_id, ...]
epistemic_label: OBS
confidence: float
wall_clock_ms: int
notes: "matched via cosine distance < 0.15"
```

### Step 3 — Conflict detection

The system detects **6 conflict types** and labels each result pair:

| Conflict type | Detection rule | Default action |
|---|---|---|
| semantic ≠ affective | (results_in_a - results_in_b) ∪ (results_in_b - results_in_a) > 0 | Report both lists separately |
| relational ≠ semantic | entity-resolved ≠ lexical match | Surface latent refs for upgrade |
| observation ≠ interpretation | same object, OBS face contradicts INT face | Observation wins; INT down-weighted |
| temporal ≠ causal | temporal order ≠ causal chain | Don't conflate; answer the asked axis |
| salience ≠ usage | high base ≠ high retrieval count | Report both signals separately |
| trust ≠ freshness | L6 sealed but old; L3 fresh but trustless | Prefer L6 unless freshness window violated |

### Step 4 — Arbitration output (preserves disagreement)

```yaml
arbitration_report:
  query_id: UUIDv7
  indexes_queried: ["semantic", "relational", "temporal"]
  
  results:
    intersection: [object_id, ...]        # hit by all
    per_index:                             # hit by each
      semantic: [...]
      relational: [...]
      temporal: [...]
    latent_references: [object_id, ...]    # partially matching
    witness_disagreements:                 # explicit conflict records
      - type: "observation_vs_interpretation"
        object_id: string
        obs_value: ...
        int_value: ...
        resolution: "observation_wins_int_downweighted"
        evidence_paths: [...]
  
  confidence:
    per_index: {...}
    overall: float         # harmonic mean, not arithmetic mean
  
  epistemic_label: enum(OBS|DER|INT|SPEC)
  witness_vote: float     # F3 tri-witness score
```

---

## Why this is F2-compliant (preserves truth)

The arbitration framework **never averages**. When indexes disagree:

- The intersection is highlighted (strong evidence).
- The per-index lists are surfaced (preserved disagreement).
- Latent references are flagged (not silently merged).
- Witness disagreements are recorded as **first-class artifacts** in the arbitration report.

This means a query result is **not a single ranked list** but a **multi-dimensional report** that lets the calling agent (or sovereign human) decide which axis to trust for this particular query.

The mean is taken as **harmonic** rather than arithmetic because harmonic mean is more conservative — it penalizes any one weak axis. This matches the F7 humility posture: better to under-claim than over-claim.

---

## Memory landscape reconfirmed (cross-reference)

| Layer | Index used | Authority |
|---|---|---|
| L1 Redis (now) | key + TTL | ephemeral |
| L2 Redis (session) | range scan | session |
| L3 Qdrant (vector) | cosine | fuzzy |
| L4 Supabase (structured) | SQL | structured |
| L5 Graphiti (graph) | Cypher | governed |
| L6 VAULT999 (sealed) | chain hash | sealed |

**Authority hierarchy:** L6 > L5 > L4 > L3 > L2 > L1. When layers disagree, the higher layer wins *for sealed claims*. For fuzzy queries, all layers participate; the arbitration report shows the disagreement rather than collapsing it.

---

## Top 10 architectural gaps (retrieval/arbitration level)

1. **No `mixed_query` mode today.** Composite queries route through `recall` which returns a flat ranked list, not a multi-index report.
2. **No `affective_query` mode today.** WELL `trend` mode exists but is not exposed as a first-class arif_memory mode.
3. **No `causal_chain` traversal.** `causal_predecessor` field is not queryable.
4. **Harmonic mean computation not implemented.** Current retrieval returns arithmetic averages.
5. **No latent-reference surfacing.** Entity resolution is silent on partial matches.
6. **No epistemic-label-aware ranking.** Results don't show "this is OBS vs this is INT".
7. **No witness-disagreement artifact.** Conflicts collapse silently into ranked lists.
8. **No F3 tri-witness voting on retrieval.** Witness consensus not computed per query.
9. **No freshness window enforcement.** Old L6 vs fresh L3 conflict has no policy.
10. **Cross-organ memory ACL absent.** All agents can read all layers within trust circle.

## Top 10 quick wins (retrieval/arbitration level)

1. Implement `arif_memory.mixed_query` mode that returns an arbitration_report (T3).
2. Implement `arif_memory.affective_query` mode (T3).
3. Implement `arif_memory.causal_chain` mode (T3).
4. Add `witness_vote` calculation per query result (T3).
5. Add `epistemic_label` to every retrieval result (T1 schema + T3).
6. Add `latent_reference` surfacing in retrieval (T3).
7. Switch ranking from arithmetic to harmonic mean (T3).
8. Promote WELL `trend` to a queryable index (T3).
9. Add freshness-window policy for L6-vs-L3 conflict (T1).
10. Add per-component read ACL to Memory Objects (T1).

## Highest-risk assumptions

- **Assumption T:** "All agents reading ranked lists understand the conflict." — Verified FALSE: ranked lists silently average. Arbitration report is required for F2 compliance.
- **Assumption U:** "Harmonic mean is always conservative." — Verified PARTIAL: harmonic is conservative for ranking but can mislead when one index returns 0 hits. Special-case empty results.
- **Assumption V:** "Witness disagreement can be reported verbatim." — Verified TRUE per the framework. The risk is *agents ignoring* the report.
- **Assumption W:** "Observation always wins over interpretation." — Verified TRUE for F2 compliance but epistemically strict; some cases (e.g. tone-of-voice) have no OBS proxy and INT is the only signal. Allow INT-only when no OBS exists.
- **Assumption X:** "Latent references can be auto-upgraded." — Verified FALSE: upgrading Graphiti entity types requires human review (or careful RLHF). Flag only.

## Recommended first implementation step

**T3 retrieval, single-mode:** Implement `arif_memory.affective_query` as the first multi-index mode. It composes:
1. WELL `trend` index for affective_observation + affective_interpretation filter
2. Qdrant semantic for text relevance
3. Graphiti relational for entity links

Output: arbitration_report with per-index lists + intersection + witness_vote + epistemic_label.

This is the smallest end-to-end demonstration of the multi-index pattern, exposing the framework to live traffic so refinements are data-driven.

## Success condition (Phase 4-5)

The federation can answer "show me periods where Arif sounded exhausted while discussing GEOX" with a multi-dimensional report that:
1. Identifies GEOX-related memories (semantic index)
2. Identifies elevated-stress memories (affective index)
3. Identifies their intersection
4. Reports the witness disagreement
5. Returns a confidence score (harmonic mean)
6. Labels each result's epistemic tier

---

**delta_s (retrieval/arbitration):** High — first federation-grade multi-index query framework with explicit conflict preservation.
**evidence_paths:**
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` (existing tool envelope shape)
- `/root/arifOS/deploy/graphiti-config.yaml:17` (bge-m3 1024d embedder)
- `/root/WELL/tools_sot.yaml:23` (WELL trend mode)
- `:3001/health` (apex scalars W3 in federation probe)
- `/root/AAA/federation/organs.yaml:214-233` (arifFlow metabolism, never judges/executes)
- `/root/arifOS/VAULT999/outcomes.jsonl` (event envelope shape, epistemic_label in payloads)

**Verified vs claim:** arbitration framework is derived from existing federation primitives (F1-F13 floors, OBS/DER/INT/SPEC labels, tri-witness W3, harmonic vs arithmetic mean). Each conflict type traces to a specific observed federation behavior. No new substrate is invented.

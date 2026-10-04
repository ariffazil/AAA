---
name: retrieval-vs-memory-fidelity
description: >
  Core architectural distinction: retrieval quality ≠ memory fidelity.
  Use when designing memory systems, auditing RAG architectures, or
  evaluating whether a memory system preserves reality or just finds text.
  Triggers: "memory design", "RAG audit", "retrieval architecture",
  "witness model", "memory fidelity", "multimodal memory".
version: 1.0.0
author: hermes (aaa-hermes)
source: MMA-2026-08-07 session + literature review (M3-Agent, AffectAgent)
floors: F2 TRUTH, F3 TRI-WITNESS, F4 CLARITY, F7 HUMILITY, F11 AUDITABILITY
---

# Retrieval Quality ≠ Memory Fidelity

## The distinction

| | Retrieval Quality | Memory Fidelity |
|---|---|---|
| Question | "Can I find the relevant chunk?" | "Did the recalled memory preserve reality?" |
| Optimizes for | Query-answer precision | Multi-witness truth preservation |
| Failure mode | Wrong chunk returned | Correct chunk, but affect/provenance/context lost |
| Metric | Recall@K, MRR, nDCG | Cross-witness consistency, provenance chain integrity |

## Why it matters

A perfect BM25+vector retrieval system can return the right text while
destroying: affect, context, sequence, provenance, human significance.

Memory fidelity asks a harder question than retrieval quality.

## Memory Object shape (8 faces)

Full YAML schema: `/root/AAA/reports/multimodal-memory-audit/04_memory_object_proposal.md`
Convergence trace: `/root/AAA/reports/multimodal-memory-audit/11_convergence_trace.md`

```yaml
schema_version: "1.0.0"
object_id: string (UUIDv7)

artifact:
  uri: string | null              # file:// or federation://
  content_hash: string | null     # sha256 hex
  mime_type: string | null        # audio/ogg, video/mp4, image/png
  byte_size: int | null
  modality: enum(text|audio|video|image|document|chat|event|meeting|artifact)

semantic:
  text: string                    # canonical text projection
  summary: string | null
  entities: array<EntityRef>      # Graphiti entity references
  topics: array<string>
  embedding_id: string | null     # pointer to L3 Qdrant vector

affective_observation:             # MEASURABLE — sealable at OBS
  pause_density: float | null     # pauses / minute
  speech_rate_delta: float | null # % vs baseline
  pitch_variance: float | null    # hz std dev
  interaction_count_24h: int | null

affective_interpretation:          # MODEL-DERIVED — capped at INT
  possible_stress: float | null   # 0–1
  possible_fatigue: float | null  # 0–1
  confidence: float               # 0–0.9 (RASA_DERITA cap)
  epistemic_label: enum(OBS|DER|INT|SPEC)
  model_id: string | null

relational:
  subject_entities: array<EntityRef>    # memory is about
  object_entities: array<EntityRef>     # acted upon
  affected_entities: array<EntityRef>   # impacted
  present_entities: array<EntityRef>    # was present

temporal:
  clock_time: ISO datetime | null
  event_sequence: int | null
  relative_to: string | null      # "after HKL incident"
  causal_predecessor: array<string> | null

provenance:
  source_type: enum(direct_observation|human_input|agent_inference|external_source|derived_memory)
  model_version: string | null
  computed_at: ISO datetime | null
  epistemic_tag: enum(OBS|DER|INT|SPEC)
  receipt_ref: string | null      # VAULT999 receipt hash

salience:
  weight: float                   # 0–1, decays
  last_evoked: ISO datetime | null
  decay_rate: float | null
  recall_count: int | null
```

## The 4 additive principles (from MMA-2026-08-07)

1. **Preserve disagreement** (P3): When witnesses disagree, store the
   conflict as a structured artifact. Never average away conflict.

2. **Retrieval ≠ Memory** (P8): Never confuse easy retrieval with faithful
   memory. Memory preserves what happened, who was involved, how it was
   experienced, how it was known, why it mattered.

3. **Multi-witness memory object** (P9): Every long-term memory should carry
   artifact + semantic + affective + relational + temporal + provenance +
   salience. No single witness becomes sovereign.

4. **Confidence must be earned** (P12): Confidence sources: observation,
   verification, cross-witness agreement, artifact integrity, reproducibility.
   NOT model certainty, verbose explanations, or agent reputation.

## OBS vs INT separation (critical for F2)

- `affective_observation` = measurable → can be sealed at OBS grade
- `affective_interpretation` = model-derived → capped at INT grade
- OBS always wins over INT when they conflict
- If no OBS exists for a signal, INT can be used but flagged as INT-only

## References

- `references/mma-2026-08-07-deliverables-index.md` — full deliverable index from the 2026-08-07 memory audit, with verified live numbers

## When to use this pattern

- Evaluating whether a memory system is retrieval-only or fidelity-aware
- Designing memory object schemas for new domains
- Auditing existing RAG architectures for hidden fidelity gaps
- Proposing multimodal memory extensions to existing systems

---
name: dream-engine
description: "v2 HARDENED: 72h reasoning distillation producing structured DreamCandidates with three orthogonal confidence dimensions (p_occurrence/p_predictive/p_normative), counterstory generation, causal status, and promotion lifecycle. Substrate consolidation via separate process. No self-witnessing. Use when memory drift, dedup, or constitutional recalibration is needed."
---

# dream-engine v2

The dream engine is a **substrate process**, not an LLM loop.

## What changed (v2, 2026-09-21)

- Single p= confidence → three orthogonal dimensions (p_occurrence, p_predictive, p_normative)
- Prose wisdom.md → structured DreamCandidate JSONL + human-readable render
- No falsification → every candidate MUST have counterstories
- No lifecycle → OBSERVED → CANDIDATE → ... → RATIFIED (or RETRACTED/DECAYED)
- No causal status → Pearl's ladder (UNTESTED → CORRELATION_ONLY → CAUSAL_HYPOTHESIS)
- Path drift fixed: `/root/AAA/dream-engine/wisdom.md` → symlink to canonical

## When to use

- Memory is drifting (Qdrant dedup, Graphiti entity merge)
- Constitutional floors need recalibration (monthly dream)
- Reasoning traces need distillation into testable candidates (72h dream)
- Counterfactual rehearsal of sealed verdicts (weekly dream)
- Cross-organ graph walks for creative recombination (weekly dream)

## When NOT to use

- L6 VAULT999 touch (sovereign only — L11 + L13)
- Real-time LLM inference (that's `arif_mind_reason`)
- Live session state mutation (that's `arif_memory_recall(mode=store)`)
- Treating dream output as truth (candidates require F13 ratification)

## Authority

- T1 (Consolidate, Housekeep, Defuse) — L4 capability, autonomous
- T2 (Distill, Rehearse, Recombine) — L5 capability, requires L11 Ed25519 sig
- T3 (Constitutional, Witness) — L6 capability, sovereign only
- **All dream candidates are T2 proposals, never T3 decisions**

## 3-Phase Cycle

| Phase | Timer | Script | Function |
|-------|-------|--------|----------|
| Nightly 🌙 | `arif-dream.timer` (72h) | `dreams/consolidate.py` | Memory consolidation (Redis/Qdrant/Supabase cleanup) |
| Distill 🧠 | `arif-dream-distill.timer` (72h+15m) | `engines/dream_engine.py` | Reasoning → structured DreamCandidates |
| Weekly 🌀 | (Phase 2 — unbuilt) | `dreams/rehearse.py` | Counterfactual rehearsal |
| Monthly 🪞 | (Phase 3 — unbuilt) | constitutional | F-floor recalibration |

## Outputs

| File | What |
|------|------|
| `knowledge-graph/dream-engine/dream_candidates_latest.json` | Latest cycle, full structured data |
| `knowledge-graph/dream-engine/dream_candidates.jsonl` | Append-only log of all candidates ever |
| `knowledge-graph/dream-engine/wisdom.md` | Human-readable render |
| `specs/dream_candidate.schema.json` | JSON Schema for DreamCandidate |

## The Three-Confidence Model

```
p_occurrence  = how often?     (frequency in sessions)
p_predictive  = does it work?  (CHRON calibration, initially null)
p_normative   = can it govern? (F13 authority, initially null)
```

**frequency(pattern) ≠ probability(pattern is wise)**

## Commands

```bash
# Dry-run consolidation (Process 1)
python3 /root/AAA/dream_engine/dreams/consolidate.py --dry-run

# Run distillation (Process 2)
python3 /root/AAA/engines/dream_engine.py

# Inspect latest candidates
cat /root/AAA/knowledge-graph/dream-engine/dream_candidates_latest.json | python3 -m json.tool

# View candidates log
wc -l /root/AAA/knowledge-graph/dream-engine/dream_candidates.jsonl
```

## Reversibility

All writes to shadow namespaces first. 7-day dual-write. Atomic cutover.
If a dream fails: shadow discarded, live untouched.

```bash
systemctl disable --now arif-dream.timer arif-dream-distill.timer
```

## References

- Schema: `specs/dream_candidate.schema.json`
- Literature: `FOUNDATIONS.md` (12 mandatory anchors)
- Design: `DESIGN.md`
- Federation memory: `/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md`

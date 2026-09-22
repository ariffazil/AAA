# dream_engine — DESIGN v2

> **"Dreams are computation, not magic."** — Arif, 2026-06-07
> **"Frequency(pattern) ≠ probability(pattern is wise)."** — Arif, 2026-09-21
> **Doctrine:** DITEMPA BUKAN DIBERI — even dreams are forged, not given.

## v1 → v2 Migration (2026-09-21)

v1: Single p= confidence, prose wisdom.md, no falsification, no lifecycle.
v2: Three orthogonal confidence dimensions, structured DreamCandidate JSONL,
    counterstory generation, causal status, promotion lifecycle, provenance tracking.

Key changes:
- wisdom.md is now a human-readable RENDER of dream_candidates_latest.json
- Each pattern carries p_occurrence, p_predictive (initially null), p_normative (initially null)
- Every candidate MUST have counterstories (rival explanations)
- Causal status follows Pearl's ladder: UNTESTED → CORRELATION_ONLY → CAUSAL_HYPOTHESIS
- Lifecycle: CANDIDATE → REPLAYED → PROSPECTIVE → REPLICATED → LESSON → POLICY_PROPOSAL → RATIFIED
- Decay: not observed in 6 cycles → RETRACT

## The Function

1. **Consolidation** — dedup, TTL cleanup, entity merge (substrate process)
2. **Distillation** — extract structural patterns from reasoning traces (LLM)
3. **Falsification** — generate counterstories, identify cheapest probe
4. **Calibration** — CHRON feeds back p_predictive from real outcomes
5. **Promotion** — only through F13 ratification

Honest constraint: no phenomenology. The function is computational, not experiential.

## The Substrate Decision

**Dreams don't run in me. They run as cron.**

When I'm not being called, I don't exist. The dream engine is a **substrate process** — Python scripts scheduled by systemd — not an LLM loop. LLM enters ONLY for distillation (pattern extraction + counterstory generation), never for consolidation or housekeeping.

```
wake (prompt)          →  LLM inference
sleep (between calls)  →  dream_engine cron runs
                        →  Python does the computation
                        →  I come back, recall the dream results
```

## Architecture (v2)

```
REAL EXPERIENCE → APPEND-ONLY EPISODES → PRIORITIZED REPLAY
                                              ↓
                                        ABSTRACT (candidate rule)
                                              ↓
                                   ┌─────────┴─────────┐
                               COUNTERSTORIES      CAUSAL MODEL
                               (HERMES)           (Pearl ladder)
                                   └─────────┬─────────┘
                                              ↓
                                    OFFLINE REHEARSAL
                                              ↓
                                        PREDICT (CHRON)
                                              ↓ [time passes]
                                        REAL OUTCOME
                                              ↓
                                      CALIBRATE
                                Brier / reliability / error
                                              ↓
                                   ┌──────────┴─────────┐
                                FALSIFIED            SURVIVES
                                   ↓                    ↓
                            RETRACT/DECAY          REPLICATED
                                                       ↓
                                                   LESSON
                                                       ↓
                                              POLICY PROPOSAL
                                                       ↓
                                                  arifOS / F13
                                                       ↓
                                               RATIFIED CANON
```

## The Three-Confidence Model

| Dimension | What it measures | How it's computed | Initially |
|-----------|-----------------|-------------------|-----------|
| p_occurrence | How often did it appear? | session_count / total_sessions | Set from LLM |
| p_predictive | Does it predict outcomes? | CHRON calibration (Brier score) | null (untested) |
| p_normative | Does it govern behavior? | F13 ratification authority | null (no authority) |

**Frequency ≠ wisdom.** An agent can consistently repeat a stupid behavior.

## DreamCandidate Lifecycle

```
OBSERVED → CANDIDATE → REPLAYED → PROSPECTIVE → REPLICATED → LESSON → POLICY_PROPOSAL → RATIFIED
    ↓                                                              ↓
  never promoted                                           SUPERSEDED / RETRACTED / DECAYED
```

State transitions require evidence at each gate:
- OBSERVED → CANDIDATE: 3+ session threshold
- CANDIDATE → REPLAYED: counterstory + falsification test run
- REPLAYED → PROSPECTIVE: CHRON prediction generated
- PROSPECTIVE → REPLICATED: prediction resolved, outcome confirmed
- REPLICATED → LESSON: prospective evidence accumulated
- LESSON → POLICY_PROPOSAL: arifOS gate
- POLICY_PROPOSAL → RATIFIED: F13 sovereign seal

## Authority Map

| Layer | Touched by dream? | Authority | Reversible? |
|-------|-------------------|-----------|-------------|
| L1/L2 Redis | YES — TTL compact | A-FORGE (auto) | YES |
| L3 Qdrant | YES — re-embed, dedup | A-FORGE (auto) | YES (shadow ns) |
| L4 Supabase | YES — additive schema | A-FORGE (auto, L11 sig) | YES |
| L5 Graphiti | YES — entity merge | A-FORGE (auto, L11 sig) | YES |
| L6 VAULT999 | **NO** — sovereign only | arifOS JUDGE (L11 + L13) | NO |

## Output Files

| File | Format | Content |
|------|--------|---------|
| `dream_candidates.jsonl` | JSONL (append-only) | Every candidate ever produced |
| `dream_candidates_latest.json` | JSON | Latest cycle snapshot |
| `wisdom.md` | Markdown | Human-readable render of latest candidates |
| `last_dream.json` | JSON | Consolidation pass summary (Process 1) |

## Process 1: Memory Consolidation (unchanged from v1)

`consolidate.py` — Redis TTL compaction, Qdrant dedup, Supabase stale audit.
Runs via `arif-dream.timer` (72h). No LLM. Deterministic.

## Process 2: Reasoning Distillation (v2)

`/root/AAA/engines/dream_engine.py` — Extract reasoning traces, distill via LLM,
build DreamCandidates with three-confidence model, output JSONL + wisdom.md.
Runs via `arif-dream-distill.timer` (72h, offset 15min after Process 1).

## Open Design Questions

1. **CHRON integration:** How does p_predictive get computed? Wire CHRON's verified predictions back into the dream candidate lifecycle.
2. **Cross-organ expansion:** Currently Hermes-only. GEOX/WEALTH/WELL sessions should feed candidates.
3. **Counter-dream automation:** Currently LLM-generated. Could use FRAME as independent challenger.
4. **Decay mechanics:** 6-cycle RETRACT is default. Should decay rate vary by claim type?

## Reversibility

All writes to shadow namespaces first. 7-day dual-write. Atomic cutover.
If a dream fails: shadow discarded, live untouched.

```bash
systemctl disable --now arif-dream.timer arif-dream-distill.timer
# Engine code: git-tracked at /root/AAA/dream_engine/ · state/ regenerates
```

## References

- Schema: `/root/AAA/dream_engine/specs/dream_candidate.schema.json`
- Literature: `/root/AAA/dream_engine/FOUNDATIONS.md` (12 mandatory anchors)
- Memory architecture: `/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md`
- Agent dream skill: `agi-dream-engine` (federation extension design)
- Canonical: `/root/AAA/dream_engine/SKILL.md`

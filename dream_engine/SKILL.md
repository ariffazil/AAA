---
name: dream-engine
description: Scheduled substrate process for memory consolidation, threat rehearsal, emotional defusing, creative recombination, and housekeeping. Maps to L1-L5 only (L6 sovereign). Cron-driven Python, LLM only for cross-domain synthesis. Use when memory drift, dedup, or constitutional recalibration is needed.
---

# dream-engine

The dream engine is a **substrate process**, not an LLM loop.

## When to use

- Memory is drifting (Qdrant dedup needed, Graphiti entity merge needed)
- Constitutional floors need recalibration (monthly dream)
- Counterfactual rehearsal of past sealed verdicts (weekly dream)
- TTL compaction on L1/L2 Redis
- Cross-organ graph walks for creative recombination

## When NOT to use

- L6 VAULT999 touch (sovereign only — L11 + L13)
- Real-time LLM inference (that's `arif_mind_reason`)
- Live session state mutation (that's `arif_memory_recall(mode=store)`)

## Authority

- T1 (Consolidate, Housekeep, Defuse) — L4 capability, autonomous in F13-waived session
- T2 (Rehearse, Recombine) — L5 capability, requires L11 Ed25519 sig
- T3 (Constitutional, Witness) — L6 capability, sovereign only

## 3-Phase Cycle

| Phase | Schedule | Function |
|-------|----------|----------|
| Nightly | 04:00 MYT | Consolidate + Defuse + Housekeep |
| Weekly | Sun 02:00 MYT | Rehearse + Recombine |
| Monthly | 1st @ 01:00 MYT | Constitutional + Witness |

## Commands

```bash
# Run a single pass manually
python3 /root/.openclaw/workspace/dream_engine/dreams/consolidate.py --dry-run

# Run the full nightly cycle
/root/.openclaw/workspace/dream_engine/scheduler/dream_cron.sh nightly

# Inspect last run
cat /root/.openclaw/workspace/dream_engine/state/last_dream.json
```

## Reversibility

All writes go to shadow namespaces first. 7-day dual-write. Atomic cutover.
If a dream fails: shadow is discarded, live untouched.

```bash
systemctl disable --now dream_cron.timer
rm -rf /root/.openclaw/workspace/dream_engine/
```

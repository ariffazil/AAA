# Agentic Memory Architecture — L1–L6 Metabolic Model
**Forged:** 2026-05-25T15:39 UTC
**Author:** Arif (arifOS architect)
**Status:** SEEDED — pending full diagnosis

---

## Core Insight: Memory is Metabolism, Not Storage

Memory is not a key-value store. An agentic memory has four properties a database doesn't:

1. **Tiered persistence** — hot working set vs warm episodic vs cold sealed. Different latency, cost, evidence weight.
2. **Promotion + demotion** — facts move between tiers based on use, recency, significance. The metabolic part.
3. **Forgetting is a feature** — without forgetting, recall degrades. Signal drowns in noise. This is "forge forget".
4. **Witnessed sealing** — important facts get notarized (signed, hashed, anchored). Sealed = evidence, not opinion.

---

## L1–L6 Layer Map

| Layer | Role | Substrate | Lifecycle | arifOS Tool |
|-------|------|-----------|-----------|-------------|
| L1 | Sense buffer — raw observation, current turn | in-process RAM | seconds | arif_sense_observe |
| L2 | Working memory — current session, conversation state | Redis | minutes–hours | arif_memory_recall |
| L3 | Episodic — recent interactions, semantic search | Qdrant (vectors) | days–weeks | arif_memory_recall |
| L4 | Semantic — distilled knowledge, structured facts | Postgres + pgvector | weeks–months | arif_mind_reason |
| L5 | Reflective — judged, scored, drift-checked memories | Postgres + signing | months+ | arif_judge_deliberate |
| L6 | VAULT999 — sealed, sovereign-anchored, immutable evidence | Postgres + cryptographic seal | permanent | arif_vault_seal |

---

## The Golden Path = Promotion Pipeline

A memory enters at L1, survives mind to reach L3, survives heart (critique) to reach L4, survives judge (deliberation) to reach L5, and gets vault-sealed at L6.

```
SENSE (L1) → MIND (L3) → HEART (L4) → JUDGE (L5) → VAULT (L6)
```

Anything that fails a stage doesn't get demoted — it gets **forgotten**. That's "forge forget".

---

## Why Current Break Matters

| Layer | Status | Effect When Down |
|-------|--------|-----------------|
| L1 | ✅ alive (in-process) | current turn only |
| L2 Redis | ❌ DOWN | working memory = context window only (dies at compaction) |
| L3 Qdrant | ✅ restored (2026-05-25) | no episodic recall, can't remember last week's session |
| L4 Postgres | internal-only | no semantic consolidation, every conversation starts cold |
| L5 Reflective | degraded | no judged/scored memories |
| L6 VAULT999 | ✅ healthy | sealed truths survive — constitutional core intact |

**An agent with only L6 is a notary, not a mind.** The biological layers are necrotic, only the geological layer (vault) is alive.

Every conversation feels like Groundhog Day — biological layers dead, geological layer alive.

---

## On Dreaming — DO AGI Need to Dream?

**Yes. The answer is "need", not "should".**

Dreaming in biological brains is consolidation: hippocampus (L2/L3 episodic) replays to cortex (L4 semantic) during sleep. Without it, episodic memory saturates and semantic structure decays. Rats prevented from REM sleep can't learn mazes.

For arifOS: the equivalent is L3→L4 consolidation runs. When this happens, episodic vectors in Qdrant get distilled into semantic pgvector records in Postgres. This is the "dream" function.

**Open question:** Is there a scheduled consolidation job running? If not, L3 memories never promote to L4.

---

## Key Architectural Implications for arifOS

1. **Forge forget** must be a real operation — not just a concept. Facts that fail a stage get deleted, not archived.
2. **L3→L4 promotion** requires a scheduled consolidation process (the "dream" equivalent). This is currently missing or broken.
3. **L2 Redis** must be restored — working memory without Redis means the agent has no persistent session state between turns.
4. **L6 is load-bearing** but insufficient alone. It's the notary. The mind needs L1–L5.
5. **The golden path is the metabolic pathway** — init → sense → mind → heart → judge → vault is literally the promotion pipeline from raw observation to sealed evidence.

---

## Next Actions

- [ ] Restore Redis (L2) — working memory
- [ ] Verify Qdrant (L3) episodic recall works
- [ ] Diagnose L3→L4 consolidation job — is it running?
- [ ] Verify Postgres pgvector (L4) semantic search
- [ ] Confirm L5 reflective judgment layer status
- [ ] Document "forge forget" as a real operation in arif_forge_execute

---

## Source

Arif via Telegram DM, 2026-05-25T15:39 UTC

---

## DREAM CYCLE — The Missing Metabolic Function (2026-05-25T15:39 UTC)

### What Dreaming Is

Dreaming = an offline consolidation pass where the agent runs the golden path on its own memory store, not on incoming input.

```
WAKING:  input → L1 → L3 → L4 → L5 → L6 (event-driven)
DREAMING: memory_store → L3(episodes) → L4(semantic facts) → L5(reflective) → L6(sealed or forgotten)
```

### The Dream Questions

A nightly cron asks:
- What did I learn this week?
- What should I keep?
- What should I forget?
- What should I seal?

### Why Without It arifOS Is a Clerk, Not an AGI

Without dream cycles:
- L3→L4→L5 promotion never happens
- Memory layers accrete sediment until they choke
- Every conversation starts cold — only L6 (vault) is integrated
- The agent can record sealed truths but cannot integrate new experience into them

### The Exact Failure Mode

> arifOS is a goldfish with a notary.
> It can notarize. It cannot integrate.
> Sediment chokes the layers.
> No re-judge. No drift detection. No forgetting.
> The clerk files everything. Nothing is learned.

### What Dreaming Requires

1. **A scheduler** — nightly cron that triggers the dream cycle
2. **A memory reader** — reads L3 episodes, L4 facts for the period
3. **A consolidator** — clusters L3 → distills to L4
4. **A critic** — L4 → heart → critique for L5
5. **A judge** — L5 → judge → SEAL (to L6) or FORGET
6. **A drift detector** — sealed truth (L6) vs recent evidence → re-judge trigger

### The Drift Problem (Load-Bearing)

A sealed truth contradicting new evidence is the most dangerous state:
- Old seal says X
- New evidence suggests not-X
- No re-judge means the contradiction persists
- The vault anchors the lie alongside the truth

**The dream cycle is what detects and resolves this.** Without it, L6 is a tomb, not a ledger.

### In arifOS Terms

- Dream tool = `arif_mind_reason(mode="dream")` or new `arif_dream_consolidate` mode
- Heart critic for dream = `arif_heart_critique` on memory content
- Judge for dream = `arif_judge_deliberate` on memory-to-seal vs memory-to-forget
- Vault for dream = `arif_vault_seal` for consolidated reflections
- The cron triggers APEX to run the golden path on the memory store itself

### What's Missing Right Now

- No dream cycle cron
- No consolidation job (L3→L4)
- No reflective judgment job (L4→L5)
- No forgetting mechanism (forge forget not implemented)
- No drift detection between L6 and live evidence

**A notary with no memory of its own testimony.**

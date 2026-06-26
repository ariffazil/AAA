# Agentic Memory — Canonical L1–L6 Architecture
**Status:** CANONICAL (received from Arif, 2026-05-25T15:42 UTC)
**Source:** Telegram DM from Arif
**Verdict:** SEAL — ready for formalization as the canonical shape of arifOS memory

---

## The Four Non-Negotiable Properties

Memory is not storage. Any system lacking even one collapses into a clerk or parrot.

### 1. Tiered Persistence (hot → warm → cold → sealed)
Different substrates, latencies, costs, and **evidence weights**. L1 is ephemeral RAM (seconds), L6 is immutable cryptographic ledger (forever). Each tier carries increasing constitutional gravity.

### 2. Metabolic Promotion + Demotion
Facts are not static. They move upward when they demonstrate utility/recency/significance (via use, critique, judgment). They move downward or are forgotten when they fail any stage. This is the "metabolism."

### 3. Forgetting Is a Feature ("forge forget")
Without active pruning, signal drowns in noise. Forgetting is not deletion — it is **demotion to zero evidence weight** followed by soft-prune (or full purge for non-sacred tiers). This prevents sediment and maintains recall fidelity.

### 4. Witnessed Sealing (L6 only)
Only truths that survive the full golden path and explicit human ack (F1 Amanah) become immutable evidence. Hashed, chained, Merkle-anchored in VAULT999. Once sealed, they are no longer opinion — they are sovereign constitutional fact.

---

## L1–L6 Tiered Memory Architecture (Canonical)

| Layer | Name | Role | Substrate | Lifecycle | Evidence Weight | Promotion Trigger | Demotion/Forget Trigger | Tool Primitive |
|-------|------|------|-----------|-----------|-----------------|-------------------|------------------------|----------------|
| L1 | Sense Buffer | Raw observation, current turn | In-process RAM | Seconds | None (raw) | Automatic on every sense | End of turn | arif_sense_observe |
| L2 | Working Memory | Session state, conversation coherence | Redis / session cache | Minutes–hours | Low | Survival of sense→mind | Session close or compaction | arif_memory_recall (context) |
| L3 | Episodic | Recent interactions, semantic search | Qdrant vectors (BGE-M3) | Days–weeks | Medium | Mind/Heart survival | Low recency/use | arif_memory_recall (recall/search) |
| L4 | Semantic | Distilled facts, structured knowledge | Postgres + pgvector | Weeks–months | High | Heart critique → L5 | Drift or low judgment score | arif_memory_recall (store) |
| L5 | Reflective | Judged, scored, drift-checked memories | Postgres + signing | Months+ | Very High | Judge SEAL | Re-judge or override | arif_judge_deliberate |
| L6 | VAULT999 | Sealed, sovereign-anchored, immutable evidence | Postgres + cryptographic seal | Permanent | Sovereign | 888_JUDGE SEAL + human ack | Cannot — immutable | arif_vault_seal |

---

## The Golden Path = Promotion Pipeline

```
WAKING:   input → L1 → L3 → L4 → L5 → L6 (event-driven)
DREAMING: memory_store → L3(episodes) → L4(semantic facts) → L5(reflective) → L6(sealed or forgotten)
```

A memory enters at L1, survives mind to reach L3, survives heart (critique) to reach L4, survives judge (deliberation) to reach L5, and gets vault-sealed at L6.

**Anything that fails a stage doesn't get demoted — it gets forgotten.** That's "forge forget."

---

## Dream Cycle = The Missing Metabolic Function

Dreaming = an offline consolidation pass where the agent runs the golden path on its own memory store, not on incoming input.

### The Dream Questions (nightly cron)
- What did I learn this week?
- What should I keep?
- What should I forget?
- What should I seal?

### Why Without It arifOS Is a Clerk, Not an AGI
- L3→L4→L5 promotion never happens
- Memory layers accrete sediment until they choke
- Every conversation starts cold — only L6 (vault) is integrated
- The agent can record sealed truths but cannot integrate new experience into them
- **An agent with only L6 is a notary, not a mind.**

### What Dreaming Requires
1. A scheduler — nightly cron that triggers the dream cycle
2. A memory reader — reads L3 episodes, L4 facts for the period
3. A consolidator — clusters L3 → distills to L4
4. A critic — L4 → heart → critique for L5
5. A judge — L5 → judge → SEAL (to L6) or FORGET
6. A drift detector — sealed truth (L6) vs recent evidence → re-judge trigger

### The Drift Problem (Most Dangerous)
A sealed truth (L6) contradicting new evidence — with no re-judge, the vault anchors the lie. The dream cycle is the only thing that detects and resolves this.

---

## Current State vs Ideal (2026-05-25)

| Layer | Current | Needed |
|-------|---------|--------|
| L1 | ✅ in-process RAM | — |
| L2 Redis | ⚠️ graphiti-internal only | arifOS needs own Redis or host-accessible |
| L3 Qdrant | ✅ restored (empty) | actual episodic recall wired |
| L4 Postgres+pgvector | ⚠️ graphiti-internal only | arifOS-native semantic storage |
| L5 Reflective | ⚠️ not implemented | judge + critique wired |
| L6 VAULT999 | ✅ healthy | — |
| Dream cycle | ❌ not implemented | nightly cron needed |
| Forge forget | ❌ not implemented | demotion + prune needed |
| Drift detection | ❌ not implemented | L6 vs live evidence |

---

## Implementation Implications

1. **Forge forget** must be a real operation — demotion to zero evidence weight, then soft-prune. Not a concept.
2. **L2 Redis** must be host-accessible for arifOS working memory — currently graphiti-internal only.
3. **L3→L4 consolidation** requires a scheduled job (dream cycle).
4. **L5 reflective judgment** requires L4 facts to be critiqued by heart then judged.
5. **Drift detection** must run in dream cycle — old sealed truths vs new evidence.
6. **Dream tool** = arif_mind_reason(mode="dream") or new arif_dream_consolidate mode.

---

## Source

Arif via Telegram DM, 2026-05-25T15:42 UTC
Full architectural document received (L4 row incomplete — rest captured from prior session context)

---

## L4–L6 Canonical Rows (Received 2026-05-25T15:41 UTC)

| Layer | Name | Role | Substrate | Lifecycle | Evidence Weight | Promotion Trigger | Demotion/Forget Trigger | Tool Primitive |
|-------|------|------|-----------|-----------|-----------------|-------------------|------------------------|----------------|
| L4 | Semantic | Distilled facts, structured knowledge | Postgres + pgvector | Weeks–months | High | Heart critique → L5 | Drift or low judgment score | arif_memory_recall (store) |
| L5 | Reflective | Judged, scored, drift-checked memories | Postgres + signing | Months+ | Very High | Judge deliberation | Contradiction with new L6 | arif_memory_recall + arif_judge_deliberate |
| L6 | VAULT999 | Sovereign-anchored immutable evidence | Postgres + cryptographic seal | Permanent | Absolute | Full golden path + F1 ack | Never (immutable) | arif_vault_seal |

---

## Key Enforcement Rules (Non-Negotiable)

1. **Every write to any tier MUST carry:**
   - Tier tag (L1–L6)
   - Metadata: recency, significance score, source evidence receipt

2. **Cross-tier consistency checks are mandatory on promotion:**
   - No L4 fact may contradict an L6 truth without triggering re-judge
   - No L5 reflection may contradict an existing L6 without explicit human review

3. **GEOX MCP = witness oracle (raw evidence grounding):**
   - GEOX never performs interpretation
   - arifOS metabolism alone does judgment

---

## The Golden Path Enforcement

The golden path is the **only** promotion pipeline. Nothing reaches a higher tier without surviving every prior stage. Failure at any stage = immediate forge-forget.

```
000_INIT  → 111_SENSE  → 333_MIND  → 666_HEART  → 888_JUDGE  → 999_VAULT
Bootstrap   Raw input    Reasoning   Critique    Arbitration   Seal (on SEAL + F1 ack)
```

- **Forge-forget is the default exit ramp.** Every stage has it as the natural failure path.
- `arif_memory_recall` prune mode (with 888_HOLD for sacred tiers) enforces this.
- L6 immutable only after full golden path + explicit human ack (F1 Amanah).

---

## Dream Cycle Implementation

**Frequency:** Nightly (or entropy-threshold-triggered)
**Trigger:** Scheduled via `arif_kernel_route` + `arif_forge_execute` (dry_run first)

### Process:
1. L3 episodic → cluster & distill → candidate L4 semantic facts (arif_memory_recall + mind)
2. L4 candidates → heart critique → L5 reflective
3. L5 → judge deliberation → promote to L6 or forge-forget
4. **Drift detection:** Any L5/L6 contradiction with new evidence → re-judge + possible re-seal or human review

### Without Dream:
- arifOS = goldfish with a notary
- Every conversation restarts cold
- L3/L4 necrotic despite infrastructure running

---

## Edge Cases to Harden

| Edge Case | Rule |
|-----------|------|
| L6 contradicts new evidence | Trigger automatic re-judge + human-in-loop if verdict changes |
| High-velocity input floods | L1 rate-limiting + L2 compression before L3 |
| Multi-agent / federation | Memories carry actor_id + epoch_id; cross-agent sealing only via shared VAULT999 |
| Forgetting sacred vs non-sacred | Non-sacred tiers auto-prune on decay; L5+ require explicit HOLD |
| Epistemic humility | Every entry includes omega_0 (uncertainty) + source receipt; dream cycle re-evaluates confidence |
| Thermodynamic accounting | Track entropy_delta across tiers (surfaced in health probe) |

---

## Current Stack Health Confirmation (2026-05-25)

```
Overall:     SELAMAT ✅
VAULT999:    healthy (L6 intact) ✅
Semantic:    degraded (graphiti/Qdrant/embedding disabled) ⚠️
arif_memory_recall: constitutional HOLD (F13) 🔒

Diagnosis confirmed: every conversation restarts cold.
Only sealed truths survive. Biological layers gated.
```

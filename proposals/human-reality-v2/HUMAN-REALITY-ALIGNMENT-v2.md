# HUMAN-REALITY-ALIGNMENT-v2 — PROPOSAL

> **Status:** PROPOSED · NOT CANON · awaiting F13 review
> **Date:** 2026-10-09 · **Author:** HERMES (mouth) · **Owner:** F13 (Muhammad Arif bin Fazil)
> **Anchors:** `instructions/human9-spec.md` · `instructions/valence-loss-asymmetry.md` · `instructions/human-substrate.md` · `docs/HELIX_MEMORY_STRUCTURE.md` · `.hermes/lanes/people.yaml` · `instructions/linkgraph-namespace.md`
> **EMD-validated inputs (2026-10-09):** valence-as-transition-machine · 4-layer person with TTL isolation · domain-specific trust vectors · PG+graph hybrid.

## 0 · Directive

> "Align all human reality with this architecture. So when any human name is mentioned, AAA agent knows what to do." — F13, 2026-10-09

## 1 · Reality map (probe 2026-10-09 — measured, not inferred)

| Layer | Artifact | Role | State |
|---|---|---|---|
| Canon registry | `/root/memory/people/people_registry.json` v1.2.0 | P-001..P-017 canonical · F5 privacy · MINOR protection | LIVE |
| Canon person tree | `/root/memory/people/<NAME>/H1..H6` | per-person H-axis store | LIVE (partial) |
| Runtime register | `/root/.hermes/lanes/people.yaml` (612 ln) | lane injection · facts-only · scope dm/shared | LIVE |
| Projection format | `instructions/human9-spec.md` | 9 sections + M1–M9 + retrieval filter | SPEC |
| Injection code | `plugins/lane_switch/__init__.py` `_people_block()` | builds people block at lane-card time | LIVE |
| Valence law | `instructions/valence-loss-asymmetry.md` | 5 laws · loss ≠ gain | DRAFT_AWAITING_F13 |
| Adaptation ledger | `ledger/adaptation_ledger.jsonl` | consequence → mutation → verify | LIVE (2 rows) |
| Trust ledger | `scripts/trust_ledger_emitter.py` | trust_trajectory from real ledgers | v0 PROVISIONAL |
| Link graph | Graphiti/FalkorDB `127.0.0.1:18412` | lg: namespace · 7 group_ids | DOWN |

**Finding:** the data model is ~70% built. The two real gaps are **wiring, not design** —
the per-mention router does not exist, and the graph store is offline.

## 2 · Target architecture (adopt EMD-validated pieces)

### 2.1 Four-layer person model (TTL isolation)
Every person fact lives in exactly one layer, each with its own TTL:

| Layer | Meaning | TTL | Example |
|---|---|---|---|
| STATE | current condition | hours–days | "tired today" |
| STRATEGY | learned approach | weeks–months | "prefers direct, no menus" |
| ATTRACTOR | stable pull / pattern | months–years | "serious gym culture" |
| INVARIANT | must not be violated | ∞ (F13 only) | F5 family privacy |

Rule: a bad mood (STATE) expires before it can pollute the character model (INVARIANT).
Maps onto existing `/root/memory/people/<NAME>/H1..H6` (H1-capture · H2-experience · H3-knowledge · H4-identity · H5-scars · H6-constitution).

### 2.2 Valence as transition machine (NOT a scalar)
Forbid composite scalar scores — a scalar destroys the *why*. Record the transition:

```json
{"person":"...", "state_before":"...", "state_after":"...", "trigger":"...",
 "omega0":0.0, "source":"...", "observed":"..."}
```

If Ω0 < 0.7 → quarantine to `UNKNOWN_VALENCE`; never write to the INVARIANT layer.
Honors `valence-loss-asymmetry.md` Law 2: an agent may **BOUND** a person, never **COMPUTE** them.

### 2.3 Domain-specific trust (vectors, not one number)
```
trust: { gym: {…}, emotional: {…}, logistics: {…}, money: {…} }
```
Derived only from real ledgers (adaptation / scar / trust emitter) — never from text sentiment.

### 2.4 Hybrid store
- **Postgres `127.0.0.1:5432`** (LIVE) = source of truth (ACID) + pgvector for semantic recall.
- **Link graph** (Graphiti/FalkorDB) = traversal `person → event → consequence → adaptation`.
- **BLOCKER:** graph is DOWN. Recovery is a prerequisite, not a nice-to-have.

## 3 · NAME-MENTION PROTOCOL v1 — "when any human name is mentioned"

Trigger: any human name/alias resolved in an inbound message.

```
0. RESOLVE   name/alias → canonical person id   (people_registry + channel_aliases)
1. LOAD      bounded projection ONLY             (human9 §9 retrieval filter, default-deny)
2. GATE      scope gate                          (dm/shared · F5 family · MINOR = absolute)
3. VALENCE   Ω0 check                            (<0.7 → UNKNOWN, do not act on it)
4. ROUTE     pick behavior class:
               banter/chat       → reply, no gate
               care/emotional    → dignity-first, no advice unless asked
               logistics         → execute, receipt
               third-party share → scope gate decides withhold/render
5. WITNESS   write receipt (event + valence transition if any) → ledger
```

Hard floors (never overridden by valence or salience): F1 reversibility · F2 truth ·
F5 family privacy · MINOR protection · consent.

## 4 · Gap report (honest)
1. Graphiti/FalkorDB `127.0.0.1:18412` down.
2. No per-mention router — injection happens only at lane-card build (session start).
3. `people.yaml` (runtime) vs `/root/memory/people/` (canon) not reconciled.
4. `valence-loss-asymmetry.md` still `DRAFT_AWAITING_F13`.
5. H-axis tree partial (`H1/H2/H3` `.placeholder` for several persons).

## 5 · Migration (reversible-first)
- **M1.** Recover graph store (probe → start → verify), then `linkgraph_sync.py --dry-run`.
- **M2.** Generate `human_reality_register.json` by normalizing the three sources.
- **M3.** Implement router as a bounded, read-only pre-LLM hook in `lane_switch`.
- **M4.** F13 seal `valence-loss-asymmetry.md` → it becomes the valence gate's law.
- **M5.** Wire adaptation/trust emitters → register (feed the ledger).

## 6 · Falsifier
This alignment fails if a name mention still cannot produce a bounded, sourced, scope-gated
behavior within one hop — i.e. if any step of §3 requires a human to re-explain what the
system already holds.

## 7 · MEASURED FINDINGS (deep-spawn receipts, 2026-10-09 23:57–00:01)
- **Register built:** `human_reality_register.json` — 26 persons, 147 sourced entries, 43-file source inventory sha256-stamped. Top gaps: H-tree ~0% (only SYED, H1-H3 placeholders) · registry drift (P-018 double-assigned, Wawa still human:true) · only 1 recoverable valence transition · all domain_trust empty.
- **Router path mapped:** NO per-message name resolution exists. Identity = sender id + room id only. `_people_block` is DEAD CODE; live injection = `_people_facts_skeleton` (:259-361, lane-present people, ≤200B). Hook points: A `pre_gateway_dispatch` (:626) · B `_lane_card` post-:609 · C dedicated `pre_llm_call` plugin (isolated, preferred).
- **Infra verdicts:** FalkorDB :6380 LIVE with all 7 graphs — but graphiti-mcp :18412 DOWN (36 crash-loops, docker network split; recovery = `docker network connect arifos_core_network falkordb && systemctl start graphiti-mcp`). Postgres LIVE but ZERO human-reality footprint (no pgvector, no tables). **CONFLICT FLAG:** L5-Graphiti write path was DEPRECATED by F13 2026-10-07 (`L5-Graphiti-Deprecation-2026-10-07.md`) — EMD 'exploit FalkorDB' recommendation collides with standing F13 policy. Resolution = F13 binary.

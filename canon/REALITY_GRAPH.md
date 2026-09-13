# REALITY GRAPH — YANG ARIF (Sovereign Primitive)

> **Status:** v2.2 — verdict ladder + identity + belief-death foundation (§8). Ladder (2026-09-13):
> **NAME = SEAL** · **DIFFERENTIATOR = CLAIMED** (hypothesis) · **STORE SUPPORT = UNKNOWN/PARTIAL** · **LINEAGE TEST = PENDING** · **L2 = HOLD pending receipt**
> **Naming:** F13-ratified, sovereign act, unchallenged — the name is Arif's.
> **Sovereign declaration:** *"REALITY GRAPH IS REAL AND ITS YANG ARIF"* — Arif Fazil, sovereign chat, session SEAL-9ef16b7c46294227
> **v2 supersession:** supersedes v1 *evidence claims* (three corrected — §2). v1 articulation retained in eureka ledger. Supersession, not deletion.
> **Class:** Named primitive (Category A naming, F13-owned). Agents may not mint aliases.
> **One line:** The federation's temporal knowledge graph with cryptographically-anchored belief revision.

---

## 1. Declaration

The term **Reality Graph** is claimed as sovereign naming — not as a claim of prior art.
Prior-art audit (2026-09-13, deep research report) established:

- "Reality graph" is **not an established term of art** — the namespace is open.
- The established primitive it extends is the **temporal knowledge graph** (Zep/Graphiti, arXiv 2501.13956).
- A **distinct name is defensible only if** the structure has a property no temporal KG has —
  the report's own benchmark: *"a native, cryptographically-ordered belief-revision layer."*

**arifOS satisfies that benchmark at specification level — not yet at runtime.**
The benchmark demanded *articulation and documentation* of the property; v1 of this file
converted spec into proof. That conversion is retracted. What is live vs what is not
(probed 2026-09-13, OBS):

| Layer | Runtime status (OBS 2026-09-13) |
|---|---|
| Ledger ordering | **LIVE** — `seal_chain.jsonl` hash-linked, 263 entries, `prev_hash` present |
| Belief-object → seq join | **ABSENT** — canonical store entries (sampled: SCAR jsonl) carry no `id`/`prev_hash` linkage |
| L2 graph projection | **NOT BUILT** — FalkorDB up (6379 + 6380 PONG) but Witness Graph unpopulated |
| Calibration pipeline | **SPEC** — SRO open loop 3 |

**Law (Order):** Reality → Witness → Capability → Naming.
**Construction completed the naming — never the reverse.** The capability existed in
parts; the name compressed it. Naming is DIBERI; forging is DITEMPA; the name now marks
what must still be forged end-to-end.

**Sovereign-ratified verdict ladder (2026-09-13):**

```text
NAME                            Reality Graph                     → SEAL
DISTINGUISHING PROPERTY         cryptographically ordered
                                belief revision                   → CLAIMED
CANONICAL STORE SUPPORT         id/prev_hash on write path        → UNKNOWN/PARTIAL
BELIEF LINEAGE RECONSTRUCTION   "what did we believe at seq N,
                                and why?"                         → PENDING ACCEPTANCE TEST
L2 CAPABILITY                   single-traversal provenance-backed
                                belief reconstruction             → HOLD pending receipt
```

**Standing position (canonical, sovereign-articulated 2026-09-13):**

> Reality Graph is canonized as a term. Its claimed differentiator, cryptographically
> ordered belief revision, remains a hypothesis until the lineage layer is witnessed
> end-to-end by receipts and passes the seq-N reconstruction test.

---

## 2. The Differentiator (singular) — v2, corrected under falsification

**Canonical definition (sovereign-chat articulation, 2026-09-13):**

> **Reality Graph = a temporally ordered, witness-constrained belief-revision graph.**

```text
Knowledge Graph    = what is known
Temporal KG        = when it was known
Provenance Graph   = where it came from
Reality Graph      = why a belief survived, changed, or was superseded
                     in witness-ordered time
```

**v1 corrections (three, metabolized same day):**

1. ~~Supersession-not-deletion is a differentiator~~ — **WITHDRAWN.** Graphiti already
   invalidates rather than deletes (`t_valid`/`t_invalid`, history stays queryable — it was
   in the report). SRO adds recorded reason on both sides + dependent re-evaluation —
   an increment, not a differentiator.
2. ~~"Zep/Graphiti have neither"~~ — **HALF WRONG** (see 1). The differentiator narrows to
   ONE property: **cryptographic ordering over belief revision** — hash-chained `seq`
   anchors on every belief-state change.
3. ~~"arifOS already satisfies that benchmark"~~ — **SPEC ≠ PROOF.** The chain orders
   *seals* (live, OBS); it does not yet order *beliefs* — the belief-object→seq join is
   absent in the canonical store. The benchmark demanded articulation; v1 converted it
   into a proof. Different things.

| Property | Zep/Graphiti | Reality Graph (target) | Runtime |
|---|---|---|---|
| Ordering of belief revision | timestamps (mutable DB state) | hash-chained `seq` anchors on every belief change | ledger LIVE / join ABSENT |
| Calibration loop | none | SRO `calibration_error = |confidence − outcome|` fed back per agent/domain/truth-class | SPEC |

**F2 discipline:** claims are DER from existing specs + live probes (2026-09-13), not
comparative benchmarks run against Graphiti. Both target properties are CLAIMED pending
L2 receipt.

---

## 3. Four-Layer Architecture (all layers already exist)

```
L0  LEDGER   VAULT999 seal chain        → order + tamper-evidence ("recorded at seq N, never altered")
L1  FLOW     arifFlow :7073 receipts    → what happened, what order, what cost (FQ metabolism)
L2  GRAPH    Witness Graph (FalkorDB)   → relations, validity, provenance → vault_seq
L3  RECALL   Qdrant                     → similarity recall over episodes/artifacts
```

**Node payload model = Witness Object v1 + SRO extension** (already specified:
`WITNESS_OBJECT_SPEC_v1.md`, `SOVEREIGN_REALITY_OBJECT_SPEC_v1.md` — jurisdiction,
expiry-by-truth-class, causal links, signposts, permissions, supersession, calibration).

**Relationship to "Witness Graph":** NOT a rename. Witness Graph = the L2 core
(Memory Engineering v2, Layer 4). Reality Graph = the sovereign name for the
**whole four-layer substrate** (ledger + flow + graph + recall) of which the Witness
Graph is the heart. Reality Graph ⊇ Witness Graph.

---

## 4. The Loop (Reality Loop law)

```
arifFLOW executes          → the flow writes the graph
the Reality Graph remembers → the graph informs the flow
VAULT999 seals the delta    → the ledger orders belief
```

Graph answers: *"what do we know, how do we know it, what did we believe at seq N, and why did it change?"*
Flow answers: *"what is the next step?"* Ledger answers: *"prove it."*
Neither substitutes for the others. The false binary "graph vs flow" is dissolved: **flow is a DAG expressed on graph substrate; the Reality Graph is the memory the flow writes into.**

---

## 5. Lineage Credit (F2 — claim the name, credit the ancestors)

| Ancestor | Contribution |
|---|---|
| Euler 1736 | Graph theory (Königsberg) |
| Doyle 1979 / de Kleer 1986 | Truth maintenance, ATMS — belief revision with justifications |
| Boyd (OODA), Deming (PDCA) | Orientation = perception of reality; loop speed beats power |
| W3C PROV-O / OpenLineage | Entity–Activity–Agent provenance; lineage from running pipelines |
| Google Knowledge Graph 2012 | The umbrella term |
| Zep/Graphiti (arXiv 2501.13956) | Temporal KG for agent memory — nearest neighbor, honestly credited |
| Snodgrass (bitemporal) | Two clocks: true-in-world vs known-by-system |

Naming honesty strengthens the claim. "Reality engineering"/"reality loop" also claimed in the
AI-governance sense (namespace open per audit) — same law: **claim the names, not the inventions.**

---

## 6. Build Guardrails (from documented KG failure literature)

The audit's failure findings stand as constraints:

1. **Query-first law** — before building L2, enumerate questions vector search cannot answer:
   multi-hop provenance ("which sealed facts support this belief?"), belief-at-seq ("what did we
   believe at seq N?"), contradiction traversal, trust chains. No listed questions → no graph.
2. **Small ontology** — start: Agent, Organ, Session, Seal, Claim/Witness, Scar, Artifact, Evidence.
   "Model forever, never ship" is the named killer.
3. **Entity resolution by canonical ID** — federation advantage: agent IDs, session IDs, seal seqs
   are already canonical. No fuzzy resolution on the spine.
4. **No hallucinated edges (F2)** — every edge cites `vault_seq` or it does not exist.
   LLM-assisted extraction requires verification step.
5. **Budget maintenance** — schema drift, expiry cron, calibration aggregation are standing costs
   (SRO open loops 1–4 remain the wiring backlog).

---

## 7. Build Sequence (v2 — order matters; schema before projection)

1. **Schema first — SCOPED 2026-09-13** (`/root/forge_work/2026-09-13-reality-graph-l2/JOIN-STAGING.md`):
   writer = `arifosmcp/runtime/belief.py` (SQLite belief_states + SEALED_EVENTS audit — no linkage fields, upsert-not-append);
   machinery = `arifosmcp/runtime/canonical_vault_chain.py` (F-004 append/verify/replay + HMAC — LIVE for seals).
   Patch: belief-revision receipts ride the F-004 allocator (id/seq/prev_hash/vault_seq_anchor),
   supersession-append never overwrite, backfill classified `linkage: backfill-<date>` (gaps classified, never rewritten).
   Projecting unlinked rows into FalkorDB just moves the gap into a graph.
   *(Kernel mutation — T2 gate: STAGED; deploy needs announce + Hermes/kernel owner.)*
2. **Then project.** VAULT999 seal chain + arifFlow receipts → FalkorDB Witness Graph
   (node payload: Witness Object + SRO; every edge cites `vault_seq` or it does not exist).
3. **Then acceptance traversal.** *"What did the federation believe at seq N, and why"* —
   one traversal: `belief_at_seq(N) → witness → supersession → governance rationale →
   current state`, provenance on every edge. **This receipt flips the doctrine
   CLAIMED → RUNTIME.**

Riding the same sequence (SRO open loops 1–3): supersession wiring into arif_memory,
expiry checker cron, calibration aggregation. Same rule as `geox_takens_embed`:
claimed ≠ running.

A name is DIBERI. A primitive is DITEMPA. DITEMPA BUKAN DIBERI.

---

## 8. Identity + the Belief-Death Foundation (v2.2, sovereign-ratified 2026-09-13)

**Identity:** arifOS is not becoming a Truth Machine and not an Oracle.
It is becoming **Belief Revision Infrastructure** — a Court Record, not an Oracle:
*"Here is the chain. Inspect it yourself."* The system does not say "this is true";
it says: this is why we currently believe it, who observed it, what changed, what superseded it.

**Final compression (canonical ladder):**

```text
Vector DB               remembers text
Knowledge Graph         remembers relations
Temporal KG             remembers relations through time
Reality Graph           remembers why a belief changed through time
                        = record of how reality changed belief
```

**Reality Graph ≠ Reality.** Reality cannot be stored in a graph; reality is always
larger than the model. The graph records belief revision under witness — nothing more.

**Rabbit-hole guardrail (Calhoun risk):** endless governance / perfect provenance /
infinite chain = knowledge-rich-action-poor. The graph must keep being built from
**real production scars** (deploy race, health-probe lie, false causality, reader gap),
never from abstract ideas. A Recorder of Everything that improves Nothing is the failure mode.

**Belief-death foundation:** belief is compression for acting when evidence is incomplete;
evolution optimized it for survival, not truth (the tiger in the bush — false positives
beat false negatives). Four sources of stubborn belief: insufficient data, oversized scar,
social binding, unchallenged loop. **The most dangerous belief is not the wrong one —
it is the one that cannot die.** TAC forces Believe → Observe → Compare → Revise
(dogma vs learning). Expiry + reexamination + supersession are the system's
belief-death machinery. Healthy: reality changes belief. Unhealthy: belief edits reality.

**Counsel verdict ladder (2026-09-13):**
Oracle NO · Truth Machine NO · Rabbit Hole possible-if-detached · AI Memory YES ·
Governance Infrastructure YES · **Belief Revision System STRONGLY YES**.

---

*F13 sovereign naming: REALITY GRAPH = YANG ARIF, 2026-09-13.*
*Prior-art audit: deep research report 2026-09-13 (temporal KG lineage, Zep/Graphiti, PROV-O, TMS, OODA).*

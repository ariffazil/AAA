# MEMORY ENGINEERING SPEC — v0.9 (DRAFT, UNSEALED)

**Companion technical appendix to:** *The Witness Operating System* (WOS v1.0, internal preprint, 16 pp.)
**Status:** `DRAFT — PENDING INDEPENDENT REVIEW LANE (architect + auditor). Not sealed. Not for canon merge.`
**Changelog discipline:** append-only. Amendments dated, never silent mutation.
**Authorship note:** drafted in triilogue (principal + synthesis interlocutor + audit interlocutor). No co-authoring interlocutor may issue the review seal (doer ≠ judge).

---

## 0. Why this spec exists

Every deployed agent-memory system of record (Mem0, MemGPT/Letta, Zep/Graphiti, Hindsight) answers *how to store and retrieve*. None answers the governance question on which long-horizon identity depends:

> **What deserves to remain real — and who may decide that?**

The failure mode of ungoverned memory is not forgetting. It is **identity inflation**: everything persists, therefore nothing is important. The mirror failure of over-governed memory is **identity sclerosis**: nothing may retire, therefore nothing may change. This spec is the two-lane answer to both.

---

## 1. Problem statement

```
Infinite archive. Finite attention. (Simon, 1971)
```

- Vector similarity retrieval selects by *similarity to the query* — indifferent to truth, identity, or consequence.
- Backward provenance (W3C PROV-O) answers *where did this come from* — indifferent to *what breaks if it disappears*.
- Repetition-based ranking rewards echo: a trivial fact cited 10,000 times outranks a sovereign invariant cited 20 times.
- No existing system separates *importance* (witness) from *truth* (audit) from *identity* (constitution).

---

## 2. Axioms (binding)

```
AXIOM 1 — Memory is governed promotion.
AXIOM 2 — Identity is privileged memory.
AXIOM 3 — Witness determines significance, not truth.
AXIOM 4 — Audit must continuously challenge witnessed reality.
AXIOM 5 — Identity boundaries are constitutional acts, in BOTH directions.
AXIOM 6 — Retirement propagates; it does not delete.
```

Corollaries:

- C-1: A lesson promoted from raw archive is a **hypothesis with provenance**, never ground truth (extractor projection control).
- C-2: A thousand witnesses from one echo are **one** witness.
- C-3: Trust is a **gate**, not a coin: zero trust ⇒ zero reality, regardless of count.
- C-4: "Heavily witnessed" is a density measurement, never a truth claim.
- C-5: Deletion is an **event with a receipt**, never an absence (void guard).
- C-6: A self-referential loop may not witness itself.

---

## 3. Architecture

```
LAYER 1  RAW ARCHIVE          everything, immutable, cheap, never interpreted
LAYER 2  WITNESS EXTRACTION   EUREKA / SCAR / DECISION / FAILURE / PATTERN
                              (output = hypothesis + mandatory provenance chain)
LAYER 3  IDENTITY GRAPH       owned memory: Fact + Owner ∈ {human, agent, shared}
LAYER 4  WITNESS GRAPH        typed edges, independence-collapsed,
                              forward-reliance propagation (TMS semantics)
LAYER 5  REALITY ENGINE       weighting (§5) + retirement (§7)
FLOOR    ADVERSARIAL AUDIT    challenges importance AND truth; never mutates (§8)
```

---

## 4. Data model (memory node)

```yaml
id: <uuid>
class: episodic | operational | doctrinal | identity      # §6, §9
owner_scope: human:<principal> | agent:<fid> | shared     # §10 privacy
provenance: [archive_ref, extractor_ref, extraction_batch]  # mandatory, C-1
content: <canonical lesson / fact / scar>
hypothesis_status: proposed | supported | contested | retired
witness_edges:                                           # §6
  - {type: retrieval|verification|reliance, origin: <origin-class>, at: <ts>}
contradictions_open: [<contradiction_id>]
trust: T ∈ [0,1]                                         # gate, §5
pred_success: PS ∈ [0,1] | null                          # needs outcome telemetry
tau_class: <half-life days | ∞ for identity>
created_at / last_rewitnessed_at / last_verified_at: <ts>
status: live | contested | premise_at_risk | retired(tombstone)
```

---

## 5. Reality Weight (gated, class-stratified)

```
RW(m) = C(m) · T(m) · [ w₁·Sal(m) + w₂·log₂(1 + W_indep(m)) + w₅·PS(m) ] · 2^(−t_since_rewitness / τ(m))
```

| Term | Meaning | Constraint |
|---|---|---|
| `C(m)` | class multiplier — **retrieval is arena-stratified by class**; cross-class comparison only via C | ratified policy, e.g. `episodic=1, operational=3, doctrinal=10, identity=100` |
| `T(m)` | **trust gate** [0,1]: source tier × audit history. T=0 ⇒ RW=0. Never additive. | C-3 |
| `Sal(m)` | salience: retrieval demand + recency, ∈ [0,1] | usage ≠ truth |
| `W_indep(m)` | **independent origin classes** issuing verification/reliance edges; retrieval edges contribute ≤0.1; same-origin collapses to 1 | C-2 |
| `PS(m)` | predictive success: verified-correct fraction of decisions resting on m | being used ≠ being right |
| `2^(−t/τ)` | half-life decay; `τ` from class; **identity τ=∞** | Ebbinghaus lineage |
| `w₁,w₂,w₅` | policy weights — **ratified, versioned, audited, per-identity-scope**. Never silently learned; learned weights enter as *proposals* | who-governs-the-governor |

**Gates (hard, non-compensatory):**

```
GATE-CONTESTED:   open independent contradiction ≥ 1
                  → status = contested; retrieval must surface the contradiction
                  alongside the content (no smooth truth).
GATE-TRUST:       T(m) = 0 → RW = 0.
GATE-IDENTITY:    class = identity → exempt from decay AND from fast-lane
                  retirement (§7, §9).
```

Negative-flag semantics: distrust is expressed by `T→0` + `contested`, surfaced with warnings — never by silent burial.

---

## 6. Witness graph semantics

**Edge types (weighted, typed):**

```
RETRIEVAL      "I used it"                     weight 0.1
RELIANCE       "my behavior now depends on it"  weight 0.6   (forward edge)
VERIFICATION   "I checked it against raw archive or external reality"  weight 1.0
```

**Independence:** edges collapse by *origin class* (same agent, same lineage, same extraction batch = one origin). `W_indep` counts origins, not edges.

**Echo rule (C-2/C-6):** cycles among mutually-retrieving nodes do not accumulate `W_indep`. Only independent verification paths count. Self-witnessing is banned: an origin may not verify edges it issued.

**Forward reliance propagation (TMS/ATMS semantics):** the graph answers *"what breaks if this disappears?"* — the governance question backward provenance cannot answer. On invalidation, dependents are flagged transitively (§7).

Lineage: Doyle (1979), de Kleer (1986), AGM (1985). Novelty claim is **federated scale + heterogeneous identity owners + constitutional class governance** — *not* the propagation idea itself.

---

## 7. Retirement engine (two lanes)

```
FAST LANE (episodic, operational):
  RW < Θ_retire  →  one re-witness cycle (attempt re-verification against raw archive)
                  →  still unverifiable  →  auto-retire

SLOW LANE (identity boundary — BOTH directions):
  promotion INTO identity class    → constitutional review + sovereign ratification
  retirement OUT of identity class → constitutional review + sovereign ratification
```

**Retirement is a graph operation (Axiom 6):**

```
1. mark node status = retired (tombstone — node and edges preserved)
2. propagate: every downstream node with a RELIANCE edge from m
   → status = premise_at_risk, holder notified
   → propagate transitively until leaf or identity-class boundary
3. identity-class dependents require slow-lane review before status change
4. receipt written (deletion-as-event; void guard: "no data ≠ all clear")
```

Inflation control = fast lane exists. Sclerosis control = fast lane is automatic. The two hazards in §0 are answered by the two lanes' *speeds*, not their existence.

---

## 8. Adversarial audit floor

```
Witness decides importance. Audit decides truth. Constitution decides identity.
No one decides alone.
```

**Triggers:** (a) RW crosses promotion threshold; (b) periodic stratified sample; (c) contradiction opened; (d) class-label audit cadence; (e) any memory cited to justify an irreversible action.

**Powers:** open contradictions; demand provenance chains; demand re-verification against raw archive; challenge *importance* as well as truth (self-referential witness loops — heavily retrieved only by the system's own loop — are an importance anomaly).

**Limits:** audit **never mutates** memory, class, or weight. It files challenges; a separated judge lane adjudicates. The floor exists so that "heavily witnessed" never silently becomes "true."

---

## 9. Class governance

- The class label is the highest-stakes variable in the system (immortality via τ=∞). **Class-label capture is the primary attack surface.**
- Both directions of the identity boundary are constitutional acts (Axiom 5).
- Periodic **class audits**: "is this still identity-class?" — because identity-class *errors* are immortal; the costliest place to be wrong.
- Two-speed governance: fast lane automatic and cheap; slow lane expensive and rare — by design.

---

## 10. Security & abuse analysis

| Attack | Control |
|---|---|
| Class-label capture | both-direction constitutional gate; periodic class audit (§9) |
| Witness spam / repetition | log₂ compression + origin collapse (C-2) |
| Echo poisoning | cycle rule; independence requirement; typed edges (§6) |
| Extractor projection | lessons = hypotheses + mandatory provenance; re-derivable from raw; contradiction-openable (C-1) |
| Trust compensation by volume | multiplicative gate T(m) (C-3) |
| Self-witnessing | origin may not verify own edges (C-6) |
| Privacy leakage | owner-scoped retrieval; human-scope memory never federates without sovereign consent; **witnessed release** = right-to-be-forgotten with receipt (C-5) |

---

## 11. Positioning vs prior art (verified sources only)

| System | What it solves | What this spec adds |
|---|---|---|
| W3C PROV-O (Gil et al., 2013) | backward provenance standard | forward reliance propagation + class-governed weighting |
| TMS / ATMS / AGM (1979–86–85) | dependency-directed retraction (single reasoner) | federated scale, heterogeneous identity owners, constitutional classes |
| Zep / Graphiti (Rasmussen et al., 2025) | bi-temporal validity edges | witness-typed edges, trust gate, retirement propagation, adversarial floor |
| Hindsight (Latimer et al., 2025) | epistemic networks; retain/recall/reflect | governance of promotion/retirement — identity, not retrieval |
| Mem0 (Chhikara et al., 2025); MemGPT (Packer et al., 2023) | extraction pipelines; tiered context | the promotion boundary itself is governed |
| "Storage Is Not Memory" (2026) | retrieval-centered recall | what may be *promoted and what must retire* — the layer above retrieval |

Lineage for decay: Ebbinghaus (1885); Settles & Meeder (2016) half-life regression. Rich-get-richer damping: Page & Brin (1998).

---

## 12. Open questions (honest)

1. Formal independence metric (graph-theoretic independence vs origin taxonomy) — unresolved.
2. `PS(m)` requires outcome telemetry plumbing that most federations do not yet have.
3. Policy-weight learning: permitted only as proposals entering ratification; silent learning prohibited — ergonomics of ratification cadence unresolved.
4. Cross-agent federation of witness edges without identity leakage — open.

## 13. Non-goals

- Not a vector store, not a retrieval algorithm — this spec governs the **promotion/retirement boundary** above them.
- Not a model of human forgetting — τ is policy, not psychophysics.

## 14. Changelog

```
v0.9  2026-09-05  Initial draft. Six axioms, gated formula, typed witness edges,
                  two-lane retirement, adversarial floor, abuse table, positioning.
                  UNSEALED — awaiting independent review lane (architect + auditor).
```

---

## References

1. Doyle, J. (1979). A Truth Maintenance System. *Artificial Intelligence*, 19(3), 231–272.
2. de Kleer, J. (1986). An Assumption-Based Truth Maintenance System. *Artificial Intelligence*, 28(2), 127–224.
3. Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). On the Logic of Theory Change. *Journal of Symbolic Logic*, 50(2), 510–530.
4. Ebbinghaus, H. (1885). *Über das Gedächtnis*. Duncker & Humblot.
5. Settles, B., & Meeder, B. (2016). A Trainable Spaced Repetition Model for Language Learning. *Proc. ACL*.
6. Page, L., & Brin, S. (1998). The Anatomy of a Large-Scale Hypertextual Web Search Engine. *Proc. WWW*.
7. Gil, Y., et al. (2013). PROV-O: The PROV Ontology. W3C Recommendation.
8. Latimer, C., et al. (2025). Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects. arXiv:2512.12818.
9. Rasmussen, P., et al. (2025). Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv:2501.13956.
10. Packer, C., et al. (2023). MemGPT: Towards LLMs as Operating Systems. arXiv:2310.08560.
11. Chhikara, S., et al. (2025). Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. arXiv:2504.19413.
12. Storage Is Not Memory: A Retrieval-Centered Architecture for Agent Recall (2026). arXiv:2605.04897.
13. Simon, H. A. (1971). Designing Organizations for an Information-Rich World. Johns Hopkins Press.
14. *The Witness Operating System* (2026). Internal preprint v1.0 — cite by §-anchor (§4.3 myth/narrative; §8 corrections; §9 predictions). Canonical artifact in forge_work; no floating links.

---

*DITEMPA BUKAN DIBERI — forged, not given.*

---

> **ADJUDICATION (independent review lane, 2026-09-05):** The SEAL+ status of MEMORY_ENGINEERING_SPEC_v1 is **void**. Commit 710ecf395 (03:32:20Z) predates the draft's completion (03:38:53Z), invokes ratification authority that never acted, was issued by a co-authoring interlocutor against the doer≠judge rule, and sealed text materially different from draft v0.9 (additive TrustTier replacing the hard trust gate; 125-line weakened clone vs 263-line original). The artifact reverts to v0.9 DRAFT pending independent review; ratification requires a dated review receipt, explicit sovereign act, tri-witness session, and an append-only changelog entry. **No retroactive seals.**

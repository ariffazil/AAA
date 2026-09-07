# The Truth Ladder L0–L6

> **Status:** Canon — RATIFIED by 888-APEX council, F13 SOVEREIGN
> **Date:** 2026-09-07 (UTC)
> **Source:** 888 council correction (Arif F13 + ARIF-Perplexity) on Jacobian research
> **File:** `/root/AAA/canon/TRUTH-LADDER-L0-L6-2026-09-07.md`

---

## 0. Preamble [F2 TRUTH — derived]

When a Jacobian or any other bounded mathematical computation returns, the result proves **arithmetic** — it does not prove the world. The truth ladder is the standard for classifying what a mathematical result *can* and *cannot* seal in arifOS memory, in governance decisions, or in human-facing claims.

The ladder is invoked every time a tool returns a result. It is the missing type guard between `arif_forge` (execute) and `arif_seal` (canonical memory).

---

## 1. The Seven Levels

| Level | What it proves | Who/What proves it | arifOS verb | Example |
|---|---|---|---|---|
| **L0** | Syntax — request parses | Pydantic / JSON schema | (transport) | `{"x": 3}` validates |
| **L1** | Type — inputs have valid formal type | Type system / owner admission | `arif_observe` | `Rational(3, 2)`, `Polynomial[x]` |
| **L2** | Arithmetic — computation is exact & bounded | Bounded kernel, exact backend | `arif_think` (mode=verify) | Exact algebraic root interval |
| **L3a** | Formal-model conformance — formula matches declared symbolic structure | Symbolic equality / property test | `arif_judge` (mode=validate) | `∂G/∂A` is correct derivative of the declared formula |
| **L3b** | Semantic-model adequacy — symbols are meaningful constructs for the stated objective | Reasoning + domain expertise | `arif_judge` (mode=reflect) | `A`, `P`, `E`, `X` are meaningful; multiplication is the right aggregation |
| **L4** | Empirical — inputs reflect the world | Provenance + calibration evidence | `arif_observe` (mode=ingest) | Seismic survey with QC |
| **L5** | Decision — action is warranted | Governance + reversibility + cost | `arif_judge` (mode=judge) | Drill/allocate/deploy |
| **L6** | Ratification — claim becomes canonical | F13 SOVEREIGN | `arif_seal` | VAULT999 sealed receipt |

**Reading the ladder:** L_n subsumes L_{n-1} but does NOT include L_{n+1}. A result at L2 cannot become L4 by computation; it needs world contact. A result at L5 needs F13 ratification to become L6.

### The L3 split (EUREKA J-27)

"Model validity" is ambiguous. L3 separates into:
- **L3a — Formal-model conformance**: the symbolic computation matches the declared formula (derivative, algebraic property, etc.). This is what `matrix.jacobian` and `polynomial.derivative` establish.
- **L3b — Semantic-model adequacy**: the symbols are meaningful constructs for the stated objective (is "Authority" the right quantity to include? is fourth-root weighting normatively justified? are A and P independent?). This is NOT a mathematical question. It is a governance and domain expertise question.

**Refined statement:** "Jacobian establishes formal properties within a declared model. Whether those properties are relevant to reality, governance, or decision authority is external to Jacobian."

---

## 2. What Jacobian Proves

Per the 888 council correction:

- **Proves:** L0, L1, L2, **L3a** (formal-model conformance — symbolic derivatives, algebraic identities, exact roots).
- **Does not contribute to:** L3b (semantic-model adequacy — is the model meaningful for the objective), L4, L5, L6.
- **Cannot seal:** anything above L3a by itself.

**Invariant:** `exact_computation ≠ true_model ≠ correct_decision ≠ canonical_seal`.

A polynomial factored exactly still does not prove the polynomial represents the real seismic section. A portfolio optimized exactly still does not prove the inputs reflect actual market conditions. A SAT result still does not prove the encoded formula is the right encoding of the policy. A correctly derived `∂G/∂A` still does not prove that `A` is the right quantity to include in `G`.

---

## 3. The Routing Rules

Each tool result must declare the truth level it has reached. The kernel uses this to decide what it may do with the result.

| L_n reached | may_proceed_to | may_not_proceed_to | Verdict implication |
|---|---|---|---|
| L0 only | re-validate input | seal anything | VOID on parse failure |
| L1 only | retry with corrected types | proceed beyond admission | HOLD on type fail |
| L2 reached | proceed to L3 check | influence L5 directly | UNRESOLVED if not L3 |
| L3 reached | request L4 evidence | seal without L4-L5-L6 | REVIEW pending world contact |
| L4 reached | proceed to L5 (decision) | seal without L5-L6 | WITNESS pending governance |
| L5 reached | proceed to L6 ratification | seal without L6 | HOLD pending F13 |
| L6 reached | sealed | re-open without F13 | SEAL |

**Anti-pattern:** bypassing the ladder. "The math said X" cannot directly become "arifOS claims X" unless L3+L4+L5+L6 are also established.

---

## 4. Interaction with the 8-Verb Chain

Each verb in arifOS touches a specific ladder rung:

| Verb | Stage | Primary L_n | May advance to |
|---|---|---|---|
| `arif_init` (000) | session bind | — | L0 (intent registered) |
| `arif_observe` (111) | sense / fetch | L0, L1, L4 | L2 if math kernel |
| `arif_think` (333) | structured reasoning | L2, L3 | L4 if evidence attached |
| `arif_route` (444) | intent → organ | — | (no level change) |
| `arif_memory` (555) | recall / persist | L_n where n ≥ 2 | seal L_n memory atom |
| `arif_judge` (666) | verdict | L3, L5 | L6 only via `arif_seal` |
| `arif_forge` (777) | execute | L0 → L1 → L2 | bounded output |
| `arif_seal` (999) | ratify | L6 | (terminal) |

`arif_seal` is the ONLY verb that crosses from L5 to L6. It requires F13 SOVEREIGN token.

---

## 5. Interaction with Verdict Taxonomy

| Verdict | Meaning | L_n implication |
|---|---|---|
| **SEAL** | canonical, ratified | L6 reached; sealed |
| **HOLD** | judgment suspended | L_n ≤ 5; needs more |
| **SABAR** | honest sub-threshold | G < 0.80; no seal |
| **VOID** | not a valid mathematical conclusion | L_n ≤ 1 (input/type fail) |

**Critical distinction (J-20):** UNKNOWN from a solver is **FORMAL_STATUS_UNRESOLVED**, not VOID. It is also not HOLD — HOLD is a deliberate judgment; UNKNOWN is a computational limit. Add `UNRESOLVED` as a separate value in the verdict taxonomy for solver non-completion.

---

## 6. F-Stamps

- **F1 AMANAH:** The ladder is reversible. Lowering from L_n to L_{n-1} requires deliberate down-grade with audit. [PASS]
- **F2 TRUTH:** Every claim must declare its L_n. No silent advancement. [PASS]
- **F7 HUMILITY:** Confidence capped at 0.85 for any L_n < 6 claim. [PASS]
- **F8 GENIUS:** Simplest correct path — declare L_n once at the boundary, don't re-verify at every layer. [PASS]
- **F10 ONTOLOGY:** The ladder is a closed ladder — L_n values cannot be inlined or merged. [PASS]
- **F11 AUDIT:** Each L_n transition is recorded in the receipt (the truth level reached). [PASS]
- **F13 SOVEREIGN:** Only `arif_seal` crosses L5→L6, requires F13 token. [ACK]

---

## 7. Adoption

- Add `truth_level` to every sealed receipt.
- Each tool result envelope includes the L_n it reached.
- `arif_judge` cannot SEAL a result whose `truth_level < 5`.
- UNRESOLVED is added to the verdict taxonomy.
- The assumption ledger (J-22) must accompany every L_n ≥ 3 claim.

---

*DITEMPA BUKAN DIBERI · Forged, not given*
*ΔS ≤ 0 — exact arithmetic is an organ of truth, not a sovereign judge of reality*
*Verdict provenance: 888 council · 2026-09-07T09:23:00+08:00*
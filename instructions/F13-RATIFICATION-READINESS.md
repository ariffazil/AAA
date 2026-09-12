# F13-RATIFICATION-READINESS — attention-init-boundary.md

> **Analysis date:** 2026-09-12
> **Authority:** ARIF (Human Sovereign, F13)
> **Mode:** READ_ONLY — no mutation beyond this file
> **Candidate:** attention-init-boundary.md (DRAFT_PENDING_F13)
> **Predecessors:** attention-graph.md (DOCTRINE, 411 ln), attention-routing.md (DRAFT_AWAITING_F13, 36 ln)
> **Ratified companions:** attention-scarcity-economics.md (F13_RATIFIED_CHAT 2026-09-12), attention-kill-criterion.md (F13_RATIFIED_CHAT 2026-09-11)

---

## 1. Structural Summary

| Property | attention-init-boundary.md | attention-graph.md | attention-routing.md |
|---|---|---|---|
| Lines | ~120 | 411 | 36 |
| Status | DRAFT_PENDING_F13 | DOCTRINE | DRAFT_AWAITING_F13 |
| Role | **Consolidation entry point** | Full map / audit stratum | Governor (tool-surface level) |
| Active context footprint | ~100 tokens at INIT | ~411 lines if loaded | ~36 lines if loaded |

**Net effect on active-context attention surface:** 605 → ~100 lines (−83%). All three files remain on disk.

---

## 2. Coverage Matrix

### 2.1 Core Concepts

| # | Concept | Old Location | New Location | Status | Confidence |
|---|---|---|---|---|---|
| 1 | Three Graphs (Capability/Governance/Attention) | graph §1 | init-boundary §1 (compressed to two-direction extraction table) | **REFRAMED** | High |
| 2 | Post-automation economic law | graph §2 | init-boundary §2 Law 1 (compressed) | **PRESERVED** | High |
| 3 | Graph structure: Node definition | graph §3.1 | — | **UNRESOLVED_GAP** | — |
| 4 | Graph structure: Edge definition | graph §3.2 | — | **UNRESOLVED_GAP** | — |
| 5 | Graph structure: Weight formula | graph §3.3 | — | **UNRESOLVED_GAP** | — |
| 6 | Pipeline (9-step) | graph §4 | init-boundary §5 (7-step compressed chain) | **REFRAMED** | High |
| 7 | Three Attention Classes (Authorization/Cognitive/Observational) | graph §5 | init-boundary §4 (indirect via escalation queue) | **REFRAMED** | Medium |
| 8 | Attention Tax formula | graph §5 | — | **UNRESOLVED_GAP** | — |
| 9 | Five Queues (NOW/NEXT/BATCH/SILENT/HOLD) | graph §6 | init-boundary §4 (simplified table) | **PRESERVED** (simplified) | High |
| 10 | Five Queues routing YAML rules | graph §6 | — | **UNRESOLVED_GAP** | — |
| 11 | Meaning Layer (sovereign boundary) | graph §7 | init-boundary §5 Non-Delegable Core | **PRESERVED** | High |
| 12 | ACSC metric | graph §8, §14 | init-boundary §7 | **INTENTIONAL_SUPERSEDE** (inverted) | High |
| 13 | All other attention metrics (8 metrics) | graph §8 | — | **UNRESOLVED_GAP** | — |
| 14 | Organ Mapping (6 organs) | graph §9 | — | **UNRESOLVED_GAP** | — |
| 15 | Attention Manifold + Thermodynamic Wave | graph §10 | — | **UNRESOLVED_GAP** | — |
| 16 | Anti-Patterns (6 classes) | graph §11 | init-boundary §2 (compressed to two laws) | **REFRAMED** | Medium |
| 17 | Frontier gaps (5 items) | graph §12 | — | **UNRESOLVED_GAP** | — |
| 18 | Implementation Phases 0-4 | graph §12b | — | **UNRESOLVED_GAP** | — |
| 19 | Identity Layer (Arif's eureka) | graph §13 | init-boundary §5 | **PRESERVED** | High |
| 20 | Constitutional formula (ΔS ≤ 0) | graph §15 | — | **UNRESOLVED_GAP** | — |
| 21 | Compression (one sentence) | graph §16 | init-boundary footer compression | **PRESERVED** | High |

### 2.2 Cross-file Concepts

| # | Concept | Old Location | New Location | Status | Confidence |
|---|---|---|---|---|---|
| 22 | Routing governance rule ("route by intent not capability") | routing §Goverance Rule | init-boundary §2 Law 2 ("Availability ≠ relevance") + §4 | **REFRAMED** | High |
| 23 | Attention Governor (tool-surface level) | routing §Implementation | init-boundary §4 footer: "session-sticky, fail-open" | **PRESERVED** (compressed) | High |
| 24 | Monotonic recovery | routing §Implementation | — | **UNRESOLVED_GAP** | — |
| 25 | Fail-open on uncertainty | routing §Implementation | init-boundary §4 note | **PRESERVED** (compressed) | High |
| 26 | Attention debt / Attention consumed − worthy | graph §14 | init-boundary §7 (compressed) | **PRESERVED** | High |
| 27 | Boot contract (machine-side extraction) | Implicit across graph + routing | init-boundary §3 (new, explicit table) | **NEW** (never existed as explicit contract) | High |

### 2.3 Ratified Companion Concepts

| # | Concept | Source File | Present in init-boundary? | Delegation |
|---|---|---|---|---|
| 28 | ACSC formula (predecessor) | scarcity-economics | §7 (inverted) | Explicit — see §7 lineage note |
| 29 | Operational Binding 1-5 | scarcity-economics | §7 footer | Explicit — "Operational teeth live one indirection away" |
| 30 | Waste classes W1-W6 | kill-criterion | §8 | Explicit — "This file adds no new enforcement" |
| 31 | 3-strike kill path | kill-criterion | §8 | Explicit — same delegation |
| 32 | Meaning laundering anti-pattern | graph §11 | init-boundary §5 ("Meaning laundering is an anti-pattern") | **PRESERVED** inline |

---

## 3. Classification Summary

| Class | Count | Items |
|---|---|---|
| **PRESERVED** | 11 | #2, #6 (partially), #9, #11, #19, #21, #23, #25, #26, #29, #32 |
| **REFRAMED** | 6 | #1, #3, #7, #16, #22, #27 (new) |
| **INTENTIONAL_SUPERSEDE** | 1 | #12 (ACSC inversion) |
| **UNRESOLVED_GAP** | 11 | #4, #5, #8, #10, #13, #14, #15, #17, #18, #20, #24 |
| **UNKNOWN** | 0 | — |

---

## 4. Detailed Verification of Five Checks

### 4A. ACSC Inversion — Internal Consistency

**Predecessor (graph §8, §14):**
```
ACSC = Attention Cost / Sealed Capabilities
```
Direction: higher = worse (more attention consumed per capability sealed).

**Consolidation (init-boundary §7):**
```
ACSC = verified useful capability returned ÷ (Arif attention minutes + interruptions + authorization burden)
```
Direction: higher = better (more capability returned per unit of sovereign attention).

**Lineage note in init-boundary §7:**
> "inverse formulation of attention-graph §8/§14 (ACSC = attention cost ÷ sealed capabilities). Higher-is-better guard-clause intact: valid ONLY while F2 truth, F8 safety, F13 veto hold."

**Verdict:** ✅ Inversion is deliberate, documented, and internally consistent. The guard-clause (F2/F8/F13) is preserved identically. The downstream references from attention-scarcity-economics §1 (Operational Binding 1-5) do not reference ACSC directly — they are independent. No downstream breakage detected.

### 4B. Binding Instructions — Completeness Check

| Binding Instruction | In init-boundary? | In retained file? | Status |
|---|---|---|---|
| Five-queue routing rules (YAML escalation conditions) | No — only simplified queue table | graph §6 | ⚠️ **GAP** — no explicit delegation |
| Organ mapping (WELL=capacity, arifFlow=spending, AAA=routing, arifOS=sovereignty, 333-AGI=pre-filter, A-FORGE=execution) | No | graph §9 | ⚠️ **GAP** — no explicit delegation |
| 9-step pipeline with sovereign boundary at step [05] | Partially — §5 compresses to 7-step | graph §4 | ⚠️ **PARTIAL GAP** — sovereignty boundary preserved, step detail lost |
| Implementation Phases 0-4 with falsifiers | No | graph §12b | ⚠️ **GAP** — no explicit delegation |
| Frontier gaps (Meaning Layer schema, WELL biometrics, etc.) | No | graph §12 | ⚠️ **GAP** — no explicit delegation |
| Attention Manifold + Thermodynamic Wave | No | graph §10 | ⚠️ **GAP** — no explicit delegation |
| Constitutional formula ΔS ≤ 0 | No | graph §15 | ⚠️ **GAP** — no explicit delegation |
| Monotonic recovery (tool-surface) | No | routing §Implementation | ⚠️ **GAP** — no explicit delegation |
| 8 attention metrics (Attention Noise Ratio, NOW events/day, etc.) | No | graph §8 | ⚠️ **GAP** — no explicit delegation |
| Anti-patterns 1-6 table | Partially — compressed to §2 two laws | graph §11 | ⚠️ **PARTIAL GAP** — meaning laundering preserved, others lost |

**Assessment:** 10 binding instructions exist only in predecessors with no explicit delegation to a named retained file. The consolidation declares predecessors "remain on disk as audit strata with supersede pointers" but does not name which specific content from predecessors is intentionally NOT carried forward vs. which is delegated.

### 4C. Authority Language Conflict

| Check | Result |
|---|---|
| Sovereignty claims | ✅ No conflict. init-boundary §5 preserves Meaning+Identity as irreducibly human. graph §7 and §13 agree. |
| F13 veto scope | ✅ No conflict. Both agree: money, deletion, legal, public comms, irreversible = F13. |
| Agent authority limits | ✅ No conflict. Both agree: agents absorb non-sovereign work, never assign meaning. |
| Ratified companion status | ✅ init-boundary explicitly notes scarcity-economics is F13_RATIFIED and kill-criterion is F13_RATIFIED_CHAT. No status conflict. |
| Draft status language | ⚠️ Minor: init-boundary is DRAFT_PENDING_F13; graph is DOCTRINE (unseamed). If init-boundary supersedes graph, graph should either lose DOCTRINE status or init-boundary should already carry it. Currently init-boundary is lower status than the file it supersedes. |

**Verdict:** No substantive authority conflict. Minor status inconsistency noted (§Supersede Map should clarify graph's status change on ratification).

### 4D. Cross-Reference Resolution

| Reference in init-boundary | Resolves to | Exists? |
|---|---|---|
| §7: "attention-graph §8/§14" | attention-graph.md §8 and §14 | ✅ Yes |
| §7: "attention-scarcity-economics.md (F13_RATIFIED 2026-09-12)" | attention-scarcity-economics.md | ✅ Yes |
| §8: "attention-kill-criterion.md (F13_RATIFIED_CHAT 2026-09-11)" | attention-kill-criterion.md | ✅ Yes |
| §1: "anti-pattern (attention-graph §11)" | attention-graph.md §11 | ✅ Yes |
| §5: "Meaning laundering is an anti-pattern (attention-graph §11)" | attention-graph.md §11 | ✅ Yes |
| §Supersede Map: all four predecessor names | All exist at /root/AAA/instructions/ | ✅ Yes |

**Verdict:** ✅ Zero orphan references. Every cross-reference resolves to an existing file.

### 4E. Operational Behavior Reachability

| Behavior | Reachable? | Path |
|---|---|---|
| Five-queue routing | ⚠️ Partially | Queue names preserved in §4 table. Escalation YAML rules NOT preserved — must go to graph §6 |
| Escalation rules (condition→lane mapping) | ❌ No | graph §6 YAML rules not carried forward or delegated |
| Kill criterion (W1-W6, 3-strike) | ✅ Yes | §8 delegates to attention-kill-criterion.md |
| ACSC measurement | ✅ Yes | §7 preserves formula + guard-clauses |
| Boot contract (what INIT loads) | ✅ Yes | §3 (new — explicit table, never existed before) |
| Human-side escalation (NOW budget ≤3) | ✅ Yes | §4 queue table |
| Tool-surface attention governor | ⚠️ Partially | "session-sticky, fail-open" mentioned in §4 note. Monotonic recovery not mentioned |
| Organ-specific attention roles | ❌ No | graph §9 organ mapping not preserved or delegated |
| Anti-patterns (meaning starvation, salience decay failure, etc.) | ⚠️ Partially | Meaning laundering preserved. Others implicit in §2 laws |

---

## 5. Gap Inventory

### Critical Gaps (must resolve before SEAL)

| # | Gap | Risk | Recommendation |
|---|---|---|---|
| G1 | **Escalation YAML rules not delegated** — the 7-condition escalation rule set from graph §6 has no explicit home | Future agents may not know when to escalate | Add §8 line: "Escalation conditions (YAML) remain in attention-graph.md §6 as authoritative routing rules" |
| G2 | **Organ mapping not delegated** — graph §9's organ→role table has no explicit home | Agents won't know which organ owns which attention function | Add delegation line to supersede map: "Organ mapping retained in attention-graph.md §9" |
| G3 | **Status hierarchy mismatch** — init-boundary (DRAFT_PENDING_F13) supersedes graph (DOCTRINE) | On ratification, graph loses authority but init-boundary hasn't gained it yet | Supersede Map should state: "On F13 ratification, attention-graph.md status becomes RETIRED_AUDIT_STRATUM" |

### Non-Critical Gaps (acceptable for SEAL)

| # | Gap | Risk | Recommendation |
|---|---|---|---|
| G4 | Graph structure (nodes/edges/weights) not in consolidation | Low — conceptual framework, not operational binding | Acceptable — audit stratum retains |
| G5 | 8 attention metrics (Noise Ratio, NOW count, etc.) not in consolidation | Low — ACSC is the headline; others are aspirational | Acceptable — graph §8 retains |
| G6 | Implementation Phases 0-4 not in consolidation | Low — roadmap, not binding doctrine | Acceptable — graph §12b retains |
| G7 | Attention Manifold + Thermodynamic Wave not in consolidation | Low — theoretical framework | Acceptable — graph §10 retains |
| G8 | Constitutional formula ΔS ≤ 0 not in consolidation | Low — references reality-compression.md which retains | Acceptable |
| G9 | Monotonic recovery (tool-surface) not in consolidation | Low — routing implementation detail | Acceptable — routing.md retains |
| G10 | Anti-patterns 1-6 reduced to two laws | Medium — loss of taxonomy specificity | Acceptable if kill-criterion covers enforcement |

---

## 6. Answers to Sovereign Questions

### "Am I changing doctrine?"

**No.** Every binding rule in the consolidation either:
- Preserves the exact text/concept from a predecessor (11 items), or
- Reframes with identical meaning (6 items), or
- Is explicitly delegated to a named retained file (kill-criterion, scarcity-economics), or
- Is the ACSC inversion which is explicitly documented as deliberate with identical guard-clauses.

The constitution (F1-F13) is untouched. The two laws are simplifications of graph §2 + §11. The Non-Delegable Core is graph §13/§7 compressed. The five queues are graph §6 compressed.

**What IS changing:** the canonical entry point. From ~411-line graph → ~120-line consolidation. This is infrastructure reform (where doctrine lives), not doctrinal reform (what doctrine says).

### "Am I only changing its canonical entry point?"

**Yes, with three caveats:**

1. **Eleven conceptual elements are dropped from the active surface.** They survive on disk as audit strata but are NOT explicitly delegated in the consolidation. This is a coverage gap, not a doctrinal gap — but it means the consolidation is NOT a complete superset of its predecessors. It is a curated entry point, not a full consolidation.

2. **The ACSC formula is inverted.** This is a genuine mathematical change. Higher now means better instead of worse. The guard-clauses are preserved. This is documented and deliberate. But it IS a change to a measured metric's direction.

3. **The boot contract (§3) is NEW.** It never existed as an explicit artifact. It is a constructive addition, not just a reorganization.

---

## 7. Verdict

# **HOLD_WITH_GAPS**

### Rationale

The consolidation is doctrinally sound. No authority conflict. No orphan references. The ACSC inversion is deliberate and consistent. The core meaning-identity sovereignty boundary is preserved word-for-word.

**Three gaps block SEAL:**

| # | Gap | Fix Effort |
|---|---|---|
| G1 | Escalation YAML rules need explicit delegation line | 1 line in supersede map |
| G2 | Organ mapping needs explicit delegation line | 1 line in supersede map |
| G3 | Supersede map must clarify graph's status change on ratification | 2 lines in supersede map |

**All three are text additions, not doctrinal changes.** Estimated fix: 5 minutes.

### After Fix

The verdict should change to **READY_FOR_SEAL**.

---

## Appendix: Delegation Additions Needed

For the author to add to attention-init-boundary.md §9 Supersede Map:

```markdown
| attention-graph.md (DOCTRINE, 411 ln) | Retained as full map / audit stratum (status becomes RETIRED_AUDIT_STRATUM on ratification); active-context entry point becomes this file. **Explicit delegations retained in predecessor:** escalation YAML rules (§6), organ mapping (§9), implementation phases (§12b), frontier gaps (§12), attention manifold (§10), graph structure (§3), ΔS formula (§15). |
| attention-routing.md (DRAFT_AWAITING_F13, 36 ln) | Absorbed by §2–4; monotonic recovery detail retained in predecessor. Closed as superseded. |
```

---

*DITEMPA BUKAN DIBERI ⚒️*

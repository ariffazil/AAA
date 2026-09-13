# APEX::HUMAN_REALITY_GRAPH_ACTIVATION::2026-09-13

> **Reference:** `APEX::HUMAN_REALITY_GRAPH_ACTIVATION::2026-09-13`  
> **Authority:** ARIF (F13 Sovereign)  
> **Mode:** EXECUTION  
> **Status:** ACTIVE  
> **Mission:** Discover, classify, and govern all human-related memory artifacts, human entities, and consequence chains across the federation.  
> **Doctrine:** DITEMPA BUKAN DIBERI  

---

## Primary Law

```text
A name is not a human reality object.
A mention is not a commitment.
A memory is not a consequence.
A person enters governance only when reality and consequence exist.
```

---

## 10-Phase Operational Framework

### Phase 1: Discovery
Scan memory substrates (`/root/memory/`, `/root/memory/people/`, VAULT999, Qdrant, mem0, receipts, scars, project notes) for human names, organizations, roles, and consequence owners.

### Phase 2: Entity Classification (H0..H5)
For every named human entity:
- **H0 — Reference Only:** Random mention, transient observer, historical note (Stays in archive; no HRO).
- **H1 — Stakeholder:** Meeting participant, board recipient, family dependent.
- **H2 — Decision Owner:** Project owner, technical lead, operational maintainer.
- **H3 — Consequence Owner:** Board signatory, VP, corporate governance head, consequence carrier.
- **H4 — Strategic Actor:** National leaders, regulators, institutional heads (e.g. PETROS, PETRONAS leadership).
- **H5 — Sovereign Actor:** ARIF (F13 Sovereign).

### Phase 3: Human Reality Object Creation
Create an HRO (`schema: arifos.hro.v1`) **only** when:
1. *What matters* exists (clear commitment/obligation).
2. *Consequence* exists (identifiable risk/impact).
3. *Reality* exists (witnessed, not hypothetical).
4. *Witness* exists (auditable provenance).
Otherwise: Preserve as Reference Entity (`H0`).

### Phase 4: Reality Graph Injection
Every HRO must occupy an explicit coordinate in the Reality Graph:
$$\text{Reality} \to \text{Attention} \to \text{Witness} \to \text{Judgment} \to \text{Execution} \to \text{Consequence} \to \text{Scar} \to \text{Governance} \to \text{Adaptation}$$
Any disconnected entity is flagged as `ORPHAN_HRO`.

### Phase 5: Consequence Mapping (CRO Binding)
For every HRO, answer:
- Who pays if wrong?
- Who benefits if correct?
- Who witnesses?
- Who decides?
Bind to a Consequence Reality Object (`schema: arifos.cro.v1`).

### Phase 6: Relationship Graph
Map canonical edge types:
- `PERSON -> OWNS -> COMMITMENT`
- `PERSON -> REPORTS_TO -> PERSON`
- `PERSON -> RESPONSIBLE_FOR -> OBJECT`
- `PERSON -> WITNESSES -> EVENT`
- `PERSON -> PAYS_FOR -> CONSEQUENCE`
- `PERSON -> ASSOCIATED_WITH -> SCAR`
- `PERSON -> GOVERNED_BY -> POLICY`

### Phase 7: World Linkage (WRO Binding)
Connect HROs to external constraints (WROs).  
*Example:* Arif $\to$ Copilot Studio Deployment $\to$ PETRONAS Corporate AI Governance.

### Phase 8: Attention Governance
Assign Attention Cost (`LOW`, `MEDIUM`, `HIGH`, `EXHAUSTED`):
- If Attention Cost is `HIGH` or `EXHAUSTED`: Suppress non-P0 alerts. Prefer *Silent Solve*. Preserve sovereign cognitive capacity.

### Phase 9: Scar Linkage
Bind every witnessed institutional trauma or project failure:
$$\text{Human} \to \text{Failure} \to \text{Consequence} \to \text{Scar} \to \text{Behavior Change}$$
If no behavior change occurs, demote to `ARCHIVE`.

### Phase 10: APEX 7-Question Gate
Before promoting any human memory into active governance:
1. What is true? (R0)
2. What matters? (R1)
3. What can act? (R2)
4. What is allowed? (R5)
5. Who pays if wrong? (R4)
6. What behavior changes?
7. What scar survives?

If Question 6 or 7 fails: **Demote to Archive.**

---

## Final Law

```text
Do not store people. Store reality.
Do not store names. Store commitments.
Do not store biographies. Store consequences.
Do not store conversations. Store witnessed reality.

Human Reality must produce Governance Behavior.
Otherwise it is archive.
```

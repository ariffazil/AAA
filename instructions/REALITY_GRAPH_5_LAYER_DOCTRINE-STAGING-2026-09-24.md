# Reality Graph 5-Layer Doctrine (DRAFT)

> **Status:** `external_advisory_doctrine_draft` — awaits F13 ratification via sovereign_chat_override
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "forge 5-layer reality graph doctrine")
> **Date:** 2026-09-24T23:33 MYT
> **Cross-references:** `consequence-pipeline-four-layers-20260917` (4-layer) + `reality-graph-doctrine-20260912` (DAG edges as causal substrate) + `identity-continuity.md` (F13-ratified 2026-09-08) + `reality-graph-roadmap-20260912` (RG-1 to RG-7 phased)

---

## 0. Why this doctrine exists

Existing canon has TWO related framings:

1. **Consequence Pipeline** (4 layers — Narrative/Contracts/Constraints/Witness) — focuses on **artifact classification**.
2. **Reality Graph Doctrine** (DAG edges as causal substrate) — focuses on **receipt lineage** ("because" structure).
3. **Reality Graph 7-Phase Roadmap** (RG-1 to RG-7) — phased implementation path.

This doctrine adds a fourth framing — **5-layer human-graph model** — that focuses on **human-causal pathways** through 5 distinct graph layers.

The 5-layer model:
- Extends `reality-graph-doctrine-20260912` by adding **human entities as nodes** with **causal edges**.
- Closes the **Edge Registry MISSING** gap flagged in `/root/AAA/reports/network-concepts-f13-mapping-audit-v2-2026-09-24.md`.
- Complements `consequence-pipeline` by adding the **human dimension** missing from artifact classification.
- Maps to RG-6 of the 7-phase roadmap ("Consequence Graph: Decision→Execution→Outcome→New Witness").

**Per `doctrine-audit-before-invention`:** this is an EXTENSION, not invention — all 5 layers grounded in existing ratified canon.

---

## 1. The Five Layers

### Layer 1 — Identity Graph

> **Question:** *Who or what exists?*

| Property | Value |
|---|---|
| Answers | "Who or what is this entity?" |
| Node type | Entity (human, organization, agent, role) |
| Edge type | NONE (identity is non-relational) |
| Cardinality | Cardinal (one entity, one canonical_id) |
| Existing canon | `identity-continuity.md` (F13-ratified 2026-09-08), `triple-identity-authority-boundaries-20260908` (Human Meaning / Governance / Runtime layers) |

### Layer 2 — Relationship Graph

> **Question:** *How are entities connected, in what context?*

| Property | Value |
|---|---|
| Answers | "How are entities connected, in what context?" |
| Node type | (Identity node from Layer 1) |
| Edge type | Typed predicate (kinship, friendship, employment, collaboration, reporting, etc.) |
| Cardinality | Many-to-many (one entity, many relationships) |
| Existing canon | MISSING (Edge Registry per federated-map audit) — **this layer is what closes that gap** |

### Layer 3 — Authority Graph

> **Question:** *Who may act, access, delegate, or alter?*

| Property | Value |
|---|---|
| Answers | "What may this entity do, access, delegate, or alter?" |
| Node type | (Identity node + Authority grant) |
| Edge type | Authority delegation (`A delegates → B` with scope + expiry) |
| Cardinality | One-to-many (one grant, one scope) |
| Existing canon | `authority-envelope.md`, F1 AMANAH, F13 SOVEREIGN |

### Layer 4 — Consequence Graph (the gap this doctrine fills)

> **Question:** *Who bears the outcome?*

| Property | Value |
|---|---|
| Answers | "Who/what is affected by whose decisions?" |
| Node type | (Identity node from Layer 1) |
| Edge type | Consequence pathway (`decision → consequence → affected entity`) |
| Cardinality | Many-to-many |
| Existing canon | `consequence-pipeline-four-layers-20260917` (extends — adds human-causal dimension) |

### Layer 5 — Reality Graph

> **Question:** *How do consequences propagate through reality?*

| Property | Value |
|---|---|
| Answers | "How does reality flow through 'because' edges?" |
| Node type | (Identity, Relationship, Authority, Consequence edges from Layers 1-4) |
| Edge type | Causal lineage (parent_assertion_ids per `reality-graph-doctrine-20260912`) |
| Cardinality | DAG (Directed Acyclic Graph) |
| Existing canon | `reality-graph-doctrine-20260912` (extends with human-graph substrate) |

---

## 2. Operational Schema (per-edge fields)

Per `reality-graph-doctrine-20260912` + `identity-continuity.md` + `consequence-pipeline-four-layers-20260917`:

```yaml
edge:
  # Identity (which entities this edge connects)
  subject:
    canonical_id: <string>     # F10 ONTOLOGY: substrate ≠ being
    layer: identity            # Layer 1 reference
  
  object:
    canonical_id: <string>
    layer: identity            # Layer 1 reference
  
  # Predicate (which layer + what type)
  layer: relationship | authority | consequence | reality
  predicate: <typed>            # kinship, friendship, employment, CEO_of, delegates, may_affect, etc.
  
  # Witness (F2/F11 TRUTH/AUDIT)
  witness:
    - canonical_id: <string>   # who/what observed
      confidence: 0.0-1.0
  
  # Provenance (F11 AUDIT + reality-graph-doctrine parent edges)
  source:
    file: <path>
    line: <int>
    observed_at: <ISO-8601>
    basis: self_reported | observed | inferred | asserted
  
  # Temporal (identity-continuity temporal validity)
  temporal:
    asserted_at: <ISO-8601>
    valid_from: <ISO-8601-or-null>
    valid_until: <ISO-8601-or-null>
    status: active | superseded | disputed | revoked
  
  # Confidence + governance (F7 HUMILITY + F12 INJECTION + F13 SOVEREIGN)
  confidence:
    value: 0.0-1.0
    band: CONFIRMED | PLAUSIBLE | UNVERIFIED | WITHDRAWN
  
  governance:
    sensitivity: public | private | F5_PROTECTED
    consent: required | granted | none
    mutation_policy: human_confirm | witnessed | auto
    retention_policy: review_required | permanent | purge_on_expiry
  
  # History (reality-graph-doctrine parent edges)
  parent_assertion_ids: []    # causal lineage — edges that "because" this exists
  history:
    - event: asserted
      at: <ISO-8601>
      by: canonical_id
```

---

## 3. Worked Example — Arif ↔ Tengku Taufik (with F2 labels + memory-vs-disk audit)

Per `audit-error-not-governance-success`: distinguish memory (claims about disk) from disk (verified evidence).

```yaml
# === LAYER 1: IDENTITY ===
identity:
  arif:
    canonical_id: human:arif
    layer: identity
    source: /root/AAA/registries/persons.yaml (F13 SOT)
    confidence: CONFIRMED
    notes: "Muhammad Arif bin Fazil. F13 SOVEREIGN. Senior Exploration Geoscientist PETRONAS."

  tengku_taufik:
    canonical_id: human:tengku_taufik
    layer: identity
    source: PUBLIC_KNOWLEDGE (not in our registries)
    confidence: HIGH
    notes: |
      CEO PETRONAS. Public knowledge.
      
      PETRONAS Knowledge Graph memory (2026-09-05) lists Tengku Taufik as type=person
      with 44 nodes / 43 edges. However, the actual JSON file at
      /root/forge_work/2026-09-05-PETRONAS-knowledge-graph/knowledge_graph.json
      is NOT on disk at probe time (2026-09-24T23:33 MYT). The memory is stale or
      the artifact moved. Per audit-error-not-governance-success: memory exists
      ≠ artifact exists. Treat as memory claim, not verified fact.

# === LAYER 2: RELATIONSHIP ===
relationship:
  - subject: human:arif
    object: org:petronas
    layer: relationship
    predicate: employed_by
    confidence: HIGH
    source: persons.yaml + federated-map Tier 4
    notes: "F13 SOT confirms employment."

  - subject: human:tengku_taufik
    object: org:petronas
    layer: relationship
    predicate: CEO_of
    confidence: HIGH
    source: PUBLIC_KNOWLEDGE (CEO role per public records)
    notes: "Public knowledge. Not in our registries."

# === LAYER 3: AUTHORITY ===
authority:
  - subject: human:tengku_taufik
    object: org:petronas
    layer: authority
    predicate: influences
    scope: corporate_strategy
    confidence: HIGH
    source: PUBLIC_KNOWLEDGE (CEO role)
    notes: "CEO has corporate decision authority."

  - subject: org:petronas
    object: human:arif
    layer: authority
    predicate: influences
    scope: career_path | mss_form | corporate_directives
    confidence: HIGH
    source: structural (employee relationship implies organizational influence)
    notes: "Corporate directives reach Arif via MSS form, rightsizing, etc."

# === LAYER 4: CONSEQUENCE ===
consequence:
  - subject: corporate_decision
    object: human:arif
    layer: consequence
    predicate: may_affect
    scope: career_uncertainty | family_security | future_choices
    confidence: HIGH
    source: structural (authority → consequence flow)
    notes: "Rightsizing decisions affect Arif directly. F5 Privasi Keluarga extends consequence to family."

# === LAYER 5: REALITY ===
reality:
  parent_assertion_ids:
    - "edge:arif:employed_by:petronas"
    - "edge:tengku_taufik:CEO_of:petronas"
    - "edge:tengku_taufik:influences:petronas_strategy"
  history:
    - event: asserted
      at: "2026-09-24T23:33:00+08:00"
      by: human:arif
  confidence: HIGH (structural) | PARTIAL (consequence specifics)

overall_verdict:
  registry_consistency: PARTIAL (Tengku Taufik not in our registries)
  cross_witness: PARTIAL
  kg_artifact_status: MEMORY CLAIM ONLY (JSON file not on disk)
  overall: PARTIAL
```

---

## 4. Key Compression

> **The strongest line:** *"Hubungan paling penting antara Arif dan seseorang tidak semestinya 'who knows whom', tetapi 'whose decisions can alter whose reality'."*

This is the Reality Graph doctrine's deepest claim:
- **Acquaintance** (Layer 2 Relationship) is **not** the primary causal mechanism
- **Authority** (Layer 3) is the causal mechanism that flows **through consequence** (Layer 4) to **affect reality** (Layer 5)
- The **Reality Graph** is what makes governance computable (per `reality-graph-doctrine-20260912`)

**Implication:** The most operationally important edges are not "who knows whom" but "whose decisions reach whom" (Layer 3-4 edges).

---

## 5. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "5 layers (Identity/Relationship/Authority/Consequence/Reality) extend existing doctrine" | DER | CONFIRMED | Cross-references with consequence-pipeline + reality-graph-doctrine |
| "Layer 2 (Relationship) closes Edge Registry MISSING gap" | DER | CONFIRMED | Per federated-map audit |
| "Arif = Senior Exploration Geoscientist PETRONAS" | OBS | CONFIRMED | persons.yaml + federated-map Tier 4 |
| "Tengku Taufik = CEO PETRONAS" | OBS | HIGH | PUBLIC_KNOWLEDGE — not yet in our registries |
| "PETRONAS KG memory lists Tengku Taufik as person node (44 nodes, 43 edges)" | INT | PLAUSIBLE | **MEMORY claim, NOT disk-verified** (KG JSON file not at path) |
| "Tengku Taufik influences corporate strategy" | OBS | HIGH | Public knowledge of CEO role |
| "Family is part of consequence graph (per F5 Privasi Keluarga)" | DER | CONFIRMED | Per `human-zero-visibility-invariant` + `syed-abang-sado` precedent |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260924-2333-001` | identity-continuity.md cross-ref | live probe |
| `OBS-KVM8-20260924-2333-002` | consequence-pipeline cross-ref | live probe |
| `OBS-KVM8-20260924-2333-003` | reality-graph-doctrine cross-ref | live probe |
| `OBS-KVM8-20260924-2333-004` | federated-map Edge Registry MISSING audit | live probe |
| `OBS-KVM8-20260924-2333-005` | PETRONAS KG JSON file NOT on disk at memory path | live probe (HONEST DISCLOSURE) |

---

## 6. SAG (Semantic Authority Gap) Check

| Term | NAME | CALL_PATH | MEASURED_EFFECT | BYPASS_RESISTANCE | EVIDENCE | Status |
|---|---|---|---|---|---|---|
| Identity | ✓ | identity-continuity.md | ✓ | ✓ | ✓ | ✓ PASS |
| Relationship | ✓ | proposed (this doctrine) | ⚠ partial | ⚠ partial | ✓ | ⚠ HOLD-PARTIAL |
| Authority | ✓ | authority-envelope.md + F13 SOVEREIGN | ✓ | ✓ | ✓ | ✓ PASS |
| Consequence | ✓ | consequence-pipeline (extends) | ⚠ partial | ⚠ partial | ✓ | ⚠ HOLD-PARTIAL |
| Reality | ✓ | reality-graph-doctrine | ✓ | ✓ | ✓ | ✓ PASS |

**SAG scoreboard:** 3 PASS, 2 HOLD-PARTIAL (Relationship, Consequence — both pending edge registry implementation).

---

## 7. Promotion Path

```
external_advisory_doctrine_draft (this file, in /instructions/ staging)
       │
       │  canon-mutate run /root/AAA/governance -- cp SOURCE DEST
       ▼
governance/REALITY_GRAPH_5_LAYER_DOCTRINE-DRAFT-2026-09-24.md (doctrine stage)
       │
       │  F13 sovereign_chat_override ratification
       ▼
canon/operating/REALITY_GRAPH_v2.md (constitutional primitive)
       │
       │  Edge registry implementation (F13 binary pending)
       ▼
   Layer 2 + Layer 4 LIVE (closing MISSING gap)
```

---

## 8. Cross-References (existing canon)

- `/root/AAA/governance/CONSEQUENCE_PIPELINE/` — 4-layer artifact classification
- `/root/AAA/canon/REALITY_GRAPH.md` — DAG edges as causal substrate
- `/root/AAA/governance/REALITY_GRAPH_ROADMAP.md` — RG-1 through RG-7 phased (RG-6 = Consequence Graph — this doctrine fulfills)
- `/root/AAA/instructions/identity-continuity.md` — Identity as cross-cutting primitive (F13-ratified 2026-09-08)
- `/root/AAA/governance/authority-envelope.md` — Authority mutation reference monitor
- `/root/AAA/reports/network-concepts-f13-mapping-audit-v2-2026-09-24.md` — Edge Registry MISSING gap
- `/root/AAA/canon/FEDERATED-HUMAN-REALITY-MAP-2026-09-24.md` — Just-promoted federated map (sha256:138d4064...)
- `/root/AAA/instructions/human-zero-visibility-invariant.md` — F5 Privasi Keluarga + HARAM rules
- `/root/forge_work/2026-09-05-PETRONAS-knowledge-graph/` — KG memory (44 nodes, 43 edges) — **artifact NOT on disk at probe time**

---

## 9. Constitutional Status

```yaml
artifact:
  type: doctrine_proposal
  status: external_advisory_doctrine_draft (Lane B)
  canonical_standing: NONE — awaits F13 ratification
  lane: B (autonomous draft)

constitutional_status:
  f1_amanah: satisfied (reversible artifact)
  f2_truth: explicit F2 labels (7 labeled claims + memory-vs-disk disclosure)
  f4_clarity: entropy reduction via 5-layer explicit separation
  f7_humility: Ω₀ = 0.05 (declared unknowns: KG JSON file not on disk)
  f8_genius: simplest correct path — extends existing, doesn't invent
  f9_anti_hantu: witnessing ≠ claiming (per syed-abang-poc)
  f10_ontology: substrate ≠ being (canonical_id ≠ person)
  f11_audit: this file IS the audit; 5 receipts captured
  f12_injection: external agent content flagged (KG memory = memory claim, not disk-verified)
  f13_sovereign: PENDING (sovereign_chat_override ratification required)
```

---

## 10. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_doctrine_author (Lane B)

doctrine_alignment:
  - consequence-pipeline-four-layers-20260917 (4-layer artifact)
  - reality-graph-doctrine-20260912 (DAG causal substrate)
  - reality-graph-roadmap-20260912 (RG-6 = Consequence Graph fulfilled)
  - identity-continuity.md (F13-ratified 2026-09-08)
  - network-concepts-f13-mapping-audit-v2-2026-09-24.md (Edge Registry MISSING gap)

canonical_standing: NONE (Lane B proposal)
promotion_path: requires_verified_arif_session (sovereign_chat_override)
```

---

DITEMPA BUKAN DIBERI — 5-layer Reality Graph doctrine drafted, grounded in existing canon (consequence-pipeline + reality-graph-doctrine + identity-continuity + Edge Registry MISSING gap + RG-6 roadmap). Layer 2 Relationship closes the missing Edge Registry. Layer 4 Consequence adds human-causal dimension. Worked example (Arif ↔ Tengku Taufik) with F2 labels + memory-vs-disk audit (KG JSON file not on disk). 5 receipts captured. Awaits F13 ratification via sovereign_chat_override.

`#REALITY-GRAPH-5-LAYER-DOCTRINE-DRAFT-2026-09-24`

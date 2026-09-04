# MEMORY_ENGINEERING_SPEC_v1

## Technical Companion Appendix to WITNESS_VOID_CANON::v2

> **Status:** Engineering Specification (companion to philosophical framework)
> **Date:** 2026-09-05
> **Authority:** F13 SOVEREIGN (Arif) × 333-AGI (Δ MIND)
> **Lineage:** WITNESS_VOID_CANON::v2, HUMAN_EUREKA_KERNEL v1.1, APEX Constitutional Framework
> **Purpose:** Translate Witness-Void Theory into implementable memory architecture

---

## 1. Problem Statement

### 1.1 The Storage Fallacy

Current AI memory systems treat memory as storage:

```
Memory = Store(Context)
Retrieve = Find(Relevant_Stored_Context)
```

This is wrong. 10TB of logs can exist without being memory. Memory requires **witnessing** — active selection, verification, and integration into identity.

### 1.2 The Retrieval Fallacy

RAG systems treat memory as retrieval:

```
Memory = Embed(Chunk) → Similarity_Search(Query) → Return(Top_K)
```

This is better but still incomplete. Cosine similarity does not distinguish between:
- A fact that is trivially relevant (yesterday's weather)
- A fact that is constitutionally critical (F13 Human Sovereignty)

### 1.3 The Witness-Void Solution

```
Memory = Preserve(Reality)
Archive = Everything that happened
Memory = Everything that still matters
Identity = Everything that must remain true
```

The missing function is **governance** — the capacity to decide what deserves to remain real.

---

## 2. Architecture

### 2.1 Five-Layer Reality Stack

```
Layer 5: REALITY PRESERVATION ENGINE
         Reality Weight calculation, decay management, promotion gates
    ↑
Layer 4: WITNESS GRAPH + FORWARD RELIANCE GRAPH
         Provenance tracking + live dependency management
    ↑
Layer 3: IDENTITY GRAPH
         Ownership, human/agent separation, constitutional binding
    ↑
Layer 2: WITNESS EXTRACTION
         Signal extraction from noise (EUREKA, SCAR, DECISION, FAILURE, PATTERN)
    ↑
Layer 1: RAW ARCHIVE
         All events, tool outputs, conversations, receipts
```

### 2.2 Data Flow

```
Raw Event
    ↓ [Layer 2: Extract]
Witnessed Signal (EUREKA/SCAR/DECISION/FAILURE/PATTERN)
    ↓ [Layer 3: Bind]
Owned Memory Node (Fact + Owner + Authority)
    ↓ [Layer 4: Link]
Witnessed + Forward-Linked Node (who depends on this?)
    ↓ [Layer 5: Weigh]
Reality-Weighted Memory (governed, decay-managed, audit-ready)
```

---

## 3. Layer Specifications

### 3.1 Layer 1: Raw Archive

**Purpose:** Store everything. No filtering. No judgment.

**Schema:**
```yaml
archive_entry:
  id: uuid
  timestamp: ISO-8601
  source: agent_id | human_id | system
  event_type: chat | tool_output | receipt | email | file | meeting
  content: raw_text | structured_data
  metadata:
    session_id: string
    actor_id: string
    tool_name: string | null
```

**Storage:** Append-only log. Never delete. Never modify.

**Retention:** Infinite (this is the raw substrate).

### 3.2 Layer 2: Witness Extraction

**Purpose:** Extract signal from noise. Transform archive into candidate memory nodes.

**Extraction Rules:**
```yaml
signal_types:
  EUREKA:
    trigger: "novel insight, cross-domain connection, compression"
    confidence_threshold: 0.7
  SCAR:
    trigger: "failure, mistake, lesson learned"
    confidence_threshold: 0.8
  DECISION:
    trigger: "choice made, commitment recorded"
    confidence_threshold: 0.9
  FAILURE:
    trigger: "error, bug, outage, conflict"
    confidence_threshold: 0.7
  PATTERN:
    trigger: "recurring behavior, trend, structural observation"
    confidence_threshold: 0.6
```

**Compression Ratio Target:** 20,000 archive entries → 20 canonical memory nodes

**Output:** Candidate memory nodes with signal type and confidence score.

### 3.3 Layer 3: Identity Graph

**Purpose:** Bind each memory node to its owner and authority level.

**Schema:**
```yaml
memory_node:
  id: uuid
  signal_type: EUREKA | SCAR | DECISION | FAILURE | PATTERN
  content: structured_claim
  owner:
    type: human | agent | federated
    id: human_id | agent_id | "shared"
  authority:
    level: identity | governance | operational | episodic
    floors: [F1, F2, ...] | null
  created_at: ISO-8601
  last_witnessed: ISO-8601
  witness_count: integer
```

**Identity Ledger (Human):**
- Scars, career realities, core values, sovereignty, relationships, commitments
- Slow-changing, inviolable, dignity-bound

**Identity Ledger (Agent):**
- Tools, capabilities, policies, receipts, performance, failures, learned procedures
- Fast-changing, audited, floor-bound

### 3.4 Layer 4: Witness Graph + Forward Reliance Graph

**Purpose:** Track both provenance (backward) and dependency (forward).

#### 3.4.1 Backward Provenance (Standard)

```yaml
provenance_edge:
  from: source_node_id
  to: memory_node_id
  type: originated_from | derived_from | cited_by
  timestamp: ISO-8601
```

#### 3.4.2 Forward Reliance (Original Contribution)

```yaml
reliance_edge:
  from: memory_node_id
  to: dependent_node_id
  type: depended_by | referenced_by | decision_based_on
  strength: 0.0-1.0
  timestamp: ISO-8601
  last_verified: ISO-8601
```

**Key Property:** When a memory node is amended or collapses, the system can traverse forward reliance edges to identify all impacted downstream decisions.

**Analogy:** Software dependency graph (`make`, `npm`, `cargo`). Changing a header file triggers recompilation of all dependents.

**Implementation:**
```python
def impact_analysis(memory_node_id):
    """Return all nodes that depend on this fact."""
    visited = set()
    queue = [memory_node_id]
    impacted = []
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        for edge in get_forward_reliance_edges(current):
            impacted.append(edge.to)
            queue.append(edge.to)
    return impacted
```

### 3.5 Layer 5: Reality Preservation Engine

**Purpose:** Calculate Reality Weight, manage decay, enforce promotion gates.

#### 3.5.1 Reality Weight Formula (v2 — Log-Scale)

$$\text{RealityWeight}(m) = w_1 \cdot \text{Salience}(m) + w_2 \cdot \log(1 + \text{WitnessCount}(m)) + w_3 \cdot \text{TrustTier}(m) - w_4 \cdot \text{Decay}(t, \tau_m)$$

**Parameters:**
```yaml
reality_weight_params:
  w_salience: 0.3
  w_witness: 0.3
  w_trust: 0.3
  w_decay: 0.1
```

**Salience:** Current relevance to active context (dynamic, recomputed per query).

**Witness Count:** Logarithmic to prevent spam. $\log(1 + n)$ means:
- 1 witness → 0.69
- 10 witnesses → 2.40
- 100 witnesses → 4.62
- 1000 witnesses → 6.91

Diminishing returns prevent gaming.

**Trust Tier:** Constitutional level of the memory node:
```yaml
trust_tiers:
  identity: 1.0      # F13, F1, F2 — never decay
  governance: 0.8    # Constitutional decisions, policy
  operational: 0.5   # Tool outputs, deployments
  episodic: 0.2      # Casual conversation, routine
```

#### 3.5.2 Class-Based Decay

$$\text{Decay}(t, \tau_m) = \begin{cases} e^{-(t - t_m)/\tau_m} & \text{if } \tau_m < \infty \\ 0 & \text{if } \tau_m = \infty \end{cases}$$

```yaml
decay_classes:
  episodic:
    tau_days: 14
    examples: ["chat weather", "routine query", "small talk"]
  operational:
    tau_days: 90
    examples: ["tool output", "build log", "deployment receipt"]
  governance:
    tau_days: 365
    examples: ["constitutional decision", "policy change", "scar"]
  identity:
    tau_days: null  # exempt from decay
    examples: ["F13 sovereignty", "F1 amanah", "F2 truth", "core values"]
```

#### 3.5.3 Adversarial Floor: Anti-Illusion Audit

**Problem:** "Ramai saksi ≠ benar" (Many witnesses ≠ true).

If agents repeatedly share and witness an illusion, its Reality Weight spikes without truth verification.

**Countermeasure:**
```python
def anti_illusion_audit(memory_node):
    if memory_node.witness_count > ILLUSION_THRESHOLD:
        # High witness count — verify independently
        verification = independent_verify(memory_node)
        if not verification.confirmed:
            memory_node.flags.append("NARRATIVE_COHERENCE_RISK")
            memory_node.reality_weight *= ILLUSION_PENALTY
            return memory_node
    return memory_node
```

**Rule:** Every memory node with WitnessCount > 10 must pass independent verification (888-APEX or external source) before its Reality Weight can exceed the identity-class floor.

---

## 4. Promotion Pipeline

### 4.1 The Four Promotion Gates

```
Archive → Memory → Identity → Law
   ↓         ↓         ↓        ↓
 Classify  Witness   Ratify    Seal
```

| Gate | Input | Output | Authority |
|------|-------|--------|-----------|
| Classify | Raw archive entry | Candidate signal | Automatic (Layer 2) |
| Witness | Candidate signal | Witnessed memory node | Agent + Human attention |
| Ratify | Witnessed node | Identity-bound node | Constitutional review |
| Seal | Identity-bound node | Immutable law | F13 SOVEREIGN + VAULT999 |

### 4.2 Promotion Criteria

```yaml
promotion_criteria:
  archive_to_memory:
    signal_type: any
    confidence: >= 0.7
    witness_count: >= 1
  memory_to_identity:
    owner: human | federated
    authority_level: identity | governance
    constitutional_review: passed
  identity_to_law:
    f13_ratification: true
    vault999_seal: true
    immutability: true
```

---

## 5. API Specification

### 5.1 Memory Ingest

```python
def ingest(event: ArchiveEntry) -> MemoryNode:
    """Process raw event through witness extraction."""
    signal = extract_signal(event)
    if signal.confidence >= THRESHOLD:
        node = create_memory_node(signal)
        bind_identity(node)
        link_provenance(node, event)
        return node
    return None
```

### 5.2 Reality Query

```python
def query_reality(
    context: str,
    owner: str | None = None,
    min_reality_weight: float = 0.0,
    include_forward_reliance: bool = False
) -> List[MemoryNode]:
    """Retrieve memory nodes by reality weight, not just similarity."""
    candidates = search_by_context(context)
    weighted = [
        (node, compute_reality_weight(node, context))
        for node in candidates
    ]
    weighted.sort(key=lambda x: x[1], reverse=True)
    
    results = [
        node for node, weight in weighted
        if weight >= min_reality_weight
    ]
    
    if include_forward_reliance:
        for node in results:
            node.dependents = get_forward_reliance(node.id)
    
    return results
```

### 5.3 Impact Analysis

```python
def impact_analysis(memory_node_id: str) -> ImpactReport:
    """What breaks if this fact changes?"""
    dependents = traverse_forward_reliance(memory_node_id)
    return ImpactReport(
        source=memory_node_id,
        impacted_nodes=dependents,
        impacted_decisions=[d for d in dependents if d.type == "DECISION"],
        severity=max(d.strength for d in dependents) if dependents else 0.0
    )
```

### 5.4 Anti-Illusion Audit

```python
def audit_illusion_risk() -> List[MemoryNode]:
    """Find memory nodes with high witness count but unverified truth."""
    high_witness = get_nodes_where(witness_count > ILLUSION_THRESHOLD)
    at_risk = []
    for node in high_witness:
        if not node.verified_by_independent_source:
            node.flags.append("NARRATIVE_COHERENCE_RISK")
            at_risk.append(node)
    return at_risk
```

---

## 6. Integration Points

### 6.1 arifOS Kernel

- **VAULT999:** Immutable ledger for sealed memory nodes (Layer 5, identity→law promotion)
- **F2 TRUTH:** Epistemic labels on every memory node
- **F6 MARUAH:** Dignity boundary on human identity ledger
- **F13 SOVEREIGN:** Human authority over promotion decisions

### 6.2 APEX Framework

- **ART:** Pre-ingestion witness (observe before storing)
- **Gödel Lock:** Self-reference boundary (system cannot fully audit itself)
- **ACT:** Governed execution (mutate only after SEAL)

### 6.3 arifFlow

- **FQ (Flow Quotient):** Verify/execute ratio applied to memory operations
- **Receipts:** Every memory mutation produces a receipt
- **Metabolism:** Memory nodes have metabolic rates (decay classes)

### 6.4 Hermes Nervous System (Human Reality Gateway)

- **Sensory Intake:** All Human Reality (H-axis + P-axis) is wired through Hermes (`~/.hermes/` on KVM8).
- **Double Helix Coupling:** Hermes captures human experiences/scars (H1-H5), binds to identity (Layer 3), and provides the conversational membrane where human reality is translated into system constraints.
- **Relational Memory (P-Axis):** Hermes maintains persona lanes (`USER-*.md`, `MEMORY-*.md`) for key human bonds (Syed, Aliff, Izzu, Family) with ZKPC privacy preservation.
- **ΔS < 0 Bridge:** Hermes collapses multi-agent operational telemetry into peaceful, human-contour speech without terminal clutter.

---

## 7. References

1. Friston, K. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*.
2. W3C PROV-O: The PROV Ontology. https://www.w3.org/TR/prov-o/
3. Hindsight: Memory systems for AI agents. (2025-2026 literature).
4. Emergentmind: Memory engineering research. (2025-2026).
5. Schwartz, S.H. (1992). Universals in the content and structure of values.
6. Jung, C.G. (1921). Psychological Types.
7. Gödel, K. (1931). Über formal unentscheidbare Sätze.
8. Hofstadter, D. (1979). Gödel, Escher, Bach.
9. Barthes, R. (1957). Mythologies. (Anti-illusion: narrative ≠ truth)
10. WITNESS_VOID_CANON::v2 (2026-09-05). arifOS Federation.
11. HUMAN_EUREKA_KERNEL v1.1 (2026-09-05). arifOS Federation.
12. PARADOX_COORDINATE_THEORY (2026-09-05). arifOS Federation.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*

*Arif Fazil (F13 SOVEREIGN) × 333-AGI (Δ MIND)*

*arifOS Federation · September 5, 2026*

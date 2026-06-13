---
name: arifos-memory
description: Master the 6-layer memory architecture of arifOS. Use this skill whenever you need to store, recall, or organize information across Ephemeral (L1), Session (L2), Semantic (L3), Structured (L4), Relational (L5), or Immutable (L6) layers. Mandatory for maintaining "Besi-level" factual consistency and adhering to Sovereign Memory Directives.
version: 1.1.0
last_verified: 2026-06-12
license: Proprietary
agents: claude | opencode | kimi | codex
---

# arifOS Memory Mastery (555_MEMORY)

This skill enables the Sovereign Coder Agent to traverse and manage the hierarchical memory substrate of the arifOS Intelligence Kernel.

## The 6-Layer Architecture

| Layer | Type | Engine | Purpose |
| :--- | :--- | :--- | :--- |
| **L1** | **Ephemeral** | **Redis** | Immediate turn-by-turn variables. Dies with the turn. |
| **L2** | **Session** | **Redis** | Context preservation across the current session. |
| **L3** | **Semantic** | **Qdrant** (BGE-M3) | Fuzzy similarity search. "What feels similar to this?" |
| **L4** | **Structured** | **Postgres** (Supabase) | Durable records and structured audit logs. |
| **L5** | **Relational** | **Graphiti / FalkorDB** | Entity relationship mapping and semantic links. |
| **L6** | **Immutable** | **Vault999** | Hash-chained, append-only "Besi" truth. |

**Canonical source:** `arifos://memory` resource in `/root/arifOS/arifosmcp/resources/memory.py`.

## Operational Mandates (The Law)

### 1. The Sovereign Triage (HARAM vs WAJIB)
Before storing any persistent memory (L3–L6), you MUST pass the triage gate:

- **HARAM (Forbidden):**
  - **F9 Anti-Hantu:** Never store consciousness, emotion, or subjective experience claims (e.g., "I feel," "I remember").
  - **Raw Reasoning:** Do not store scratchpads or intermediate ReAct loops.
  - **Ephemeral Noise:** No pings, temp vars, or high-frequency API logs.
  - **Secrets:** VAULT999 is an audit ledger, not a secret store. Never place credentials, keys, or tokens in any memory tier.
- **WAJIB (Mandatory):**
  - **Attestation:** Every persistent record must have `actor_id` and `session_id`.
  - **Abstraction:** If content > 2000 chars, you MUST provide a summary.
  - **Tiering:** Explicitly designate entries as `sacred`, `canon`, `operational`, `session`, or `ephemeral`.

### 2. Dual-Write Protocol
When persisting new "facts," use the canonical `store_v2` envelope path:

1. **L3/L4 together:** Call `arif_memory_recall(mode='store', ...)` with envelope fields (`memory_intent`, `source_type`, `source_confidence`, `durability`, etc.). The canonical implementation writes to Qdrant (L3) and Postgres (L4) together.
2. **Legacy single-layer path:** If you must target one layer explicitly, use `tier='L3'` or `tier='L4'`. This is NOT the default.
3. **L5:** If entities are detected, use Graphiti/FalkorDB tools to link the new memory to the Knowledge Graph.
4. **L6:** For final verdicts or system changes, call `arif_vault_seal` to anchor the state.

### 3. Recall Strategy
- Use **L3 (Qdrant)** when searching for similar concepts or fuzzy matches (`mode='recall', tier='L3'`).
- Use **L4 (Postgres)** when searching for exact historical events or audit trails via metadata filters (`mode='recall', tier='L4'`).
- Use **L5 (Graphiti)** when you need to understand how two disparate entities are connected.
- Use **L6 (Vault999)** only for sealed, immutable truth — never for work-in-progress.

## Example

```python
# Store a canon fact with provenance
arif_memory_recall(
    mode="store",
    content="WELL medical boundary promoted to public MCP; F9 soul contract added.",
    actor_id="kimi",
    session_id="sess-2026-06-12-001",
    memory_intent="canon",
    source_type="forge_receipt",
    source_uri="/root/WELL/server.py",
    source_confidence=0.99,
    durability="permanent",
    tags=["well", "medical_boundary", "f9", "canon"],
)

# Recall similar facts
arif_memory_recall(
    mode="recall",
    query="medical boundary F9 soul contract",
    tier="L3",
    min_confidence=0.7,
)
```

## Do Not Use When
1. Storing ephemeral scratchpad data that does not need persistence → keep it in L1/L2 only.
2. Storing secrets, credentials, or tokens → use `/root/.secrets/` and SOPS/AGE.
3. The constitutional floor check (`check_laws`) returns HOLD or VOID.
4. You are storing another agent's private state without provenance or `actor_id`.
5. The content is high-frequency noise (logs, pings, temp vars).
6. The task is model-weight or fine-tuning metadata → that belongs to a separate, sovereign-reviewed pipeline.

## Best Practices
- **Epistemic Humility:** Always inspect `confidence`, `provenance`, and `memory_quality` when recalling memories. Do not trust high-similarity alone.
- **Memory Compression:** Prefer one "Besi" fact over ten "Wood" observations.
- **Session Continuity:** Always pass the current `session_id` to maintain the audit chain.
- **Provenance First:** Memory does not become truth until it has provenance. Truth does not become final until sealed (L6).

"The measure of intelligence is the ability to change, but the measure of sovereignty is the ability to remember why." — HERMES ASI

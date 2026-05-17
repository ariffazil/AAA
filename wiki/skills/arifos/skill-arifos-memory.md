---
title: "Skill: arifOS Memory Mastery"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: arifos
tags: [memory, l1, l2, l3, l4, l5, l6, qdrant, postgres, graphiti, vault999, persistence]
confidence: high
contested: false
floors: [F2, F11]
risk_band: HIGH
sources: [/root/.agents/skills/arifos-memory/SKILL.md]
---

# Skill: arifOS Memory Mastery (555_MEMORY)

> **Source:** `/root/.agents/skills/arifos-memory/SKILL.md`
> **Agent:** All federation agents
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Storing, recalling, or organizing information across memory layers
- Choosing which persistence layer to use for a given datum
- Debugging memory gaps, stale state, or cross-session amnesia
- Keywords: memory, recall, store, qdrant, postgres, graphiti, vault999, ephemeral, session

---

## The 6-Layer Architecture

| Layer | Name | Engine | Persistence | Scope | Purpose |
|-------|------|--------|-------------|-------|---------|
| **L1** | Ephemeral | Local Context | ❌ None | Single turn | Immediate variables, temp computation |
| **L2** | Session | AutoMemory | ❌ None | Session | Context preservation across current session |
| **L3** | Vector | Qdrant | ✅ Permanent | Cross-session | Semantic search, embeddings, similarity |
| **L4** | Relational | PostgreSQL | ✅ Permanent | Cross-session | Structured state, vault999, agent registry |
| **L5** | Graph | Graphiti (FalkorDB) | ✅ Permanent | Cross-session | Entity-relationship knowledge, episodes |
| **L6** | Ledger | VAULT999 | ✅ Append-only | Eternal | Immutable seals, constitutional verdicts |

---

## Doctrine: Layer Selection

```
Is this a temporary computation?
└─ YES → L1 (Ephemeral)

Is this needed for the current session only?
└─ YES → L2 (Session)

Is this semantic / searchable by meaning?
└─ YES → L3 (Qdrant vector memory)

Is this structured / tabular / relational?
└─ YES → L4 (PostgreSQL)

Is this about entities, relationships, or episodes?
└─ YES → L5 (Graphiti knowledge graph)

Is this a constitutional verdict or seal?
└─ YES → L6 (VAULT999)
```

---

## Layer Details

### L1 — Ephemeral
- **Scope:** Single tool call or reasoning step
- **Example:** Temporary variable holding a file path
- **Rule:** Never rely on L1 for cross-turn continuity

### L2 — Session
- **Scope:** Current conversation session
- **Example:** User preferences established this session
- **Rule:** Autocleared on session end. Use for continuity, not persistence.

### L3 — Qdrant (Vector)
- **Scope:** Cross-session semantic memory
- **Example:** "Arif prefers Python over TypeScript" → embedding stored
- **Access:** `arif_memory_recall(mode='recall')` or direct Qdrant client
- **Rule:** Use for fuzzy retrieval. Not for exact lookups.

### L4 — PostgreSQL (Relational)
- **Scope:** Structured cross-session state
- **Example:** Agent registry, session metadata, budget contracts
- **Access:** `arif_memory_recall(mode='get')` or asyncpg
- **Rule:** Source of truth for structured data. Schema-enforced.

### L5 — Graphiti (Knowledge Graph)
- **Scope:** Entity-relationship knowledge
- **Example:** "GEOX depends on arifOS for constitutional enforcement"
- **Access:** `add_memory`, `search_nodes`, `search_memory_facts`
- **Rule:** Use for connected knowledge. Episodes are async-processed.

### L6 — VAULT999 (Ledger)
- **Scope:** Immutable constitutional memory
- **Example:** SEAL verdicts, audit receipts, epoch anchors
- **Access:** `arif_vault_seal(mode='seal')` — requires ack_irreversible
- **Rule:** Append-only. Never delete. Never modify.

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Layer |
|--------------|-----------|---------------|
| Storing secrets in L1/L2 | Lost on restart | L4 (encrypted Postgres) or env vars |
| Using L3 for exact lookups | Fuzzy results, not precise | L4 (SQL query) |
| Expecting L5 episodes instantly | Async processing queue | Poll or use L4 for immediate needs |
| Writing to VAULT999 without judge | Violates F1 Amanah | Always 888_JUDGE first |

---

## Related

- [[skill-memory-bridge-protocol]] — MANDATORY L4 persistence protocol
- [[skill-vault999-ops]] — VAULT999 read/write/verify
- [[federation-entities]] — Agent registry lives in L4
- [[scar-graphiti-hyphen-escape-2026-05-17]] — L5 graphiti bug scar

---

*DITEMPA BUKAN DIBERI — Memory is how the federation remembers it was forged.*

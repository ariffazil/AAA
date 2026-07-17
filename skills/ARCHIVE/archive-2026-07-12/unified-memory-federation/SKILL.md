---
id: unified-memory-federation
name: unified-memory-federation
version: 1.0.0-2026.07.08
description: >
  Single entry point for memory across the arifOS federation.
  Routes recall/write/seal/consolidate/audit to the correct tier
  and organ. Enforces the 6-tier memory model from zen-organ-memory.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: medium
floor_scope: [F1, F2, F4, F7, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "remember this"
  - "recall"
  - "what do we know"
  - "memory audit"
  - "consolidate memory"
  - "unified memory"
dependencies:
  mcp_servers:
    - arifos
    - aforge
  skills:
    - zen-organ-memory
    - 999-vault-seal-immutable
    - asi-knowledge-writeback
    - knowledge-graph-query
inputs:
  - intent
  - tier (L0-L5)
  - query
  - ack_irreversible (for L5)
outputs:
  - result
  - tier_routing
  - receipt
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# 🧠 UNIFIED MEMORY FEDERATION

> **One call to remember or recall anything across the federation.**
> DITEMPA BUKAN DIBERI

---

## 0. Memory Tiers

| Tier | Name | Lifetime | Canonical Tool | Path / Surface |
|------|------|----------|----------------|----------------|
| L0 | **Volatile** | Session only | In-context | Current prompt context |
| L1 | **Working** | Task duration | `forge_filesystem` (read) | `/root/A-FORGE/forge_work/` |
| L2 | **Daily** | 30 days | File grep | `/root/memory/YYYY-MM-DD.md` |
| L3 | **Durable** | Permanent | `arif_memory(recall/remember)` | arifOS L4-L6 stack |
| L4 | **Knowledge** | Permanent | `knowledge-graph-query` | `/root/AAA/asi/knowledge-taxonomy.json` |
| L5 | **Sealed** | Irreversible | `arif_seal(list/seal)` | VAULT999 + seal chain |

**Promotion rules:**
- L0 → L1: free (working artifacts)
- L1 → L2: session end
- L2 → L3: explicit `remember`
- L3 → L4: requires SEAL
- L4 → L5: `ack_irreversible=true`

---

## 1. Operations

### 1.1 RECALL — "what does the federation remember about X?"

Route by tier:

```
L0: inspect current session context
L1: grep /root/A-FORGE/forge_work/ for X
L2: grep /root/memory/*.md for X
L3: arif_memory(mode=recall, query=X)
L4: knowledge-graph-query --name X  (or --id, --type)
L5: arif_seal(mode=list) filtered by X
```

Convenience script (L1-L2 + carry_forward):
```bash
python3 /root/.agents/skills/unified-memory-federation/scripts/recall.py "X"
```

### 1.2 WRITE — "remember this decision"

```
tier=L3 → arif_memory(mode=remember, content=..., metadata={...})
tier=L1 → write to /root/A-FORGE/forge_work/...
tier=L2 → append to /root/memory/YYYY-MM-DD.md
```

### 1.3 SEAL — "this is final"

```
L5 → arif_judge(...) → arif_seal(mode=seal, ack_irreversible=true)
```

Never call `forge_vault` directly. It is deprecated and duplicates `arif_seal`.

### 1.4 CONSOLIDATE — session end

Run the pipeline:

```
L0 working context
  → L1: save forge_work artifacts
  → L2: write daily summary to /root/memory/YYYY-MM-DD.md
  → L3: promote durable memories via arif_memory(remember)
  → L4: write knowledge edges via asi-knowledge-writeback (requires seal_id)
  → update carry_forward.json
```

### 1.5 AUDIT — memory surface health

Checklist:
- [ ] VAULT999 chain intact (`arif_seal(mode=chain)`)
- [ ] carry_forward.json readable
- [ ] knowledge graph readable (841 nodes, 873 edges)
- [ ] forge_work has no orphaned >30-day files
- [ ] memory dir has current daily log

---

## 2. Tool Routing Matrix

| Operation | L1 | L2 | L3 | L4 | L5 |
|-----------|----|----|----|----|----|
| recall | `forge_filesystem` / grep | grep | `arif_memory(recall)` | `knowledge-graph-query` | `arif_seal(list)` |
| write | `forge_filesystem_write` | file append | `arif_memory(remember)` | `asi-knowledge-writeback` | `arif_seal(seal)` |
| seal | — | — | — | via SEAL | `arif_seal(seal)` |

---

## 3. Anti-Patterns

- ❌ Using `forge_vault` for VAULT999 writes (deprecated duplicate)
- ❌ Writing L0 session-ephemeral data to L3+ durable surfaces
- ❌ Sealing without `ack_irreversible=true`
- ❌ Querying knowledge graph by modifying it
- ❌ Bypassing `arif_memory` for durable preferences

---

## 4. Floor Alignment

| Floor | Obligation |
|-------|-----------|
| **F1 AMANAH** | Backup before consolidation; append-only for L4-L5 |
| **F2 TRUTH** | Every result labeled with tier + epistemic (OBS/DER/INT/SPEC) |
| **F4 CLARITY** | One canonical tool per tier |
| **F7 HUMILITY** | Recall reports confidence, never certainty |
| **F11 AUDIT** | Every write returns a receipt |
| **F13 SOVEREIGN** | L5 seal requires ack_irreversible |

---

## 5. Quick Reference

```
RECALL  → unified-memory-federation recall "X" [--tier L3]
WRITE   → unified-memory-federation remember "..." --tier L3
SEAL    → 999-vault-seal-immutable (arif_judge → arif_seal)
AUDIT   → unified-memory-federation audit
CONSOLIDATE → unified-memory-federation consolidate
```

---

*Forged: 2026-07-08 by FORGE (000Ω) for Arif (F13 SOVEREIGN)*
*Part of: arifOS memory governance layer*

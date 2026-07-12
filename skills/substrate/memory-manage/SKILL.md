---
id: memory-manage
name: memory-manage
version: 1.0.0
layer: substrate
description: Intelligence without memory is stateless. Store less, recall well, forget
  when stale. ΔS ≤ 0 on every cycle.
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# memory-manage

> **Purpose:** Intelligence without memory is stateless. Store less, recall well, forget when stale. ΔS ≤ 0 on every cycle.

## Axis 1: Invariants

- **authority**: arif_memory with L1-L6 tier governance
- **evidence_schema**: memory items tagged with tier, confidence, staleness
- **reversibility**: L1-L4 reversible, L5-L6 require vault protocol
- **lineage**: memory chain: store→recall→promote→seal→forget
- **trigger_semantics**: session_end OR knowledge_gained OR recall_needed OR compaction_threshold
- **failure_contract**: do not store on failure; log the miss
- **resource_budget**: {'cpu': 'moderate', 'time_ms': 10000, 'entropy': 'must_decrease'}
- **audit_surface**: ['tier_distribution', 'compaction_ratio', 'stale_count', 'vault_entries']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_memory']
- **skills**: ['audit-seal', 'observe-ground']
- **knowledge**: ['know-math', 'know-language']
- **protocol**: synchronous_rpc
- **inputs**: {'content': 'string', 'tier_hint': 'enum[L1,L2,L3,L4,L5,L6]', 'importance': 'enum[low,medium,high,critical]'}
- **outputs**: {'memory_id': 'string', 'tier': 'enum', 'compressed': 'boolean'}

## Axis 3: Contrast

- **Not**: mem-dream, mem-graph, mem-session
- **Distinction**: GENERAL memory lifecycle discipline. mem-dream is AUTONOMOUS consolidation. mem-graph is IMPLEMENTATION detail. mem-session is SESSION-SCOPED working memory.
- **Trigger conflicts**: fires on memory lifecycle events; domain mem-* fires on specific implementations

## Replaces

- `mem-session`
- `mem-bridge`
- `mem-federation`
- `mem-writeback`
- `mem-dream`
- `mem-graph`
- `mem-vault`
- `mem-claim-receipt`
- `session-continuity-inhabit`
- `agent-memory-bridge`
- `unified-memory-federation`
- `knowledge-graph-query`
- `asi-knowledge-writeback`
- `agentic-dream-engine`
- `claim-receipt-v1`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*

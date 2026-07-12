---
id: audit-seal
name: audit-seal
version: 1.0.0
layer: substrate
description: Every decision logged. Irreversible decisions sealed. ΔS ≤ 0 on every
  output. Receipts > narratives.
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# audit-seal

> **Purpose:** Every decision logged. Irreversible decisions sealed. ΔS ≤ 0 on every output. Receipts > narratives.

## Axis 1: Invariants

- **authority**: arif_seal requires ack_irreversible for L6 writes
- **evidence_schema**: receipt = {action, actor, timestamp, hash, verdict}
- **reversibility**: L1-L4 logs reversible; L5-L6 vault seals irreversible
- **lineage**: hash-chained seal chain with prev_hash linkage
- **trigger_semantics**: decision_made OR action_completed OR seal_requested OR session_end
- **failure_contract**: log anyway with FAILED flag; never lose the attempt
- **resource_budget**: {'cpu': 'low', 'time_ms': 5000, 'entropy': 'must_decrease'}
- **audit_surface**: ['seal_count', 'chain_integrity', 'last_seq', 'vault_ref']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_seal', 'arif_compose']
- **skills**: ['verify-gate', 'memory-manage']
- **knowledge**: ['know-math', 'know-language']
- **protocol**: ledger_append
- **inputs**: {'payload': 'string', 'verdict': 'object', 'actor': 'string'}
- **outputs**: {'seal_id': 'string', 'vault_ref': 'string', 'hash': 'string'}

## Axis 3: Contrast

- **Not**: mem-vault, meta-observe, meta-drift
- **Distinction**: DECISION audit discipline. mem-vault is STORAGE mechanism. meta-observe is AGENT SELF-MONITORING. meta-drift is SCHEMA change detection.
- **Trigger conflicts**: fires on decisions and completions; mem-vault fires on storage operations

## Replaces

- `meta-observe`
- `meta-drift`
- `ops-verify`
- `dev-readme-check`
- `vault999-integrity`
- `arifos-observability`
- `drift-watch`
- `verify-runtime`
- `readme-truth-check`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*

---
id: FORGE-vault999-witness
name: FORGE-vault999-witness
version: 1.0.0-2026.07.17
description: "VAULT999 witness — immutable ledger integration, seal chain verification, and audit trace."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F11', 'F13']
autonomy_tier: T2
---
# ⚒️ VAULT999 Witness — Immutable Ledger Integration

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Read from, write to, and verify the VAULT999 append-only hash-chained ledger. Generate structured receipts for every consequential action. Verify chain integrity.

## When to Use
- Writing a seal entry to VAULT999 (verdicts, receipts, critical events)
- Reading seal history for audit, carry-forward, or session resume
- Verifying chain integrity — hash continuity from genesis to head
- Generating witness receipts for tri-witness evidence
- Anchoring cross-session state via seal chain

## When NOT to Use
- High-frequency logging (use Postgres or stdout)
- Caching or temporary state (use Redis)
- Relational queries on seal data (use Postgres index)

## ⚠️ Canonicalizer Rule (F-004 · 2026-07-19)

When verifying chain integrity, use the DOCUMENTED canonicalizer from `arifSeal.ts:94-110`:

```typescript
function canonicalSerialize(record: Omit<SealRecord, "hash">): string {
  // 9 mandatory + 2 optional fields, alphabetically sorted keys
  // EXCLUDES the hash field itself
}
```

**NEVER use naive `JSON.stringify(record, Object.keys(record).sort())`** — this includes the hash field and produces false verification failures. The canonical payload EXCLUDES `hash` and includes only: seq, ts, tool, args, judge_decision, exit_code, stdout_sha256, stderr_sha256, prev_hash (+ optional: approver, notes).

Reference: `/root/arifOS/docs/CANONICALIZER-VAULT999-2026-07-19.md`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | VAULT999 is append-only — never delete, never modify; chain rewrite = doctrine violation |
| F2 TRUTH | Every seal entry carries SHA256 hash of its content and the previous link hash |
| F3 WITNESS | Tri-witness seals anchored in VAULT999 — geometric mean of H×AI×Ext |
| F4 CLARITY | Seal entries are structured JSON, not free text; schema validated before write |
| F11 AUDIT | Seal chain IS the audit trail — every consequential action logged |
| F13 SOVEREIGN | Irreversible seals require F13 approval token |

## Commands & Patterns

```typescript
// Seal entry structure
interface SealEntry {
  seq: number;
  actor: string;
  verdict: 'SEAL' | 'HOLD' | 'SABAR' | 'VOID';
  content_hash: string;
  previous_hash: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

// Write seal via forge_vault
forge_vault({
  mode: 'seal',
  name: 'session-end-2026-07-16',
  content: JSON.stringify({ summary, receipts }),
  reason: 'AUTONOMOUS_SESSION_SEAL',
  tier: 'VAULT999',
  category: 'session.seal',
  actor_id: 'ARIF',
});

// Verify chain integrity
// Check tail -1 seal_chain.jsonl → verify previous_hash matches
// Script: /root/arifOS/scripts/verify_vault_chain.py

// Witness receipt pattern
const receipt = {
  receipt_id: crypto.randomUUID(),
  action_hash: sha256(action),
  witness: { h: 0.85, ai: 0.80, ext: 0.75 },
  w3: Math.cbrt(0.85 * 0.80 * 0.75),
  timestamp: new Date().toISOString(),
};
```

## Refusal Surface
- ❌ Editing or deleting existing seal entries
- ❌ Writing seals without actor_id
- ❌ Skipping chain integrity verification before trusted reads
- ❌ Storing raw secrets or PII in seal payloads
- ❌ Writing unstructured free text as seal content (must be valid JSON)

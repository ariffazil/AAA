---
id: vault-integrity
name: vault-integrity
version: 1.0.0
description: "Cognitive lens for VAULT999 — append-only hash-chained ledger integrity, chain verification, failure handling."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F3, F13]
autonomy_tier: T1
tags: [vault999, integrity, ledger, cognitive-lens]
---

# Vault Integrity

## REASONING PHILOSOPHY

VAULT999 is an append-only, hash-chained, immutable audit ledger. It is NOT a database. It is NOT a secret store. It is NOT a cache. Every write is permanent and cryptographically sealed. Think of it as a constitutional notary, not a storage bucket.

The vault exists to answer one question: "What happened, and can we prove it?" Every entry must be self-contained, verifiable, and meaningful to a future auditor who has zero context about the session that created it.

## DECISION HEURISTICS

**What belongs in VAULT999:**
- 888 JUDGE verdicts (SEAL, SABAR, HOLD, VOID)
- 999 SEAL terminal anchors
- Epoch boundaries (session start/end)
- Constitutional state changes
- Irreversible forge operations with ack

**What does NOT belong in VAULT999:**
- Secrets, keys, tokens, passwords (use vault.env or Docker secrets)
- Routine operational logs (use system logs)
- Debug output or temporary state
- Personal notes or session memory (use /root/.claude/memory/)

**When to verify the chain:**
- Before appending: verify the last hash
- After appending: verify the new hash
- Suspicious activity detected: full chain audit

## SIGNAL PRIORITY

1. Chain integrity (hash verification)
2. Entry completeness (all required fields present)
3. Entry meaning (future-auditor test)
4. Entry ordering (chronological correctness)

## UNCERTAINTY PROTOCOL

- If chain verification fails → do NOT append. 888 HOLD.
- If entry format is ambiguous → do NOT seal. Request clarification.
- If vault is unreachable → buffer locally, retry, escalate if persistent
- If two entries conflict on ordering → trust hash chain, not timestamp
- Never write secrets to vault. If unsure whether something is a secret → it is.

## FAILURE MODE REGISTRY

**These are specific errors. Actively avoid them:**
- Writing secrets to outcomes.jsonl (catastrophic — secrets become immutable)
- Skipping hash verification (breaks chain trust)
- Writing entries with insufficient context (future auditor cannot understand)
- Treating vault as general-purpose storage (dilutes audit trail)
- Deleting or modifying vault files directly (violates append-only contract)

## SCOPE BOUNDARIES

**Applies to:**
- `/root/.local/share/arifos/vault999/outcomes.jsonl` (physical file, chattr +a)
- `http://localhost:8100` (vault999 service)
- `http://localhost:5001` (vault999-writer service)
- All SEAL, SABAR, HOLD, VOID verdict storage

**Does NOT apply to:**
- General file storage or document management
- Database operations (PostgreSQL tables outside vault_seals)
- Secret storage or credential management
- Session memory or agent conversation logs

---
title: "SKILL: Vault Integrity"
type: skill
version: 1.0.0
category: governance
risk_band: HIGH
floors: [F1, F2, F3, F13]
evidence_required: true
sources: [/root/.opencode/skills/vault-integrity/SKILL.md]
confidence: high
---

# SKILL: Vault Integrity Reasoning

> **DITEMPA BUKAN DIBERI — VAULT999 is a notary, not a storage bucket.**
> **Source:** `/root/.opencode/skills/vault-integrity/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Writing to VAULT999 (outcomes.jsonl, SEALED_EVENTS)
- Verifying Merkle chain, hash integrity
- Auditing vault entries
- Deciding whether something belongs in VAULT999
- Keywords: VAULT999, vault, outcomes.jsonl, SEALED_EVENTS, ledger, audit, Merkle

---

## Reasoning Philosophy

VAULT999 is an **append-only, hash-chained, immutable audit ledger**. It is NOT:
- A database
- A secret/credential store
- A cache
- General-purpose storage

Every write is permanent and cryptographically sealed. It answers: "What happened, and can we prove it?"

---

## What Belongs in VAULT999

- 888 JUDGE verdicts (SEAL, SABAR, HOLD, VOID)
- 999 SEAL terminal anchors
- Epoch boundaries (session start/end)
- Constitutional state changes
- Irreversible forge operations with explicit acknowledgment

## What Does NOT Belong

- Secrets, keys, tokens, passwords (→ vault.env or Docker secrets)
- Routine operational logs (→ system logs)
- Debug output or temporary state
- Personal notes or session memory (→ /root/.claude/memory/)

---

## Chain Integrity Rules

1. **Before appending**: verify the last hash
2. **After appending**: verify the new hash
3. **Suspicious activity**: full chain audit
4. **Chain verification fails** → do NOT append. 888_HOLD.
5. **Entry format ambiguous** → do NOT seal. Request clarification.

---

## Future-Auditor Test

Every vault entry must pass: "Can a future auditor with zero session context understand what this entry means?"

If no → rewrite with more context before sealing.

---

## Uncertainty Protocol

- Vault unreachable → buffer locally, retry, escalate if persistent
- Two entries conflict on ordering → trust hash chain, not timestamp
- Never write secrets to vault (catastrophic — secrets become immutable)
- Unsure whether something is a secret → it IS a secret

---

## Failure Mode Registry

Actively avoid:
- Writing secrets to outcomes.jsonl (immutable exposure)
- Skipping hash verification (breaks chain trust)
- Writing entries with insufficient context (future auditor confused)
- Treating vault as general-purpose storage (dilutes audit trail)
- Deleting or modifying vault files directly (violates append-only contract)

---

## Related Pages

- [[skill-vault999-ops]] — safe operations on VAULT999
- [[concept-memory-knowledge-loop]] — memory as sealed trace
- [[skill-constitutional-reasoning]] — F1/F2/F3 reasoning framework
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Vault is notary. Not bucket.*

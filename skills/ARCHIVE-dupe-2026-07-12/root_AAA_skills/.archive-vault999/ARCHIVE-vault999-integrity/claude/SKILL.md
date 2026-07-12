---
id: vault999-integrity
name: Vault999 Integrity — Operational Lens
version: 1.0.0
description: Operational lens for the append-only hash-chained ledger—what belongs,
  chain verification, and failure handling.
owner: AAA
risk_tier: critical
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills: []
  servers: []
  tools: []
examples:
- Verify the chain before appending a new SEAL verdict
- Audit VAULT999 after detecting suspicious ordering or missing hashes
- Decide whether a proposed entry belongs in the ledger or in another store
tests:
- Hash chain verifies before and after append
- Entry containing secrets is rejected before sealing
- Chain mismatch triggers 888 HOLD without append
- Future-auditor can understand an entry from its fields alone
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  - Audit
  layer: HEXAGON
  autonomy_tier: T3
floor_scope:
- F1
- F2
- F3
- F11
- F13
---

# Vault999 Integrity — Operational Lens

## Overview

VAULT999 is an append-only, hash-chained, immutable audit ledger. It is a constitutional notary, not a database, cache, or secret store. Every write is permanent and cryptographically sealed. This skill tells you what belongs in the ledger, how to verify chain integrity, and what to do when something fails.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Before appending any SEAL, SABAR, HOLD, or VOID verdict
- Before storing an epoch boundary or constitutional state change
- Before logging an irreversible forge operation with sovereign ack
- When you need to verify chain integrity before or after a write
- When you suspect suspicious activity, missing hashes, or ordering conflicts

## When NOT to Use

- **Do not use** to store secrets, keys, tokens, or passwords (use `vault.env` or Docker secrets)
- **Do not use** for routine operational logs, debug output, or temporary state
- **Do not use** for personal notes or session memory (use `/root/.claude/memory/`)
- **Do not use** as general-purpose storage; doing so dilutes the audit trail

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| proposed_entry | yes | The entry candidate to append or evaluate |
| prior_hash | yes | Hash of the previous vault entry for chain verification |
| vault_path | no | Local path to `outcomes.jsonl` (default: `/root/.local/share/arifos/vault999/outcomes.jsonl`) |
| service_endpoint | no | `vault999` API endpoint (default: `http://localhost:8100`) |

## Procedure

### Step 1: Classify the Entry

Decide whether the entry belongs in VAULT999:

**Belongs:**
- 888 JUDGE verdicts (SEAL, SABAR, HOLD, VOID)
- 999 SEAL terminal anchors
- Epoch boundaries (session start/end)
- Constitutional state changes
- Irreversible forge operations with sovereign ack

**Does NOT belong:**
- Secrets, keys, tokens, passwords
- Routine operational logs
- Debug output or temporary state
- Personal notes or session memory

### Step 2: Verify Chain Integrity

Before appending:
- Read the last entry.
- Confirm its hash matches `prior_hash`.
- If the chain is broken → **do not append**. 888 HOLD.

After appending:
- Compute the new entry hash.
- Confirm it links back to the previous hash.
- If the new hash fails → treat as a chain failure. 888 HOLD.

### Step 3: Validate Entry Completeness

Ensure the entry passes the future-auditor test:
- All required fields are present.
- Meaning is clear without session context.
- No secrets are embedded.
- Ordering is chronological; if ordering conflicts with a timestamp, trust the hash chain.

### Step 4: Handle Failures

- **Chain verification fails** → STOP. Do not append. 888 HOLD.
- **Entry format is ambiguous** → Do not seal. Request clarification.
- **Vault is unreachable** → Buffer locally, retry, and escalate if persistent.
- **Two entries conflict on ordering** → Trust the hash chain, not the timestamp.
- **Unsure whether something is a secret** → Treat it as a secret.

## Allowed Tools

| Tool / Capability | Purpose |
|---|---|
| `arifos_hermes_vault_query` | Read and inspect VAULT999 entries |
| `arifos_arif_seal` / `arifos_vault_seal` | Append a verdict to the ledger |
| `arifos_arif_judge` | Obtain an 888 JUDGE verdict before sealing |
| `arifos_arif_measure` | Check vault service health before acting |

## Forbidden Actions

- **NEVER** write secrets, keys, tokens, or passwords into VAULT999.
- **NEVER** append without verifying the previous hash.
- **NEVER** append when chain verification fails.
- **NEVER** treat VAULT999 as a database, cache, or general file store.
- **NEVER** delete or modify vault files directly; append-only means append-only.
- **NEVER** seal an entry that fails the future-auditor test.
- Escalate to **arifOS 888_JUDGE** if chain integrity cannot be verified or a secret may have been written.

## Output Format

```
## Skill Result: vault999-integrity

### Summary
One-paragraph summary of the entry classification and chain-verification outcome.

### Evidence
- Entry belongs in VAULT999: true / false
- Prior hash verified: true / false
- New hash verified: true / false
- Future-auditor test: pass / fail
- Secrets scan: clean / flagged

### Recommendations
- Proceed to append under SEAL, or
- Reject entry and route to the appropriate store, or
- Escalate to 888 HOLD with reason

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Chain verification fails | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Potential secret written to vault | security.agent + arifOS judge | immediate hold + audit |
| Vault service unreachable | A-FORGE ops + arifOS ops | health triage |
| Ambiguous entry format | Request clarification from task owner | hold |
| Ordering conflict | arifOS 888_JUDGE | chain-truth ruling |

---

*Skill version 1.0.0 — AAA Skill Library*

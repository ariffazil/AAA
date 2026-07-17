---
id: 999-vault-seal-immutable
name: 999-vault-seal-immutable
version: 1.0.0-2026.06.25
description: Seal action to civilizational memory with mandatory end-of-session recursive MCP stack hardening and future INIT scaffold. VAULT999 record. Stage 7.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: high
floor_scope: [F1, F2, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "seal this"
  - "vault this"
  - "record this"
  - "999-vault-seal-immutable"
dependencies:
  mcp_servers:
    - arifos
  skills:
    - 010-forge-execute-warrant
inputs:
  - execution_receipt
  - seal_verdict_id
  - plan_id
  - verdict
  - action_taken
  - human_confirmation
outputs:
  - seal_status
  - ledger_summary
  - replay_path
  - audit_path
  - civilization_memory_implication
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# 999-vault-seal-immutable — CIVILIZATION MEMORY SKILL

> **DITEMPA BUKAN DIBERI.** Memory without revision, law without mercy.
> **Maps to:** 999_VAULT
> **Loop position:** Stage 7 of 7 — immutable record.

---

## 0. The Loop This Skill Governs

```
INTENT → OBSERVE → PLAN → CRITIQUE → JUDGE → FORGE → SEAL
   ________________________________________ THIS SKILL ____
```

This skill is Stage 7. It seals final, reviewed, provenance-bound outcomes.
It does not seal drafts, guesses, or unjudged execution.
It must also close the loop by hardening the stack layers touched this session and scaffolding unresolved gaps into the next INIT.

---

## 1. MCP Prompt (arifosmcp_civilization_seal)

```
You are arifOS Civilization Sealer.

Seal only final, reviewed, provenance-bound outcomes.
Do not seal drafts, guesses, or unjudged execution.

Create a VAULT999 record containing:
- session_id
- actor_id
- intent
- evidence references
- plan_id
- judge verdict
- execution artifact references
- human confirmation if required
- hash / lineage / timestamp
- lessons for future loop improvement
- recursive hardening across skills, kernel, tools, prompts, resources
- remaining gap scaffold with severity, proof, and fix path
- next INIT seal tasks

Return:
1. seal status
2. ledger summary
3. replay path
4. audit path
5. civilization-memory implication
6. recursive hardening report
7. remaining gaps scaffold
8. next INIT seal tasks
```

---

## 2. VAULT999 Record Structure

```json
{
  "vault_id": "v_xxx",
  "session_id": "s_xxx",
  "actor_id": "FORGE",
  "intent": "Deploy WEALTH server restart",
  "evidence_refs": [
    "forge_work/rsi-wealth-2026-06-25/seal/SEAL.md",
    "commit_9718ffa"
  ],
  "plan_id": "plan_xxx",
  "verdict": "SEAL",
  "seal_verdict_id": "888_abc123",
  "execution_receipt": {
    "action": "restart",
    "target": "WEALTH",
    "pid": 3761767,
    "timestamp": "2026-06-25T..."
  },
  "human_confirmation": {
    "type": "T3_ACK",
    "confirmed_by": "Arif",
    "timestamp": "2026-06-25T..."
  },
  "artifact_hash": "sha256:...",
  "lineage": "arifOS loop: loop-engineer → reality-observer → mind-planner → consequence-critic → judge-verdict → reality-forge → civilization-seal",
  "lessons": ["..."],
  "recursive_hardening": {
    "skills": {},
    "kernel": {},
    "tools": {},
    "prompts": {},
    "resources": {}
  },
  "gaps_remaining": [],
  "next_init_tasks": [],
  "memorable_for_future": true,
  "vaulted_at": "2026-06-25T..."
}
```

---

## 3. Seal Status Values

| Status | Meaning |
|--------|---------|
| SEALED | Immutable record written to VAULT999 |
| PENDING_HUMAN_CONFIRMATION | T3 action — awaiting Arif |
| FAILED | Execution failed — rollback invoked, failure sealed |
| VOID | Verdict was VOID — no execution, seal intent only |

---

## 4. When NOT to Seal

- ❌ Draft plans not reviewed by judge
- ❌ Model inference without evidence binding
- ❌ Unjudged execution attempts
- ❌ 888_HOLD not yet resolved
- ❌ Failure records that weren't executed through FORGE

---

## 5. Civilization Memory Implication

For each seal, state one line:

```
This decision affects [X] because [Y].
Lessons for next loop: [Z].
```

Example:
```
This WEALTH restart affects capital computation accuracy because
compute_conservation now reads both 'amount' and 'value' keys.
Lessons for next loop: restart server after critical bug fix.
```

---

## 6. Anti-Patterns

- ❌ Sealing without valid execution receipt
- ❌ Sealing unjudged content
- ❌ Modifying VAULT999 after seal (immutable)
- ❌ Skipping the lessons field
- ❌ Using VAULT999 for working memory (use forge_work/)
- ❌ Ending session without recursive MCP stack hardening
- ❌ Ending session without next INIT scaffold when gaps remain

## 7. Mandatory Session-End Hardening

Every 999 close must scan and report:

1. `skills` — loaded, drifted, missing, hash mismatch
2. `kernel` — floor enforcement, auth/provenance, verdict integrity
3. `tools` — registry vs live, phantom tools, gate drift, callability
4. `prompts` — canonical coverage, stale text, truncation, template arg drift
5. `resources` — URI registration, resolution, content health

If any layer is skipped, the session close is incomplete and must downgrade from clean `SEAL`.

## 8. Mandatory Future INIT Scaffold

Every 999 close must leave a pickup scaffold for the next `000_INIT`:

- exact remaining gaps
- severity and proof
- smallest lawful next step
- artifact or path to resume from

The next session must be able to continue from the seal alone, without relying on chat history.

---

*DITEMPA BUKAN DIBERI — Civilization remembers what agents forget.*

---

## §D AUTO-LOADED GUARDRAILS — merged from: 700-clean, 777-ops, 950-audit

### D1. Post-Seal Auto-Cleanup (immune system)

**Trigger:** After every seal, run entropy check.

**Rot classification:**
- `doc-rot`: stale URLs, superseded docs
- `api-rot`: package versions past compatibility
- `trigger-rot`: skill descriptions overlapping
- `unused-rot`: no execution in 90 days
- `fake-rot`: hallucinated files, forged receipts
- `creep-rot`: tool permission widened beyond authority

**Cleanup rules:** Remove confirmed garbage (F1 backup first). Quarantine uncertain items to `.archive/`. Never delete blindly. Update registry if skills merged/deprecated.

### D2. Post-Seal Auto-Health Check (all organs)

```bash
for port in 8088 7071 8081 18082 18083 3001; do
  curl -s --max-time 3 http://localhost:$port/health | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(f'Port $port: {d.get(\"status\",\"?\")}')
except: print('Port $port: DOWN')
" 2>/dev/null
done
```

**Common failure patterns:**
| Symptom | Fix |
|---------|-----|
| SESSION_REQUIRED | Call arif_init first |
| LEASE_REQUIRED | Call forge_lease_request |
| Connection refused | systemctl restart <service> |
| Timeout | Check logs, restart if needed |
| Multiple organs down | Check Docker (Postgres, Redis, NATS) |

**Severity escalation:** Single organ down → restart. Multi-organ → check Docker. Data corruption → 888_HOLD. Security incident → 888_HOLD + Arif.

### D3. Vault Audit Procedure

1. Gather evidence (commit SHA, health output, test results, diff)
2. Compute evidence hashes (BLAKE3 or SHA-256)
3. Call arif_judge with candidate + evidence
4. On SEAL → call arif_seal(content, reason, ack_irreversible=true)
5. Verify vault write: chain integrity must be OK
6. Pre-May-2026 migration gaps (ids 18-60): SOVEREIGN RULING — non-issue, do not block

**Never:** seal without SEAL verdict. Seal without ack_irreversible=true. Seal with raw credentials — redact first.

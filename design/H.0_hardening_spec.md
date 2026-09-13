# H.0 Hardening Specification

**F13 Ratified Design (2026-09-13)**
**Intent**: Constitutional control plane for capability onboarding. Not provider integration.

---

## Core Theorem
```text
Capability is easy. Attribution is hard.
```

---

## H.0a — SOT Mutation Attribution
### Objective
*"Who changed the SOT?"*

### Components
1. **Git Strategy**
   - Repo: `/root/.config/federation-models.git`
   - Hooks:
     - `pre-commit`: Schema validation (`jq . federation-models.json`)
     - `post-commit`: Emit receipt to VAULT999 (`/root/arifOS/VAULT999/receipts/SOT/`)
   - Branch:
     - `main`: Protected (F13-gated)
     - `drafts/*`: Ephemeral
   - Tag: `sealed/<sha256>` (immutable, F13-gated)

2. **Flock Strategy**
   - Lockfile: `/root/.config/federation-models.lock` (fcntl.flock)
   - Timeout: 30s (auto-release)
   - Audit: `flock -n /path/to/lock -c "<command>"` → log PID + timestamp

3. **Audit Rules**
   ```audit
   -w /root/.config/federation-models.json -p wa -k SOT_MUTATION
   ```
   - Output: `/var/log/audit/audit.log` → parsed by `arifFlow` for receipt binding

4. **Mutation Receipts**
   **Schema** (`arifos.canonical_receipt.v1`):
   ```json
   {
     "event_id": "SEAL-<uuid>",
     "timestamp": "ISO-8601",
     "actor": {
       "id": "<actor_id>",
       "verified": false,
       "canonical": "<canonical_id>"
     },
     "action": "CREATE|UPDATE|DELETE",
     "target": "/root/.config/federation-models.json",
     "diff": "<unified_diff>",
     "sha256_before": "<hex>",
     "sha256_after": "<hex>",
     "authority_band": "FORGE|SEAL",
     "session_id": "<session_id>",
     "witnesses": ["<agent_id>", ...]
   }
   ```
   - Storage: VAULT999 (`/root/arifOS/VAULT999/receipts/SOT/`)

5. **Rollback Model**
   - Mechanism: `git revert HEAD` (atomic, receipted)
   - Fallback: Restore from `federation-models.json.bak-<timestamp>` (auto-backup on write)

---

## H.0b — Actor Serialization Completeness
### Objective
*"Who called the system?"*

### Components
1. **Schema Fix**
   - **Current**: `"actor": "unknown"`
   - **Proposed**:
     ```json
     "actor": {
       "id": "<actor_id>",
       "verified": false,
       "canonical": "<canonical_id>"
     }
     ```

2. **Registration Gate**
   - Registry: `/root/AAA/registry/actors.json` (F13-gated)
   - Fields:
     ```json
     {
       "actor_id": "<id>",
       "canonical_id": "<id>",
       "authority_band": "OBSERVE|THINK|FORGE|SEAL",
       "registration_timestamp": "ISO-8601",
       "witnesses": ["<agent_id>", ...]
     }
     ```

3. **Session Binding**
   - Tool: `arif_init` (MCP arifOS)
   - Output: `session_token` with `actor_id` claim (JWT)

---

## H.0c — Identity Proof Chain
### Objective
*"Can they prove who they are?"*

### Components
1. **Challenge-Response Protocol**
   - Endpoint: `http://localhost:18900/crypto_auth`
   - Flow:
     1. Hermes → `POST /issue_challenge` → `{"actor_id": "hermes-asi", "purpose": "identity_escalation"}`
     2. Signing Lane → `{"nonce": "<base64>", "challenge_id": "<uuid>"}`
     3. Hermes → Sign nonce with sovereign key (Ed25519) → `POST /verify_challenge`
     4. Signing Lane → Verify → Mint `session_token` with `actor_verified: true`

2. **Authority Ceiling**
   - Registry: `/root/AAA/registry/authority_ceilings.json`
   - Example:
     ```json
     {
       "hermes-asi": {
         "max_band": "FORGE",
         "domains": ["multimodal", "memory", "session"],
         "witness_requirement": "tri-channel (human + AI + external)"
       }
     }
     ```

---

## Threat Model
| Threat | Mitigation |
|---|---|
| Unauthorized SOT mutation | Git + flock + auditd + receipts |
| Actor spoofing | Challenge-response + authority ceiling |
| Attribution decay | VAULT999 receipts + actor registry |
| Rollback failure | Git revert + auto-backup |
| Audit log tampering | Linux auditd (immutable) + VAULT999 |

---

## Receipt (F11)
```json
{
  "event_id": "SEAL-<uuid>",
  "timestamp": "2026-09-13T16:00:00+08:00",
  "actor": {
    "id": "hermes-asi",
    "verified": true,
    "canonical": "hermes-asi-gateway"
  },
  "action": "H.0_SPEC_DESIGN",
  "target": "/root/AAA/design/H.0_hardening_spec.md",
  "sha256": "<hex>",
  "authority_band": "FORGE",
  "session_id": "SEAL-89c0fa4ecea54d43",
  "witnesses": ["FI-008", "AAA", "arifOS"],
  "floors": {
    "F1_AMANAH": "No Secret mutation",
    "F2_TRUTH": "Design-only, no implementation",
    "F11_AUDIT": "Receipt emitted"
  },
  "888_HOLD": "H.1 implementation blocked until F13 ratification",
  "ΔS": 0
}
```

---

## Next Steps
1. **H.1 Implementation**: Git init + flock + audit rules (F13-gated).
2. **A.1 Token Plan Witness**: Spec-only (F13-gated).
3. **B.1 MiniMax Vision Admission**: New capability proposal (F13-gated).

DITEMPA BUKAN DIBERI ⚒️
# SOVEREIGN INVOCATION GUIDE — mcp-ops v3.1.1 seal

> **Purpose:** give Arif (F13 sovereign) the exact payload and command sequence to issue
> the `arif_seal` against VAULT999, ratifying the mcp-ops v3.1.1 canonical.
> **Date:** 2026-09-21
> **Producer:** 333-AGI autonomous continuation (this file does NOT issue the seal;
> only the sovereign with `actor_signature` + `key_id` can).

---

## TL;DR — what Arif does

In a sovereign session (Telegram/Termux/any channel with F13 authority):

1. **Open** the F13 sovereign session against `127.0.0.1:8088` (arifOS MCP).
2. **Mint** a session via `arif_init` with `actor_id="arif"`, `requested_authority="SOVEREIGN_SEAL"`.
3. **Get verdict** via `arif_judge mode=judge candidate="<sealed payload>" seal_purpose="mcp-ops canonical ratification" action_class="SEAL" action_tier="T5"`.
4. **Issue seal** via `arif_seal mode=seal payload="<sealed payload>" seal_purpose="..." constitutional_chain_id="<from verdict>" judge_state_hash="<from verdict>" actor_signature="<F13>" nonce="<fresh>" key_id="<F13 key>" ack_irreversible=true`.

If any step rejects, the kernel will say so with a specific reason. The 888_HOLD_ESCALATION.md already documents one such reason (AGENT cannot seal without F13 credentials).

---

## Kernel-canonical reference (probed 2026-09-21)

The following documents are the kernel's own canonical answers to the questions the F13 reviewer
will have. Pulled from `arifos://seal-readiness`, `arifos://refusal-surface`, and `arifos://identity`
via direct MCP read at 2026-09-21T16:05+00:00.

### From `arifos://seal-readiness`

```
SEAL TYPES (disambiguated):
  KERNEL_SEAL_AWARENESS    — kernel knows about it (informational)
  DOMAIN_SEAL_VALIDITY     — calculation valid in domain (e.g. WEALTH NPV converged)
  JUDGE_SEAL_AUTHORIZATION — action authorized (F1–L13 cleared, APEX present)
  VAULT999_SEAL_RECORD     — record written (immutable audit trail entry exists)
  PUBLIC_SEAL_READINESS    — candidate posture, not execution approval

SEAL GATE (what must pass before a SEAL):
  1. F1 AMANAH:         ack_irreversible = true
  2. F2 TRUTH:          tau_confidence >= 0.99
  3. F3 WITNESS:        witness triad scores present
  4. F8 REVERSIBILITY:  escape path documented
  5. F9 ANTIHANTU:      C_dark < 0.30
  6. L11 AUTH:          actor identity verified
  7. L13 SOVEREIGN:     human ratifier = arif-fazil

NON-SEAL VERDICTS: SABAR (held, needs more evidence), HOLD (blocked by floor),
                    VOID (rejected or self-contradictory)

"Bare 'SEAL' without namespaced context is NON-COMPLIANT."
```

**Recommended SEAL type for the mcp-ops v3.1.1 ratification:**
`JUDGE_SEAL_AUTHORIZATION` (the consolidation has been F1–L13 cleared and APEX-confirmed
empirically; the seal records the authorization to ratify) **+** `VAULT999_SEAL_RECORD`
(the seal write IS a VAULT999 append; both types apply; declare both in `seal_purpose`).

### From `arifos://refusal-surface` (the relevant subset)

```
SOFT REFUSALS (888_HOLD — requires F13 sovereign acknowledgment):
  • Any action classified IRREVERSIBLE by the reversibility engine
  • Vault999 append (immutable — cannot be undone)         ← THIS IS THE SEAL
  • External email or message dispatch
  • Financial transactions or commitments
  • Deployment to production infrastructure
  • Schema migrations on live databases
  • DNS or certificate changes
  • Any action with blast_radius > LOW and no rollback path
```

**This is the kernel's own admission that Vault999 append is a 888_HOLD action.**
The 888_HOLD_ESCALATION.md is the canonical response to this soft refusal — already written.

### From `arifos://identity` (sovereign identity)

```
Sovereign:       Muhammad Arif bin Fazil
Role:            L13 SOVEREIGN — final veto authority
Identity Source: identity.toml
Identity Hash:   BLAKE3 (verified at boot)

Authority Chain:
  APEX (Arif Fazil, L13 SOVEREIGN)
    → arifOS constitutional kernel
      → F1–L13 floor receipts
        → domain organ advisory output (GEOX/WEALTH/WELL)
          → AAA operator surface
            → VAULT999 audit seal
              → A-FORGE execution

A2A Autonomy Tiers:
  T1 (Execution)     — Routine tasks, local run/test/build, precise FS edits. Auto-do.
  T2 (Negotiation)   — Multi-file refactor, dep updates, local service restarts. Announce-and-execute.
  T3 (Architectural) — Constitutional changes, production deploys, secret rotations, vault999 writes. 888_HOLD required.
```

The mcp-ops v3.1.1 ratification is T3-class (vault999 write), so 888_HOLD is doctrine.

### From `arifos://vault/head` (current VAULT999 state — sample of prior seal format)

The most recent seal in the chain (sequence 40, 2026-09-16T18:41 UTC) was issued by:

```
{
  "actor": "arif",
  "actor_id": "arif",
  "actor_verification": {"actor_verified": true, "method": "ed25519_verified", "signature_verified": true},
  "authority_state": "SOVEREIGN",                  ← what the F13 sovereign has; what AGENT lacks
  "decision_reference": "SOV-3278ad34e404",
  "envelope_version": "f004-v1",
  "epoch_id": "F004-CANONICAL-2026-07-17",
  "input_hash": "sha256:9439d318f8d6c6b8a0365463732129c3d991ead6dcdf59f340dea7585233dcea",
  "operation_id": "3c56625a781d4a18",
  "prev_hash": "sha256:f9fc245f7cf2779eefac73f5d275750406e2c3d8b6d6ceebc52965ca1cb93f64",
  "receipt_hash": "sha256:c8826155b86af4f2f5b07ec2225c3ed72b387fb9e8bbf6b75a2a26b8ac0c662a",
  "reversibility": "IRREVERSIBLE",
  "seq": 40,
  "session_id": "SEAL-e226d45da1a54554",
  "sig_key_id": "vault-hmac-1",                     ← the F13 sovereign's signing key
  "timestamp": "2026-09-16T18:41:41.393549Z",
  "tool_name": "arif_seal",
  "verdict": "SEAL"
}
```

The next seal (seq=41) should follow this same shape. F13 sovereign's `sig_key_id` was
`vault-hmac-1` for the prior seal; the new seal will use the same key unless rotated.


## Suggested sealed payload

```text
mcp-ops v3.1.1 canonical ratification.

Source SKILL.md:        /root/AAA/skills/engineering/mcp-ops/SKILL.md
SHA-256 (canonical):    de09f5faf0ef2319750bb4c1f26f4be066e276a45dc6977d873d79ed23f0c3dc
Size:                   44724 bytes / 796 lines
Version:                3.1.1
Accordant to:           https://modelcontextprotocol.io/llms.txt
                        (9-stage workflow: Stage 0 LEARN -> Stage 8 GOVERN, RETIRE in 8h)
Era covered:            2026-07-28 (stateless preferred) + 2025-11-25 (legacy handshake)

Audit corpus:           /root/AAA/skills/.frozen/2026-09-21-llms-alignment/audit/
Frozen chain:           /root/AAA/skills/.frozen/2026-09-21-llms-alignment/
OWNERSHIP_MAP:          /root/AAA/skills/OWNERSHIP_MAP.yaml (P3_mcp_tooling ratified to single canonical chain)

Absorptions (24 names preserved as tombstones + references):
  FORGE-mcp-ops · FORGE-mcp-federation-ops · FORGE-mcp-lifeguard
  FORGE-fastmcp · forge-fastmcp
  FORGE-mcp-gui · forge-mcp-gui
  FORGE-mcp-a2a-agentic · forge-mcp-a2a-agentic
  FORGE-mcp-testing (inode-consolidated with engineering/mcp-ops; sha ebe2ebdfa487)
  FORGE-mcp-governance-wrapper · forge-mcp-governance-wrapper
  federation-mcp-drift-audit
  mcp-organ-probe · mcp-edit-activation · mcp-transport-fix
  mcp-ecosystem-indexing · forge-mcp-registry-publish
  external-platform-mcp · mcp-context-compression
  forge-minimax-mcp-direct-invoke · telegram-mcp-product-line
  mcp-testing · mcp-sota-shopping-list

22/22 federation tombstones resolve to v3.1.1 across 4 mirror trees.
0 dead links. 0 destructive operations during this consolidation.
arifOS :8088 healthy (13/13 floors, vault999 healthy, deployment_drift aligned).

Closure-flow verdict: SEAL-READY (Phases 1-6 complete; F13 seal pending).
```

## Suggested `arif_judge` call (after sovereign session minted)

```bash
# Step 1: Mint sovereign session
curl -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":1,
    "method":"tools/call",
    "params":{
      "name":"arif_init",
      "arguments":{
        "mode":"init",
        "actor_id":"arif",
        "requested_authority":"SOVEREIGN_SEAL",
        "ack_irreversible":true
      }
    }
  }'
# Expected response: session_id, session_token, actor_cryptographically_verified=true

# Step 2: Get SEAL verdict (requires judge_state_hash for the seal)
curl -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <session_id_from_step_1>" \
  -d '{
    "jsonrpc":"2.0","id":2,
    "method":"tools/call",
    "params":{
      "name":"arif_judge",
      "arguments":{
        "mode":"judge",
        "candidate":"<the sealed payload above>",
        "actor_id":"arif",
        "session_id":"<session_id>",
        "session_token":"<session_token>",
        "actor_signature":"<F13 signature over candidate>",
        "nonce":"<fresh>",
        "key_id":"<F13 key id>",
        "constitutional_chain_id":"P3_mcp_tooling.2026-09-21",
        "action_class":"SEAL",
        "action_tier":"T5",
        "reversibility_level":"irreversible",
        "blast_radius":"ORG",
        "seal_purpose":"mcp-ops canonical ratification"
      }
    }
  }'
# Expected response: verdict=SEAL, judge_state_hash, constitutional_chain_id, signature

# Step 3: Issue the seal
curl -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <session_id>" \
  -d '{
    "jsonrpc":"2.0","id":3,
    "method":"tools/call",
    "params":{
      "name":"arif_seal",
      "arguments":{
        "mode":"seal",
        "payload":"<the sealed payload above>",
        "actor_id":"arif",
        "session_id":"<session_id>",
        "session_token":"<session_token>",
        "constitutional_chain_id":"<from verdict>",
        "judge_state_hash":"<from verdict>",
        "witness_type":"arif",
        "seal_purpose":"mcp-ops canonical ratification",
        "actor_signature":"<F13 signature over payload + chain_id + nonce>",
        "nonce":"<fresh>",
        "key_id":"<F13 key id>",
        "ack_irreversible":true
      }
    }
  }'
# Expected response: VAULT999 entry id, sealed hash, signature chain id
```

## What the AGENT (333-AGI) cannot do

Without `actor_signature` and `key_id` (which only the sovereign F13 key can produce),
`arif_seal` rejects with `HOLD` (per the empirical probe in `888_HOLD_ESCALATION.md`).

The AGENT can:
- ✅ Run `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`
- ✅ Mint a session with `LIMITED_MUTATE` authority (mutation allowed, seal disallowed)
- ✅ Read all audit artefacts and frozen bodies

The AGENT cannot:
- ❌ Mint a session with `SOVEREIGN_SEAL` authority (requires F13 cryptographic identity)
- ❌ Produce an `actor_signature` over the payload (requires the F13 private key)
- ❌ Invoke `arif_seal` for a T5 IRREVERSIBLE write (the kernel removes `arif_seal` from
   `allowed_next_verbs` when the actor cannot seal)

## After the seal

Once `arif_seal` succeeds:
- `arif_seal` returns a `va_entry_id` and `sealed_hash`
- The mcp-ops v3.1.1 ratification becomes immutable in VAULT999
- `arif_seal mode=verify` can be called by anyone to verify the seal against the payload
- `arif_seal mode=ledger` returns the new ledger tip

The 333-AGI can then run `arif_seal mode=changelog` to enumerate the seal event in the audit trail.

## Failure recovery

If any step rejects:
1. Read the rejection reason carefully (the kernel is precise about authority requirements).
2. If `actor_signature` is rejected → F13 key configuration mismatch; check the sovereign key setup.
3. If `judge_state_hash` is rejected → the previous verdict was not a SEAL; run `arif_judge mode=validate` first.
4. If `seal_allowed: false` returns → AGENT is acting, not the sovereign; abort and let the sovereign retry.
5. If a previous seal exists with the same payload (duplicate) → check ledger first.

## Standing by

333-AGI is idle. The audit corpus is durable. The seal can be issued at any sovereign session.

DITEMPA BUKAN DIBERI ⚒️

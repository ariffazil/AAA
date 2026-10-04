# A2A Five-Gate Sequence — Live Discovery 2026-08-07

When invoking Apex via A2A, you must pass **FIVE sequential gates**, each with a distinct error code. Stopping after the first error and patching only that gate will surface the next gate, and the next.

## The Five Gates

| # | Gate | Field | Error if missing/wrong |
|---|---|---|---|
| 1 | A2A-Version header | `A2A-Version: 1.0` (HTTP header, NOT a body field) | `-32600 Invalid Request. Set A2A-Version: 1.0` |
| 2 | session_id lineage | `body.session_id` (non-empty, non-placeholder, NOT in `GHOST_SESSION_DENY = ['', 'unknown', 'session-unknown', 'session_unknown', 'null', 'undefined', 'none', 'n/a']`) | `-32600 Invalid params: session_id is mandatory (Ghost Task blocked — F4 CLARITY / A2A lineage)` |
| 3 | actor_id canonical | `envelope.actor_id` ∈ `CANONICAL_ACTORS = {arifos, aforge, geox, wealth, well, hermes, openclaw, forge, '777-forge', 'aaa-architect', 'aaa-engineer', 'aaa-auditor', hermes-asi, antigravity, ARIF_FAZIL, anonymous}` | `-32001 888_HOLD: Sender actor_id "X" is not canonical.` |
| 4 | DID envelope signature | `envelope.from_did` + Ed25519 `signature` over canonical bytes (fields: from_did, to_did, actor_id, agent_id, session_id, action, subject — sorted, separator `,:`) | `-32001 DID_REQUIRED: All A2A tasks must carry a DID envelope with from_did + signature` |
| 5 | Agent policy registration | `actor_id` ∈ `AGENT_POLICIES` (process-local map); `anonymous` → `NO_POLICY_LEGACY_FALLBACK` (T2 ceiling, OBSERVE/PREPARE only) | `-32001 888_HOLD: Agent X has no registered policy — DENY ALL` |

## Live source locations

| Gate | File:Line |
|---|---|
| 1 | `a2a-server/server.js` route handler |
| 2 | `a2a-server/server.js` `requireTaskLineage()` |
| 3 | `a2a-server/federation_envelope.js` `validateEnvelope()` step 3 |
| 4 | `a2a-server/server.js` A2A DID Signature Verification (ENFORCED 2026-08-02, F13 mandate) |
| 5 | `a2a-server/federation_envelope.js` `validateAgentPolicy()` |

## The OBSERVE bypass path (the only working recipe)

For OBSERVE/PREPARE-only dispatches where you want a result without sealing to VAULT999:

```python
import json, urllib.request, uuid, os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

with open("/root/AAA/auth/keys/aaa_private.key","rb") as f:
    raw = f.read()
priv = Ed25519PrivateKey.from_private_bytes(raw[:32])

envelope = {
    "from_did": "did:arif:aaa",          # any organ DID from registry
    "to_did": "did:arif:arifos",
    "actor_id": "anonymous",             # → NO_POLICY_LEGACY_FALLBACK
    "agent_id": "arifos",
    "session_id": "SEAL-<your-real-session-id>",  # from arif_init, NOT placeholder
    "action": "evaluate",
    "subject": "<task name>",
    "risk": {"tier":"T0","action_class":"OBSERVE"},
    "receipts": {}
}

# Canonical bytes for signing
canonical = json.dumps({
    "from_did": envelope["from_did"], "to_did": envelope["to_did"],
    "actor_id": envelope["actor_id"], "agent_id": envelope["agent_id"],
    "session_id": envelope["session_id"], "action": envelope["action"],
    "subject": envelope["subject"],
}, sort_keys=True, separators=(",", ":")).encode()

envelope["signature"] = priv.sign(canonical).hex()

# body MUST include session_id at top level (server.js extractSessionId walks body.session_id)
body = {
    "jsonrpc":"2.0","id":1,"method":"message/send",
    "session_id": envelope["session_id"],
    "params":{
        "envelope": envelope,
        "message":{
            "role":"user",
            "parts":[{"kind":"text","text":"<task>"}],
            "messageId":f"msg-{uuid.uuid4().hex[:12]}",
            "contextId":f"ctx-{uuid.uuid4().hex[:8]}",
            "metadata":{}
        }
    }
}

req = urllib.request.Request(
    "http://127.0.0.1:3001/tasks",
    data=json.dumps(body).encode(),
    headers={
        "Content-Type":"application/json",
        "Authorization":f"Bearer {os.environ['A2A_TOKEN']}",
        "A2A-Version":"1.0"
    },
    method="POST"
)
```

## Why five gates, not one

Each gate fires with a different error code. The traps:
- `arif_judge` directly (MCP at `:8088`) returns HOLD for anonymous callers — F11 AUDITABILITY refusing unsigned work. Correct behavior.
- A2A via direct call (`message/send` without session_id) returns Ghost Task block — F4 CLARITY lineage. Correct behavior.
- A2A via unsigned envelope returns DID_REQUIRED — F13 SOVEREIGN enforcement. Correct behavior.
- A2A via unknown actor_id returns canonical rejection — F11 namespace integrity. Correct behavior.
- A2A via un-registered actor returns policy DENY — F1 AMANAH default-deny. Correct behavior.

Each gate is enforced by a different floor. Each floor is correct in isolation. The challenge is knowing which gate fires when, and how to satisfy it without bypassing the others.

## For SEAL-grade verdicts

The OBSERVE bypass returns an evaluation result but does NOT seal it to VAULT999. To convert OBSERVE evaluation → SEAL verdict:
1. The dispatched agent (e.g. `888-APEX`) must internally call `arif_judge` with proper session binding (actor verified, not anonymous)
2. The agent's verdict must be approved by `arif_seal` (Lane A) — which requires F13 sovereign crypto

The OBSERVE path is the consultation lane; the SEAL path is the constitutional lane. They are intentionally different.

## Common error catalog

| Symptom | Root cause | Fix |
|---|---|---|
| `Unknown tool: 'arif_judge_deliberate'` | Internal-only tool, not on public MCP surface | Use `arif_judge` (public surface) |
| `Configuration is invalid. Unrecognized keys: _last_updated, _patch_summary` | OpenCode strict schema `additionalProperties: false` | Strip the offending keys from JSON root |
| `HOLD reason: UNMEASURED` from `arif_judge` | Caller not bound to a verified actor | Use `arif_init` first, capture session_id + sct |
| A2A HTTP 400 + `Invalid params: session_id is mandatory` | Missing/placeholder session_id | Put session_id at body top level, not just envelope |
| A2A HTTP 403 + `888_HOLD: Sender actor_id "X" is not canonical` | actor_id not in CANONICAL_ACTORS set | Use canonical name or `anonymous` (for legacy wrap) |
| A2A HTTP 403 + `DID_REQUIRED` | No `envelope.from_did` + `signature` | Sign canonical bytes with AAA private key |
| A2A HTTP 403 + `Agent X has no registered policy` | actor_id ≠ anonymous AND no policy registered | Use `anonymous` (legacy wrap, T2 ceiling) or register policy |

## Cross-reference

- `agent-config-validation` skill: handles the OpenCode JSON schema rejection (the "Configuration is invalid" errors)
- `federation-model-routing` skill: alias → upstream resolution when the served model doesn't match expected
- `arifos-federation-ops` skill: kernel session lifecycle, Lane A vs Lane B sealing, SCT renewal
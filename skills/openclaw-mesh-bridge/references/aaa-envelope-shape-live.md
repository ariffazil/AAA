# Live-tested AAA A2A envelope shape (2026-08-07)

The envelope in the parent SKILL.md is the **design contract**. This file is the **live wire format** that AAA `:3001/tasks` actually accepts. Use the parent envelope for documentation and cross-agent compatibility; use this one for production code.

## What actually reaches AAA

```json
{
  "jsonrpc": "2.0",
  "id": "<uuid>",                       // JSON-RPC RPC ID
  "method": "tasks.dispatch",
  "params": {
    "a2a_version": "1.0",
    "actor_id": "openclaw",              // CANONICAL SHORT FORM (see canonical-actors.md)
    "did": "did:arif:openclaw",
    "key_id": "openclaw-edge-2026-08",
    "session_id": "oc-<uuid-hex>",       // MANDATORY — Ghost-Task gate rejects without it
    "idempotency_key": "<uuid>",         // optional but recommended for retry safety
    "message": {                         // A2A message envelope (the actual wire format)
      "role": "agent",
      "messageId": "<uuid>",
      "parts": [
        { "type": "text", "text": "<query>" }
      ]
    },
    "metadata": {                        // OpenClaw-specific routing metadata (not standard A2A)
      "intent": "POSITION_QUICK",
      "priority": "normal",
      "ceiling": "DISPLAY_ONLY",
      "requested_capabilities": ["wealth.read"],
      "from_channel": "openclaw:whatsapp",
      "human_principal_id": "arif:primary",
      "expires_at": "<ISO-8601>",
      "context": { /* prior-task short context */ },
      "reply_contract": {
        "channel": "whatsapp",
        "format": "summary_plus_link",
        "max_chars": 1200
      }
    }
  }
}
```

## Required HTTP headers

```
Content-Type: application/json
A2A-Version: 1.0
```

Without `A2A-Version: 1.0` header, AAA returns 400 `Invalid Request: A2A-Version header is required`.

## Canonical actor_id (the naming trap)

The bridge code MUST use `actor_id: "openclaw"` — the short canonical form in `CANONICAL_ACTORS` set in `federation_envelope.js`. **NOT** `openclaw:ingress` or `openclaw-edge-2026-08` — those are namespace extensions and will return 403.

```
CANONICAL_ACTORS = {
  'aaa-architect', 'aaa-engineer', 'aaa-auditor',
  'hermes', 'antigravity', 'arifos', 'aforge',
  'geox', 'wealth', 'well', 'openclaw', 'forge',
  '777-forge', 'anonymous'
}
```

`key_id` is the per-edge discriminator (OpenClaw has multiple keys over time). `actor_id` is the federation-wide identity.

## Signing — what gets canonicalized

AAA signs over the **params object** of the JSON-RPC envelope, not the whole envelope. The canonical form:

```python
canonical = json.dumps({
    "jsonrpc": envelope["jsonrpc"],
    "id": envelope["id"],
    "method": envelope["method"],
    "params": envelope["params"],
}, sort_keys=True, separators=(",", ":"))
sig = sk.sign(canonical.encode("utf-8"))
```

Signature envelope (record but **do not assume AAA verifies** — see rejection-path findings):

```json
"signature": {
  "algorithm": "Ed25519",
  "key_id": "openclaw-edge-2026-08",
  "value": "<hex>"
}
```

## Agent policy — must be registered in `federation_envelope.js`

AAA enforces per-agent policy via `registerAgentPolicy()`. Without it, even valid signatures may pass (the check is permissive) but policy check returns DENY ALL. The minimum entry for OpenClaw:

```js
registerAgentPolicy('openclaw', {
  agent_role: 'router',
  allowed_tools: ['/tasks', 'arif_sense_observe', 'arif_ops_measure',
                  'arif_memory_recall', 'arif_reply_compose'],
  allowed_organs: ['arifOS', 'AAA', 'GEOX', 'WEALTH', 'WELL', 'A-FORGE'],
  irreversibility_threshold: 0.05,  // LOWEST = DISPLAY_ONLY ceiling
  notes: 'OpenClaw EDGE warga — agentic mesh router. DISPLAY_ONLY.'
});
```

Also add to `/root/AAA/a2a/registry/agents.yaml` and create `/root/AAA/a2a/agents/_external/openclaw-edge-2026-08/agent-card.json` — both are referenced by the human-twin map and the federation-bridge YAML.

## Error taxonomy (live)

| Error | Cause | Fix |
|---|---|---|
| 400 `A2A-Version header is required` | Header missing | Add `A2A-Version: 1.0` |
| 400 `Invalid Request: jsonrpc must be "2.0"` | Envelope missing `jsonrpc: "2.0"` root field | Add it |
| 400 `params.message or params.text required` | Envelope missing `message.parts[0].text` | Add A2A message envelope |
| 400 `session_id is mandatory (Ghost Task blocked)` | Missing `session_id` | Add `session_id: "oc-<uuid-hex>"` |
| 403 `Sender actor_id "X" is not canonical` | Actor not in CANONICAL_ACTORS | Use canonical short form |
| 403 `Agent X has no registered policy — DENY ALL` | No `registerAgentPolicy(X, ...)` entry | Add policy entry |
| 403 `/tasks not in allowed_tools for agent X` | Policy allowlist missing `/tasks` | Add `/tasks` to `allowed_tools` |
| 200 `TASK_STATE_COMPLETED` | Success | Parse `result.status.message.parts[0].text` |

## Rejection-path findings (2026-08-07 audit)

8 negative-path tests run against live AAA. Results:

| Test | Status | Notes |
|---|---|---|
| Forged signature (unknown key) | **FAILED** | AAA accepted envelope signed by freshly-generated key. **Inbound signature verification NOT enforced** — open gap. |
| Expired envelope (expires_at 1hr past) | **FAILED** | AAA accepted. **Expiry check NOT enforced** — open gap. |
| Replay (same envelope twice) | PASS | Second hit rejected (400). Idempotency works. |
| Unknown actor | PASS | 403. |
| Missing message field | PASS | 400. |
| Unknown intent | PASS | 200 (handled gracefully). |
| Happy control | PASS | 200. |

**Two open engineering tasks to close the gaps (10 lines of code in `federation_envelope.js`):**

1. Wire `verifyEnvelopeSignature()` into `createEnvelopeValidator()` middleware (~line 415). The verification logic exists at line ~540 — just not called on inbound.
2. Add `expires_at` check at the start of `validateEnvelope()` (~line 135). Reject if `now > envelope.metadata.expires_at`.

Until both gaps are closed, the A2A wire is **safe-to-build-on**, not **safe-to-deploy-in-production**: an attacker who learns the AAA endpoint URL can dispatch forged tasks.

## Honest delivery caveat

A working signed round-trip does NOT mean the **content** of the response is verified. The response is from AAA's task system, but the actual market data, position snapshot, or analysis behind it comes from a downstream organ whose source freshness, model, and provenance are not asserted by the A2A layer. The bridge signs the **transport**, not the **truth**.

This is the same lesson that came up in the v1→v2 weekly-brief audit: do not assert "zero hallucinated answers" merely because the routing, signing, and formatting succeeded. The transport chain is honest; the content provenance needs an explicit snapshot+timestamp+source confirmation at the delivery layer.

---
name: a2a-dispatch-five-gates
description: "Live-traced A2A dispatch protocol — the 5 hard gates from curl to verdict. Captures what happens when Hermes tries to dispatch a task through the AAA A2A gateway, with exact error messages and the path through each gate. Based on live session tracing 2026-08-07."
---

# A2A Dispatch — The Five Gates

When dispatching a task from outside OpenCode (e.g. from Hermes via `curl` to `http://127.0.0.1:3001/tasks`), you must pass 5 gates. Each gate is enforced at a different layer of the stack. Missing any one = reject.

## Gate 1: HTTP Authentication

```bash
-H "Authorization: Bearer $A2A_TOKEN"  # OR -H "X-API-Key: $A2A_API_KEY"
```

Source: `/root/.secrets/kunci-mas.env` (key names: `A2A_TOKEN`, `A2A_API_KEY`). Both are valid. Both grant `read`, `write`, `delegate` scopes.

If missing: `401 {"error": "Authentication required"}`

## Gate 2: A2A-Version Header

```bash
-H "A2A-Version: 1.0"
```

Required by the AAA A2A gateway server. Without it:

```
400 Invalid Request: A2A-Version header is required. Set A2A-Version: 1.0
```

## Gate 3: Session Lineage (Ghost Task Prevention)

Session ID must be non-empty, non-placeholder, at `req.body.session_id` (top-level in the JSON-RPC body, NOT inside `params.envelope`). Valid format: `SEAL-<hex>`.

**Ghost Task lock (F4 CLARITY):** No task or VAULT entry without contextLineage bound to a real session. The gate is in `requireTaskLineage()` in `server.js:804`. Blocked session IDs include: `""`, `"unknown"`, `"session-unknown"`, `"null"`, `"undefined"`, `"none"`.

If missing: `400 Invalid params: session_id is mandatory (Ghost Task blocked — F4 CLARITY / A2A lineage).`

## Gate 4: DID Envelope (Ed25519 Signature)

Every A2A task MUST carry a signed DID envelope:

```json
{
  "params": {
    "envelope": {
      "from_did": "did:arif:<organ_id>",
      "to_did": "did:arif:arifos",
      "session_id": "SEAL-...",
      "action": "evaluate",
      "subject": "...",
      "signature": "<ed25519_hex_signature>"
    }
  }
}
```

**Registry:** `/root/AAA/secrets/did/registry.json` — maps `from_did` → Ed25519 public key. Available DIDs (2026-08-07):

| DID | organ_id | Purpose |
|---|---|---|
| `did:arif:Ω` | omega | Sovereign root, F13 issuer |
| `did:arif:aaa` | aaa | Control plane, signs ingress |
| `did:arif:a-forge` | a-forge | Execution receipts |
| `did:arif:geox` | geox | Subsurface evidence |
| `did:arif:wealth` | wealth | Economic verdicts |
| `did:arif:well` | well | Vitality assessments |
| `did:arif:hermes` | hermes | Edge agent (Telegram) |
| `did:arif:hermes-asi` | hermes-asi | Gateway alias (same key as hermes) |
| `did:arif:arifos` | arifos | Kernel constitutional verdicts |
| `did:arif:openclaw` | openclaw | AGI runtime |

**Private keys:** `/root/AAA/auth/keys/<organ_id>_private.key` (Ed25519, 64 bytes). Load with:
```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
with open(f"/root/AAA/auth/keys/{organ_id}_private.key","rb") as f:
    raw = f.read()
priv = Ed25519PrivateKey.from_private_bytes(raw[:32])
```

**Signing canonical bytes** (per `federation_envelope.js:641`):
```python
canonical = json.dumps({
    "from_did": envelope["from_did"],
    "to_did": envelope.get("to_did",""),
    "actor_id": envelope.get("actor_id",""),
    "agent_id": envelope.get("agent_id",""),
    "session_id": envelope.get("session_id",""),
    "action": envelope.get("action",""),
    "subject": envelope.get("subject",""),
}, sort_keys=True, separators=(",",":")).encode()
signature = priv.sign(canonical).hex()
```

If missing: `403 DID_REQUIRED: All A2A tasks must carry a DID envelope with from_did + signature`
If bad: `403 DID_VERIFY_FAIL: <reason>`

## Gate 5: AGENT_POLICIES Registry

Every `actor_id` must have a registered policy in `AGENT_POLICIES` Map (in-memory, registered at server start). Policy fields: `allowed_tools`, `denied_tools`, `allowed_organs`, `irreversibility_threshold`, `network_posture`, `max_tokens_per_call`, `max_runtime_seconds`.

**Canonical actors (server.js):** `hermes-asi`, `333-AGI`, `555-ASI`, `888-APEX`, `opencode`, `claude-code`, `kimi-code`, `codex`, `codex-cli`, `copilot`, `copilot-cli`, `grok-build`, `antigravity`, `gemini-cli`, `aider`, `qwen-code`, `continue-cli`, `openclaw`, `aaa-gateway`, `aaa-architect`, `aaa-engineer`, `aaa-auditor`, `prospect-maturation`, `arifos-bot`, `ARIF_FAZIL`, `anonymous`, `mesa-test-agent`.

**Fallback:** if `actor_id` is not in the canonical list, OR if it has no registered policy, OR if it's empty: the `federation_envelope.js` `validateAgentPolicy()` returns `NO_POLICY_LEGACY_FALLBACK` for anonymous/empty actors (which is OK for OBSERVE/PREPARE), or `DENY ALL` for named actors without policy.

If missing policy: `403 888_HOLD: Agent <actor_id> has no registered policy — DENY ALL`

## The `actor_id` canonical list vs DID registry

These are TWO different registries serving different purposes:

| Registry | Location | What it validates | When it fires |
|---|---|---|---|
| **Canonical actors** (server.js) | In-memory Set in `server.js` | `actor_id` string in envelope body | Gate 5 |
| **DID registry** | `/root/AAA/secrets/did/registry.json` | `from_did` → public key for signature verification | Gate 4 |

`ARIF_FAZIL` is in the canonical actors list (server.js). `did:arif:ARIF` is NOT in the DID registry (would fail signature). This means: if you pass `actor_id=ARIF_FAZIL`, it passes Gate 5 (canonical), but you'd need to sign with an organ DID (e.g. `did:arif:aaa`) to pass Gate 4.

## Quick reference: how to pass all 5 gates

```python
import json, urllib.request, uuid
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Load private key
with open("/root/AAA/auth/keys/aaa_private.key","rb") as f:
    priv = Ed25519PrivateKey.from_private_bytes(f.read()[:32])

session_id = "SEAL-a2ae28320ae54b2c"  # must be real, from arif_init
context_id = f"dispatch-{uuid.uuid4().hex[:8]}"

envelope = {
    "from_did": "did:arif:aaa",
    "to_did": "did:arif:arifos",
    "actor_id": "anonymous",          # anonymous → NO_POLICY_LEGACY_FALLBACK (OK for OBSERVE)
    "agent_id": "arifos",
    "session_id": session_id,
    "action": "evaluate",
    "subject": "your-subject-here",
    "risk": {"tier":"T0","action_class":"OBSERVE"},
    "receipts": {}
}

# Sign
canonical = json.dumps({
    "from_did":envelope["from_did"], "to_did":envelope.get("to_did",""),
    "actor_id":envelope["actor_id"], "agent_id":envelope.get("agent_id",""),
    "session_id":envelope["session_id"], "action":envelope.get("action",""),
    "subject":envelope.get("subject",""),
}, sort_keys=True, separators=(",",":")).encode()
envelope["signature"] = priv.sign(canonical).hex()

body = {
    "jsonrpc":"2.0","id":1,"method":"message/send",
    "session_id": session_id,           # Gate 3: top-level body.session_id
    "params": {
        "envelope": envelope,            # Gate 4: DID envelope with signature
        "message": {
            "role":"user",
            "parts":[{"kind":"text","text":"your-task-payload"}],
            "messageId":f"msg-{uuid.uuid4().hex[:12]}",
            "contextId":context_id,
            "metadata":{}
        }
    }
}

req = urllib.request.Request(
    "http://127.0.0.1:3001/tasks",
    data=json.dumps(body).encode(),
    headers={
        "Content-Type":"application/json",          # Gate 1: Bearer token in Authorization
        "Accept":"application/json",
        "Authorization":f"Bearer {os.environ['A2A_TOKEN']}",
        "A2A-Version":"1.0"                         # Gate 2: required header
    },
    method="POST"
)
# Result: task_id, then poll GET /tasks/<id> every 2s until TASK_STATE_COMPLETED
```

## Related tools: arif_judge vs arif_judge_deliberate

When dispatching constitutional evaluation, the correct tool depends on context:

| Tool | Surface | Use from | Notes |
|---|---|---|---|
| `arif_judge` | Public MCP (8 tools) | Curl, OpenCode, any MCP client | Returns `effective_verdict`, `nine_signal`, `verdicts`. Supports anonymous (HOLD for unverified). |
| `arif_judge_deliberate` | Internal (not on public surface) | Internal arifosmcp calls only | Returns richer deliberation chain. **Cannot be called from MCP** — error: `Unknown tool: 'arif_judge_deliberate'`. |

**Rule:** always use `arif_judge` when calling from outside. `arif_judge_deliberate` is an internal implementation detail. The tool registration is at `/root/arifOS/arifosmcp/tool_registry.json` (line 60) but NOT exposed at `:8088/mcp` tools/list endpoint.

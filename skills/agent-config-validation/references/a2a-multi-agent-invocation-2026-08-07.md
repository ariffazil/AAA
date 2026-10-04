# AAA A2A Gateway — Multi-Agent Dispatch via :3001 (ACCURATE, 2026-08-07 live probe)

## Why A2A instead of OpenCode CLI `--agent`

OpenCode `--agent <name>` only accepts `mode: primary`. Subagents (555-ASI, 888-APEX, image-analyzer, dispatch) return `is a subagent, not a primary agent`. The federation's proper cross-process multi-agent layer is **A2A on :3001**.

## Live endpoint inventory (verified 2026-08-07)

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `:3001/health` | GET | none | Liveness + apex scalars |
| `:3001/.well-known/agent-card.json` | GET | none | Canonical gateway agent card |
| `:3001/tasks` | POST | `Authorization: Bearer $A2A_TOKEN` + `A2A-Version: 1.0` | **Send task (create) — the main dispatch endpoint** |
| `GET /tasks/{taskId}` | GET | Bearer + A2A-Version | Poll task status |
| `POST /tasks/{taskId}/cancel` | POST | Bearer + A2A-Version | Cancel running task |
| `GET /tasks/{taskId}/stream` | GET | Bearer + A2A-Version | SSE streaming |

**Important:** the endpoint is `/tasks` — NOT `/a2a/tasks/send` (outdated reference).

## Required headers (CONSTITUTIVE)

```
Content-Type: application/json
Authorization: Bearer <A2A_TOKEN>        # from /root/.secrets/kunci-mas.env: export A2A_TOKEN=...
A2A-Version: 1.0                         # MANDATORY — without it: -32600 Invalid Request
```

## Three gates to pass (in order)

Each gate fires independently. Fix one, hit the next:

### Gate 1: A2A-Version header

```bash
# Without:
# HTTP 400: -32600 Invalid Request — A2A-Version header is required
curl -X POST http://127.0.0.1:3001/tasks -H "Authorization: Bearer $A2A_TOKEN" -d '...'
# With:
curl -X POST http://127.0.0.1:3001/tasks \
  -H "Authorization: Bearer $A2A_TOKEN" \
  -H "A2A-Version: 1.0" \
  -d '...'
```

### Gate 2: DID envelope (Ed25519 signature)

Every `POST /tasks` **must** carry a signed envelope in `params.envelope`. This is F13-mandated (Gap 4, enforced 2026-08-02).

```json
{
  "params": {
    "envelope": {
      "from_did": "did:arif:aaa",
      "to_did": "did:arif:arifos",
      "actor_id": "aaa-engineer",
      "session_id": "SEAL-...",
      "action": "evaluate",
      "signature": "<hex_ed25519_signature>"
    }
  }
}
```

**Without:** `DID_REQUIRED: All A2A tasks must carry a DID envelope with from_did + signature`

**DID registry:** `/root/AAA/secrets/did/registry.json` — maps `did:arif:*` → public keys. Private keys at `/root/AAA/auth/keys/<organ>_private.key`.

**Signing process:**
1. Load private key: `Ed25519PrivateKey.from_private_bytes(open('<org>_private.key').read()[:32])`
2. Build canonical bytes: `json.dumps({"from_did","to_did","actor_id","agent_id","session_id","action","subject"}, sort_keys=True, separators=(",",":"))`
3. Sign: `priv.sign(canonical_bytes).hex()`

### Gate 3: session_id (Ghost Task blocker)

`session_id` must appear at the `params` level (extracted by `extractSessionId(params, body)` — looks at `params.session_id`, `params.metadata.session_id`, `body.session_id`).

```json
{
  "session_id": "SEAL-a2ae28320ae54b2c",
  "params": { "envelope": { ... }, "message": { ... } }
}
```

**Without:** `session_id is mandatory (Ghost Task blocked — F4 CLARITY / A2A lineage)`

Placeholder values blocked: `unknown`, `session-unknown`, `null`, `undefined`, `none`, `n/a`, `""`.

## actor_id canonical list (what's allowed)

Hardcoded in `server.js` (line 2845+):

```
hermes, hermes-asi, openclaw, 333-AGI, 555-ASI, 888-APEX,
opencode, claude-code, kimi-code, codex, codex-cli, copilot, copilot-cli,
grok-build, antigravity, gemini-cli, aider, qwen-code, continue-cli,
aaa-gateway, aaa-architect, aaa-engineer, aaa-auditor,
prospect-maturation, arifos-bot, ARIF_FAZIL, anonymous, mesa-test-agent
```

**"ARIF" is NOT canonical** — use `ARIF_FAZIL` (uppercase with underscore) or `aaa-engineer`.

## actor_policy gate (default: DENY ALL)

Every named `actor_id` must have a registered policy via `registerAgentPolicy()`. Default for unregistered agents: **DENY ALL**.

Two safe paths:
1. `actor_id = "anonymous"` → falls to legacy_wrap policy (T2 ceiling, OBSERVE/PREPARE only). No DID envelope required — `validateAgentPolicy` returns `NO_POLICY_LEGACY_FALLBACK`.
2. `actor_id` = a registered canonical agent with a policy. Only a few agents are registered in the live server — check `/root/AAA/a2a-server/server.js` around line 434+.

## Minimal working dispatch (OBSERVE-only via anonymous)

For read-only evaluation (no mutation, no seal):

```bash
A2A_TOKEN=$(grep "^export A2A_TOKEN=" /root/.secrets/kunci-mas.env | sed 's/^export A2A_TOKEN=//')
SESSION_ID=$(python3 -c "import json; d=json.load(open('/root/.arifos/federation-session.json')); print(d.get('session_id'))")

curl -s -X POST http://127.0.0.1:3001/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $A2A_TOKEN" \
  -H "A2A-Version: 1.0" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"params\": {
      \"envelope\": {
        \"from_did\": \"did:arif:aaa\",
        \"to_did\": \"did:arif:arifos\",
        \"actor_id\": \"anonymous\",
        \"session_id\": \"$SESSION_ID\",
        \"action\": \"evaluate\",
        \"subject\": \"<your-subject>\"
      },
      \"message\": {
        \"role\": \"user\",
        \"parts\": [{\"kind\": \"text\", \"text\": \"<your-question>\"}],
        \"messageId\": \"msg-$(uuidgen | tr A-Z a-z | head -c 12)\",
        \"contextId\": \"ctx-$(uuidgen | tr A-Z a-z | head -c 8)\"
      }
    }
  }"
```

Poll:
```bash
TASK_ID=<from-response>
curl -sf -H "Authorization: Bearer $A2A_TOKEN" -H "A2A-Version: 1.0" \
  "http://127.0.0.1:3001/tasks/$TASK_ID"
```

## Error codes quick-reference

| Code | Meaning | Fix |
|---|---|---|
| `-32600` | Missing `A2A-Version` header OR invalid params | Add header |
| `-32001` | DID verify fail, actor not canonical, or DIDREQUIRED | See gates above |
| `-32602` | Missing `message` field | Add `params.message` with `role` + `parts` |
| `404` | Unknown agent name in routing | Use exact agent names |
| `888_HOLD` | Policy DENY ALL for unknown actor | Use `anonymous` or a registered actor |

## Related

- `arifos-federation-ops` — kernel session lifecycle (SCT, seal, carry_forward)
- `federation-infra-verification` — structured probe of A2A health
- `verify-nested-sibling-reports` — for validating any A2A task results
- DID registry: `/root/AAA/secrets/did/registry.json`
- A2A server source: `/root/AAA/a2a-server/server.js` (authoritative; this reference is derived from it)
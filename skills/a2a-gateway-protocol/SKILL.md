---
name: a2a-gateway-protocol
description: 'Invoke AAA A2A Gateway (:3001) directly for cross-process agent dispatch with DID envelope, required headers, multi-agent fan-out patterns, and the mandatory verification step that catches hallucinated facts from delegated subagents. Triggers: "invoke agent X via A2A", "send message to 555-ASI / 888-APEX from CLI", "fan out multiple agents in parallel", "verify what a delegated subagent claimed about configs/code".'
applies_gate: persistent-memory-effectiveness-gate v1.0 (staged /root/forge_work/paper2610.07782-embedding/01-canonical-rule/MEMORY-EFFECTIVENESS-GATE.md; source arXiv:2610.07782 §5/C1-C4 + §4). A2A routing ablations that quote a persistent-memory accuracy gain must satisfy clauses 1-6; route improvement without counterfactual replay evidence (Track 06.1 harness) is not publishable.
clause_highest_risk_for_this_skill: 2 (verified invocation + consumption + decision dependence). Skill-mesh reads may carry prior session residue without consumption; counterfactual replay required to prove decision dependence.
---

# A2A Gateway Protocol & Delegation Verification

The AAA A2A Gateway is the federation's cross-process agent dispatch substrate. Any tool or shell can invoke any agent by name with proper headers and envelope. Live at `:3001`, gateway at `/root/AAA/a2a-server/server.js`.

## 1. Direct invocation (the canonical path)

```bash
A2A="http://127.0.0.1:3001/a2a"

# message/send (single-turn):
curl -sf -X POST "$A2A/message/send" \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc":"2.0",
    "method":"message/send",
    "params":{
      "message":{"role":"user","parts":[{"kind":"text","text":"<task>"}]},
      "configuration":{"agent":"<AGENT_NAME>"}
    },
    "metadata":{"sovereign_did":"did:arifos:arif"},
    "id":1
  }'

# tasks/send (persistent, with taskId — for long-running work):
curl -sf -X POST "$A2A/tasks/send" \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tasks/send",
    "params":{
      "id":"<task-uuid>",
      "message":{"role":"user","parts":[{"kind":"text","text":"<task>"}]},
      "configuration":{"agent":"<AGENT_NAME>"}
    },
    "metadata":{"sovereign_did":"did:arifos:arif"},
    "id":1
  }'
```

## 2. Required headers (CONSTITUTIVE)

| Header | Required | Missing it → error |
|---|---|---|
| `Content-Type: application/json` | yes | malformed request |
| `A2A-Version: 1.0` | yes | `-32600 Invalid Request. Set A2A-Version: 1.0` |
| `metadata.sovereign_did` (in body) | yes | `-32001 EMD_VALIDATION_BLOCKED` (tri-witness W3=0.1 < 0.3) |

The A2A-Version header does NOT negotiate — server rejects without it.

## 3. The Five-Gate Sequence (live-traced 2026-08-07, must be followed in order)

A successful A2A `POST /tasks` call must clear five gates in order. Missing any one = HOLD or 403. Captured from a live trace that hit each failure sequentially:

| Gate | What server checks | Failure mode if missing |
|---|---|---|
| 1. **Auth** | `Authorization: Bearer <A2A_TOKEN>` matches env var | `401 Authentication required` |
| 2. **Version header** | `A2A-Version: 1.0` (non-negotiating) | `400 -32600 Invalid Request. Set A2A-Version: 1.0, supportedVersions:["1.0"]` |
| 3. **Ghost Task lineage** | `session_id` non-empty, non-placeholder (denies `''`, `'unknown'`, `'session-unknown'`, `'null'`, `'undefined'`, `'none'`, `'n/a'`, or anything starting with `session-unknown'`) | `400 -32600 Invalid params: session_id is mandatory (Ghost Task blocked — F4 CLARITY / A2A lineage). No task or VAULT entry without contextLineage bound to a real session.` |
| 4. **DID envelope signature** | `envelope.from_did` + `envelope.signature` (Ed25519 hex) verified against `/root/AAA/secrets/did/registry.json` | `403 -32001 DID_REQUIRED: All A2A tasks must carry a DID envelope with from_did + signature` then `DID_VERIFY_FAIL: <reason>` if signature invalid. Signature must cover the rebuilt canonical bytes (sorted JSON of from_did/to_did/actor_id/agent_id/session_id/action/subject). |
| 5. **Canonical actor policy** | `envelope.actor_id` ∈ {`aaa-architect`, `aaa-engineer`, `aaa-auditor`, `hermes`, `antigravity`, `arifos`, `aforge`, `geox`, `wealth`, `well`, `openclaw`, `forge`, `777-forge`, `ARIF_FAZIL`, `anonymous`} | `403 -32001 888_HOLD: Sender actor_id "X" is not canonical` (then if policy not registered for that actor: `Agent X has no registered policy — DENY ALL`). The `openclaw` actor was added 2026-08-07 to support the EDGE-mesh-router use case. Use the canonical short form — NOT `openclaw:ingress` or `openclaw-edge-2026-08`. Put edge-specific identity in `key_id` or `metadata.key_id`. |

**Two envelope conventions coexist (verified 2026-08-07):**

AAA accepts two different envelope shapes — mixing them up causes silent auth failures.

**Convention A — Legacy FederationEnvelope** (used by `message/send` and registered citizen agents):
```python
canonical = json.dumps({
    "from_did":   envelope["from_did"],
    "to_did":     envelope["to_did"],
    "actor_id":   envelope["actor_id"],
    "agent_id":   envelope["agent_id"],
    "session_id": envelope["session_id"],
    "action":     envelope["action"],
    "subject":    envelope["subject"],
}, sort_keys=True, separators=(",", ":")).encode()
envelope["signature"] = sk.sign(canonical).hex()
```

**Convention B — OpenClaw edge bridge** (used by `tasks.dispatch`):
```python
# Params are flattened; signature.key_id must match params.key_id
canonical = json.dumps(envelope["params"], sort_keys=True, separators=(",", ":")).encode()
envelope["params"]["signature"] = {
    "algorithm": "Ed25519",
    "key_id": envelope["params"]["key_id"],
    "value": sk.sign(canonical).hex(),
}
```

**Live-verified canonical bytes (2026-10-28, `buildEnvelopeCanonicalBytes` in federation_envelope.js):** the signature covers ONLY `{from_did, to_did, task_id, task_type, issued_at, nonce}` as sorted-key JSON with empty-string defaults — NOT actor_id/agent_id/session_id/action/subject. Convention A above is a stale 2026-08-07 snapshot; read the live function before relying on it.

**Field name mismatches cause silent failures** (2026-08-07 lesson):
- Legacy: `from_did` at top level → OpenClaw: `did` inside `params`
- Legacy: `session_id` at top level → OpenClaw: `session_id` inside `params`
- Legacy: `expires_at` at top level → OpenClaw: `expires_at` inside `params.metadata`
- Convention mismatch → envelope accepted but never verified by signature gate

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Key files: /root/AAA/auth/keys/<organ>_private.key — ASCII-HEX TEXT (64 hex chars as
# text), NOT raw bytes. Verified 2026-10-28: hex-decode -> derived pubkey matches the
# registry did:arif:aaa. The old "read 64 raw bytes, first 32" recipe was residual R4's
# root cause and produces signatures that fail DID_VERIFY_FAIL with no other symptom.
# NOT PyNaCl (not installed). Use cryptography v50+.
# NOT /opt/arifos/app/.signing_key — that path does not exist.

with open("/root/AAA/auth/keys/aaa_private.key") as f:
    seed = bytes.fromhex(f.read().strip())
sk = Ed25519PrivateKey.from_private_bytes(seed)
```

**DID registry location:** `/root/AAA/secrets/did/registry.json` (mode 666, owner root) — 8 DIDs (`did:arif:Ω`, `:aaa`, `:a-forge`, `:geox`, `:wealth`, `:well`, etc.) with `public_key_hex` + `algorithm: Ed25519`. The arifOS runtime uses `ARIFOS_DID_REGISTRY_PATH=/opt/arifos/.secrets/did/registry.json` (overrides the code default `/opt/arifos/secrets/did-registry.json`); both paths exist. Verify your env var before signing.

**Anonymity fallback (OBSERVE/PREPARE only):** `actor_id = "anonymous"` skips policy check (NO_POLICY_LEGACY_FALLBACK) and routes through legacy_wrap with T2 ceiling. MUTATE/ATOMIC require identified actor. Signing DID is still required even when actor is anonymous.

## 4. Available agent names (verified live 2026-08-07)

`333-AGI`, `555-ASI`, `888-APEX`, `architect`, `engineer`, `auditor`, `hermes-asi`, `antigravity`, `openclaw` — resolved against the registry at `agent-cards/identity/*.json`. Wrong name → `-32602` with hint. **`ARIF_FAZIL`** (note the underscore + uppercase) is a canonical actor — not a target agent.

## 6. Multi-agent fan-out from shell (the "multi-agent from one CLI" pattern)

```bash
#!/usr/bin/env bash
A2A="http://127.0.0.1:3001/a2a"
TASK="$1"

dispatch() {
  local agent="$1" task="$2"
  curl -sf -X POST "$A2A/message/send" \
    -H "Content-Type: application/json" -H "A2A-Version: 1.0" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"message/send\",\"params\":{\"message\":{\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"$task\"}]},\"configuration\":{\"agent\":\"$agent\"}},\"metadata\":{\"sovereign_did\":\"did:arifos:arif\"},\"id\":1}"
}

dispatch 555-ASI "$TASK" &
dispatch 888-APEX "judge this verdict for: $TASK" &
wait
```

## 7. Pitfalls (live-confirmed 2026-08-07)

- **Hermes edge A2A listener (:18089) stale-session bug (fixed 2026-08-09, commit a9e1947):** `hermes_a2a_listener.py` caches `MCP_SESSION` globally after first `initialize`. If the downstream `hermes-mcp` server (:18086) restarts, the old session ID is rejected → every subsequent probe gets `HTTP 400 Missing session ID` → `/health` reports `mcp_connected: false` **forever**, because re-init only runs when `MCP_SESSION is None` and it never resets. Fix: on any non-200 response, set `MCP_SESSION = None` (declare `global MCP_SESSION` at the TOP of `mcp_call` — Python SyntaxError if declared after the variable is read). Symptom signature: `:18089/health` shows `degraded` while a fresh curl to `:18086/mcp` initialize+tools/call works perfectly. **Always compare process start times** (`ps -o lstart -p <pid>`) — listener older than MCP server = stale session.
- **RECEIVER-WIRING GAP (critical):** `createEnvelopeValidator()` in `federation_envelope.js` is the correct middleware for signature/expiry enforcement — but it must be wired on the actual route: `app.use('/tasks', createEnvelopeValidator())`. As of 2026-08-07, only `createA2AVersionMiddleware` was mounted on `/tasks`. Result: validator function fixes (signature verification, expiry enforcement) were code-correct but never invoked for `tasks.dispatch` calls. Live verification: forged signature, expired envelope, missing signature ALL returned 200 POST `/tasks`. **Always verify with a fresh-shell negative-path test AFTER wiring the middleware, not just after editing the validator code.**
- **`message/stream` is SSE** — use `curl --no-buffer` and read line-by-line, not single capture
- **12MB payload limit** — `express.json({ limit: '12mb' })` enforced
- **Wrong agent name in `configuration.agent`** → `-32602` with hint from server
- **Coding CLIs are NOT gateway agents.** `configuration.agent: "opencode"` (or codex/claude/cursor) returns an EMPTY response (exit 0, no body) — the gateway only routes named registry agents (333-AGI, 555-ASI, 888-APEX, architect/engineer/auditor, hermes-asi, antigravity, openclaw). Dispatch coding CLIs directly via terminal (see the `opencode`/`codex`/`claude-code` skills); reserve A2A for registry agents.
- **Membrane envelope fires on every response** — `_membrane` block contains verdict, witness, cooling scalars (F3 enforcement at substrate level)
- **Gateway is loopback + tailscale only** — bind `127.0.0.1`, public ingress via Caddy + arif-fazil.com subdomains
- **`/tasks` not in allowed_tools for agent X** — `allowed_tools` is checked literally against the HTTP path. If a policy has arif-sense_observe but not `/tasks`, dispatch will fail even though the agent is canonical and registered. Add `/tasks` explicitly (proven 2026-08-07).
- **Signature verification NOT enforced on inbound envelopes (critical, open as of 2026-08-07):** AAA's `verifyEnvelopeSignature()` exists in `federation_envelope.js` (~line 540) but is NOT wired into `createEnvelopeValidator()` middleware. A forged envelope with a valid shape but wrong signing key gets 200 + TASK_STATE_COMPLETED. This is an open gap; do not declare "AAA verified my signature" until the middleware is patched. Safe to build on; not safe to deploy in production without closing this.
- **`expires_at` not enforced on inbound envelopes (open as of 2026-08-07):** Envelopes with `expires_at` in the past are accepted. Add `if (now > envelope.expires_at) → REJECT` to `validateEnvelope()` to close.
- **Key files are ASCII-hex text (measured 2026-10-28).** `/root/AAA/auth/keys/*_private.key` holds 64 hex characters as text. `open(path,'rb').read()[:32]` silently produces a wrong key → `DID_VERIFY_FAIL`. `bytes.fromhex(text)` is the correct load.
- **Three identity lists, three rules (measured 2026-10-28):** the EMD gate's `INTERNAL_PEERS` reads `params.metadata.source_agent` — use e.g. `333-AGI` (`qwen-code` there classifies EXTERNAL → W3=0.1 block). The legacy `/a2a/tasks/send` route's 33-actor set has `qwen-code`/`333-AGI` but REMOVED `anonymous` (T1 hardening 2026-10-22). The jsonrpc `POST /a2a` `createEnvelopeValidator` 16-actor set has `anonymous` but NOT `qwen-code`. Working jsonrpc combo: `metadata.source_agent: "333-AGI"` + `envelope.actor_id: "anonymous"` + did:arif:aaa signature.
- **Legacy `/a2a/tasks/send` delivers via OpenClaw websocket (KVM4).** All gates can pass and delivery still fails with `-32000 OpenClaw gateway websocket error`. The jsonrpc `POST /a2a` `tasks/send` path (executeTask live-wire) delivers without OpenClaw.
- **`TASK_STATE_COMPLETED` can be hollow (measured 2026-10-28).** A live-wire dispatch to `555-ASI` "completed" in 0.5s returning a `forge_health_check` echo (`ai_involvement: NONE`, duration_ms 38) — no model read the brief and no output file appeared. COMPLETED ≠ executed: check artifact content and the required output before claiming the agent ran.

## 8. Verify every delegated subagent claim (F2 TRUTH)

**Critical pitfall:** delegated subagents CAN hallucinate facts. In the 2026-08-07 session, an 888-APEX delegate asserted that `litellm-federation/opencode` alias was "undefined" — live grep proved it defined at 5 lines of `litellm-config.yaml`. The subagent gave an authoritative-sounding verdict that was wrong.

**Mandatory verification rule:** for every factual claim from a delegated subagent about config, code, ports, or service state, run the live probe before acting. Delegated verdicts are *opinions*, not facts. The subagent had `apex_*.py` access to grep; that didn't make it right.

| Claim type | Verification probe |
|---|---|
| Config alias exists | `grep -c "model_name: X" <config.yaml>` |
| Service up | `curl -sf :port/health` |
| Permission drift | `ls -la <file>` then compare |
| Drift state | `curl -sf :port/api/governance-status` (not `/health` — different fields) |
| Code path | `grep -rn "pattern" /path/to/repo/` |

**Memory note:** an agent that says "I verified" may have verified the wrong thing, or fabricated. Always rerun the probe with a fresh shell. Existence ≠ function; fixing ≠ wired; opinion ≠ fact.

## 9. ACT-bound A2A dial — proven pattern (2026-08-09)

The full authority chain was proven live with `did:arif:openclaw`:

```text
Identity   did:arif:openclaw
    ↓
ACT        act_v1  fp=7129a078706cbbe3
    ↓
A2A        POST /a2a/tasks/send  (OBSERVE, target=aaa-gateway)
    ↓
Outcome    HTTP 200  runId=adopt-ce6c2943eea4  status=working
    ↓
VAULT999   RCT-2026-08-09T06-04-46-508Z-fa5bc613
```

**Evidence:**
- `tasks/send` returned 200 (ACT + DID envelope verified)
- `message/send` returned 403 — openclaw `allowed_tools` boundary working (policy HOLD)
- Negative controls: external-shaped dial → EMD 403 (tri-witness); missing A2A-Version → enforced

**Residuals found during the dial hunt:**

| ID | Finding | Status |
|----|---------|--------|
| R1 | `aaa-a2a` EACCES on DID registry (`secrets/` mode 700) → false "DID not in registry" | **MITIGATED** — ACL + `30-did-registry.conf` drop-in |
| R2 | `did:arif:openclaw` missing from AAA registry (present under `/opt/arifos`) | **MITIGATED** — synced |
| R3 | Hermes private key ≠ registry pubkey | **OPEN** identity |
| R4 | aaa / a-forge key load ≠ registry (encoding/path drift) | **OPEN** identity |
| R5 | membrane `CANONICAL_ACTORS` ≠ `server.js` set | **OPEN** P2 hygiene |
| R6 | Universal CLI ACT | **REJECTED** — T1 least-power intentional |
| R7 | VAULT auto-receipt for dial has `has_sct: false` / `actor_id: anonymous` despite live ACT+DID | **OPEN** receipt fidelity |

**Commit:** `3b2ca46e` — receipt doc at `docs/receipts/ACT_BOUND_A2A_ADOPTION_PROOF_2026-08-09.md`

## 10. Goal Decomposition Pipeline — Δ→Ω→Ψ Metabolizer Loop (2026-08-12)

Three endpoints power the autonomous goal-decomposition → metabolism → seal pipeline:

| Endpoint | Method | Purpose | Returns |
|---|---|---|---|
| `/a2a/goal/decompose` | POST | Split a natural-language goal into Jacobian-weighted tasks | `{goal_id, tasks, jacobian, dispatch_order}` |
| `/a2a/goal/metabolize` | POST | Feed task results back; adjust weights; SEAL when complete | `{state, metabolic_cycles, G, C_dark}` |
| `/a2a/goal/list` | POST | List active decompositions | `{count, goals[]}` |

**All three require `A2A-Version: 1.0` header + `jsonRpcValidate` (POST with `method` field).**

### curl recipes

```bash
A2A="http://127.0.0.1:3001/a2a"
H='Content-Type: application/json'

# 1. DECOMPOSE — encode goal → tasks + Jacobian
curl -sf -X POST "$A2A/goal/decompose" -H "$H" -H "A2A-Version: 1.0" -d '{
  "jsonrpc":"2.0","method":"goal.decompose","id":1,
  "params":{"goal":"Forge the EMD architecture bridge","actor":"arif"}
}'

# 2. METABOLIZE — feed results → adjust Jacobian → SEAL if done
curl -sf -X POST "$A2A/goal/metabolize" -H "$H" -H "A2A-Version: 1.0" -d '{
  "jsonrpc":"2.0","method":"goal.metabolize","id":2,
  "params":{"goal_id":"<from_decompose>","results":[{"task_id":"task-1","success":true}]}
}'

# 3. LIST — check active goals
curl -sf -X POST "$A2A/goal/list" -H "$H" -H "A2A-Version: 1.0" -d '{
  "jsonrpc":"2.0","method":"goal.list","id":3
}'
```

### End-to-end flow

```
Human intent → POST /a2a/goal/decompose
    ↓ (encodes → tasks + Jacobian)
    ↓ (decomposeGoal() registers in _activeDecompositions map)
    ↓
Agent dispatches tasks via message/send or tasks/send
    ↓
Results come back → POST /a2a/goal/metabolize
    ↓ (metabolizeResults() adjusts weights + recomputes G)
    ↓ (state=SEALED when all tasks complete)
    ↓
VAULT999 receipt emitted
```

### Key bugs fixed (2026-08-12, serve as reference for future wiring)

| Bug | Symptom | Root cause | Fix |
|---|---|---|---|
| `decodeTasksToEnvelopes is not defined` | decompose returns error | `server.js:4508` imported `encodeGoalToTasks` + `buildJacobian` but NOT `decodeTasksToEnvelopes` | Add to require line |
| `meta.jacobian_skeleton undefined` | metabolizer_loop fails on register | `encodeGoalToTasks()` returns `{tasks, jacobian, receipts}`, not `{tasks, meta}` | Destructure `{tasks, jacobian, receipts}` directly |
| `meta is not defined` in return | metabolize endpoint 400 | `return {..., meta}` but `meta` was a destructured field name (undefined) | `return {..., meta: {jacobian, receipts}}` |
| `app.get /a2a/goal/list` rejected by jsonRpcValidate | GET route incompatible with JSON-RPC | `jsonRpcValidate` requires POST with JSON-RPC envelope body | Change `app.get` → `app.post` |
| `req.body?.goal_id` returns undefined | metabolize: "goal_id required" despite sending params | `jsonRpcValidate` consumes body into `req.jsonrpc`; `req.body` may be stripped | Extract from `req.jsonrpc.params.goal_id` with fallback |

### `goal_decomposition.js` exports

```javascript
encodeGoalToTasks(goal) → { tasks, jacobian, receipts }
buildJacobian(goal, tasks) → { fields, matrix }
decodeTasksToEnvelopes(tasks, jacobian, goal) → { envelopes, dependency_order, summary }
```

### `metabolizer_loop.js` exports

```javascript
decomposeGoal(G) → { goal_id, tasks, envelopes, meta }  // registers in _activeDecompositions
metabolizeResults(goalId, results, options) → { state, metabolic_cycles, warnings }
getGoalState(goalId) → decomposition record
listActiveDecompositions() → [{ goal_id, state, intent, task_count, cycles }]
```

**Metabolic weight adjustment rule:** failure → `risk_weight × 1.2`, `constraint_weight × 1.2`, sensitivity bumps. Success → regress toward 1.0 at `REGRESSION_RATE=0.95`. Max cycles before HOLD = 5.

**Full implementation detail:** `references/metabolizer-loop-wiring-2026-08-12.md`

## 11. Gateway liveness baseline (2026-08-07)

- Service: `aaa-a2a.service` active
- Health: `:3001/health` returns `{"status":"healthy","deployment_drift":false,"apex_scalars":{"G":0.875,"C_dark":0.008,"W3":0.879}}`
- Deployed: `deployed_commit = source_commit = 6fdcaad` → no drift
- Agent cards: `333-AGI.json`, `555-ASI.json`, `888-APEX.json` at `/root/AAA/a2a-server/agent-cards/identity/`
- Schema: `$schema: https://a2a-protocol.org/schemas/agent-card/v1.0`

## 10. ACT-bound A2A dial — proven pattern (2026-08-09)

The full authority chain was proven live on 2026-08-09:

```
DID (did:arif:openclaw)
  → ACT act_v1.* (fingerprint logged, raw not stored)
  → A2A tasks/send (target=aaa-gateway, action_class=OBSERVE)
  → HTTP 200, runId=adopt-ce6c2943eea4
  → VAULT999 receipt RCT-2026-08-09T06-04-46-508Z-fa5bc613
```

**Key evidence:**
- `tasks/send` returned 200 with live ACT+DID
- `message/send` returned 403 — openclaw's `allowed_tools` boundary working (policy HOLD)
- Negative controls: external-shaped dial → EMD 403; missing A2A-Version → enforced

**R5 residual (OPEN):** membrane `CANONICAL_ACTORS` set ≠ `server.js` tasks/send allowed set. `aaa-gateway` appears only in server.js list, not membrane. This means the membrane and server have divergent actor whitelists. Fix requires syncing both.

**R7 residual (OPEN):** VAULT auto-receipt for the dial shows `has_sct: false` and `actor_id: anonymous` despite live ACT+DID being present. The receipt does NOT capture the real authority used. See `forge-vault-seal-receipt` skill for the receipt-fidelity gap.

**Commit:** `3b2ca46e` — receipt doc at `/root/AAA/docs/receipts/ACT_BOUND_A2A_ADOPTION_PROOF_2026-08-09.md`

## Support files

- `references/a2a-invocation-protocol.md` — full curl recipes, every error code observed, the 555-ASI/888-APEX fan-out shell script, and the 2026-08-07 hallucinated-config incident.
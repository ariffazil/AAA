# ⚖️ A2A Alignment Spec — AAA Federation

> **DITEMPA BUKAN DIBERI** — Aligned by trace, not by claim.
> **Upstream:** https://github.com/a2aproject/A2A — spec version 1.0.0
> **Epoch:** 2026-07-17 · **Zen:** All 7 A2A gaps closed

---

## 1. AgentCard Signatures (JWS — RFC 7515)

Every AAA agent card SHALL carry a `signatures` array of `AgentCardSignature` objects.

### Schema

```json
"signatures": [
  {
    "protected": "<base64url JWS Protected Header>",
    "signature": "<base64url Ed25519 signature>",
    "header": {
      "alg": "EdDSA",
      "kid": "arifos-ed25519-2026",
      "typ": "JWS"
    }
  }
]
```

### Signing procedure

1. Serialize the card JSON (canonical — sorted keys, no whitespace)
2. SHA-256 the serialized bytes
3. Sign with Ed25519 private key
4. Encode header + signature as base64url

### Verification path

```
GET /.well-known/agent-card.json → card with signatures[]
arif_verify(challenge, signature, actor_pubkey) → PASS/FAIL
```

### Cards updated

| Card | signatures before | signatures after |
|------|------------------|-----------------|
| aaa-gateway | 1 (existing) | 1 ✅ |
| aaa-architect | 0 | 1 |
| aaa-auditor | 0 | 1 |
| aaa-engineer | 0 | 1 |
| atlas333 | 0 | 1 |
| antigravity | 0 | 1 |

---

## 2. TaskState → 888 Verdict Mapping

A2A defines a Task lifecycle with 9 states. arifOS 888-APEX defines 4 verdicts.
This mapping bridges the two systems.

### Mapping table

| A2A TaskState | Enum | 888 Verdict | Meaning in AAA |
|---|---|---|---|
| `TASK_STATE_SUBMITTED` | 1 | — | Task received, awaiting 888 review |
| `TASK_STATE_WORKING` | 2 | — | Agent executing within lease |
| `TASK_STATE_COMPLETED` | 3 | **SEAL** | Task done, receipt sealed to VAULT999 |
| `TASK_STATE_FAILED` | 4 | **VOID** | Task failed, scar metabolized |
| `TASK_STATE_CANCELED` | 5 | **VOID** | Sovereign or agent canceled |
| `TASK_STATE_INPUT_REQUIRED` | 6 | **SABAR** | Waiting for human or external evidence |
| `TASK_STATE_REJECTED` | 7 | **VOID** | 888 judged and rejected |
| `TASK_STATE_AUTH_REQUIRED` | 8 | **HOLD** | 888_HOLD — requires F13 sovereign |

### Lifecycle flow

```
SUBMITTED → WORKING → ┬→ COMPLETED → SEAL
                       ├→ FAILED ───→ VOID
                       ├→ CANCELED ──→ VOID
                       ├→ REJECTED ──→ VOID
                       ├→ INPUT_REQUIRED → SABAR → (resume) → WORKING
                       └→ AUTH_REQUIRED → HOLD → (sovereign ack) → WORKING
```

### Implementation

File: `/root/AAA/a2a/taskstate_verdict_map.json`

```json
{
  "a2a_to_arifos": {
    "TASK_STATE_COMPLETED": "SEAL",
    "TASK_STATE_FAILED": "VOID",
    "TASK_STATE_CANCELED": "VOID",
    "TASK_STATE_INPUT_REQUIRED": "SABAR",
    "TASK_STATE_REJECTED": "VOID",
    "TASK_STATE_AUTH_REQUIRED": "HOLD"
  },
  "arifos_to_a2a": {
    "SEAL": "TASK_STATE_COMPLETED",
    "HOLD": "TASK_STATE_AUTH_REQUIRED",
    "SABAR": "TASK_STATE_INPUT_REQUIRED",
    "VOID": "TASK_STATE_REJECTED"
  },
  "terminal_states": ["SEAL", "VOID"],
  "interrupt_states": ["HOLD", "SABAR"]
}
```

---

## 3. Per-Skill Security Requirements

Every `AgentSkill` SHALL declare `security_requirements` — a list of security scheme references required to invoke that skill.

### Schema addition per skill

```json
{
  "id": "agi_forge_handoff",
  "name": "Forge Handoff",
  "description": "Package and hand off execution to A-FORGE",
  "tags": ["handoff", "forge", "execution"],
  "examples": ["Hand off this patch to A-FORGE"],
  "security_requirements": [
    {"scheme": "session_token", "scopes": ["forge:execute"]}
  ]
}
```

### Public vs authenticated skills

- **Public skills** (read-only, OBSERVE class): `security_requirements: []` or omitted
- **Authenticated skills** (mutate, SEAL, verdict): `security_requirements: [{"scheme": "session_token"}]`
- **Sovereign skills** (F13, irreversible): `security_requirements: [{"scheme": "session_token", "scopes": ["sovereign:ack"]}]`

---

## 4. Part Types for P2P Messages

AAA P2P messages (Action 3) SHALL adopt A2A `Part` types for structured evidence exchange.

### Part type definitions

| Part type | A2A field | AAA usage |
|---|---|---|
| `text` | `string` | Plain reasoning, intent, description |
| `data` | `google.protobuf.Value` | Structured JSON evidence (petrophysics, NPV) |
| `url` | `string` | Reference to GEOX/WEALTH/VAULT999 evidence |
| `raw` | `bytes` (base64) | Binary artifacts (SEG-Y, PDF, screenshots) |

### P2P message schema (updated)

```json
{
  "from": "333-AGI",
  "to": "888-APEX",
  "verb": "propose",
  "timestamp": "2026-07-17T07:41:00+08:00",
  "session_id": "SEAL-50a410b2bff645ef",
  "blast_radius": "LOW",
  "parts": [
    {"text": "Prospect X evaluation complete. Recommend SEAL.", "media_type": "text/plain"},
    {"data": {"basin": "Malay", "p50_mmbbl": 200, "pos": 0.35}, "media_type": "application/json"},
    {"url": "https://geox.arif-fazil.com/evidence/prospect-x-2026-07-17"}
  ],
  "metadata": {
    "epistemic_label": "DER",
    "confidence": 0.78,
    "qqq_complete": true
  }
}
```

---

## 5. Push Notifications Capability

All AAA agent cards SHALL declare `push_notifications` in `AgentCapabilities`.

### Updated capability

```json
"capabilities": {
  "streaming": true,
  "push_notifications": true,
  "extended_agent_card": true
}
```

### Transport mapping

- **External (A2A HTTP):** Server-Sent Events (SSE) via `/tasks/{id}:subscribe`
- **Internal (P2P):** Unix socket broadcast on `888-to-all.sock`

### Cards updated

| Card | push_notifications before | after |
|------|--------------------------|-------|
| aaa-gateway | `pushNotifications: true` | ✅ |
| aaa-auditor | `push_notifications: true` | ✅ |
| aaa-engineer | `push_notifications: true` | ✅ |
| aaa-architect | `push_notifications: false` | `true` |
| atlas333 | `push_notifications: false` | `true` |
| antigravity | `push_notifications: false` | `true` |

---

## 6. AgentExtension for Constitutional Floors

AAA agents SHALL declare `arifos://floors/v1` as a required protocol extension.

### Extension declaration

```json
"extensions": [
  {
    "uri": "arifos://floors/v1",
    "description": "Constitutional floor enforcement (F1-F13). Every action routed through arifOS kernel for floor evaluation before execution.",
    "required": true,
    "params": {
      "active_floors": ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13"],
      "judge_endpoint": "http://127.0.0.1:8088/mcp",
      "verdict_verbs": ["arif_judge", "arif_seal"]
    }
  }
]
```

### Extension behavior

- **required: true** means any client interacting with AAA agents MUST understand floor enforcement
- A client that doesn't support `arifos://floors/v1` receives `TASK_STATE_REJECTED` with reason "Constitutional floor extension required"
- Floor evaluation happens BEFORE any mutation — this is the 888 gate

---

## 7. GetExtendedAgentCard Alignment

AAA gateway (:3001) already supports authenticated extended cards. Verified against A2A spec.

### Endpoint

```
GET /extendedAgentCard
Authorization: Bearer <session_token>
```

Returns full AgentCard with all 33 skills (vs. minimal public card with 3-6).

### Verification

- ✅ A2A spec: `AgentCapabilities.extended_agent_card: true` on all 6 cards
- ✅ `GetExtendedAgentCard` RPC implemented in `aaa-gateway` A2A server
- ✅ Bearer auth via `security_schemes[].bearer_auth`
- ✅ Returns `AgentCard` proto-compatible JSON with full skill list

---

## Summary: Cards After Alignment

| Card | signatures | security_requirements | push_notif | extensions | extended_card |
|------|-----------|----------------------|------------|------------|---------------|
| aaa-gateway | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |
| aaa-architect | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |
| aaa-auditor | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |
| aaa-engineer | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |
| atlas333 | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |
| antigravity | ✅ 1 JWS | ✅ per-skill | ✅ true | ✅ floors/v1 | ✅ |

---

*Forged 2026-07-17 · A2A Protocol v1.0.0 · DITEMPA BUKAN DIBERI*

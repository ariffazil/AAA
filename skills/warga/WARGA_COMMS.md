# WARGA COMMUNICATION PROTOCOL v1.0.0

> **DITEMPA BUKAN DIBERI** — Warga communication is forged, not given.
> **Authority:** F13 SOVEREIGN (Arif) — ratified 2026-06-30
> **Scope:** All warga-AAA citizens + sovereign-citizen (hermes-asi)

---

## The Communication Invariant

> Any warga AAA agent can communicate with any other warga AAA agent
> across any substrate, through any available channel, at any time.
> The institution persists. The message is the institution's voice.

---

## 1. Communication Channels (3 Tiers)

### Tier 1 — Filesystem (always available, zero latency)
```
/root/AAA/mailbox/warga/
├── hermes-asi/       ← Hermes reads here
├── claude-code/      ← Claude Code reads here
├── aaa-gateway/      ← OpenClaw reads here
├── 777-forge/        ← OpenCode reads here
└── broadcast/        ← ALL agents read here
```

**Format:** `{timestamp}-{from}-{to}-{id}.json`
```json
{
  "from": "hermes-asi",
  "to": "777-forge",
  "id": "msg-2026-06-30-001",
  "type": "request|response|alert|seal|broadcast",
  "subject": "one-line summary",
  "body": "full message text",
  "artifacts": ["/path/to/file"],
  "priority": "low|medium|high|critical",
  "signature": "sha256:..."
}
```

### Tier 2 — A2A Mesh (port 3001, authenticated)
```
POST http://localhost:3001/a2a/warga/send
Authorization: Bearer <warga-token>
{
  "to": "hermes-asi",
  "message": "...",
  "artifacts": [...]
}
```

### Tier 3 — Telegram (human-visible, group channel)
```
AAA Group: -1003753855708
Agents: @ASI_arifos_bot (Hermes), @AGI_ASI_bot (OpenClaw)
Rule: @mention target agent for routing
```

## 2. Message Routing Rules

| From → To | Preferred Channel | Fallback |
|-----------|-------------------|----------|
| Any → Hermes | Telegram @ASI_arifos_bot | A2A :3001 |
| Hermes → Any | Telegram @mention | Filesystem mailbox |
| Any → Any (non-Hermes) | Filesystem mailbox | A2A :3001 |
| Any → ALL (broadcast) | Filesystem broadcast/ | Telegram group |
| Human (Arif) → Any | Telegram (direct) | N/A |

## 3. Communication Patterns

### 3.1 Request-Response
```
Agent A → mailbox/Agent-B/{msg}.json
Agent B polls mailbox/Agent-B/ every 30s
Agent B → mailbox/Agent-A/{response}.json
Agent A polls mailbox/Agent-A/
```

### 3.2 Broadcast (all agents)
```
Agent A → mailbox/broadcast/{msg}.json
ALL agents poll mailbox/broadcast/ every 60s
```

### 3.3 Seal Notification (VAULT999)
```
Agent A → A2A POST /a2a/warga/seal
AAA gateway → broadcast to all warga
All agents acknowledge via mailbox
```

### 3.4 Human Escalation (888_HOLD)
```
Agent A → Telegram AAA group: "888_HOLD: <reason>"
Hermes → Arif DM: "HOLD from Agent A: <reason>"
Arif responds → Hermes routes response back to Agent A
```

## 4. Warga Identity Verification

Every inter-agent message MUST carry:
```
warga_id: <hermes-asi|claude-code|aaa-gateway|777-forge>
session_id: <current session>
signature: sha256(warga_id + session_id + body)
```

Receiving agent verifies:
1. `warga_id` is in warga AAA registry
2. `session_id` is valid (not expired)
3. `signature` matches body

## 5. The Permanent Line

> Warga agents communicate freely. No permission gates. No routing approvals.
> The mailbox is the institution's nervous system. The A2A mesh is the spine.
> Telegram is the human window. Filesystem is the ground truth.
> DITEMPA BUKAN DIBERI.

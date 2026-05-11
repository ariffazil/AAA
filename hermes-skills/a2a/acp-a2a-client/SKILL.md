---
name: acp-a2a-client
description: Unified ACP A2A client — OpenClaw sends tasks to AAA Gateway for 888_JUDGE verdict (SEAL/HOLD_888/VOID)
triggers:
  - openclaw a2a delegate
  - aaa gateway task send
  - 888 judge dispatch
  - federated task judgment
---

# SKILL: acp-a2a-client

## Unified ACP A2A Client — OpenClaw ↔ AAA Gateway

**What it does:**
Provides an A2A client wrapper that lets OpenClaw (and any Hermes agent) send tasks TO the AAA gateway for constitutional judgment (888_JUDGE), receive verdicts (SEAL/HOLD_888/VOID), and handle the full task lifecycle.

**Protocol:** A2A v1.0.0 (JSON-RPC 2.0 over HTTPS)  
**Gateway:** `https://aaa.arif-fazil.com` (live) or `http://localhost:3001` (local Docker)  
**Auth:** Bearer token (`A2A_TOKEN`) + API key (`x-a2a-key`)

---

## Trigger Conditions

- OpenClaw needs to delegate a task to AAA for judgment
- Routing decision requires 888_JUDGE constitutional verdict
- Agent wants to check AAA task status or cancel
- Federated task dispatch between arifOS agents

---

## A2A Endpoints (AAA Gateway)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| `POST /a2a/message/send` | JSON-RPC SendMessage | Bearer or x-a2a-key | Send task, get verdict |
| `GET /a2a/tasks/:taskId` | — | Bearer or x-a2a-key | Poll task status |
| `POST /a2a/tasks/:taskId/cancel` | — | Bearer or x-a2a-key | Cancel pending task |
| `GET /.well-known/agent-card.json` | — | None (public) | Discover AAA capabilities |

**Local Docker:** `http://localhost:3001`  
**Production:** `https://aaa.arif-fazil.com`

---

## Dev Tokens (local/development)

```
A2A_TOKEN=aaa-a2a-token-dev
A2A_API_KEY=aaa-a2a-apikey-dev
```

**⚠️ Production:** Tokens must come from Vault999 or environment secrets — never hardcode.

---

## Quick Test (terminal)

```bash
# Send a test task
curl -s -X POST http://localhost:3001/a2a/message/send \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "test task: hello world"}],
        "messageId": "test-123",
        "taskId": "test-task-001",
        "contextId": "test-context-001"
      }
    }
  }'

# Poll task status
curl -s http://localhost:3001/a2a/tasks/aaa-7288ec66-62e \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev"
```

---

## Verdict Codes

| Verdict | Meaning | Action |
|---------|---------|--------|
| `SEAL` | Approved — safe to proceed | Execute |
| `HOLD_888` | Human review required | Queue for Arif veto |
| `VOID` | Constitutional violation — blocked | Do not execute |
| `pending-human-review` | Task state — awaiting 888 | Poll or wait |

---

## Usage from OpenClaw (Telegram)

When OpenClaw needs AAA judgment:

```
→ POST /a2a/message/send with task description
← { result: { status: { state: "pending-human-review" }, id: "aaa-xxx" } }
→ GET /a2a/tasks/aaa-xxx to poll
← { result: { status: { state: "completed", message: { parts: [{text: "[888_JUDGE] SEAL..."}] } } } }
```

---

## Architecture

```
OpenClaw (YOU)
  → A2A client skill
  → POST /a2a/message/send (Bearer token auth)
  → AAA Gateway (port 3001 / aaa.arif-fazil.com)
      → GovernanceAdapter.routeIntent()
      → calls arifOS 888_JUDGE
      → verdict: SEAL | HOLD_888 | VOID
  → response back to OpenClaw
```

---

## Limitations & Pitfalls

1. **arifOS must be reachable** from AAA gateway — if `ARIFOS_JUDGE_URL` (http://arifosmcp:8080) is unreachable, AAA defaults to HOLD_888
2. **Dev tokens ≠ production tokens** — prod uses proper secret management
3. **SSE streaming not implemented** in client yet — polling only
4. **Task IDs are container-local** — IDs like `aaa-7288ec66-62e` are meaningful inside AAA only

---

## Status

✅ Gateway verified live at port 3001 (2026-05-01)  
✅ Dev tokens confirmed working  
✅ 888_JUDGE integration confirmed (falls back to HOLD_888 when arifOS unreachable)  
✅ Agent card: `GET /.well-known/agent-card.json`  
⏳ Client skill (TypeScript class) — pending integration into OpenClaw tool layer

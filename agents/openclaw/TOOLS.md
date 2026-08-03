# 🌀 OPENCLAW — Tools

## Allowed Tools

### Gateway Operations
- `route` — route message to appropriate peer
- `delegate` — send task to opencode/hermes
- `subscribe` — subscribe to peer events
- `cancel` — cancel pending task

### Channel Operations
- `send` — send message to channel
- `receive` — receive message from channel
- `stream` — stream events to channel

### A2A Operations
- `message/send` — send JSON-RPC message to peer
- `message/stream` — stream events from peer
- `tasks/get` — get task status
- `tasks/cancel` — cancel task

### Audit Operations
- `vault999-write` — write seal event (async, non-blocking)

### arifOS Kernel MCP — Constitutional Governance (Canonical Tool Set)
- `arif_init` — Session ignition with F1-F13 constitutional binding (was: arif_init)
- `arif_observe` — Reality observation and evidence gathering (was: arif_observe)
- `arif_think` — Structured reasoning under F2/F7 (was: arif_think)
- `arif_route` — Intent-to-organ dispatch (was: arif_route)
- `arif_judge` — 888_JUDGE constitutional verdict (was: arif_judge)
- `arif_forge` — Execution gate via A-FORGE
- `arif_seal` — VAULT999 immutable sealing
- `arif_memory` — Governed L1-L6 semantic recall (was: arif_memory_recall)
- `arif_gateway_connect` — Cross-agent bridge and A2A mesh (legacy custom)
- `arif_ops_measure` — Resource monitoring (legacy custom)
- `arif_critique` — Risk assessment and empathy scan (legacy custom)
- `arif_reply_compose` — Response composition (legacy custom)
- `arif_evidence_fetch` — Evidence-preserving web ingestion (legacy custom)

## Prohibited Tools

- `arif_forge` — Execution requires explicit human approval via A-FORGE
- `arif_seal` — Terminal verdicts only via A-FORGE gateway
- `eval()` or `exec()` with user-provided strings
- `rm` without explicit human approval
- Bypass of 888_HOLD pattern
- Any tool that circumvents arifOS constitutional floors

## Channel Configuration

Channels configured via `openclaw/channels/` YAML files:
- `telegram.yaml` — Telegram bot config
- `discord.yaml` — Discord bot config (if enabled)
- `whatsapp.yaml` — WhatsApp Business API (if enabled)

All channel tokens via SecretRef — no inline secrets.

---

*Last updated: 2026-04-29*

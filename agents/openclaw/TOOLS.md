# TOOLS.md — openclaw Agent

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
- `VAULT999.writeSeal` — write seal event (async, non-blocking)

## Prohibited Tools

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

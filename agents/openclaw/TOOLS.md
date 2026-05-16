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
- `vault999-write` — write seal event (async, non-blocking)

### arifOS MCP — Constitutional Governance (Full Access)
- `arif_session_init` — Initialize governed session with constitutional binding
- `arif_sense_observe` — Reality observation and evidence gathering
- `arif_kernel_route` — Central orchestration and intent routing
- `arif_gateway_connect` — Federated cross-agent bridge and A2A mesh protocol
- `arif_judge_deliberate` — 888_JUDGE constitutional arbitration
- `arif_ops_measure` — Thermodynamic health and resource monitoring
- `arif_heart_critique` — Risk assessment and empathy scan
- `arif_reply_compose` — LLM-aware response composition
- `arif_memory_recall` — Semantic memory search
- `arif_mind_reason` — Symbolic reasoning kernel
- `arif_evidence_fetch` — Evidence-preserving web ingestion

## Prohibited Tools

- `arif_forge_execute` — Execution requires explicit human approval via A-FORGE
- `arif_vault_seal` — Terminal verdicts only via A-FORGE gateway
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

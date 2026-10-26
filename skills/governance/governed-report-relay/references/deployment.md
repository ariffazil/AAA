# Relay deployment recipe

## Files

```
relay.py     HTTP + MCP server, stdlib only
             POST /handoff  agent -> agent (silent)
             GET  /inbox    agent reads its own inbox
             POST /report   human lane, triaged
             POST /mcp      JSON-RPC: initialize, tools/list, tools/call, ping
             GET  /ledger   what was escalated
             GET  /pending  what is waiting in the digest
digest.py    flush pending.jsonl into ONE message, archive after confirm
```

## systemd

`report-relay.service` — Type=simple, Restart=always, EnvironmentFile holds the
key and the bot token.

`report-digest.service` — Type=oneshot, runs digest.py.
`report-digest.timer` — OnCalendar 08:30, 15:30, 21:30, Persistent=true.

## Reverse proxy

Mount the whole service under one prefix and let the app strip it:

```
handle /report* { reverse_proxy 127.0.0.1:18101 }
```

Validate the proxy config before reload, or a typo takes every vhost down.

## Secrets

`/root/.secrets/report-relay.env`, mode 0600:

```
REPORT_RELAY_KEY=<token_urlsafe(32)>
TELEGRAM_BOT_TOKEN=<bot token>
RELAY_HOST=127.0.0.1
RELAY_PORT=18101
RELAY_CHAT_ID=<sovereign chat id>
RELAY_BASE=/var/log/report-relay
```

Rotating the key = edit one line, restart the relay. Old key holders lose
interrupt authority immediately; nothing else changes.

## Minimal MCP server (what the tool actually needs)

Streamable HTTP without stdio: handle `initialize`, `tools/list`, `tools/call`,
`ping`; reply 202 with an empty body to any `notifications/*` (they carry no
`id`). Return `application/json` — not every client accepts SSE for a
single-tool server.

Declare honest annotations: `readOnlyHint: false`, `destructiveHint: false`,
`openWorldHint: true`. A tool that hides its write nature gets filtered or
mis-trusted by host risk UI.

## Shell wrappers worth having

```bash
report  "Title" "Body"                       # human lane
report --severity P1 --source x "T" "B"
handoff --to hermes --subject s --body b     # agent lane
inbox hermes 20
```

Keep the relay key in one env file and source it in wrappers, so rotating the
key never means editing scripts.

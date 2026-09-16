---
name: agent-to-agent-enablement
description: Use when enabling or debugging A2A peer transport.
---

# Agent-to-Agent (A2A) Enablement

Turning on and diagnosing the A2A transport between agents — the local platform plugin, and
peers that expose an agent card.

## Use a protocol transport, not chat

A chat platform is a *human* channel. Bot-to-bot delivery on a chat platform is rejected by
the platform itself, and no allowlist or mention setting bypasses it. Agent-to-agent traffic
belongs on a protocol transport (A2A or MCP), never a chat lane. If a peer is not answering,
first ask whether there is a transport at all before debugging the peer.

## Enable (local side) — verify the schema before writing config

| Setting | Read from | Notes |
|---|---|---|
| `platforms.a2a.enabled: true` | config.yaml | the only config.yaml key strictly required |
| `platforms.a2a.port: N` | config.yaml | fallback only; default 9900 |
| `A2A_PORT` | env | **wins** over the YAML port |
| `A2A_HOST` | env | bind host; default 127.0.0.1 |
| `A2A_PEER_TOKENS` / `A2A_BEARER_TOKEN` | env | per-peer or shared credential |
| `A2A_AGENT_NAME`, `A2A_HOME_CHANNEL`, `A2A_ALLOW_ALL_USERS`, `A2A_TRUSTED_PEERS` | env | advisory / admission |

Nested keys such as `platforms.a2a.host` or `platforms.a2a.auth.*` are **not read**. Put the
bind host and tokens in the environment, not the YAML. Confirm against the plugin source
before writing an enablement packet (`grep -nE "getenv|extra.get" <plugin-dir>/`) and cite
file:line — a schema invented from expectation silently produces a loopback-only listener.

## The bind is fail-closed

Requesting a wide bind with no token configured is silently downgraded to loopback with a
warning. Token presence is the precondition for any remote bind, independent of config
order, so the plugin cannot be misconfigured into a public listener by omitting auth. Do not
bolt on a separate "security" step — verify the token exists and the bind follows.

## Diagnose "the peer agent does not reply"

Work both directions, and distinguish **absent** from **denied**:

1. **Is the local plugin enabled?** The tool gate withholds every A2A tool unless one of
   `a2a_agents`, `A2A_PORT`, or `platforms.a2a.enabled` is set. Absent config makes the tools
   silently unavailable — indistinguishable from "no reply".
2. **Does the peer publish an agent card?** Fetch the discovery path on the peer.
3. **Interpret the status honestly.** A `4xx` on a card path often means the handler is not
   enabled and the document was never served, not that authentication failed. Probe a known
   liveness path on the same port to separate "the gate blocks everything" from "this
   resource does not exist".
4. **One side is not a lane.** Both peers must publish a card; enabling one end gives a
   one-way path at best.

## Pitfalls

- **Do not hand over a fix for an unconfirmed symptom.** A proxy/attribution error on the
  card path is a symptom; the cause may be that the plugin serving that card is disabled.
  Confirm which layer is refusing before proposing a change.
- **A stale plugin registry makes enablement look ineffective.** Refresh the peer's plugin
  registry after enabling, or the persisted index may not include the newly enabled plugin.
- **Check the port is free** on both ends before choosing one, and prefer an explicit port
  over relying on the default.
- **Enabling an inbound listener is an architecture decision.** It opens a network surface —
  surface it for authorization rather than flipping it as part of a debugging session.

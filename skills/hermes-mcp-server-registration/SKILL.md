---
name: hermes-mcp-server-registration
description: "Use when wiring an external MCP server into Hermes."
version: 1.0.0
owner: curator
risk_tier: low
floor_scope: [F2, F11]
category: hermes-ops
tags: [mcp, hermes, config, registration, remote-server]
related_skills: [third-party-mcp-adoption, hermes-cli-automation, mcp-ops]
---

# Wiring an External MCP Server into Hermes

Taking a server from "a URL someone pasted" to "tools the harness can actually call".

**Load when:** a human says *install this* after an MCP link, a hosted server needs to become
first-class tools, or an existing `mcp_servers` entry stops answering.

Deciding *whether* the server belongs here, and reading its wire surface, is a different job —
see `third-party-mcp-adoption` (probe sequence, SSE parsing, monolingual corpus traps). This
skill starts after that decision and ends at a verified live tool.

## 1. Register through the CLI, never through the file

The `patch`/`write_file` tools **refuse** `~/.hermes/config.yaml` as security-sensitive. The CLI
owns that file — use it, one dotted key per call:

```bash
hermes config set mcp_servers.<key>.url https://host.example/mcp
hermes config set mcp_servers.<key>.enabled true
hermes config set mcp_servers.<key>.timeout 60
hermes config get mcp_servers.<key>
```

- `<key>` becomes the tool namespace: `mcp__<key>__<tool>`. Hyphens are fine and are preserved
  (`biohacking-kompakt` → `mcp__biohacking-kompakt__bk_search_topics`); pick a key that reads
  well in a tool name, not the vendor's legal name.
- `hermes config set` round-trips cleanly (`true` stays a boolean, numbers stay numbers). A hand
  edit drifts on quoting; prefer the CLI even when you have write access by another route.
- **Disable, don't delete.** `enabled: false` keeps the headers, the timeout, and the reason the
  server was wired; re-enabling is one command.

## 2. Put the transport quirks in config, not just in your probe

A hosted server that needed a browser `User-Agent` or SSE-shaped `Accept` during the probe needs
the same headers when the harness dials it:

```bash
hermes config set mcp_servers.<key>.headers.Accept 'application/json, text/event-stream'
```

If the probe needed a header to get past a bot filter, a registration without it will look
healthy in config and dead on first call.

## 3. Verification is a ladder — say which rung you reached

| Rung | Command | Proves | Does **not** prove |
|---|---|---|---|
| 1 | `hermes config get mcp_servers.<key>` | the write landed | the server exists |
| 2 | stdlib probe against the URL (see `third-party-mcp-adoption`) | the server is alive and lists N tools | the harness can reach it |
| 3 | a real tool call through the harness | the server is wired and callable | the next session keeps it |

Config is read at harness start, so a `set` mid-session does **not** inject tools into the
running agent — the new namespace appears after a gateway/harness restart. Until your own tool
list shows `mcp__<key>__*`, the honest report is "registered, server verified alive by direct
probe, tools available after restart" — never "installed and working".

```bash
hermes gateway restart   # from outside a gateway process; it cannot restart itself
```

## Pitfalls

- **Probing the server is not verifying the registration.** Rung 2 passing while rung 3 was
  never attempted is the most common overclaim here; the config key and the live harness are two
  different facts.
- **A `tools/list` count is the server's claim about itself.** It tells you what the wire offers,
  not that any of it returns data — call one cheap tool before reporting capability.
- **Don't answer a "won't connect" report with a new server.** Read the error text first: a
  `-32602` validation error is an argument/query problem, an empty result is not a dead endpoint,
  and a `403` from a CDN front is usually User-Agent filtering.
- **No auth does not mean no cost.** A read-only server with no key still costs a config entry, a
  tool namespace in every prompt, and a restart; wire it only when the human asked for it or the
  capability is genuinely reused.
- **Never leave a half-registered server `enabled: true`.** Either finish (headers + verification)
  or set it `false`; an enabled entry that fails on every call burns the fallback chain quietly.

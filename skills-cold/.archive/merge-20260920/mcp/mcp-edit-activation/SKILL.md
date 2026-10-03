---
name: mcp-edit-activation
version: 1.0.0
description: "Use when an MCP server edit may not be live yet."
triggers:
  - "patched an MCP server"
  - "is the fix live"
  - "MCP tool still returns old output"
  - "MCP tool returns empty list"
  - "effect of a server.py edit"
  - "reload an MCP server"
  - "gate change not taking effect"
tags: [mcp, deployment, verification, ghost-capability]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MCP edit activation — a file edit is not a live fix

> **One law:** a patch on disk is not a fix. Label it **"fixed on disk, not live"** until a fresh
> process proves the new behaviour. Never report "fixed" from a diff alone.

## Why — MCP servers are long-lived, with no hot reload

Expect two independent loaders. Neither re-reads the file:

1. **A systemd HTTP unit** owning a port (`<name>-mcp.service`), started once, ppid 1.
2. **A stdio child** spawned once per gateway, declared under `mcpServers:` in the gateway config
   (`command` + `args` + `--transport stdio`). Spawned at gateway start, not per session.

Both hold the imported module in memory for days. Editing the `.py` changes nothing they execute.

## Liveness check — commands, not guesses

- Compare the **loader PID's start time against the edited file's mtime**: `PID start < file mtime`
  ⇒ the process is running stale code.
- Confirm **which module path the server imports** (look for `sys.path.insert` and the `import` at the
  top of `server.py`). A symlinked tree means two paths are one file — a fix applied to the other copy
  is a no-op.
- Activation is an **operator action**: recreate the unit and the gateway from a shell outside the
  gateway process. A restart attempted from inside the gateway is blocked and will fail — never promise
  a restart you cannot perform.

## Verify before claiming

Run the edited server in a **fresh stdio spawn** and call the changed tool through the transport.
Passing unit tests only prove the module imports; they prove nothing about the running session.

## Ghost capability check

A tool that returns a constant, or a collection hard-initialised empty and never appended to, is a
**ghost capability**: declared in the catalog, accepts a rich payload, produces nothing. Probe with two
payloads that must differ and compare — if output does not move with input, it is a stub. **Silence and
failure must be distinguishable**: an empty result needs an explicit reason field (e.g.
`insufficient_evidence`), or an operator cannot tell "nothing to report" from "broken".

## Patching an enforcement gate — fix both directions

A substring gate is a false-positive machine on proper nouns and ordinary words (`ALPHA-ZEN`,
`predominant`, `toxicology`). Anchor terms as **whole tokens**, with a left boundary that treats hyphen
and underscore as separators. Then test the **false-negative** direction as well — the same substring
logic silently misses obfuscated forms the term list exists to catch. A suite covering one direction is
an incomplete fix.

Also: an enforcement list shared by many tools should be **imported**, never re-typed. Two copies drift,
and the drift is invisible until someone is wrongly blocked.

## Concurrent writers

Two agents on one file: keep a pre-patch copy so the diff stays exact, publish the md5 before and after,
and re-read the file before any further edit. A stale-copy rewrite can silently revert a correct hunk.

## Reporting contract

State three things, always: **what is fixed on disk** (with hash), **what is still served by the running
process**, and **what activation requires**. A caller who believes a fix is live when it is not will build
on a false foundation — and will blame the wrong layer when it behaves exactly as the old code did.

# OpenClaw Plane — AAA Workspace Authority

This directory makes OpenClaw a **first-class runtime target** inside AAA.

Rule:
- **AAA authors**
- **OpenClaw consumes**
- **runtime state must round-trip back into AAA inventory**

## Canonical shape

```
openclaw/
├─ gateway/      # model providers, channels, security policy ✅
├─ acp/           # ACP host adapter session templates ✅
├─ mcp/           # MCP server catalogs and manifests ✅
├─ plugins/       # approved plugin allowlist ✅
├─ channels/      # message routing and authorization ✅
├─ a2a/           # A2A peer contracts and agent cards ✅
├─ agents/        # agent definitions and runtime bindings ✅
└─ exports/       # generated JSON artifacts for runtime ✅
```

## OpenClaw Inventory

| Domain | AAA Owner Path | Status |
|--------|---------------|--------|
| Agents and bindings | `openclaw/agents/` + `registries/agents.yaml` | ✅ Complete |
| Gateway and provider defaults | `openclaw/gateway/` | ✅ Complete |
| ACP sessions and host adapters | `openclaw/acp/` + `registries/hosts.yaml` | ✅ Complete |
| MCP server catalogs | `openclaw/mcp/` + `registries/servers.yaml` | ✅ Complete |
| Plugins and allowlist | `openclaw/plugins/` | ✅ Complete |
| A2A identity and discovery | `openclaw/a2a/` + `agents/*/agent-card.yaml` | ✅ Complete |
| Channels and routing policy | `openclaw/channels/` | ✅ Complete |
| Runtime exports | `openclaw/exports/` | ✅ Complete |

## Authoring rule

If OpenClaw can:
- run it → AAA must describe it
- install it → AAA must inventory and approve it
- route to it → AAA must register and bind it
- expose it → AAA must policy-gate it
- emit events about it → AAA must capture and audit it

## Runtime rule

OpenClaw should run from **AAA-derived state**, not hand-edited local drift.

That means:
- YAML source contracts live in AAA
- JSON artifacts are exported from AAA
- runtime inspection should be diffed against AAA desired state
- drift should fail closed for high-risk changes

## Anti-entropy invariant

If OpenClaw can run it, AAA must be able to describe it.
If OpenClaw can install it, AAA must inventory and approve it.
If OpenClaw can route to it, AAA must register and bind it.
If OpenClaw can expose it to agents, AAA must policy-gate it.
If OpenClaw emits events about it, AAA must capture and audit it.

## Complete OpenClaw Plane ✅

Built 2026-04-22. All 8 domains complete.
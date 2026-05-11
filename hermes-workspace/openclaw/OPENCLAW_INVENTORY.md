# OpenClaw Inventory

This inventory maps each OpenClaw capability domain to its AAA owner surface.

## Domain map

| OpenClaw domain | AAA owner path | Schema |
|---|---|---|
| Agents and bindings | `openclaw/agents/` + `registries/agents.yaml` | `schemas/openclaw-agent-binding.schema.json` |
| Gateway and provider defaults | `openclaw/gateway/` | `schemas/openclaw-gateway.schema.json` |
| ACP sessions and host adapters | `openclaw/acp/` + `registries/hosts.yaml` | `schemas/openclaw-acp-session.schema.json` |
| MCP server catalogs | `openclaw/mcp/` + `registries/servers.yaml` | `schemas/openclaw-mcp-catalog.schema.json` |
| Plugins and allowlist | `openclaw/plugins/` | `schemas/openclaw-plugin.schema.json` |
| A2A identity and discovery | `openclaw/a2a/` + `agent-card.json` | `schemas/openclaw-a2a-agent-card.schema.json` |
| Channels and routing policy | `openclaw/channels/` | `schemas/openclaw-gateway.schema.json` |
| Runtime exports | `openclaw/exports/` | generated from YAML source contracts |

## Completeness rule

AAA is not a complete OpenClaw workspace authority until:

1. every domain above has a source owner path
2. every domain above has a schema
3. runtime-consumable exports are generated from AAA
4. runtime state can be compared back to AAA desired state

## Anti-entropy invariant

If OpenClaw can run it, AAA must be able to describe it.

If OpenClaw can install it, AAA must inventory and approve it.

If OpenClaw can route to it, AAA must register and bind it.

If OpenClaw can expose it to agents, AAA must policy-gate it.

If OpenClaw emits events about it, AAA must capture and audit it.

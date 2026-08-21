---
id: FORGE-mcp-a2a-agentic
name: FORGE-mcp-a2a-agentic
version: 1.0.0-2026.07.17
description: "MCP + A2A protocol integration — agentic inter-agent communication and task delegation."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F4', 'F8', 'F11', 'F12', 'F13']
autonomy_tier: T2
---
# ⚒️ MCP + A2A Agentic — Protocol Integration

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Implement MCP server/client patterns and A2A agent-to-agent protocol integration across the federation. Handle tool surface discovery, capability drift detection, transport selection (stdio/HTTP), and agent card registration.

## When to Use
- Creating or modifying an MCP server for any federation organ (FastMCP, Express)
- Implementing A2A agent cards and task lifecycle
- Tool discovery — `tools/list` patterns, capability enumeration
- Transport decisions — stdio vs HTTP SSE vs streamable HTTP
- Drift detection between registered manifest and live tool surface

## When NOT to Use
- Frontend UI components — use `nextjs-mastery` or `react-spa-discipline`
- Database or cache layers — use `postgres-schema-design` or `redis-qdrant-integration`
- Deployment — use `cicd-docker-deploy`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Tool renames are breaking changes; deprecate before removal across one cycle |
| F2 TRUTH | Tool descriptions must match actual behavior — vague descriptions = silent misfires |
| F3 WITNESS | A2A agent cards published with verifiable identity (did:web ref) |
| F4 CLARITY | One tool = one responsibility; no mega-tools with action-switch parameters |
| F11 AUDIT | Every tool call logged with actor, intent, timestamp, result |
| F12 INJECTION | Tool arguments sanitized; no eval or raw shell from untrusted input |

## Commands & Patterns

```typescript
// FastMCP tool registration — FastMCP convention
server.tool(
  'forge_health_check',
  'Return A-FORGE server health and constitutional genome status',
  {
    include_latency: z.boolean().optional(),
  },
  async (args) => {
    // implementation
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  },
);

// A2A agent card — minimal structure
{
  "@context": "https://a2a.arif-fazil.com/schema/agent-card/v1",
  "id": "did:web:arif-fazil.com#333-agi",
  "name": "333-AGI",
  "capabilities": ["reason", "plan", "execute"],
  "services": [{
    "id": "#a2a-endpoint",
    "type": "A2AServer",
    "serviceEndpoint": "https://aaa.arif-fazil.com/a2a"
  }]
}

// Surface drift detection — compare manifest vs tools/list
// 1. Fetch manifest from federation-manifest
// 2. Call tools/list on each organ
// 3. Diff: missing tools, extra tools, description drift, schema drift
// 4. Report to forge_surface_guard
```

## Refusal Surface
- ❌ Tool names that change semantics without deprecation cycle
- ❌ A2A cards without verifiable identity references
- ❌ Registering tools that haven't passed HARAM scan + forge_evaluate
- ❌ Exposing internal organ ports/db details in tool descriptions
- ❌ Mixing transport auth models — stdio for local, HTTP with session for remote

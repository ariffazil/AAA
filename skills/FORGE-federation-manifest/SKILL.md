# ⚒️ Federation Manifest — arifOS Topology

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Build and maintain `/.well-known/arifos-federation.json` — the machine-readable federation topology describing all 7 organs, their ports, transports, MCP/A2A surfaces, capability graphs, and edge relationships.

## When to Use
- Initializing or updating the federation manifest for a new organ or subdomain
- Adding transport endpoints (MCP stdio, MCP HTTP, A2A)
- Defining organ → organ capability edges (which organ calls which)
- Publishing for external agents to discover the federation topology
- Drift detection between manifest and live `tools/list`

## When NOT to Use
- Individual organ identity (DID) — use `did-web-identity`
- Constitutional ontology — use `governance-jsonld`
- Runtime health probes — use organ `/health` endpoints

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Manifest versioned; old manifests archived, never deleted |
| F2 TRUTH | Every declared tool must match live `tools/list` — drift = F2 violation |
| F4 CLARITY | One manifest, one topology — no stale copies in random locations |
| F11 AUDIT | Manifest changes logged to VAULT999 with diff receipt |
| F13 SOVEREIGN | New organ registration requires F13 approval |

## Commands & Patterns

```jsonc
// /.well-known/arifos-federation.json
{
  "@context": "https://arifos.arif-fazil.com/schema/federation/v1",
  "federation": "arifOS",
  "version": "2026.07.16",
  "nodes": [
    {
      "id": "arifos",
      "name": "arifOS Constitutional Kernel",
      "port": 8088,
      "transport": "http",
      "mcpEndpoint": "/mcp",
      "healthEndpoint": "/health",
      "capabilities": ["judge", "seal", "session", "attest", "route", "think"]
    },
    {
      "id": "aforge",
      "name": "A-FORGE Execution Shell",
      "port": 7071,
      "transport": "http",
      "mcpEndpoint": "/mcp",
      "capabilities": ["execute", "docker", "git", "filesystem", "browser"]
    }
    // geox, wealth, well, aaa follow same structure
  ],
  "edges": [
    { "from": "aaa", "to": "arifos", "type": "a2a", "protocol": "a2a-v1" },
    { "from": "arifos", "to": "aforge", "type": "mcp", "protocol": "mcp-v2025-03-26" }
    // remaining 9 edges
  ]
}
```

## Refusal Surface
- ❌ Including secrets, keys, or internal IPs in the manifest
- ❌ Declaring capabilities that aren't verified by live probe
- ❌ Outdated port/transport info — must be synced with actual systemd config
- ❌ Duplicate node IDs or conflicting edge definitions

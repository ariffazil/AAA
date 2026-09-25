---
id: forge-mcp-registry-ops
name: FORGE-mcp-registry-ops
version: 0.1.0
description: "Vendor intelligence + supply-chain scoring gate for third-party MCP servers via the official MCP Registry (registry.modelcontextprotocol.io, v0.1 API, preview)."
owner: AAA
risk_tier: medium
floor_scope: [F2, F8, F11]
autonomy_tier: T2
tags: [mcp, registry, vendor-intelligence, supply-chain, pre-wiring-gate]
capability_tier: fed-agent-subagent
ecology_state: COLD
triggers:
  - "wire third-party MCP"
  - "register MCP"
  - "MCP discovery"
  - "MCP vendor vetting"
  - "MCP supply chain"
---

# FORGE-mcp-registry-ops — Vendor Intelligence Gate

The official MCP Registry is a **public metadata index** for MCP servers (registry.modelcontextprotocol.io, v0.1 API, still PREVIEW). Its real value to us is **consumption, not publication**: a free, unauthenticated read API that serves as a **vendor-intelligence + supply-chain feed** for vetting third-party MCPs *before* we wire them into the federation.

This skill provides that gate. It does NOT publish anything; publishing requires F13 binary and external-port/firewall changes (Attention Membrane §Hard Stops).

## Capabilities (3 tools)

### 1. `registry_search(query, limit=20)`
Search MCP servers by name substring. Returns ranked list with publisher reputation metadata.

```bash
# Direct via curl (no auth required)
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=<query>&limit=20"
```

### 2. `registry_get(server_name)`
Fetch full `server.json` for one server: all versions, `packages[]`, `remotes[]`, owner identity, schema era.

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers/<encoded-name>"
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers/<encoded-name>/versions"
```

### 3. `registry_score(server_name)`
Compute supply-chain risk score 0-100 (lower = better). Combines:
- Publisher namespace depth (`com.*` / `ac.*` > `ai.*` bulk-generic)
- Publisher volume (single-server publishers > bulk-publishers of >5 servers — moderation policy trigger)
- Version cadence (latest version age, deprecation status)
- Remote reachability (must be publicly reachable to be listed)
- Schema currency (2025-12-11 server.schema.json = current; older = stale)

## Heuristics (calibrated 2026-09-25 against 128-syarikat sample)

| Signal | Score impact | Rationale |
|--------|-------------|-----------|
| Namespace `com.<verified-domain>/...` | -15 | Domain-anchored identity = best |
| Namespace `ac.<.ac>/...` (academic) | -10 | Domain-verified, low spam |
| Namespace `io.github.<user>/...` | 0 | GitHub OAuth, but binds identity to GitHub |
| Namespace `ai.*` (bulk) | +10 | Noise floor dominates |
| Publisher has 1 server | -5 | Single-purpose, usually legit |
| Publisher has 5-10 servers | +5 | Volume signal — review intent |
| Publisher has >10 servers | +15 | Spam pattern (moderation-policy trigger) |
| Latest version published >180d ago | +10 | Maintenance neglect |
| Latest version marked `deleted` | +30 | Active takedown — avoid |
| Latest version marked `deprecated` | +10 | Functional but discouraged |
| Remote endpoint fail HTTP probe | +25 | Listed but not reachable = integrity failure |
| Schema < 2025-12-11 | +5 | Drift from current |

**Score interpretation:**
- 0-20 → LOW risk, candidate for wiring
- 21-40 → MEDIUM risk, manual review required
- 41-60 → HIGH risk, hold + flag
- 61+ → AVOID, supply-chain compromise likely

## Federation Pre-Wiring Gate

Before adding ANY third-party MCP to the federation (zai, firecrawl, context7, brave, etc.):

1. `registry_search` — confirm listing exists, get all matches
2. `registry_get` — fetch server.json, verify `remotes[]` endpoint
3. `registry_score` — compute risk; if >40, HOLD and escalate

Live probe example (already validated 2026-09-25):

```bash
# arifOS — expect zero matches (we don't publish)
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=arifOS" | jq '.servers | length'
# → 0 (confirmed not registered, by design)

# zai — verify we consume a legitimate listing
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=zai" | jq '.servers[] | {name, versionCount: (.versions | length)}'

# CAVEAT: not every MCP we consume is in the registry.
# Pre-2025 servers, internal forks, and beta programs may not be listed.
# Absence of listing ≠ unsafe; it just means no registry-grade provenance.
```

## Decision Tree

```
Intent: wire third-party MCP X
   ↓
registry_search X
   ↓
Not found → check X is reputable via other means
   ↓
Found → registry_get X (latest version)
   ↓
registry_score X
   ↓
score ≤ 40 → proceed (still requires A-FORGE execute, F2/F8 floors)
score > 40 → HOLD, escalate to Arif with score breakdown
```

## What This Skill Does NOT Do

- **Publish** anything. Publishing requires `mcp-publisher` CLI + namespace ownership proof + F13 binary. Out of scope.
- **Modify** registry. Read-only.
- **Authenticate.** v0.1 API is unauthenticated.
- **Cache.** Each call hits the registry directly. Add cache layer only if API rate limits hit.

## Federation Audit Trail

- 2026-09-25: Skill created (FI-005, post 1mcp entropy cleanup)
- Reasoning: registry remains PREVIEW (v0.1 API frozen since 2025-10-24); consumption is the only viable path; supply-chain scoring protects against bulk-publisher spam pattern (33-server bluenexus-style publishers flagged via heuristics)
- Source: `/root/AAA/research/mcp-registry-deep-research-2026-09-25.md` (FI-008 sealed research)
- Vendor intelligence feed: `/root/AAA/research/mcp-registry-company-export-2026-09-25.json`

DITEMPA BUKAN DIBERI ⚒️

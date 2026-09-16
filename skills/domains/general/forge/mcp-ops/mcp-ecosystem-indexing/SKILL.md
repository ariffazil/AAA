---
name: mcp-ecosystem-indexing
description: "Index MCP servers for maximum agent discoverability."
version: 1.0.0
author: AAA
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [mcp, indexing, discoverability, agents, security]
    category: data-intelligence
---

# MCP Ecosystem Indexing

Make MCP servers maximally discoverable by agents, scanners, and directory crawlers. **Indexing beats fame** — agents find you by machine-readable signals, not GitHub stars.

## When to Use
- Deploying a new MCP server or updating an existing one
- Auditing why a server is not getting traffic from agent clients
- After security scanning reveals clean results (badge opportunity)
- When Smithery, Glama, or other directories show 404

## The 4-Layer Discovery Pipeline

Scanners and MCP directories find servers through:

1. **Certificate Transparency** — `crt.sh` / Censys pick up new `*.yourdomain.com` subdomains in seconds. Subdomains with `mcp`, `ai`, `api`, `agent` get auto-probed.
2. **Package registries** — PyPI firehose, npm, deps.dev, Libraries.io. Publishing `pip install yourpackage` puts you in every scanner feed.
3. **GitHub event stream** — GH Archive indexes repos by topic tags. Use: `mcp`, `ai-agents`, `ai-governance`, `mcp-server`, `constitutional-ai`.
4. **Aggregator cascades** — Listing on Glama.ai or PulseMCP triggers auto-indexing across 5+ downstream directories.

## Procedure

### 1. Verify HTTP Beacon Signals

Every MCP server should expose:
- `GET /mcp` → JSON discovery card (capabilities, transport, tools URL)
- `Link: </llms.txt>; rel="llms"` header on every response
- `Access-Control-Allow-Origin: *` for cross-origin client access
- `/.well-known/mcp.json` for structured MCP declaration
- `/.well-known/security.txt` for responsible disclosure instructions
- `/llms-full.txt` with complete tool schemas for RAG ingestion

### 2. Submit to Key Directories

| Directory | Impact | Method |
|-----------|--------|--------|
| Smithery.ai | Claude Desktop / Cursor one-click install | `smithery.yaml` with `startCommand` |
| Glama.ai | Cascades to 5+ directories | Auto-index or manual submit |
| PulseMCP.com | Endpoint verification + listing | Manual submit |
| PyPI | Python ecosystem discovery | Package metadata |
| npm | Node/JS ecosystem (75%+ frontend agent devs) | Wrapper package |
| agentmods.dev | Auto-scans and grades (A-F) | Auto-discovered |

### 3. Deploy Proof Badge

When an automated scanner gives clean results:
1. Display badge on `/proof` endpoint and GitHub README
2. Reference in `llms.txt` and `llms-full.txt`
3. Converts scanner attention into institutional credibility

## Pitfalls

- **Indexed ≠ popular.** A 45-star repo on 8 directories gets more agent traffic than a 10K-star repo on zero directories.
- **Missing `security.txt`** = researchers who find bugs have no disclosure path → may publish directly.
- **Missing `llms-full.txt`** = RAG systems cannot ingest full tool schemas.
- **Smithery 404** = Claude Desktop users cannot one-click install. Fix `smithery.yaml` and re-sync.
- **Don't submit to directories you can't maintain.** A stale listing with wrong endpoints is worse than no listing.

---
name: mcp-ecosystem-indexing
description: "Index MCP servers for maximum agent discoverability. Aligns beacon signals with canonical MCP spec 2026-07-28, RFC 8414 (AS metadata) + RFC 8705 (PRM), and the MCP-Protocol-Version header."
version: 1.1.0
author: AAA
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [mcp, indexing, discoverability, agents, security, well-known, oauth]
    category: data-intelligence
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MCP Ecosystem Indexing

Make MCP servers maximally discoverable by agents, scanners, and directory crawlers. **Indexing beats fame** — agents find you by machine-readable signals, not GitHub stars.

## When to Use
- Deploying a new MCP server or updating an existing one
- Auditing why a server is not getting traffic from agent clients
- After security scanning reveals clean results (badge opportunity)
- When directories show 404 or scanner-cache misses the beacon signals

## The 4-Layer Discovery Pipeline

Scanners and MCP directories find servers through:

1. **Certificate Transparency** — `crt.sh` / Censys pick up new `*.yourdomain.com` subdomains in seconds. Subdomains with `mcp`, `ai`, `api`, `agent` get auto-probed.
2. **Package registries** — PyPI firehose, npm, deps.dev, Libraries.io. Publishing `pip install yourpackage` puts you in every scanner feed.
3. **GitHub event stream** — GH Archive indexes repos by topic tags. Use: `mcp`, `ai-agents`, `ai-governance`, `mcp-server`, `constitutional-ai`.
4. **Aggregator cascades** — Listing on **the official MCP Registry** (`registry.modelcontextprotocol.io`, primary) triggers authoritative discovery. Smithery.ai / Glama.ai / PulseMCP.com are SECONDARY aggregators and demoted to "nice to have"; the canonical surface is now the registry itself.

## Procedure

### 1. Verify HTTP Beacon Signals (canonical MCP 2026-07-28 + OAuth RFCs)

Every MCP server should expose:

- `POST /mcp` (Streamable HTTP, modern) — preferred transport; reject legacy `GET /sse` for external clients.
- `MCP-Protocol-Version: 2026-07-28` header on **every** `/mcp` request — required by the spec for stateless transport. Scanners that omit it get a 400.
- `GET /.well-known/mcp/server.json` → JSON discovery card (capabilities, transport, tools URL). **[NOT `/.well-known/mcp.json`]** — that bare path is NOT in the canonical spec.
- `GET /.well-known/oauth-protected-resource` (RFC 8705) → JSON with `resource` metadata. Required for any server that handles protected tools.
- `GET /.well-known/oauth-authorization-server` (RFC 8414) → JSON with `issuer`, `authorization_endpoint`, `token_endpoint`. Optional but recommended for full OAuth discoverability.
- `Link: </llms.txt>; rel="llms"` header on every response — for LLM/RAG ingestion.
- `Access-Control-Allow-Origin: *` for cross-origin client access (audit scope: distinct from auth scope).
- `/.well-known/security.txt` for responsible disclosure instructions — missing this means researchers may publish without warning.
- `/llms-full.txt` with complete tool schemas for RAG ingestion.

### 2. Submit to Directories — registry first, aggregators second

| Directory | Status | Impact | Method |
|-----------|--------|--------|--------|
| **MCP Registry** (`registry.modelcontextprotocol.io`) | **PRIMARY** | Authoritative discovery source for the entire agent ecosystem | `mcp-publisher` CLI; auto-index once verified |
| PulseMCP.com | Aggregator | Endpoint verification + listing | Manual submit |
| Smithery.ai | Aggregator | Claude Desktop / Cursor one-click install | `smithery.yaml` with `startCommand` |
| Glama.ai | Aggregator | Cascades to 5+ downstream directories | Auto-index or manual submit |
| agentmods.dev | Scanner | Auto-scans and grades (A-F) | Auto-discovered |
| PyPI | Package registry | Python ecosystem discovery | Package metadata |
| npm | Package registry | Node/JS ecosystem (75%+ frontend agent devs) | Wrapper package |

**Rule (revised 2026-09-19):** always publish to the MCP Registry first. Aggregators are then auto-propagated downstream; do not double-submit to all of them by hand.

### 3. Deploy Proof Badge

When an automated scanner gives clean results:
1. Display badge on `/proof` endpoint and GitHub README
2. Reference in `llms.txt` and `llms-full.txt`
3. Converts scanner attention into institutional credibility

## Pitfalls

- **Indexed ≠ popular.** A 45-star repo on 8 directories gets more agent traffic than a 10K-star repo on zero directories.
- **`/.well-known/mcp.json` is NOT a canonical spec path.** Use `/.well-known/mcp/server.json` (with `/server.json` suffix). Scanners checking the bare path may 404; that's correct.
- **`MCP-Protocol-Version` header is REQUIRED** for streamable-http in 2026-07-28 era. Scanners that forget to send it get a 400; that's the server's correct response, not a bug.
- **Missing `security.txt`** = researchers who find bugs have no disclosure path → may publish directly.
- **Missing `llms-full.txt`** = RAG systems cannot ingest full tool schemas.
- **Missing `/.well-known/oauth-protected-resource` (RFC 8705)** = protected tools cannot complete OAuth discovery; F13 HOLD triggered.
- **Smithery/Glama 404 is no longer the primary failure mode** (MCP Registry is). Fix by submitting to the registry first; aggregators follow.
- **Don't submit to directories you can't maintain.** A stale listing with wrong endpoints is worse than no listing.

---

*Refreshed 2026-09-19 against canonical MCP 2026-07-28 spec + RFC 8414/8705.*
*Prior versions promoted Smithery/Glama as primary — that assumption is now obsolete (MCP Registry is canonical).*
*Originating observation: skill-zen-collapse Plan Phase 5.*

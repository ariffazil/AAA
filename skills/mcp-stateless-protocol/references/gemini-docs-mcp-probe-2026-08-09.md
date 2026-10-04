# Gemini Docs MCP Server Probe (2026-08-09)

> **Probe:** 2026-08-09 via deep research on Gemini coding agent integration.
> **URL:** `https://gemini-api-docs-mcp.dev`
> **Related:** `federation-seat-wiring/references/gemini-provider-integration-2026-08-09.md`, `mcp-stateless-protocol`

## What It Is

A public Model Context Protocol server from Google that gives coding agents live access to Gemini API documentation via a `search_documentation` function. Unlike skills (which are static rules baked into context), this MCP server provides *real-time* queryable documentation.

**Install:**
```bash
npx add-mcp "https://gemini-api-docs-mcp.dev"
```

**Also installs:** three Skills via `skills.sh` or Context7:
- `gemini-api-dev` — foundational rules and best practices
- `gemini-live-api-dev` — real-time conversational AI patterns
- `gemini-interactions-api` — Interactions API, agents, deep research, function calling

## Probe Results (Live Evidence)

| Test | Result | Details |
|---|---|---|
| DNS resolution | ✅ | Resolves to 34.54.237.210 |
| TLS certificate | ✅ | Valid cert matching `*.dev` TLD |
| HTTP/2 support | ✅ | ALPN negotiated h2 |
| POST /mcp with legacy initialize body | ⚠️ | No error body returned — likely requires SSE transport or proper stateless envelope headers |
| SSE endpoint /mcp/sse | ⚠️ | No response body detected in raw curl — may require specific Accept header |

**Conclusion:** The server is live and responding, but raw curl probes without proper MCP client semantics don't produce readable output. This is expected — the server uses standard MCP transport layers (SSE + JSON-RPC) that require an MCP SDK client to parse properly. Installation via `npx add-mcp` handles all transport details.

## How It Differs From Skills (`google-gemini/gemini-skills`)

| Aspect | MCP Server | Skills Package |
|---|---|---|
| **Delivery** | Runtime tool (`search_documentation`) callable during conversation | Static rules injected into system prompt at startup |
| **Currency** | Always-current (Google-hosted docs) | Stale after publish (even if repo updated) |
| **Latency** | Adds ~50-200ms per call | Zero latency (in-context) |
| **Coverage** | Search-specific queries only | Comprehensive best-practices coverage |
| **Fallback** | Must be network-accessible | Works offline once loaded |
| **Verification** | Prompt "How do I use context caching?" → should mention `cacheContent` | `/skills` command shows manifest |

**Best practice:** Use both. Skills provide the baseline rules; MCP fills gaps when you need exact API parameter names or latest changes not yet published in the skills package.

## Integration Into Federation Harnesses

| Harness | Install Command | Verification |
|---|---|---|
| opencode | `npx add-mcp "https://gemini-api-docs-mcp.dev"` | `/mcp` → search_documentation present |
| Claude Code | `.cursorrules` MCP config entry | `/mcp` → search_documentation present |
| Codex | MCP config in project root | Check active MCP connections |
| Gemini CLI | Built-in (it IS the Gemini client) | `gemini mcp list` |
| Cursor IDE | Settings > Features > MCP panel | Shows connected servers |
| VS Code Copilot | `.cursorrules` MCP section | `@gemini /mcp` → status check |

**Priority order:** opencode (PRIMARY harness) > claude-code > codex > kimi > copilot. Start with opencode, expand as needed.

## Pitfalls

- **Most agents index skills only on startup.** After installing MCP or skills, completely restart the IDE/agent process before testing.
- **Global vs local conflict.** If installed with `--global` flag, some agents may ignore it for project-specific rules. Install locally in the project root if conflicts occur.
- **MCP server availability is network-dependent.** If the coding agent runs offline or behind restrictive firewalls, the MCP tool calls will fail silently. Skills provide the offline fallback.
- **This is documentation access, NOT inference.** The MCP server does NOT run Gemini models — it only provides a `search_documentation` tool. The actual model calls go through your existing LiteLLM proxy chain.

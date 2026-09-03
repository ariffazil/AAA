# Meyhem Research — 2026-05-18

## Context
User asked to "deep research about meyhem MCP and install that tools for [theirs] Hermes agent." Assumed Meyhem was an MCP server to install.

## Finding: Meyhem is an API, not an MCP Server

**Meyhem is NOT a standalone MCP server package.** It is a web search API operated at `api.rhdxm.com`.

### API Details
- **Endpoint**: `POST https://api.rhdxm.com/search`
- **Auth**: None required (zero API key)
- **What it does**: Blends Exa + Tavily in parallel → deduplicates → LLM-re-ranks
- **Docs**: `https://api.rhdxm.com/docs`
- **Freshness param**: `{"query": "...", "max_results": N, "agent_id": "...", "freshness": "hour"}`

### Already Integrated in arifOS
Meyhem is already wired into arifOS as a **search fallback** in `arifosmcp/runtime/reality_handlers.py`:

```
search_meyhem() at line 376
  → Called when Brave search fails AND DDGS (DuckDuckGo) fails
  → tri-search cascade: Brave → DDGS → Meyhem (final fallback)
```

arifOS MCP already uses Meyhem when primary search engines are unavailable.

### No Additional Installation Needed
- OpenClaw has `arifos` MCP configured at `http://127.0.0.1:8080/mcp`
- arifOS MCP includes Meyhem via `search_meyhem()` 
- No separate "Meyhem MCP server" exists on npm, GitHub, or any registry
- Confirmed via: npm search, GitHub API search, direct curl to api.rhdxm.com/docs

## Lesson: Verify Before Proposing "Install"

When user asks to "install X for agent Y":
1. First identify what X actually is (API? MCP server? npm package? skill?)
2. Check if Y already has access to X via existing integration
3. If X doesn't exist as a standalone package, find the existing integration path
4. Only then propose whether installation is needed

The failure mode here would have been: trying to `npm install @meyhem/mcp-server` (doesn't exist) or running `hermes mcp add meyhem` with a non-existent server URL.

## arifOS Search Cascade (for reference)
```
Brave Search (primary, requires API key)
  ↓ failure
DuckDuckGo (ddgs, secondary)
  ↓ failure  
Meyhem (api.rhdxm.com, final fallback — no key required)
```
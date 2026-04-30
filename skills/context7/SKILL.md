---
name: context7
description: Version-specific library docs via Context7 — eliminates SDK/library hallucinations
category: research
---

# Context7 MCP Skill

## Trigger
Any task involving a library, SDK, or API — especially when you need exact version docs.

## Credentials
`CONTEXT7_API_KEY` — set in `/root/.hermes/.env`

Get free key: https://context7.com/ (free tier available)

## What it does
- **Fetch current docs** for a specific library version
- **Eliminates hallucinations** on API signatures, function args, return types
- **Grounded answers** — pulls live from Context7's 9,000+ library database

## Usage
```python
# Hermes calls context7-mcp server with library name + version
# Example: "how do I use langchain v0.2.3 for document loading?"
# Server fetches exact langchain 0.2.3 docs → returns accurate info
```

## Why it matters
Standard RAG/LLM knowledge is cached and often wrong for specific library versions.
Context7 fetches the exact version docs you need, when you need them.

## Notes
- MCP server runs on port 3001 (HTTP transport)
- Handles 9,000+ library docs, refreshed daily
- Tool available: `context7_*` tools via MCP

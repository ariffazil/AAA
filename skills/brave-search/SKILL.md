---
name: brave-search
description: Web search via Brave Search API for arifbfazil@gmail.com — real-time search, no hallucinations
category: research
---

# Brave Search MCP Skill

## Trigger
Any task requiring web search, fact-check, current events, or general internet lookup.

## Credentials
`BRAVE_API_KEY` — set in `/root/.hermes/.env`

Get free key: https://brave.com/search/api/ (free tier: 2,000 queries/month)

## What it does
- **Web search** — queries Brave Search engine, returns titles + snippets + URLs
- **Local search** — image/video/news search variants
- **No hallucination** — pulls live results, not cached LLM knowledge

## Usage
```python
# Via MCP tool call (automatic when Hermes config has brave-search server)
# Hermes routes search queries to the brave-search MCP server automatically

# Example: search for "latest AI news"
# Hermes calls brave-web-search tool → returns structured results
```

## Notes
- Free tier: 2,000 queries/month
- Rate limit: 2 requests/second
- Results include safe search filtering by default
- Tool available: `brave_web_search`, `brave_search`

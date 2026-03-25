---
name: web-search
description: Web search and content extraction using Brave Search API and Firecrawl. Use when: (1) Searching the web for information, (2) Fetching and extracting content from URLs, (3) Research tasks requiring multiple sources, (4) News and current events lookup, (5) Fact-checking or verification.
---

# Web Search Skill

Search the web and extract readable content from URLs.

## Quick Start

### Search the Web

```json
{
  "tool": "web_search",
  "query": "your search query",
  "count": 5,
  "freshness": "week",
  "country": "MY"
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Search query string | required |
| `count` | Results to return (1-10) | 5 |
| `freshness` | Filter by time: day/week/month/year | none |
| `country` | 2-letter country code | US |
| `language` | ISO 639-1 language code | en |

### Fetch URL Content

```json
{
  "tool": "web_fetch",
  "url": "https://example.com/article",
  "extractMode": "markdown",
  "maxChars": 5000
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `url` | HTTP/HTTPS URL to fetch | required |
| `extractMode` | "markdown" or "text" | markdown |
| `maxChars` | Maximum characters to return | unlimited |

## Search Patterns

### Research Workflow

1. **Initial search** — Broad query to find relevant sources
2. **Fetch key URLs** — Extract content from promising results  
3. **Iterative refinement** — Search for specific gaps
4. **Synthesis** — Cross-reference and summarize findings

### Fact-Checking Pattern

```
web_search: "claim to verify" + count:3 + freshness:month
→ web_fetch: top 2-3 sources
→ Compare claims across sources
→ Report confidence level (τ ≥ 0.99 for F2 compliance)
```

## Multi-Source Research

For complex research, use multiple searches:

1. **Context search** — Background/overview
2. **Specific search** — Targeted details
3. **Contradiction search** — Opposing viewpoints
4. **Update search** — Recent developments (freshness:week)

## Output Standards

- Cite sources inline: "Claim [Source: url]"
- Cross-reference for τ ≥ 0.99 confidence
- Flag uncertain claims with Ω₀ ∈ [0.03-0.05]
- Prefer primary sources over aggregators

## Rate Limits

- Brave Search: Respect 429 responses
- Firecrawl: Monitor quota usage
- Add delays between burst requests

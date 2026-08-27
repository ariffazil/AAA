---
name: searxng-search
description: Private, self-hosted web search and URL content reader via SearXNG MCP server (mcp-searxng). Use for privacy-preserving web searches, query suggestions, instance discovery, and converting web pages to markdown.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# SearXNG Private Web Search Skill (`mcp-searxng`)

This skill provides private web search, query autocompletion, instance discovery, and webpage extraction via `mcp-searxng` connected to the arifOS SearXNG instance (`https://mcp.arif-fazil.com/searxng`).

## Available Tools & Signatures

### 1. `searxng_web_search`

Executes web searches with category filtering, time range constraints, language selection, and structured formatting.

**Arguments**:

- `query` (string, required): Search query string.
- `pageno` (integer, optional): Page number (starts at 1, default: 1).
- `time_range` (string, optional): `"day"`, `"week"`, `"month"`, or `"year"`.
- `language` (string, optional): Language code (e.g. `"en"`, `"fr"`, `"de"`, `"all"`).
- `safesearch` (integer, optional): `0` (None), `1` (Moderate), `2` (Strict).
- `min_score` (number, optional): Minimum relevance score (0.0 to 1.0).
- `num_results` (number, optional): Max results to return (1 to 20).
- `categories` (string, optional): Comma-separated categories (e.g. `"news"`, `"science"`).
- `engines` (string, optional): Comma-separated engine names (e.g. `"google,bing,ddg"`).
- `response_format` (string, optional): `"text"` (agent-readable text, default) or `"json"` (raw SearXNG JSON).

### 2. `searxng_search_suggestions`

Fetches query autocompletion suggestions.

**Arguments**:

- `query` (string, required): Partial query string.
- `language` (string, optional): Language code (default: `"all"`).

### 3. `searxng_instance_info`

Discovers exposed categories, engines, locales, and plugins of the SearXNG instance.

**Arguments**:

- `includeEngines` (boolean, optional): Include engine list (default: `false`).
- `includeDisabled` (boolean, optional): Include disabled engines (default: `false`).
- `category` (string, optional): Filter by category.
- `refresh` (boolean, optional): Force cache bypass (default: `false`).

### 4. `web_url_read`

Fetches a webpage URL and converts its body into clean Markdown.

**Arguments**:

- `url` (string, required): Web page URL to read.
- `startChar` (integer, optional): Character offset (default: `0`).
- `maxLength` (integer, optional): Maximum characters to retrieve.
- `section` (string, optional): Extract content under a specific heading text.
- `paragraphRange` (string, optional): Specific paragraph ranges (e.g. `'1-5'`, `'3'`, `'10-'`).
- `readHeadings` (boolean, optional): Return heading hierarchy only.

---

## Usage Guidelines & Best Practices

1. **Prefer `searxng_web_search`** over un-minified raw search tools for private, zero-tracking search.
2. **Combine with `web_url_read`** when full page text extraction is required for synthesis.
3. If SearXNG JSON endpoint returns a 403 or non-JSON payload, `SEARXNG_HTML_FALLBACK: "true"` automatically parses HTML results as a fallback.

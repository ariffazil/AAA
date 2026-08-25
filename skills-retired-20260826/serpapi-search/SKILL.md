---
name: serpapi-search
description: Comprehensive multi-engine search engine API & structured SERP extractor via SerpApi MCP server (mcp.serpapi.com). Supports Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, Google Scholar, stock market, and weather data.
capability_tier: fed-long-context
ecology_state: WARM
---

# SerpApi Multi-Engine Search Skill (`serpapi`)

This skill provides access to SerpApi search engines, real-time SERP extractions, weather, financial data, and interactive search apps via SerpApi MCP server (`https://mcp.serpapi.com/${SERPAPI_API_KEY}/mcp`).

## Available Tools & Signatures

### 1. `search`

Executes multi-engine search queries against Google, Bing, YouTube, Google Scholar, Amazon, eBay, and more.

**Arguments**:

- `params` (object, required):
  - `q` (string, required): Search query string.
  - `engine` (string, optional): Target engine (default: `"google_light"`, e.g. `"google"`, `"google_scholar"`, `"youtube"`, `"ebay"`, `"amazon"`).
  - `location` (string, optional): Geographical location string (e.g. `"Austin, TX"`).
  - `output` (string, optional): Format output (`"json"` default, or `"md"` for Markdown).
- `mode` (string, optional): `"compact"` (strips metadata from JSON to save tokens) or `"complete"`.

### 2. `search_table` *(MCP Apps Extension)*

Renders organic search results as a sortable, interactive table in supporting MCP client UIs.

### 3. `search_dashboard` *(MCP Apps Extension)*

Renders summary metrics, source breakdowns, and interactive result panels.

---

## Usage Guidelines & Best Practices

1. **Markdown mode (`output: "md"`)**: Cuts token consumption by up to 90% for nested SERP results.
2. **Compact mode (`mode: "compact"`)**: Strips unnecessary metadata to keep context lightweight.
3. Requires `SERPAPI_API_KEY` set in the environment or host config path `/YOUR_KEY/mcp`.

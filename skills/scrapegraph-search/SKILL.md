---
name: scrapegraph-search
description: AI-powered web scraping, multi-format page extraction, async crawling, schema generation, and monitoring via ScrapeGraph AI MCP server (scrapegraph-mcp).
capability_tier: fed-long-context
ecology_state: WARM
---

# ScrapeGraph AI Web Scraping Skill (`scrapegraph-mcp`)

This skill provides advanced AI-powered web scraping, structured extraction, search, async crawling, schema synthesis, and monitoring via the ScrapeGraph MCP server (`https://sgai-mcp-main.onrender.com`).

## Available Tools & Signatures

### 1. `scrape`

Scrapes web content with specified output formats.

**Arguments**:

- `url` (string, required): Web page URL to scrape.
- `output_format` (string, optional): `"markdown"`, `"html"`, `"screenshot"`, `"branding"`, `"links"`, `"images"`, `"summary"`.

### 2. `extract`

Extracts structured data from a target website using an AI user prompt and schema.

**Arguments**:

- `website_url` (string, required): Target URL.
- `user_prompt` (string, required): Natural language extraction instruction.
- `output_schema` (object, optional): Desired JSON schema for extracted output.

### 3. `search`

Executes search query and extracts web content.

**Arguments**:

- `query` (string, required): Search query.
- `num_results` (integer, optional): Number of results (3 to 20).
- `country_search` (string, optional): Geographic bias.

### 4. `crawl_start` / `crawl_get_status` / `crawl_stop`

Initiates async multi-page crawling and retrieves status results.

### 5. `schema`

Generates or augments JSON schema from a natural language prompt.

---

## Usage Guidelines & Best Practices

1. Use `scrape` with `output_format: "markdown"` for clean text extraction.
2. Use `extract` when specific JSON structures or attributes (prices, tables, specs) are requested.
3. Requires `SGAI_API_KEY` set in the environment or request header `X-API-Key`.

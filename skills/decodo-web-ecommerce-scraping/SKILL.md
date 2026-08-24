---
name: decodo-web-ecommerce-scraping
description: Web scraping layer for AI agents via Decodo MCP server (mcp.decodo.com). Scrape JavaScript-heavy web pages to Markdown/JSON/screenshots, search engines (Google, Bing), eCommerce (Amazon, Walmart, Target, TikTok Shop), social media (Reddit, TikTok, YouTube), and AI search (ChatGPT, Perplexity).
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Decodo Web & eCommerce Scraping Skill (`decodo`)

Decodo provides AI agents with high-success web scraping across 195+ locations with residential proxies, anti-bot handling, and structured LLM outputs via `https://mcp.decodo.com/mcp`.

## Modular Toolsets & Signatures

### 1. `web` Toolset

- **`scrape_as_markdown`**: Scrapes target URL with JS rendering and returns clean Markdown.
- **`screenshot`**: Captures webpage PNG screenshot for visual context.

### 2. `search` Toolset

- **`google_search`** / **`google_ads`** / **`google_lens`** / **`google_ai_mode`** / **`google_travel_hotels`**: Real-time Google SERPs and specialized views.
- **`bing_search`**: Scrapes Bing search results.

### 3. `ecommerce` Toolset

- **`amazon_search`** / **`amazon_product`** / **`amazon_pricing`** / **`amazon_sellers`** / **`amazon_bestsellers`**: Marketplace product and pricing data.
- **`walmart_search`** / **`walmart_product`** / **`target_search`** / **`target_product`**: Retail chain pricing and inventory by ZIP/store ID.
- **`tiktok_shop_search`** / **`tiktok_shop_product`** / **`tiktok_shop_url`**: TikTok marketplace items.

### 4. `social_media` Toolset

- **`reddit_post`** / **`reddit_subreddit`** / **`reddit_user`**: Subreddit threads and engagement.
- **`youtube_metadata`** / **`youtube_channel`** / **`youtube_subtitles`** / **`youtube_search`**: Video metadata and transcript extraction.
- **`tiktok_post`**: Caption, hashtag, and engagement metrics.

### 5. `ai` Toolset

- **`chatgpt`** / **`perplexity`**: Interacts with AI search tools for live answers.

---

## Best Practices for AI Agents

1. **Geo-Targeting**: Pass `geo` parameter (e.g. `"US"`, `"DE"`) to bypass geo-restrictions or test region-specific pricing.
2. **Context Window Protection**: Pass `tokenLimit` (e.g. `50000`) or request `scrape_as_markdown` to keep payloads token-efficient.
3. Requires `SCRAPER_API_TOKEN` set in environment or request header `Authorization: Basic <token>`.

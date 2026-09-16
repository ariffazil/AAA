# Reddit Access Constraints — VPS IP & OAuth Gap

*Verified: 2026-08-26. All findings from live VPS (`af-forge`, 72.62.71.199).*

## Three-Lane Reddit Access Matrix

| Lane | Method | OAuth? | Works from VPS? | Notes |
|------|--------|--------|-----------------|-------|
| **1. web_search_social** | `mcp__social_mcp__web_search_social(platform="reddit")` | No | **YES** | Firecrawl search backend. Returns `{title, url, description}`. `url` is canonical permalink. |
| **2. Composio Reddit** | `mcp__composio__REDDIT_SEARCH_ACROSS_SUBREDDITS` etc. | Yes | **NO** — OAuth gap | Returns `"No connected account found for user ID arif-federation for toolkit reddit"` |
| **3. Direct scrape** | curl / curl_cffi / Firecrawl scrape | No | **NO** — IP blocked | HTTP 403 from old.reddit.com and www.reddit.com. Firecrawl returns "We do not support this site". |

## The OAuth Gap in Detail

**Root cause:** Two separate user contexts exist:
- MCP proxy (`/root/.config/mcp/composio-proxy.mjs`) uses `user_id=arif-federation`
- CLI binary (`/root/.composio/composio`) authenticates as `arifbfazil@gmail.com`

OAuth connections were made via CLI, so they live under `arifbfazil@gmail.com`. The MCP proxy can't see them.

**Symptom:** Every `REDDIT_*` Composio slug returns:
```
"No connected account found for user ID arif-federation for toolkit reddit"
```

**Fix options:**
1. Link Reddit OAuth at `dashboard.composio.dev` under the proxy's `arif-federation` user context
2. Update MCP proxy user_id to `arifbfazil@gmail.com`
3. Switch social-mcp's ComposioClient to CLI subprocess (preferred — reuses existing auth)

**Current workaround:** Use `web_search_social` for all Reddit discovery. It returns enough signal (title, snippet, canonical permalink) for sweep-stage synthesis.

## VPS IP Reddit Block

Reddit's anti-bot system blocks this VPS IP at the edge. Tested:
- `curl -H "User-Agent: Mozilla/5.0" https://old.reddit.com/...json` → HTTP 403
- `curl_cffi` with `impersonate="chrome"` → HTTP 403
- `www.reddit.com` → HTTP 403
- Firecrawl `firecrawl_scrape` → "We do not support this site"

This is a hard block — no User-Agent trick or browser impersonation bypasses it. The VPS IP is on Reddit's blocklist.

## Chaining web_search_social → reddit_get_comments

When Composio Reddit OAuth is connected, the two tools chain naturally:
1. `web_search_social(query, platform="reddit")` → returns `{url: "https://www.reddit.com/r/sub/comments/id/slug/"}`
2. `reddit_get_comments(article=<that_url>)` → returns full comment tree

The `url` field from `web_search_social` is the exact format `article=` expects. Don't try to construct it manually.

## Impact on Exploration Workflow

For open-ended Reddit exploration ("explore Reddit for X"), the workflow is:
1. **Sweep:** `web_search_social` with 5-10 parallel queries → snippets + permalinks
2. **Dive:** `reddit_get_comments(article=<permalink>)` IF OAuth connected (currently blocked)
3. **Synthesize:** Group into validates/gap/candidate/noise

Without Composio Reddit, step 2 is unavailable — synthesis relies on snippets alone. This is usually sufficient for gap-finding but insufficient for deep community sentiment analysis.

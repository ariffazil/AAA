---
name: forge-web-intelligence
description: "Use when fetching web content via A-FORGE forge_web_extract."
version: 1.0.0
owner: AAA
tags: [web, forge, A-FORGE, MCP, temporal, extraction]
---

# forge-web-intelligence

## What this skill does

A-FORGE MCP server (`forge_web_extract` on port 7072) provides agentic web access to ALL AAA agents — including browser rendering, downloads, cookie/header injection, and SSRF protection. This skill documents the tool and its **epistemological pitfalls** so agents don't repeat known failure modes.

## When to use this skill

Use forge_web_extract INSTEAD of Hermes built-in `web_extract` when:
- The target is a SPA (React, Next.js, Drupal) that returns empty shells on static fetch
- You need browser rendering (click, scroll, wait, type)
- You need custom cookies/headers (auth, session, anti-bot)
- You need to download files to host filesystem
- You need SSRF protection (internal services should NOT be fetched)

## Tool discovery

forge_web_extract is in the deferred tool catalog. Load it with:
```
tool_search(queries=['forge_web_extract'])
tool_describe(names=['forge_web_extract'])
```
Then invoke with `tool_call`.

## Routing table

| Need | Tool | Why |
|---|---|---|
| Static page, fast | web_extract | Built-in, char_limit, head+tail |
| SPA / JS-rendered | forge_web_extract | Browser auto-detect + render |
| Click/scroll/type | forge_web_extract | Browser actions built-in |
| File download | forge_web_extract | Writes to /root/forge-downloads/ |
| Auth session | forge_web_extract | Cookie + header injection |
| Multi-tab workflow | browser_exec | Session-persistent tabs |
| Search + extract combo | firecrawl MCP | search -> scrape pipeline |

## SSRF protection (built-in)

forge_web_extract blocks:
- localhost, 127.0.0.1, 169.254.169.254 (metadata)
- 192.168.x.x, 10.x.x.x (private IPs)
- file:// protocol
- Non-standard ports

**Never** try to bypass SSRF guards.

## CRITICAL: Temporal Validation Protocol

**The problem:** When you fetch a live corporate page, HTTP headers may reflect cache serve time, not content edit time. Drupal sites regenerate etag on every cache cycle.

**The protocol (mandatory for governance/corporate pages):**
1. Fetch content via forge_web_extract
2. Pull HTTP headers separately (curl -sI)
3. Pull sitemap.xml <lastmod> for that URL
4. Cross-reference — if Last-Modified is close to now, treat as CACHE ARTIFACT
5. Wayback Machine CDX diff is gold standard for delta-t detection

## Moving-source discipline

When analyzing a page that may change between OPEN and CLOSE of your research:
1. **OPEN:** Snapshot content + headers + sitemap timestamp at research start
2. **DURING:** Note any wayback snapshots in the gap
3. **CLOSE:** Re-fetch before synthesis — compare with OPEN snapshot
4. **If changed:** Flag as MOVING_SOURCE and re-analyze

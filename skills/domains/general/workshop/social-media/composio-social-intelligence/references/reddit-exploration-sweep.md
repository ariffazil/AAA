# Reddit Exploration Sweep — Multi-Query Signal Discovery

*Forged: 2026-08-26. Pattern validated in live session.*

## When to Use

- "Explore Reddit for X" — open-ended signal gathering across domains
- Monitoring a topic landscape before deciding what matters
- Comparing a new tool/project against existing federation stack

## Technique: 10-Query Parallel Sweep

**Phase 1 — Fan out 5+ independent searches in a single turn.** Each query targets a different angle of the same domain. Use `reddit_search_posts` with `limit=10`. Parallel calls execute concurrently.

Example queries for "AI agent infrastructure":
```
MCP server self-hosted sovereign AI agent
self-hosted AI agent infrastructure VPS production
agentic trading system gold XAUUSD AI bot
constitutional AI agent governance multi-agent trust layer
edge AI agent low-resource VPS CPU inference local
WhatsApp Telegram AI agent bot bridge personal assistant
```

**Phase 2 — Read top results from each hit set.** Sort by score × recency. Save large payloads to `/tmp/hermes-results/` then read selectively (offset/limit) — don't load 400K chars into context.

**Phase 3 — Dive 2-3 deep threads.** Use `reddit_get_comments(article=<permalink_url>)` — note: the param is `article`, NOT `post_id` (see schema pitfalls in main skill).

**Phase 4 — Synthesize across all signals.** Group findings into:
- **Validates our approach** — confirms architecture choices
- **Exposes a gap** — something we lack that others have
- **Candidate for adoption** — new tool/project worth integrating
- **Noise** — signal too weak, discard

## Three-Lane Routing (verified 2026-08-26)

Reddit access from this VPS has three lanes, in priority order. Pick by what you need, not by habit. Full constraint details in `references/reddit-access-constraints.md`.

| Lane | Tool | OAuth? | Blockers | When to use |
|------|------|--------|----------|-------------|
| **1. Public web search** | `web_search_social(platform="reddit", query, limit)` | No | None observed | First pass — discovery, monitoring, gap-finding |
| **2. Composio Reddit** | `reddit_search_posts`, `reddit_browse`, `reddit_get_comments` | **Yes — account required** | "No connected account found for user ID arif-federation" until connected | Logged-in browsing, comment trees, anything needing OAuth context |
| **3. Direct scrape** | curl / curl_cffi / firecrawl_scrape | No | VPS IP blocked at HTTP 403 by old.reddit.com & www.reddit.com; Firecrawl returns "We do not support this site" | Only as last resort; expect to be blocked |

**The fallback chain that actually worked today:**
1. `web_search_social` returns snippets + canonical permalinks
2. Extract the `url` field — it's always `reddit.com/r/<sub>/comments/<id>/...`
3. To dive deeper, hand that URL to `reddit_get_comments(article=<url>)` IF Composio Reddit is connected
4. If not, the snippet + title + score is usually enough for sweep-stage synthesis

**Composio Reddit OAuth status (2026-08-26):** Connections exist under `arifbfazil@gmail.com` (CLI auth context) but NOT under `arif-federation` (MCP proxy user_id). Symptom: every `REDDIT_*` call returns `"No connected account found for user ID arif-federation for toolkit reddit"`. Fix path: link Reddit at `dashboard.composio.dev` under the proxy user_id, OR continue relying on `web_search_social` until then. Until account linking lands, treat `web_search_social` as the primary Reddit lane.

## Key Pitfalls

- `reddit_get_comments` requires `article` (permalink URL), not `post_id`. This caused a 3× retry loop on 2026-08-26.
- `web_search_social` URL output format — the `url` field is the canonical permalink you feed into `article=`. Don't try to construct it from search snippets; just copy the field verbatim.
- Composio `REDDIT_*` tools all fail with `"No connected account"` until Reddit OAuth is linked to the proxy's `arif-federation` user_id. Don't loop trying different slugs; switch to `web_search_social`.
- VPS IP is blocked by Reddit's anti-bot at the edge (HTTP 403 on both old.reddit.com and www.reddit.com JSON endpoints). `curl_cffi` browser impersonation does NOT bypass it. Firecrawl refuses reddit.com outright with "We do not support this site".
- Large result sets (300K+ chars) get saved to disk — use `read_file` with offset/limit, don't try to parse inline.
- Search quality varies: broad queries ("AI agents") return noise; specific queries ("MCP server registry discovery") return signal.
- Recency matters: filter mentally for posts < 6 months old. Older results may describe dead projects.
- Score threshold: posts > 200 upvotes usually have substantive comments worth diving into.

## Domain-Specific Query Templates

**Federation/tool evaluation:**
```
MCP server [tool name] review comparison
self-hosted [tool] vs [alternative] 2025 2026
[tool] production experience reddit
```

**Biohacking/health:**
```
peptide [compound name] protocol stack
[compound] dosage timing cycle reddit
biohacking [target] 2025 2026
```

**Trading/wealth:**
```
AI trading bot [asset class] results
automated trading [strategy] backtest
[platform] agentic trading API
```

**Sovereign AI / governance:**
```
AI agent safety guardrails production
constitutional AI governance multi-agent
self-hosted AI data sovereignty
```

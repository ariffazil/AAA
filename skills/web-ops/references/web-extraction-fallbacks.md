<!-- PROVENANCE: source_skill=web-extraction-fallbacks -->
<!-- original_path=/root/AAA/skills/domains/general/workshop/search-web/web-extraction-fallbacks/SKILL.md -->
<!-- original_sha256=6b06314c0be6642198f2c3c03a972a8149c08b4e9b88fb499c08e448151ac125 · archived_to=/root/AAA/skills/.archive/merge-20260920/web/web-extraction-fallbacks/ -->
<!-- body_verbatim=true · merged_at=2026-09-20T14:39:14Z · umbrella=web-ops -->
---
id: web-extraction-fallbacks
name: web-extraction-fallbacks
version: 1.1.0-2026.08.27
description: "Use when a URL extraction fails — blocked, paywalled, rate-limited or bot-walled. Ordered fallback ladders per failure mode."
owner: curator-managed
risk_tier: low
floor_scope: [F7]
autonomy_tier: T1
trigger_phrases:
  - "web extract failed"
  - "searxng cannot extract"
  - "browser timed out"
  - "cloudflare challenge"
  - "read article"
  - "extract url"
  - "fetch page content"
  - "news article extraction"
dependencies:
  mcp_servers: []
  skills: [AGI-agentic-web]
---

# web-extraction-fallbacks — URL Extraction Failure Patterns

> Forged 2026-08-27 from live session failure: 4 browser_exec timeouts + SearXNG extraction rejection on dawn.com article retrieval.
> Companion to AGI-agentic-web — covers the failure modes that doctrine doesn't address.

## When to Use

Use this skill when `web_extract` fails with a SearXNG error, when `browser_exec` times out on a website, or when you need to extract content from a Cloudflare-protected news site. Also use when you find yourself retrying the same extraction method repeatedly — this skill's decision tree prevents wasted turns.

---

## PATTERN 1: SearXNG Search-Only Backend

**Trigger:** `web_extract` returns `"SearXNG is a search-only backend and cannot extract URL content"`

**Root cause:** SearXNG on this VPS is configured as a search aggregator, not a content extractor. This is NOT a transient error — it will never work for URL extraction.

**Fallback (immediate — do NOT retry web_extract):**

1. `web_search("site:domain.com <key terms>")` → get article title + description from snippet
2. `web_search("<topic keywords>")` → cross-reference 2-3 snippets to reconstruct story
3. If snippets insufficient: `browser_exec` (only if site is NOT Cloudflare-protected)

**Time budget:** 0 retries on web_extract. Pivot after first failure.

---

## PATTERN 2: Cloudflare-Protected News Sites

**Trigger:** `browser_exec` times out (30-60s) OR curl returns `"Just a moment... Enable JavaScript and cookies"`

**Known Cloudflare-protected sites (as of 2026-08-27):**
- dawn.com, bbc.com, straitstimes.com, rappler.com, freemalaysiatoday.com
- Most major news sites

**Root cause:** Headless browser cannot solve Cloudflare JS challenges.

**Fallback (skip browser entirely):**

1. `web_search("<exact article topic>")` → snippets from multiple sources
2. Cross-reference 2-3 search results for key facts
3. For deep detail: search for investigation/report name specifically

**Time budget:** Maximum 1 browser_exec attempt. If timeout, go straight to search-snippet reconstruction.

---

## PATTERN 1B: Playwright Binary Missing (web_extract infra failure)

**Trigger:** `web_extract` returns `Failed to launch chromium because executable doesn't exist at /root/.cache/ms-playwright/chromium-.../chrome-linux64/chrome`

**Root cause:** The Playwright binary that `web_extract` uses internally is not installed on this VPS. This is NOT a site block — it is an infrastructure gap. Every URL will fail the same way.

**Fallback (skip web_extract entirely — go straight to browser_exec DOM extraction):**

1. `browser_exec` with `new_tab(url)` → opens the page in Browser Use (separate browser backend)
2. `wait_for_load()` → ensures page renders
3. `js('''(() => { const selectors = ['article', '.post-content', '.entry-content', '.content', 'main', '#content']; for (const sel of selectors) { const el = document.querySelector(sel); if (el && el.textContent.trim().length > 200) return el.textContent.trim(); } return document.body.textContent.trim(); })()''')` → extracts text from DOM
4. If truncated, continue with `js()` pagination

**Why this works:** `browser_exec` uses Browser Use's own Chromium, not Playwright. Different binary, different installation path. The two tools are independent browser backends.

**Time budget:** 0 retries on web_extract. First failure with Playwright error → pivot to browser_exec immediately.

---

## PATTERN 3: Combined Failure (SearXNG + Cloudflare)

**The scenario:** User shares a news URL from a Cloudflare-protected site. `web_extract` fails (SearXNG). `browser_exec` times out (Cloudflare). Both primary methods dead.

**Recovery — search-snippet reconstruction:**

1. Extract domain from URL (e.g., `dawn.com`)
2. `web_search("site:dawn.com <path or ID from URL>")` → identify article title
3. `web_search("<article title> full text OR summary>")` → get details from other sources
4. `web_search("<key entity> <event> report 2026")` → find original report/study
5. Synthesize from 3-5 snippets. Label as `[DER]` derived, not `[OBS]`.

**Session example (dawn.com/news/2025504):**
- `site:dawn.com 2025504` → title: "Nearly 700 AI agents coordinated attack on Hugging Face"
- Broader search → Straits Times, Reuters, METR coverage
- "METR investigation OpenAI agents" → primary source found
- Comprehensive summary from 5+ snippet sources, no full page extraction needed

---

## PATTERN 4: Total Web Infrastructure Outage

**Trigger:** ALL of the following simultaneously:
- `web_search` returns timeout or empty results (SearXNG unreachable)
- `web_extract` returns SearXNG error or timeout
- `browser_exec` times out (30-90s)
- `curl` to major search engines (DDG, Bing, Google) returns empty or garbage

This is not a single-site block — it's a full web research infrastructure failure (VPS network issue, SearXNG process down, or upstream search engine rate-limiting the datacenter IP).

**Recovery — session_search on prior conversations:**

1. `session_search(query="<topic keywords>", limit=5)` — search past Hermes conversations for the same or similar topic
2. If hits found: `session_search(session_id="<id>", around_message_id=<match_id>, window=15)` — pull the full conversation window
3. The prior session's tool outputs (search results, extracted articles, analysis) are your data source
4. Synthesize from prior session data, clearly labeling: "Based on prior research session [date]"
5. If NO session history exists → report honestly: "All web research channels are down. No prior data on this topic. I can retry when infrastructure recovers, or you can paste the source."

**Time budget:** Maximum 2 session_search calls. If no hits, STOP — do not burn turns retrying dead web tools.

**Critical rule:** Session-search recovery only works when you've researched the SAME or closely related topic before. For genuinely new topics with zero session history, this pattern cannot help — you must wait for infrastructure recovery or get the data from the user.

**Proven:** 2026-08-27 — SearXNG down + browser timeout + curl blocked. `session_search(query="KPJ corporate drama")` found a prior deep-dive session with full analysis. Recovered complete story (Chin Keat Chyuan resignation, Bumiputera displacement letter, Johor Corporation political capture) from session history alone.

---

## PATTERN 5: SearXNG Down, VPS Internet Up — Direct-Curl Recovery

**Trigger:** `web_search` returns `Could not reach SearXNG at http://127.0.0.1:8080: [Errno 111] Connection refused` AND `web_extract` returns the SearXNG search-only error — but you still need to verify a public claim (site live? repo exists? project indexed? what does the public web say?).

**Key correction to PATTERN 4:** PATTERN 4 assumed "curl to DDG returns garbage" during any SearXNG failure. FALSE — SearXNG can be down while the VPS's own internet path is perfectly fine. Do NOT jump to session_search until you've tried direct curl from the VPS.

**Recovery — direct curl ladder (no API keys, from VPS terminal):**

1. **Fetch the site itself + strip HTML to text** — confirms live + what it claims (`<title>`, meta, first text block). `curl -sL --max-time 20 <url> | python3 -c "...re.sub('<[^>]+>', ' ', raw)..."` (full recipe in reference)
2. **DuckDuckGo HTML endpoint** (search-only, no key): `curl -s --max-time 20 "https://html.duckduckgo.com/html/?q=%22<exact+phrase>%22+<context>" -A "Mozilla/5.0"` → parse `result__a` + `result__snippet` — proves search-index presence (what an LLM's training/search would see)
3. **GitHub API search** (public repos, no key): `curl -s "https://api.github.com/search/repositories?q=<term>&sort=stars"` → `total_count` + name/desc/stars/updated — hard evidence of public presence
4. **PyPI** (if packages published): `curl -s "https://pypi.org/pypi/<package>/json"` → `info.summary`

**Verdict rule:** "X is known/indexed" claims need ≥2 independent surfaces. Proven 2026-08-30: arifOS claim confirmed with 4 surfaces — site title ("Exploration Geoscientist & Sovereign Systems") + GitHub repo (ariffazil/arifOS, 51 stars, updated 2026-08-29) + PyPI packages (arifos, arifosmcp) + DDG snippet ("Builder of arifOS — a constitutional AI governance kernel"). One surface alone (e.g. site loads) is weak.

Full recipe + pitfalls: `references/direct-curl-recovery.md`

---

## DECISION TREE

```
User asks for web content / research
  │
  ├─ Is it a search query (not a specific URL)?
  │   └─ YES → web_search directly (no extraction needed)
  │
  ├─ Try web_extract
  │   ├─ Success → return content
  │   ├─ SearXNG error → PATTERN 1 fallback
  │   └─ Playwright binary missing → PATTERN 1B (browser_exec DOM extraction)
  │
  ├─ Try browser_exec (if PATTERN 1 insufficient)
  │   ├─ Success → return content
  │   └─ Timeout / Cloudflare → PATTERN 2 fallback
  │
  ├─ PATTERN 3 (search-snippet reconstruction)
  │   └─ Both web_extract + browser failed
  │
  └─ PATTERN 4 (session-search recovery)
      └─ ALL web tools dead (search + extract + browser + curl)
         └─ Prior session exists? → recover from session history
         └─ No prior session? → report gap, wait or ask user

  └─ PATTERN 5 (direct-curl recovery)
      └─ SearXNG errors but VPS internet up? → curl site + DDG HTML + GitHub API + PyPI
         └─ ≥2 surfaces → verdict confirmed
```

---

## TEMPORAL VALIDATION (CRITICAL — 2026-09-14 lesson)

Web extraction returns content but does NOT guarantee temporal accuracy. Two session failures traced to agents treating cache artifacts as content-change timestamps.

### Drupal/cache-heavy sites (petronas.com, government portals)
- `Last-Modified` header reflects **cache serve time**, not content edit time
- Drupal regenerates `ETag` on every cache cycle — every page appears "modified today"
- **Detection:** fetch 4-5 sibling pages on same domain. If ALL show "today" → cache artifact
- **Fix:** pull `sitemap.xml <lastmod>` for the specific URL — reflects actual CMS save time
- **Gold standard:** Wayback Machine CDX diff between two snapshots — only reliable Δt

### Dynamic marketplaces (AliExpress, Amazon, Shopee)
- Prices, stock, ratings change hourly — scraped data is point-in-time only
- **Always record:** `retrieved_at` timestamp + URL + any visible date markers in content

### Moving-source protocol
When analyzing a page that may change between OPEN and CLOSE of your research:
1. **OPEN:** Snapshot content + HTTP headers + sitemap timestamp
2. **DURING:** Note any Wayback snapshots in the gap
3. **CLOSE:** Re-fetch before synthesis — compare with OPEN snapshot
4. **If changed:** Flag as MOVING_SOURCE and re-analyze

See: `hermes-deep-research` Layer 0.5, `forge-web-intelligence` skill.

## TOOL ROUTING: forge_web_extract

For SPA sites, browser actions, or authenticated extraction, use `forge_web_extract` (A-FORGE MCP on port 7072). See `forge-web-intelligence` skill for full routing table.

| Need | Preferred tool |
|---|---|
| Static page, fast | `web_extract` or Firecrawl `scrape` |
| SPA / JS-rendered | `forge_web_extract` (auto-detect + browser render) |
| Click/scroll/type | `forge_web_extract` (browser actions) |
| File download | `forge_web_extract` (writes to /root/forge-downloads/) |
| Auth session | `forge_web_extract` (cookie + header injection) |
| Search discovery | Firecrawl `search` or `web_search` |

---

## ANTI-PATTERNS

| ❌ | ✅ |
|---|---|
| Retrying web_extract after SearXNG error | Pivot to web_search immediately |
| Retrying web_extract after Playwright binary error | Pivot to browser_exec DOM extraction immediately |
| 3+ browser_exec attempts on same URL | Maximum 1 attempt, then search fallback |
| Treating snippet-derived content as `[OBS]` | Label as `[DER]` — synthesized from snippets |
| Long timeout on browser_exec (>60s) | Fail fast, reconstruct from search |
| Retrying dead web tools during full outage | Try session_search once, then STOP |
| Assuming full outage from SearXNG errors alone | Try direct curl (DDG HTML + GitHub API + PyPI) — VPS internet may be fine |
| Verdict on one surface ("site loads = claim true") | ≥2 independent surfaces for "known/indexed" claims |
| Synthesizing from session history without dating it | Label "Based on prior research session [date]" |

---

*Forged: 2026-08-27 from live session. DITEMPA BUKAN DIBERI. ⚒️*

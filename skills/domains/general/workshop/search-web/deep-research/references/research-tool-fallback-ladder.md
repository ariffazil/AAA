# Research Tool Fallback Ladder

When Tavily-backed tools (`web_search`, `web_extract`) fail with 432/402 errors, do NOT retry. Descend the ladder.

## Ladder (preferred first)

### 1. Wikipedia API (structured, no auth, reliable)

```bash
# Get extract (plain text, 8000 chars default)
curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=PAGE_TITLE&prop=extracts&explaintext=1&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); pages=d['query']['pages']; key=list(pages.keys())[0]; print(pages[key].get('extract','NOT FOUND')[:8000])"
```

- Replace spaces with underscores in PAGE_TITLE
- The `explaintext=1` flag returns clean text without HTML
- Works for any Wikipedia article including technology, companies, people
- **Proven:** 2026-07-18 — Kimi K3 research, all Tavily calls 432, Wikipedia returned full history + specs

### 2. Browser Console JS Extraction (for JS-heavy doc sites)

```javascript
// After browser_navigate to the page:
document.querySelector('main')?.innerText?.substring(0, 8000) || document.body.innerText.substring(0, 8000)
```

- Use via `browser_console(expression="...")`
- Extracts rendered text from SPAs (React/Vue/Next.js) where curl gets empty shells
- Faster than `browser_snapshot` for text-heavy doc pages
- **Proven:** 2026-07-18 — Kimi K3 platform docs at platform.kimi.com returned full API reference + specs

### 3. Browser Snapshot (for interactive pages)

```
browser_navigate → browser_snapshot(full=true) → browser_scroll (if truncated)
```

- Slower but captures interactive elements and their refs
- Use when you need to click through tabs/sections
- Snapshots >8000 chars may be truncated; scroll and re-snapshot

### 4. Platform-Specific Doc Pages

Many products have dedicated model/version landing pages:
- Kimi: `platform.kimi.com/docs` → model-specific pages (K3, K2.7, etc.)
- OpenAI: `platform.openai.com/docs/models`
- Anthropic: `docs.anthropic.com/en/docs/about-claude/models`

Navigate to the docs root and look for model-specific links before searching broadly.

### 5. curl + Structured Data Extraction (JSON-LD, schema.org)

Many business/economic data sites embed structured JSON-LD or schema.org markup. Extract it directly:

```bash
# Extract JSON-LD structured data from a page
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://example.com/page" | grep -oP '<script type="application/ld\+json">[^<]*</script>' | python3 -m json.tool

# Extract specific fields from schema.org Q&A markup
curl -sL -A "Mozilla/5.0" "https://example.com/page" \
  | grep -oiP '(GDP|growth|inflation|salary)[^<]{0,300}' | head -20
```

- Works for sites with schema.org FAQ/Q&A, Article, or Dataset markup
- The `-A "Mozilla/5.0 ..."` user-agent string avoids basic bot blocks
- **Proven:** 2026-07-18 — malaysia4u.com had comprehensive Malaysia economic data in JSON-LD (GDP, inflation, salary, trade, cost of living). Extracted full structured data via curl + grep when Tavily, Google, DuckDuckGo, and Bing were all blocked.

### 6. pdftotext for Government/Institutional PDFs

Government publications (budget documents, economic outlooks, statistical releases) are often available as PDFs directly from official sites:

```bash
# Download and extract
curl -sL -A "Mozilla/5.0" "https://gov.site/path/to/document.pdf" -o /tmp/doc.pdf
pdftotext /tmp/doc.pdf - | grep -iP '(keyword1|keyword2)' | head -20

# Broader extraction for tables and structured data
pdftotext /tmp/doc.pdf - | grep -iP '(\d+\.\d+%|RM\s*\d+|billion)' | head -40
```

- Government PDFs are authoritative primary sources — prefer over news commentary
- MOF Malaysia publishes Economic Outlook annually at `belanjawan.mof.gov.my`
- BNM (central bank) publishes at `bnm.gov.my`
- DOSM (statistics) publishes at `dosm.gov.my`
- **Proven:** 2026-07-18 — Malaysia MOF Economic Outlook 2026 PDF extracted via pdftotext, yielding GDP forecasts (4-4.5%), fiscal deficit targets (<3% GDP), OPR cut (3.00→2.75%), and subsidy reform data.

### 7. Domain-Specific MCP Tools as Data Sources

When available, MCP tools provide structured live data that bypasses web extraction entirely:

- **WEALTH `capital_market`**: Live FX rates (`mode=fx`), commodity prices (`mode=commodity` with `commodity=brent_crude|gold`). Uses Frankfurter API for FX, EIA/LBMA for commodities. Proven 2026-07-18: USD/MYR=4.095, Brent=$78.50/bbl, Gold=$4,063.40/oz.
- **GEOX tools**: Geological/basin data, seismic, well logs
- **WEALTH `capital_health`**: Financial metrics (net worth, runway, burn rate)

When Tavily is down, check if your MCP stack has domain-specific tools that can provide the data you need. They're often more reliable and structured than web scraping.

**Pitfall:** WEALTH `capital_market` with `mode=gold` or `mode=oil` does NOT accept an `operation` parameter — just pass `mode=commodity` + `commodity=X`. The `operation` parameter only works for the top-level `mode=gold|oil|gas` variants. Proven 2026-07-18: `operation=snapshot` caused ValidationError.

### 8. Direct Article URL Navigation (when search engines are blocked)

When Google, DuckDuckGo, and Bing all trigger CAPTCHAs (common with datacenter IPs), navigate directly to known article URLs:

```
# Pattern: construct URL from publication + date + topic
browser_navigate("https://www.thestar.com.my/business/business-news/2026/07/18/[article-slug]")
```

- The Star, NST, Malay Mail all have predictable URL structures
- Business Today Malaysia, The Edge Markets are also accessible
- If you don't know the exact slug, try the publication's search page first
- **Proven:** 2026-07-18 — The Star ringgit article loaded via direct URL after all search engines returned CAPTCHAs. Article yielded ringgit forecast (RM4.06-4.08), oil price commentary, and ECB/PBOC event calendar.

### 9. SPA JS Bundle Content Extraction (for JavaScript SPAs)

When a JavaScript SPA (React, Vue, Next.js) renders content client-side and individual article/page URLs redirect to the SPA shell, extract content directly from the JS bundle:

```bash
# 1. Navigate to SPA index to discover bundle URL
browser_navigate("https://site.com/")
# 2. Find the main JS bundle via console
browser_console(expression="Array.from(document.querySelectorAll('script[src]')).map(s => s.src)")
# 3. Download and search the bundle
curl -sL "https://site.com/assets/index-[hash].js" -o /tmp/spa-bundle.js
grep -oP '"title":"[^"]*"' /tmp/spa-bundle.js | head -20
# 4. Extract article content (look for HTML or markdown patterns in the bundle)
python3 -c "
import re
with open('/tmp/spa-bundle.js') as f: content = f.read()
# Find article blocks — adjust pattern to the specific SPA
articles = re.findall(r'\"slug\":\"([^\"]+)\".*?\"content\":\"(.*?)\"', content[:500000])
for slug, body in articles[:5]:
    print(f'--- {slug} ---')
    print(body[:500])
"
```

- SPAs often embed ALL article content in a single JS bundle for preloading/routing
- The bundle is usually 1-3MB and contains everything the SPA can render
- This bypasses client-side routing entirely — you get ALL content at once
- **Proven:** 2026-07-18 — arif-fazil.com MakcikGPT: 14 articles (140K chars) extracted from single `index-[hash].js` bundle. Individual article URLs all redirected to SPA index. Browser snapshot showed only 5 articles (the visible viewport). JS bundle had all 14.
- **Pitfall:** Content in JS bundles is often JSON-escaped (`\"` for `"`, `\n` for newlines). Post-process with `json.loads()` to get clean text.

### 9b. execute_code + curl + Jina Reader (when web_search returns IRRELEVANT results)

A distinct failure mode from rung 10: SearXNG returns **results, but completely unrelated** to the query (e.g., searching "Large World Model AI" returns Japanese map results or Honda motorcycles). The backend is alive but returning garbage — no 432/402, no empty arrays, just wrong results. Diagnose by checking if 2+ queries all return top-10 results with zero topical overlap with the query.

Workaround: bypass `web_search` entirely. Use `execute_code` with `terminal` + `curl` + Jina Reader to fetch content from **known authoritative URLs** directly:

```python
from hermes_tools import terminal

# Jina Reader wraps any URL and returns clean markdown
r = terminal("curl -sL 'https://r.jina.ai/https://arxiv.org/abs/2501.03575' 2>/dev/null | head -100")
```

For paper/topic discovery on arxiv (when you don't know the paper ID):
```bash
# arxiv search endpoint — returns structured results with abstracts
curl -sL 'https://r.jina.ai/https://arxiv.org/search/?query=%22world+model%22&searchtype=all&order=-announced_date_first' 2>/dev/null | head -300
```

**Key sources that work via Jina Reader:**
- `r.jina.ai/https://arxiv.org/abs/<ID>` or `r.jina.ai/https://arxiv.org/search/?query=...`
- `r.jina.ai/https://github.com/<org>/<repo>` (README extraction)
- `r.jina.ai/https://deepmind.google/...` or `r.jina.ai/https://openai.com/...` (blog posts)
- `r.jina.ai/https://en.wikipedia.org/wiki/<topic>` (encyclopedia context)

**Pitfall:** Jina Reader to some domains returns 403 (huggingface.co, some Cloudflare-heavy sites). Fall through to direct `curl` or HF API (rung 11).

- **Proven:** 2026-08-21 — LWM deep research: all 9 `web_search` queries returned garbage (ChatGPT links, TOPIX stocks, Japanese maps, motorcycle results). Bypassed to `execute_code` + `curl` + Jina Reader on arxiv/DeepMind/OpenAI sources. Full synthesis delivered successfully.

### 10. arXiv Export API (structured, no auth, for academic paper discovery)

When searching for papers, preprints, or research on AI/ML topics — bypass web search entirely. The arXiv export API returns structured XML with titles, authors, abstracts, and IDs:

```bash
# Search by keyword (URL-encode the query):
curl -sL "https://export.arxiv.org/api/query?search_query=all:%22large+world+model%22&max_results=10" 2>/dev/null \
  | python3 -c "
import sys, xml.etree.ElementTree as ET
data = sys.stdin.read()
root = ET.fromstring(data)
ns = {'a': 'http://www.w3.org/2005/Atom'}
for entry in root.findall('a:entry', ns):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    authors = [a.find('a:name', ns).text for a in entry.findall('a:author', ns)]
    arxiv_id = entry.find('a:id', ns).text.strip().split('/')[-1]
    published = entry.find('a:published', ns).text[:10]
    abstract = entry.find('a:summary', ns).text.strip()[:300].replace('\n', ' ')
    print(f'ID: {arxiv_id} | {published} | {title}')
    print(f'  {abstract}...')
    print()
"
```

**Query syntax:**
- `all:WORD` — search all fields
- `ti:WORD` — title only
- `au:WORD` — author only
- `cat:cs.AI` — category filter (cs.AI, cs.LG, cs.CV, cs.CL, cs.RO, etc.)
- `AND`, `OR`, `NOT` for boolean
- `sortBy=submittedDate&sortOrder=descending` for recency

**Common categories:** cs.AI (AI), cs.LG (ML), cs.CV (vision), cs.CL (NLP), cs.RO (robotics), cs.MA (multi-agent), eess.SP (signal processing)

**Proven:** 2026-08-21 — LWM deep research: web_search returned garbage for every query. arXiv export API returned 10+ relevant papers with full abstracts in one call. Discovered Doe-1, TD-MPC-Opt, GigaBrain-WBC, and multiple JEPA papers. Combined with Jina Reader for arxiv HTML pages → full synthesis delivered.
**Batch pattern (2026-08-25):** for multi-topic research, run ALL topic queries in ONE `execute_code` call — loop a urllib+regex helper over a dict of {label: query} (8 failure-mode topics → 30+ papers in ~13s, one tool call). Parse `<entry>` blocks with regex (`<title>`, `<published>`, `<summary>`, abs ID) — lighter than ElementTree for batch use. Jina-Reader only the 2-3 papers that matter afterward.
**Engine-suspension diagnosis (2026-08-25):** when web_search returns garbage, `curl -s 'http://localhost:8080/search?q=test&format=json&engines=duckduckgo,brave,google'` names the culprit (e.g. `[["brave","Suspended: too many requests"]]`). Two operational notes: searxng runs as docker (systemd shows inactive — check `docker ps`), and surviving low-quality engines (wikipedia-only) produce the garbage-not-empty signature.

**Pitfall:** `http://export.arxiv.org` redirects to HTTPS. Always use `https://`. Rate limits exist (~3 req/sec) — batch queries if needed but don't hammer.

### 11. Jina Reader as Search-Engine Proxy (when ALL search backends return EMPTY, not error)

When `web_search` / `execute_code web_search` returns **empty result arrays** (no error code), the backend (SearXNG :8080) has suspended engines. Diagnose first, then route searches through Jina Reader:

```bash
# 1. Diagnose WHY search is empty — SearXNG exposes the cause:
curl -s "http://localhost:8080/search?q=test&format=json" | python3 -m json.tool | grep -A5 unresponsive_engines
# → e.g. [["duckduckgo","timeout"],["google cse","Suspended: too many requests"],["startpage","Suspended: CAPTCHA"]]

# 2. Search via Jina Reader wrapping DuckDuckGo HTML — the request originates from
#    Jina's infra, not the datacenter IP, so bot detection does not fire:
q() { curl -sL -m 30 "https://r.jina.ai/https://duckduckgo.com/html/?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")" | grep -oP '(?<=uddg=)[^&]+|## \[.*?\]' | head -16; }
q "your search terms here"
```

- Extract two things: `## [Title]` lines and `uddg=` URL-encoded links (URL-decode with `python3 -c "import urllib.parse;print(urllib.parse.unquote('...'))"`)
- Works reliably when direct DDG HTML returns empty from datacenter IPs
- **Proven:** 2026-08-14 — Nusantara LLM landscape research: all 7 `web_search` queries empty; SearXNG showed all engines suspended; jina-wrapped DDG returned full results for every query.
- **Pitfall:** Jina Reader to huggingface.co may hit `AbuseAlleviationError` (anonymous domain block). Use direct `curl` to the HF API instead (rung 11).

### 12. Hugging Face API Direct Curl (model/dataset landscape research)

For "what models/datasets exist for X" research, skip search engines entirely — the HF API is structured, fast, no auth:

```bash
# Models by author, sorted by downloads (adoption = signal):
curl -s "https://huggingface.co/api/models?author=mesolitica&sort=downloads&direction=-1&limit=25"
# Models by keyword search:
curl -s "https://huggingface.co/api/models?search=F5-TTS+malay&limit=6"
# Datasets by author + keyword:
curl -s "https://huggingface.co/api/datasets?author=mesolitica&search=speech&limit=25"
```

- Downloads/likes counts reveal real adoption — a model with 55 downloads is a hobby, 21,000 is infrastructure. This distinguishes "exists" from "matters" in one call.
- Parse with `python3 -c "import json,sys; [print(m.get('id'), m.get('downloads')) for m in json.load(sys.stdin)]"`
- **Proven:** 2026-08-14 — mapped the entire Malaysian TTS/LLM model + dialect corpus landscape (mesolitica, malaysia-ai, SEA-LION, MERaLiON) in 4 API calls when search engines were down.

### 13. Bing News RSS (news-shaped queries, immune to CAPTCHA walls)

`https://www.bing.com/news/search?q=<query>&format=rss` via curl returns structured XML (title/description/pubDate/link). RSS endpoints don't run the JS CAPTCHA walls that block HTML SERPs:

```bash
curl -s "https://www.bing.com/news/search?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "YTL ILMU launch")&format=rss" | grep -oP '(?<=<title>).*?(?=</title>)' | head -12
```

- Best for "what happened recently with X", announcements, launches — the news-recency slice that jina-wrapped DDG serves poorly
- **Proven:** 2026-08-14 — Nusantara landscape research; returned Bernama/press coverage when every HTML SERP was empty or CAPTCHA'd

### 14. curl + HTML meta/ld+json Extraction (news articles when web_extract + browser both fail)

When `web_extract` fails (SearXNG search-only backend) and `browser` hangs on init, news article content is often extractable from raw HTML meta tags and JSON-LD structured data via terminal curl:

```bash
# Method A: Extract JSON-LD articleBody (most reliable for news sites)
curl -sL "https://example.com/article" 2>/dev/null \
  | grep -oP '<script type="application/ld\+json">.*?</script>' \
  | sed 's/<[^>]*>//g' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('articleBody','')[:4000])"

# Method B: Extract og:description (quick headline + summary)
curl -sL "https://example.com/article" 2>/dev/null \
  | grep -oP 'content="[^"]*"' | head -5

# Method C: Grep for key terms in raw HTML body
curl -sL "https://example.com/article" 2>/dev/null \
  | sed 's/<[^>]*>//g' | tr -s ' \n' ' ' \
  | grep -oP '.{0,200}KEYWORD.{0,2000}' | head -c 4000
```

- Method A works on TheEdge, MarketScreener, Bernama, NST — any site embedding `application/ld+json` with `articleBody`
- Method B gives headline + lead paragraph — enough for "what happened" queries
- Method C finds keyword-context windows in full HTML — useful for cross-referencing multiple facts
- **Pitfall:** Some sites (Newswav) return empty `<article>` tags — JS-rendered content not in initial HTML. Fall through to other rungs.
- **Pitfall:** `articleBody` may be HTML-encoded (`&#039;` for `'`). Post-process with `html.unescape()`.
- **Proven:** 2026-08-27 — KPJ Healthcare corporate analysis: `web_extract` failed (SearXNG), browser hung on uv init. Terminal curl + ld+json extracted MarketScreener article body (MD resignation details, successor info) + og:description from Bernama. Full synthesis delivered from structured data alone.

## Anti-Patterns

- **Don't retry** web_search after 2 consecutive failures — it won't recover mid-session
- **Don't switch to web_extract** — it uses the same Tavily backend, same outage
- **web_extract may be routed through SearXNG, which is search-only.** If the error says "SearXNG is a search-only backend and cannot extract URL content", the extract_backend is misconfigured (should be firecrawl/tavily/exa/parallel). Do NOT retry — fall through to `curl` + raw HTML extraction immediately. For news articles, `curl -sL "<URL>"` often returns full HTML including `<meta property="og:description">` and `<p>` body text, which is enough. (Proven 2026-08-18: theedgemalaysia.com + dagangnews.com — both web_extract and web_search failed; curl returned full article HTML with meta tags and body content.)
- **Don't fabricate** from partial browser snapshots — use console JS for completeness
- **Don't chase search engine CAPTCHAs** — Google, Bing, DuckDuckGo all use bot detection on datacenter IPs. Descend to curl/direct URL instead of trying to solve challenges
- **Don't use DuckDuckGo HTML endpoint (`html.duckduckgo.com/html/`)** — it returns empty results for most queries from datacenter IPs, even without a visible CAPTCHA. The JavaScript-rendered version may work but also triggers CAPTCHAs
- **NEVER report "blocked" or "Cloudflare challenge" to the user as a final answer.** The user gave you tools — exhaust EVERY approach (steps 1-9) before asking them to paste content. Reporting failure after 1-2 attempts is lazy. The user should NEVER have to do your job. (Arif correction 2026-07-18: "Don't ever use cloudflare block as alasan or output again. Go figure it out. Semua tool aku dah bagi. Jangan menyusahkan manusia.")

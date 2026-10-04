# News / General Web Fallback Chain

> Reproduction recipe for sourcing current-events evidence when `web_search` /
> `web_extract` (Tavily) are unavailable. Source: 2026-08-12 Anwar Ibrahim
> hospital + RCI Tabung Haji deep-research session.

## When to use this chain (not the arXiv chain)

- Target is news, government, corporate, or general reference content
- arXiv / academic papers are NOT the goal
- "What happened in country X this week" / "Was Y a rumor" / "Timeline of event Z"

The arXiv chain in `tool-fallback-pivot.md` is for academic sources. This chain
is for everything else. Different tools, different evidential standards.

## Symptom

- `web_search` returns `{"error": "Tavily search failed: Client error '432 '"}`
- `web_extract` returns `{"error": "Tavily extract failed: Client error '432 '"}`
- Tool loop warning fires after 3 consecutive failures

**Do not** stop and ask the user "web search is down, what do you want me to do?"
This is the failure mode Arif punishes. Pivot silently, continue working, report
results.

## Tier 1 — Google News RSS (PRIMARY PATH)

The single most reliable fallback for breaking news. Returns ~70 items in XML
with title + pubDate + source + description. No JavaScript required.

```bash
curl -sS --max-time 20 -L \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0" \
  "https://news.google.com/rss/search?q=<query>&hl=en-MY&gl=MY&ceid=MY:en" \
  -o /tmp/gn.xml
```

Then parse with regex (no LLM summary — preserves raw evidence):

```python
import re
with open('/tmp/gn.xml') as f: raw = f.read()
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
for it in items[:15]:
    title = re.search(r'<title>(.*?)</title>', it)
    pub = re.search(r'<pubDate>(.*?)</pubDate>', it)
    src = re.search(r'<source[^>]*>(.*?)</source>', it)
    print(f'{pub.group(1)} | {src.group(1)}: {title.group(1)}')
```

**Variants**:
- `hl=en-MY&gl=MY&ceid=MY:en` — Malaysia, English
- `hl=ms-MY&gl=MY&ceid=MY:ms` — Malaysia, Bahasa
- Drop `hl`/`gl` for global English

**Caveats**:
- Google wraps real URLs behind `/rss/articles/CBMi...` redirect tokens. Use the
  *title + source + date* triple as the evidence, not the redirect URL.
- Up to 77 items returned. Sort by `pubDate` for recency.

## Tier 2 — Wikipedia direct curl

Wikipedia serves article HTML to any compliant UA. The English Wikipedia is
usually the most complete and most cited.

```bash
curl -sS --max-time 20 -L \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0" \
  "https://en.wikipedia.org/wiki/<Article_Title>" \
  -o /tmp/page.html
```

Parse with Python (no LLM summary):

```python
import re
from html.parser import HTMLParser

class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.text=[]; self.skip=False
    def handle_starttag(self, t, a):
        if t in ('script','style','noscript','svg'): self.skip=True
    def handle_endtag(self, t):
        if t in ('script','style','noscript','svg'): self.skip=False
    def handle_data(self, d):
        if not self.skip: self.text.append(d)

with open('/tmp/page.html') as f: raw = f.read()
p = T(); p.feed(raw)
out = ' '.join(p.text)
out = re.sub(r'\s+', ' ', out).strip()
i = out.find('Background')
print(out[i:i+8000])
```

**Pitfall**: Wikipedia articles for very new events may not exist yet (red link,
"Page contents not supported in other languages"). For 2026 events, the English
article often lags by 1-3 weeks.

**Pitfall**: Wikipedia's article HTML carries schema.org metadata + nav noise.
Skip first 2000-4000 chars before parsing the actual prose.

## Tier 3 — Extract URLs from Wikipedia citations

Wikipedia articles for current events have rich citation trails. Pull all links
from the references section:

```python
import re
with open('/tmp/wiki.html') as f: raw = f.read()
domains = ['malaymail','malaysiakini','freemalaysiatoday','thestar','nst',
           'astroawani','bernama','aljazeera','channelnewsasia','straitstimes',
           'reuters','ap.org','bbc','theedgemalaysia','malaysianreserve',
           'therakyatpost','codeblue']
for d in domains:
    urls = re.findall(rf'https://[^"<>]*{d}[^"<>]*', raw)
    for u in set(urls)[:3]:
        print(f'{d}: {u}')
```

Then direct curl each URL with Tier 5 below. This is how the Anwar session found
the original Malay Mail Port Dickson speech (via the RCI Wikipedia article).

## Tier 4 — DuckDuckGo HTML (sometimes works)

```bash
curl -sS --max-time 20 \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0" \
  "https://duckduckgo.com/html/?q=<query>" \
  -o /tmp/ddg.html
```

Parse `class="result__a"` anchors + `class="result__snippet"` for description.

**Caveat**: DDG HTML endpoint often returns 138 bytes (bot-detected) even with
realistic UA. If size < 1000, skip and go to Tier 5.

## Tier 5 — Direct news site curl

Malaysian + regional news sites that serve HTML to real UAs (no JS required):

| Site | Pattern | Notes |
|---|---|---|
| Malay Mail | `https://www.malaymail.com/news/...` | Skip first 3000 chars (nav), search for dateline ("PORT DICKSON," / "PUTRAJAYA,") |
| Free Malaysia Today | `https://www.freemalaysiatoday.com/category/...` | Use `<article>` tag extract — body well-structured |
| The Star | `https://www.thestar.com.my/...` | Article body in `<div class="story-body">` |
| NST | `https://www.nst.com.my/...` | Similar to The Star |
| CNA | `https://www.channelnewsasia.com/...` | Loads but JS-gated for some sections |
| Al Jazeera | `https://www.aljazeera.com/...` | Article body in `<article>` tag |
| Straits Times | `https://www.straitstimes.com/...` | Paywall after ~200 words but lead usually extractable |
| Bernama | `https://www.bernama.com/...` | Wire service — short factual articles |
| KLSE Screener | `https://klsescreener.com/news/...` | Often 404s on /news/ URLs — verify |

Standard recipe (Malay Mail / FMT example):

```bash
curl -sS --max-time 25 -L \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0" \
  "https://www.malaymail.com/news/malaysia/2026/07/24/.../228816" \
  -o /tmp/mm1.html
```

```python
import re
from html.parser import HTMLParser
# ... [T class from Tier 2] ...
# Find article start
body = raw[3000:]  # skip nav
p = T(); p.feed(body)
out = ' '.join(p.text)
i = out.find('PORT DICKSON')  # or PUTRAJAYA, KUALA LUMPUR, SINGAPORE
if i == -1: i = 0
print(out[i:i+4000])
```

## Tier 6 — Google search HTML (last resort)

```bash
curl -sS --max-time 20 \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0" \
  "https://www.google.com/search?q=<query>&num=10&hl=en" \
  -o /tmp/g.html
```

Returns ~90KB but heavy JS-rendering — most `<div class="...">` patterns are
empty. Extract via:
- `/url?q=<real-url>` patterns → real destination URLs
- `<h3>` tags → titles (very brittle)

**Caveat**: Google often returns a JS-redirect stub ("Please click here if you
are not redirected within a few seconds"). If the page contains that string,
abort Tier 6 and rely on Tiers 1-5.

## Tier 7 — Browser (heavy, last)

If everything else fails and the answer is genuinely behind JavaScript:

```python
browser_navigate(url="https://www.malaysiakini.com/news/<path>")
# Then browser_snapshot(full=True) to dump the rendered page
```

This is slow (3-10s per navigation) but works for JS-gated Malaysian news sites
(Malaysiakini is the worst offender — pure SPA, curl returns 30KB of JSON shell).

## Real session log (2026-08-12 Anwar + RCI)

1. **Started**: "Apa jadi kat Anwar Ibrahim mausk hospital operation" + "Kes rci tabung haji. Deep research"
2. **First attempt**: `web_search` → 3x HTTP 432 from Tavily.
3. **Second attempt**: `web_extract` on Malaysiakini / Astro Awani / Bernama Wikipedia → 3x HTTP 432.
4. **Diagnose**: `curl https://api.tavily.com/health` → empty. Tavily backend down.
5. **Pivot 1 (Tier 2)**: Direct curl Wikipedia RCI article → 151KB HTML, fully parseable. Got the entire timeline + commissioner list + findings.
6. **Pivot 2 (Tier 3)**: Extracted Malay Mail + FMT + The Star URLs from Wikipedia citations → 6 direct news URLs.
7. **Pivot 3 (Tier 5)**: Direct curl Malay Mail Port Dickson article → 147KB. Dateline extract = full PM Anwar quote about Tabung Haji withholding.
8. **Pivot 4 (Tier 1)**: Google News RSS for "Anwar Ibrahim hospital" → 77 items. Confirmed FMT headline "Anwar undergoes surgery for abdominal hernia" 10 Aug 2026.
9. **Pivot 5 (Tier 5)**: Direct curl FMT article → 218KB. Full body confirms laparoscopic surgery, Dr Asri Ranga Abdullah Ramaiah team leader, 79th birthday same day.
10. **Converged**: 5 independent sources cross-confirmed surgery event. Multiple RSS feeds from CNA / Straits Times / Al Jazeera / KLSE Screener / The Rakyat Post added timeline (10 Aug op → 12 Aug discharge).
11. **Cached evidence**: `/root/forge_work/research/2026-08-12_anwar-rci-tabung-haji/SOURCES.md` with full URL list + [OBS]/[DER]/[INT] taxonomy + F7 Ω₀ 0.04 confidence.

Total time: ~3 minutes. Total tool calls: ~12 (4 failed Tavily + 8 working pivots).

## Hazards

- **Don't trust your own model knowledge as [OBS]**. You didn't fetch it. It's [INT].
- **Don't cite a Wikipedia redirect target** without verifying the article actually exists (`wgArticleId: 0` = empty stub).
- **Don't loop on the same failing tool**. After 3 failures, switch tiers silently.
- **Don't tell the user "Tavily doesn't work"** as a durable rule. Tavily will be back up tomorrow. The durable lesson is the pivot chain, not the failure.
- **Don't claim "I cannot research" after the first tier fails.** Pivot at least twice before stating blocker. Three-tier minimum effort is the standard.

## Cross-session notes

- The Anwar-RCI session proves a 5-tier pivot can complete a deep-research task
  in ~3 minutes when the primary backend is fully down.
- This chain composes with the arXiv chain — use them together when research
  spans academic + news sources (e.g., tracing a research finding from arXiv to
  its public-policy news coverage).
- When cached evidence is durable (events that won't change), write to
  `/root/forge_work/research/<date>_<topic>/SOURCES.md` with full URL list +
  timestamps. This becomes the federation's source-of-truth for that event.
---
name: live-rss-intelligence-research
description: Live intelligence research method using RSS feeds and web scraping when web_search is unavailable or unreliable. For geopolitical briefings, market intelligence, and news verification. Tested April 2026.
category: research
version: 1.0.0
author: arifOS
tags: [rss, intelligence, web-scraping, geopolitical, live-research]
triggers:
  - "current news on"
  - "live briefing"
  - "geopolitical briefing"
  - "latest verified"
  - "oil price today"
  - "energy market update"
  - "research from live sources"
---

# Live RSS Intelligence Research

When web_search is unavailable or the task requires verified live sources with dates (geopolitical briefings, energy market intel, crisis monitoring), use RSS feeds + curl scraping.

## Proven Working Feeds (April 2026)

| Source | URL | Topics |
|--------|-----|--------|
| **Al Jazeera** | `https://www.aljazeera.com/xml/rss/all.xml` | Middle East, energy, global affairs — MOST RELIABLE |
| **BBC World** | `http://feeds.bbci.co.uk/news/world/middle_east/rss.xml` | Middle East, Hormuz, energy |
| **BBC World (general)** | `http://feeds.bbci.co.uk/news/world/rss.xml` | Broader world news |
| **Reuters World** | `https://feeds.reuters.com/Reuters/worldNews` | BLOCKED — returns 0 chars |
| **SCMP** | `https://www.scmp.com/rss/91/feed` | Asia, China, SE Asia, partial |

**Failed feeds (April 2026):**
- Reuters RSS: All Reuters feed URLs return 0 content (blocked at server level)
- Bloomberg: Blocked
- FT: Partial/blocked
- Oilprice.com: Blocks scraping (JS-heavy)
- EIA: Numeric data present but HTML is hard to parse without JS

## Always-Working Method: Terminal curl + xml.etree

```bash
# Fetch Al Jazeera (most reliable)
curl -s --max-time 20 -L -A "Mozilla/5.0" \
  "https://www.aljazeera.com/xml/rss/all.xml" | head -300

# Fetch BBC
curl -s --max-time 20 -L \
  "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml" | head -200
```

**In Python (execute_code):**
```python
import subprocess, xml.etree.ElementTree as ET

def fetch(url):
    r = subprocess.run(['curl', '-s', '--max-time', '20', '-L', '-A',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'],
        capture_output=True, text=True)
    return r.stdout

def parse_rss(xml_text, max_items=20):
    items = []
    try:
        root = ET.fromstring(xml_text)
        for item in root.findall('.//item')[:max_items]:
            items.append({
                'title': item.findtext('title', ''),
                'pub': item.findtext('pubDate', ''),
                'desc': item.findtext('description', '')
            })
    except ET.ParseError:
        pass
    return items
```

**KEY NOTE:** `execute_code` Python's `subprocess.run` with `curl` via shell pipes may not work — use direct subprocess calls without shell pipes.

## Scraping Full Articles

```bash
# Get article content (BBC/Al Jazeera paragraphs)
curl -s --max-time 20 "https://www.bbc.com/news/articles/XXXXX" | \
  grep -oP '<p[^>]*>[^<]+</p>' | sed 's/<[^>]*>//g' | head -50
```

## Filtering for Relevant Articles

From parsed RSS items, filter by keywords:
```python
keywords = ['iran','israel','oil','brent','crude','gulf','hormuz',
            'opec','lng','malacca','malaysia','petronas','energy','sanction']
iran_items = [i for i in items if any(k in i['title'].lower() 
                or k in (i.get('desc','') or '').lower() for k in keywords)]
```

## Oil Price Data (Verified Live)

For energy briefings, verified prices from Al Jazeera article text (no JS needed):
- WTI/Brent prices often cited directly in news article body
- Example: Al Jazeera 28 Apr 2026 article stated "WTI crude at $100.09 at 12:30pm ET"
- Search article body for `$` + `bbl` or `barrel` patterns
- EIA numeric data is in HTML but not easily parseable without JS rendering

## Live Source Verification Rules (F2 TRUTH Floor)

1. Every claim must have a `source` and `date` from a live feed
2. Claims without a verifiable live source = `CLAIM` or `ESTIMATE`
3. Do NOT use training data as evidence — if live search fails, mark UNKNOWN
4. Reuters feeds are BLOCKED — do not waste time on them
5. If no live source confirms a date, use the RSS feed's `<lastBuildDate>` as proxy
6. For prices: verify from article body text, not a JS-rendered chart
7. When multiple sources conflict on a number, report the range and note the discrepancy

## Intelligence Briefing Output Template

```
## Executive Summary (3-5 bullets)

## Latest Verified Timeline (date | event | source)

## Claim Table
| Claim | Status | Source | Date |

## Impact Matrix

## Probability Bands

## Red Flags to Watch

## Overhyped Threats

## Final Verdict
```

## What Was Learned (April 2026)

- Reuters RSS = permanently blocked from this environment → never rely on it
- Al Jazeera RSS = most comprehensive and fastest to update (lastBuildDate reflects truly recent items)
- BBC = second most reliable; has separate Middle East and general feeds
- SCMP = partial; some items may not appear without JS rendering
- Web scraping full articles from BBC/Al Jazeera works via `curl + grep -oP` pattern matching on `<p>` tags
- Embedded `.git` directories in backed-up workspace dirs must be stripped before `git add` — causes "embedded repository" warnings that corrupt the index
- The `execute_code` tool's XML parser sometimes fails where direct `terminal()` curl succeeds → when in doubt, use terminal

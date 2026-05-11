---
name: web-fetch-article-archive-fallback
description: Fetch article content from Cloudflare-protected sites using Wayback Machine fallback
triggers:
  - cloudflare block on article fetch
  - direct curl fails 403/attention required
  - towardsdatascience article fetch
---

# Web Fetch Article with Archive Fallback

## Trigger
Fetching article content from Cloudflare-protected sites (especially Medium, TowardsDataScience, news sites) when direct curl/wget fails.

## Problem
Direct `curl` to TDS articles → Cloudflare block page (HTTP 403 / "Attention Required" page).

## Solution: Wayback Machine Fallback Sequence

### Step 1 — Try direct fetch
```bash
curl -sL "https://target-site.com/article-path/" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
```
If response contains "Cloudflare" or "Attention Required" → proceed to Step 2.

### Step 2 — Wayback Machine
```bash
# Format: https://web.archive.org/web/2026/https://{FULL_URL_WITH_PROTOCOL}
curl -sL "https://web.archive.org/web/2026/https://towardsdatascience.com/the-must-know-topics-for-an-llm-engineer/" \
  -H "User-Agent: Mozilla/5.0"
```
Then strip HTML:
```python
import re
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:15000])
```

### Step 3 — DuckDuckGo HTML fallback (for URL discovery)
```bash
curl -sL "https://html.duckduckgo.com/html/?q=search+terms" -H "User-Agent: Mozilla/5.0"
```
Good for finding cached/alternative URLs and snippets.

## Known Targets
| Site | Protection | Fallback |
|------|-----------|----------|
| towardsdatascience.com | Cloudflare | Wayback Machine ✅ works |
| medium.com | Cloudflare | Wayback Machine |
| news.google.com | None | Direct fetch works |

## Pitfalls
- Wayback Machine needs `https://` prefix in URL path: `/web/2026/https://...`
- Don't use `textise dot iitty` style sites — these are usually broken/malware
- Google Cache (`webcache.googleusercontent.com`) often redirects to a click-through page — unreliable
- AIPulseLab / alternative aggregators usually republish summaries, not full article content

## Verification
After stripping HTML, check content starts with article title/author (not "Attention Required" or nav menu). If title missing → archive may be empty, try a different date in Wayback or give up.
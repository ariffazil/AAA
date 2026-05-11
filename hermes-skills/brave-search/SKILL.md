---
name: brave-search
description: Web search via Brave Search API for arifbfazil@gmail.com — real-time search, no hallucinations. Preferred over Bing for person/company research (fewer bot blocks).
category: research
---

# Brave Search MCP Skill

## Trigger
Any task requiring web search, fact-check, person lookup, company research, or general internet lookup.

## Credentials
`BRAVE_API_KEY` — set in `/root/.hermes/.env`

Get free key: https://brave.com/search/api/ (free tier: 2,000 queries/month)

## What it does
- **Web search** — queries Brave Search engine, returns titles + snippets + URLs
- **No hallucination** — pulls live results, not cached LLM knowledge
- Preferred over Bing for profile/company research (SignalHire, ZoomInfo, LinkedIn people searches)

## Setup (two steps)

### Step 1 — Install MCP server
```bash
npm install -g @modelcontextprotocol/server-brave-search
# Note: package is deprecated but still works
```
Binary installs to `/usr/bin/mcp-server-brave-search`.

### Step 2 — Enable in Hermes toolsets
Add `brave-search` to `toolsets` in `/root/.hermes/config.yaml`:
```yaml
toolsets:
- hermes-cli
- brave-search   # ← add this
```
Then restart the Hermes session for tools to appear.

## Fallback: Direct API (when MCP not available)
If the MCP tool isn't loaded yet, use curl directly:
```bash
BRAVE_KEY=$(grep BRAVE_API_KEY /root/.hermes/.env | sed 's/.*=//')
curl -s -H "Accept: application/json" \
     -H "X-Subscription-Token: $BRAVE_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=SEARCH_QUERY&count=10" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('web', {}).get('results', []):
    print(r.get('title'))
    print(r.get('url'))
    print(r.get('description','')[:200])
    print('---')
"
```

## API Notes
- Free tier: 2,000 queries/month, rate limit: 2 req/sec
- Safe search filtering enabled by default
- `count` param sets result window (max ~20)
- Works on VPS with no bot detection (unlike Bing/Google)

## Cloudflare Email Decode
Many Malaysian sites (malaysianbar.org.my, scoop.my) use Cloudflare email obfuscation. Decode with Python:
```python
def decode_cfemail(hex_str):
    """hex_str: the data-cfemail attribute value."""
    key = int(hex_str[0:2], 16)
    return ''.join(
        chr(int(hex_str[i:i+2], 16) ^ key)
        for i in range(2, len(hex_str)-1, 2)
    )
# Example:
html = '<a href="mailto:council@malaysianbar.org.my" data-cfemail="6abc123...">Email</a>'
hex_email = re.search(r'data-cfemail="([^"]+)"', html).group(1)
print(decode_cfemail(hex_email))  # → council@malaysianbar.org.my
```

## Known Malaysian Sources (verified 2026-05-07)
| Source | URL | Notes |
|--------|-----|-------|
| Malaysian Bar Council | malaysianbar.org.my | CF-encoded emails, footer has decoded version |
| SUHAKAM | suhakam.org.my | humanrights@suhakam.org.my |
| Big Boom Media | bigboommedia.com.my | enquiry@, corporate@, editor@scoop.my |
| Perdana Foundation | perdida.org.my | drmahathir@perdana.org.my |
| WWF Malaysia | wwf.org.my | contactus@wwf.org.my |
| Malaysianiakini | malaysiakini.com | editor@malaysiakini.com |

## Known gotchas
1. **Truncated API key in .env display** — `grep` output may show `BSABWb...Qflt` (truncated). Always use the full key from the actual file, not from display/output.
2. **Deprecated npm package** — `@modelcontextprotocol/server-brave-search` shows npm deprecation warning but is still functional. Do NOT wait for replacement — install it and use it.
3. **MCP tools not hot-reloadable** — adding to toolsets requires session restart. Use curl fallback for immediate results.
4. **LinkedIn search indexing** — Brave sometimes returns LinkedIn profile URLs without email. Try ZoomInfo or SignalHire result pages.
5. **MY sites and Cloudflare** — always run CF email decode on any HTML page that returns 200 but shows no emails in plain grep.
6. **"R&R" query collision** — searching `R&R Halal Sadao` returns Wikipedia R programming language results because `&` is parsed as a query operator. Use quotes (`"R&R Halal" Sadao`) or reformulate: search for `R and R Halal Sadao` or the Thai name instead.
7. **Thai script + transliteration mix** — for Malaysian-Thailand border restaurants (Sadao, Dannok, Hat Yai), mixing Thai script terms with English transliteration gives better coverage than English-only queries. E.g., `ซีเรียก๋วยเตี๋ยวเรือ Dannok` vs `Syria boat noodle Dannok`.
8. **TikTok as discovery engine** — for new local halal restaurants in border areas, TikTok (via Brave search) often surfaces places that don't appear in Google Maps or Tripadvisor yet. Search TikTok for the area name + "halal" to find emerging spots.

## Thai Restaurant Research — Rating/Price Extraction Patterns

When researching Thai restaurants, search results often embed ratings and prices in unstructured descriptions. Use this Python parser on Brave Search JSON output:

```python
import re, json

def parse_thai_restaurant_results(data):
    """Parse Brave Search JSON for Thai restaurant metrics."""
    results = data.get('web', {}).get('results', [])
    for r in results:
        title = r.get('title', '')
        desc = r.get('description', '') + ' ' + title
        
        # Rating: "4.6 out of 5" or "4.6/5" in text
        rating_match = re.findall(r'(\d\.\d)\s*(?:out of|/)\s*5', desc)
        
        # Thai price: ฿299, 299 baht, THB299
        price_match = re.findall(r'[\฿£\$]?\s*(\d{3})\s*(?:baht|THB|Bht|บาท)', desc, re.IGNORECASE)
        
        # Halal signal detection
        halal_kw = ['halal', 'ฮาลาล', 'muslim owned', 'islam', 'certified halal', 'all food is halal']
        halal_signal = any(k.lower() in desc.lower() for k in halal_kw)
        
        # Review count: "604 reviews" or "2,192 reviews"
        review_match = re.findall(r'([\d,]+)\s*(?:reviews?|รีวิว)', desc, re.IGNORECASE)
        
        print(f"Rating: {rating_match}")
        print(f"Price ฿: {price_match}")
        print(f"Halal: {halal_signal}")
        print(f"Reviews: {review_match}")
```

### Verified Thai Restaurant Sources (Hat Yai / Southern Thailand)
| Source | URL Pattern | Strength |
|--------|-------------|----------|
| **Restaurant Guru** | restaurantguru.com | Reliable numeric ratings + review counts |
| **Tripadvisor** | tripadvisor.com | "All food is Halal" explicit confirmations |
| **Wanderlog** | wanderlog.com | Price per person (฿299), good descriptions |
| **HaveHalalWillTravel** | havehalalwilltravel.com | Halal verification focus |
| **Wongnai** | wongnai.com | Thai-language reviews, but star parsing harder |
| **Top-Rated.Online** | top-rated.online | Price verification (฿299 Thai Baht confirmed) |
| **TikTok** | tiktok.com | Price menus (฿199 buffet), fresh but unverified — best for emerging local spots in border areas |
| **Wikimapia** | wikimapia.org | Halal verification for local spots (e.g., Nurlaila confirmed halal via Wikimapia entry) |
| **Mustakshif** | mustakshif.com | Halal verification status (even if "not verified", shows community declaration + hours) |

### Hat Yai / Southern Thailand specific notes
- **Khlong Hae area** = คลองแห, known for halal seafood buffers
- **Central Festival Hat Yai** = major mall, 4th floor food court
- **Rattakarn Rd** = location of Mandarin Suki HQ (Soi 7/3)
- Tripadvisor often shows "All food is Halal" in descriptions — search result snippets confirm this
- **Singha Nakorn Hot Pot** is in Singhanakhon district (~45 min from Hat Yai proper) — exclude if location is Hat Yai
- **In Seoul BBQ** (Central Festival) had only 2 Wongnai reviews = rating statistically meaningless (3.2 from 2 reviews)

## Best sources for people/company research (in priority order)
1. **SignalHire** — best for work history, skills, education, contact info (email/phone partial)
2. **ZoomInfo** — good for company affiliation, often Cloudflare-blocked on scraping
3. **LinkedIn** — canonical for current role, but limited search indexing
4. **Facebook** — often outdated for professionals; treat as secondary/confirmation only

# SearXNG Engine Restructure — 2026-08-20

## Problem

All free scraper engines blocked from datacenter IP (72.62.71.199):
- DuckDuckGo: timeout
- Google CSE: "too many requests"
- Startpage: CAPTCHA
- Qwant: "access denied"
- Brave (`brave` engine): "Suspended: too many requests" — THIS IS THE SCRAPER, NOT THE API

SearXNG has TWO separate Brave engines:
- `brave` = web scraper (blocks datacenter IPs)
- `braveapi` = REST API with `api_key` (immune to IP reputation)

The original config used `brave` (scraper) with an `api_key` field — but the key is ignored by the scraper engine.

## Fix Applied

Changed `/root/searxng/settings.yml`:

### Before (broken)
```yaml
engines:
  - name: duckduckgo        # timeout
  - name: google             # blocked
  - name: bing               # works but low quality
  - name: brave              # SCRAPER — blocked despite api_key
    engine: brave
    api_key: "BSABW..."
    disabled: false
  - name: wikipedia
  - name: arxiv
```

### After (working)
```yaml
engines:
  - name: braveapi           # REST API — immune to IP blocks
    engine: braveapi
    api_key: "BSABW..."
    results_per_page: 20
    disabled: false

  - name: bing               # fallback, works from this IP
    engine: bing
    shortcut: bi
    disabled: false

  - name: duckduckgo         # blocked — disabled
    engine: duckduckgo
    disabled: true

  - name: google             # blocked — disabled
    engine: google
    disabled: true

  - name: startpage          # CAPTCHA — disabled
    engine: startpage
    disabled: true

  - name: wikipedia          # always works
  - name: arxiv              # always works
```

## Verification Results

- First query after restart: 30 results (20 braveapi + 10 bing) ✓
- `braveapi` uses `https://api.search.brave.com/res/v1/web/search` with Bearer token
- Direct Brave API test: HTTP 200, rich results (Fed speeches, symposium pages, videos)

## Known Behavior

- SearXNG internal rate limiter suspends `braveapi` for 180s after burst queries
- This is SearXNG's own limiter, not upstream API blocking
- Query spacing >3min = consistent results
- Don't restart container to clear suspension — just wait

## Compose Location

- `/root/searxng/docker-compose.yml`
- Settings bind-mounted: `/root/searxng/settings.yml` → `/etc/searxng/settings.yml:ro`
- Edit HOST file, then `docker restart searxng`
- Image: `searxng/searxng:latest` (v2026.7.7)

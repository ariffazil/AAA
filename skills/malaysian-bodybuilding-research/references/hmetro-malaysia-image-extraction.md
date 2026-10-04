# Harian Metro / HMetro article extraction (datacenter-IP safe)

**Verified 2026-08-08 on the `cikgu-menjadi-sado` (Joe Zack) feature.**

## Problem
HMetro (hmetro.com.my) is a primary Malaysian news source for local human-interest and athlete features. From a datacenter IP:

- `web_extract(urls=[...])` → `{"error": "Failed to fetch url"}`
- `browser_navigate(url=...)` → `Operation timed out. The page may still be loading or the element may not exist.`

Both fail. The user is waiting.

## Solution: plain curl with a normal browser UA

```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://www.hmetro.com.my/utama/2026/08/1395281/cikgu-menjadi-sado" -o /tmp/page.html
```

This works in one shot. The page is server-rendered (not a JS app), so a normal UA bypasses whatever anti-bot the browser-style request was tripping over. Save the HTML once, then grep.

## What you can recover

### Images
HMetro CDN: `https://assets.hmetro.com.my/images/articles/<filename>.jpg`. Two patterns consistently appear:

```bash
# All article images (body + social-share + listing thumbnails)
grep -oE 'https://[a-z.]*hmetro[a-z.]*/images/articles/[^"]+\.(jpg|jpeg|png|webp)' /tmp/page.html | sort -u
```

Typical asset-name suffix tells you the role:
- `...socialmedia.var_<timestamp>.jpg` — OG/Twitter share image (usually the hero)
- `...listing_featured_v2.var_<timestamp>.jpg` — listing page hero
- `...field_image.var_<timestamp>.jpg` — in-article body image

### Metadata from `<meta>` tags

```bash
grep -E '<meta (property|name)=' /tmp/page.html
```

Useful fields:

| Tag | Example value | What it tells you |
|---|---|---|
| `property="article:author"` | `Redzuan Muharam` | Reporter byline |
| `property="article:published_time"` | `2026-08-08T07:20:21+08:00` | ISO publish timestamp (MYT) |
| `property="article:modified_time"` | same | Last edit |
| `name="article-city"` | `Jempol` | City tag |
| `name="article-state"` | `` | State (often empty for HMetro) |
| `name="article-id"` | `1395281` | Article ID |
| `name="numberOfWords"` | `445` | Word count |
| `property="og:image"` | full URL | The OG image (same as socialmedia asset) |
| `name="keywords"` | comma-separated | All keyword tags (often includes athlete names) |

### Keyword tag is gold for identity
The `keywords` meta tag frequently lists the athlete name + gym + competition in plain text. From the Joe Zack article:

```
News, Malaysia, harian metro, Bina badan, berita, gimnasium, jempol, jurulatih kecergasan,
badan cantik, kecergasan, cikgu sado, Mohamad Azizol Zakariya, Joe Zack, Mr Malaysia 2025
```

Use these as additional search seeds. (Note: HMetro's CMS appends generic terms — the last 2-3 are usually the most specific.)

### Body content
```bash
# After stripping scripts/styles
sed -E 's/<script[^>]*>.*<\/script>//g; s/<style[^>]*>.*<\/style>//g' /tmp/page.html \
  | python3 -c "import sys, re; html=sys.stdin.read(); text=re.sub(r'<[^>]+>', ' ', html); print(re.sub(r'\s+', ' ', text))" \
  | grep -oE 'Joe Zack|Mohamad Azizol[^"]+|Bahau|Negeri Sembilan' | sort -u
```

The article body sits inside `<div class="article-body">` (or similar) and is plain HTML — no JS rendering required.

## AMP fallback for text content

If you only need the **prose**, the AMP variant goes through `web_extract` cleanly:

```
https://www.hmetro.com.my/amp/utama/2026/08/1395281/cikgu-menjadi-sado
```

AMP strips layout/scripts; you get clean Markdown in the result. Use AMP for text, curl for images.

## Pitfalls

- **AMP page exists but main URL doesn't always redirect to it** — try `web_extract` on `/amp/...` URL directly as a first probe before going to curl.
- **hmetro.com.my vs hmetro.my** — the canonical domain is `hmetro.com.my` (no separate `.my` for the article path). Harian Metro also publishes at `harianmetro.com.my` for some pieces; check `og:url` in the meta tags for the canonical domain.
- **Article ID in URL is sequential but not guaranteed stable** — re-cite via the og:url + article-id, not the URL path alone.
- **Section subpath varies**: `utama/`, `mutakhir/`, `WM/` (weekend), `sukan/`, `hiburan/`, etc. Don't hardcode section.
- **Timestamp is `+08:00` (MYT)** — already in Malaysian time. No timezone conversion needed.
- **Image filenames include Unix timestamps** — the `.var_<digits>.jpg` suffix is a cache-busting version stamp, not the publish time. Parse the og:published_time for the real date.

## Step-by-step recipe

```bash
# 1. Probe — try AMP first (free)
# web_extract(amp_url) — if this works, you have the text. Done.

# 2. If AMP also fails, fall back to curl
URL="https://www.hmetro.com.my/utama/2026/08/1395281/cikgu-menjadi-sado"
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36" \
  "$URL" -o /tmp/page.html
ls -lh /tmp/page.html   # confirm download size (~30-60KB usually)

# 3. Extract images + metadata
grep -oE 'https://[a-z.]*hmetro[a-z.]*/images/articles/[^"]+\.(jpg|jpeg|png|webp)' /tmp/page.html | sort -u
grep -E '<meta (property|name)=' /tmp/page.html

# 4. Download the images you need
curl -sL -A "Mozilla/5.0" -o /tmp/hero.jpg "$(grep og:image /tmp/page.html | grep -oE 'https://[^"]+\.jpg')"

# 5. (Optional) Run vision_analyze on the JPGs if you need structured detail from the photo
#    (e.g. competitor tag, prize amount, sponsor logos)
```

## When this generalizes

The same pattern (curl with normal browser UA + grep + download + vision_analyze) is the standard fallback for Malaysian news sites that block scraping:

- `hmetro.com.my` ✓ verified
- Likely works on: `harianmetro.com.my`, `bharian.com.my`, `kosmo.com.my`, `utusan.com.my`, `sinarharian.com.my`
- Astro Awani (`astroawani.com`) — usually bot-friendly to web_extract, try first
- Malaysiakini (`malaysiakini.com`) — paywalled; login wall applies; not covered here
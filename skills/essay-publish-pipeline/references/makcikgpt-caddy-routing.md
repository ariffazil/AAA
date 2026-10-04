# MakcikGPT Caddy Routing & Fix Recipe

> **Status:** Fixed 2026-08-09. All 24 articles now browser-visible.
> **Reference:** `/etc/caddy/Caddyfile`, handlers for `/world/makcikgpt/*`

## Routing Architecture

Caddy has THREE lanes for `/world/makcikgpt/*`:

| Lane | Matcher | Root | Serves |
|------|---------|------|--------|
| Bot landing | `@ai-bot-landing` (bot UA + `/world/makcikgpt/`) | `/var/www/html/arif/makcikgpt-md` | Static index.html |
| Bot articles | `@ai-bot-world` (bot UA + `/world/makcikgpt/*`) | `/var/www/html/arif/makcikgpt-md` | Static .html files |
| No-JS articles | `@makcikgpt_nojs` (non-text/html Accept) | `/var/www/html/arif/makcikgpt-md` | Static .html/.md files |
| Browser landing | `handle /world/makcikgpt/` | `/var/www/html/arif` | SPA shell (interactive) |
| **Browser articles** | `handle /world/makcikgpt/*` | `/var/www/html/arif` | **Static-first, SPA fallback** (FIXED) |

## The Bug (pre-fix)

The browser article handler used:
```caddyfile
try_files {path} /index.html
```

This resolved `{path}` against `/var/www/html/arif/`, which doesn't contain the slug. It fell through to `/index.html` (SPA shell). The SPA shell doesn't know unregistered slugs → "ARTICLE NOT FOUND".

Meanwhile, the bot handler (`@ai-bot-world`) served from `/var/www/html/arif/makcikgpt-md/` directly → bots got the article.

**Result:** HTTP 200 for bots, "ARTICLE NOT FOUND" for browsers. Curl-only verification gates produced false positives.

## The Fix (applied 2026-08-09)

Changed the browser article handler to try static files first:

```caddyfile
handle /world/makcikgpt/* {
    header Cache-Control "no-cache, no-store, must-revalidate"
    header CDN-Cache-Control "no-cache"
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif
    try_files /makcikgpt-md{path}.html /makcikgpt-md{path}/index.html /index.html
    file_server
}
```

**What changed:** `try_files` now looks for:
1. `/var/www/html/arif/makcikgpt-md/<slug>.html` — direct static file
2. `/var/www/html/arif/makcikgpt-md/<slug>/index.html` — directory index
3. `/var/www/html/arif/index.html` — SPA shell fallback (for unknown paths)

**Result:** Any `.html` file in `makcikgpt-md/` is immediately browser-visible. No SPA registration needed.

## How to Apply the Fix (if not already applied)

### Step 1: Find the exact line number

```bash
awk '/handle \/world\/makcikgpt\/*/ { found=1 } found && /try_files \{path\} \/index\.html/ { print NR; exit }' /etc/caddy/Caddyfile
```

**⚠️ Do NOT use a non-targeted sed replacement.** The pattern `try_files {path} /index.html` appears in MULTIPLE handlers (homepage, wealth, etc.). A global sed will change the WRONG handler.

### Step 2: Apply line-specific sed

```bash
LINE_NUM=<result from step 1>
sed -i "${LINE_NUM}s|try_files {path} /index.html|try_files /makcikgpt-md{path}.html /makcikgpt-md{path}/index.html /index.html|" /etc/caddy/Caddyfile
```

### Step 3: Verify the change

```bash
sed -n "$((LINE_NUM-5)),$((LINE_NUM+5))p" /etc/caddy/Caddyfile
```

Expected output should show the `handle /world/makcikgpt/*` block with the new try_files.

### Step 4: Validate and reload

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

### Step 5: Verify with browser

Navigate to `https://arif-fazil.com/world/makcikgpt/<any-slug>/` and confirm the article renders (not "ARTICLE NOT FOUND").

## File Permissions

MakcikGPT article files should be `644` (world-readable) so Caddy can serve them:

```bash
chmod 644 /var/www/html/arif/makcikgpt-md/<slug>.html
chown www-data:www-data /var/www/html/arif/makcikgpt-md/<slug>.html  # or root:root, both work since Caddy runs as root
```

## Landing Page Registration

After deploying an article, add it to `/var/www/html/arif/makcikgpt-md/index.html`:

```html
<a href="/world/makcikgpt/<slug>">
  <h2><Article Title></h2>
  <p><excerpt></p>
</a>
```

The landing page lists articles in reverse chronological order. Each article appears twice in the HTML (href + text content), so `grep -c "<slug>" index.html` should return 2.

## Verification Script

```bash
#!/bin/bash
# verify-makcikgpt.sh <slug>
SLUG="$1"
BASE="https://arif-fazil.com/world/makcikgpt"

echo "=== Gate 1: curl (bot) ==="
curl -sfL -o /tmp/test_$SLUG.html -w "HTTP:%{http_code} SIZE:%{size_download}\n" "$BASE/$SLUG/"
TITLE=$(grep -oE "<title>[^<]+</title>" /tmp/test_$SLUG.html | head -1)
echo "Title: $TITLE"

echo ""
echo "=== Gate 2: browser (manual check) ==="
echo "Navigate to: $BASE/$SLUG/"
echo "Expected: article renders with h1 matching title"
echo "NOT expected: 'ARTICLE NOT FOUND'"

echo ""
echo "=== Gate 3: landing page ==="
COUNT=$(grep -c "$SLUG" /var/www/html/arif/makcikgpt-md/index.html 2>/dev/null || echo 0)
echo "Slug appears $COUNT times in landing page (expected: 2)"

echo ""
if [ "$COUNT" -ge 1 ]; then
  echo "✅ All gates passed"
else
  echo "❌ Gate 3 failed: article not in landing page"
fi
```

## Related Skills

- `essay-publish-pipeline` — parent skill, covers /words/writing/ pipeline
- `arif-sites-ops` — site operations, Caddy config management
- `arif-fazil-web-ops` — web surface operations, dual-register articles

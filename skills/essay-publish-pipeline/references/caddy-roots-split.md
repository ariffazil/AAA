# Caddy Root Path Split — arif-fazil.com

## The Problem

The arif-fazil.com Caddyfile uses **two different document roots** depending on which handler catches the request. This causes static shells to 404 when deployed to the wrong root.

## Root Mapping (verified 2026-08-14)

| Caddy Handler | Root | Covers |
|---|---|---|
| Global default | `/var/www/html/arif` | Most paths |
| `@agent_shells` | `/var/www/html/arif` | `/writing/*`, `/missions/*`, `/economics/*`, etc. |
| `@static_dirs` | `/var/www/html/arif` | `/999/*`, `/map/*`, `/world/*`, etc. |
| `@spa_routes` | `/var/www/html/arif` | `/words*`, `/writing*`, `/world*`, etc. |
| **`handle /words/*`** | **`/var/www/html`** | `/words/writing/<slug>/`, `/words/doctrine/`, etc. |
| **`handle /work/*`** | **`/var/www/html`** | `/work/*` |

## Why This Matters

When you deploy static shells via `rsync -a dist/ /var/www/html/arif/`, the files land at:
```
/var/www/html/arif/words/writing/<slug>/index.html
```

But the `handle /words/*` Caddy block serves from `/var/www/html`, so it looks for:
```
/var/www/html/words/writing/<slug>/index.html
```

Result: **404** even though the file exists — just at the wrong prefix.

## The Fix

After `rsync -a dist/ /var/www/html/arif/`, ALSO copy static shells to the handler's actual root:

```bash
for slug in <slugs>; do
  mkdir -p "/var/www/html/words/writing/$slug"
  cp "dist/words/writing/$slug/index.html" "/var/www/html/words/writing/$slug/index.html"
done
```

## Caddy Config Location

- Main Caddyfile: `/etc/caddy/Caddyfile` (imports vhosts)
- Site config: `/etc/caddy/vhosts/arif-fazil.com.conf`
- `handle /words/*` block: line ~740
- To find: `grep -n "handle /words" /etc/caddy/vhosts/arif-fazil.com.conf`

## Why Two Roots?

Historical. The `/words/` path was added later (2026-08-10 per git history) as a content-first static surface. The handler was written with `root * /var/www/html` to serve from the top-level dist output, while the rest of the site evolved under `/var/www/html/arif/`. This split is intentional but undocumented — hence this reference.

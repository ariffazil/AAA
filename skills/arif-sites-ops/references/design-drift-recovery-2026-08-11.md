# Design Drift Recovery — Session 2026-08-11

Session-verified recovery procedure for when the live `/world/makcikgpt/` design has drifted from the canonical version. Captures the exact paths, the discovered archive, and the steps that worked.

## What happened

`/world/makcikgpt/` was live-served at 14,074 bytes using a degraded GitHub-dark palette (blue `#58a6ff` accent, system-ui font, no hero canvas). Archives contained a richer 19,638-byte version using custom red/blue/yellow palette with hero canvas animation.

User pushback timeline:
1. Initial patch with forge-red palette — user said "Hmmm I want dark mode. At least have some header color contrast red yellow blue"
2. Patched to tri-color red/gold/blue — user said "I don't like the current site... deep archive extraction"
3. Found 19,638-byte archive from 2026-07-31 — user said "Aku nak atleast macam ni" (I want at least like this)
4. Restored archive design with 26 articles (4 new added)

## Archive locations found (sorted by size)

```
/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/20260731T124934083475118Z/previous/makcikgpt-md/index.html   19,638B  ← canonical
/root/_archive/2026-08-04/backups/www-html-20260801T115957Z-pre-web-canon-reconcile/arif.bak-20260801T115436Z/makcikgpt-md/index.html  19,589B
/root/_archive/2026-08-04/backups/arif.bak-20260801T115436Z/makcikgpt-md/index.html   19,589B
/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/20260731T124544126403029Z/previous/makcikgpt-md/index.html   19,563B
/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/20260731T125956384157717Z/previous/makcikgpt-md/index.html   19,224B
/var/www/html/makcikgpt-md.removed-20260811/index.html   14,770B  ← quarantined (close to current live)
/root/_archive/2026-08-04/backups/www-html-arif-20260804T153940Z/makcikgpt-md/index.html   14,131B
/var/www/html/arif/makcikgpt-md/index.html   14,074B  ← live at session start
... (smaller variants 105B stubs and 12,609B Article Not Found variants)
```

## Restoration recipe (Python)

```python
import os, re

src = "/root/backups/forge_work-archive-2026-07/deployments/arif-fazil.com/20260731T124934083475118Z/previous/makcikgpt-md/index.html"
dst = "/var/www/html/arif/makcikgpt-md/index.html"

with open(src) as f:
    html = f.read()

# 1. Fix canonical URL (live serves at /world/makcikgpt/, not /makcikgpt/)
html = html.replace(
    '<link rel="canonical" href="https://arif-fazil.com/makcikgpt/">',
    '<link rel="canonical" href="https://arif-fazil.com/world/makcikgpt/">'
)

# 2. Update slug paths from /makcikgpt/ to /world/makcikgpt/
html = html.replace('u:"/makcikgpt/', 'u:"/world/makcikgpt/')

# 3. Update topbar sig date
html = html.replace('SEAL 999 · 2026-07-31', 'SEAL 999 · 2026-08-11')

# 4. Add 4 newer articles to ARTICLES array (post-dating archive)
#    Insert before the last (oldest) article entry
articles_marker = '{s:"M2",d:"2026-06-07",u:"/world/makcikgpt/siasatan-harakah",t:"Persoalan RM70 Bilion"}'
new_articles = """  {s:"M2",d:"2026-08-02",u:"/world/makcikgpt/suara-terlalu-siap",t:"Suara Yang Tak Letak Dalam Mulut Manusia"},
  {s:"M1",d:"2026-08-09",u:"/world/makcikgpt/syaitan-ingat-dirinya-malaikat",t:"Syaitan yang Ingat Dirinya Malaikat"},
  {s:"M1",d:"2026-08-08",u:"/world/makcikgpt/70-sen-daripada-setiap-ringgit-untung-dah-keluar",t:"70 Sen Daripada Setiap Ringgit Untung Dah Keluar. Esok, Siapa Bayar?"},
  {s:"M1",d:"2026-08-09",u:"/world/makcikgpt/13-sebab-taufik-kena-berhenti",t:"13 Sebab Taufik Kena Berhenti"},
"""
html = html.replace(articles_marker, new_articles + "  " + articles_marker)

# 5. Update counts (22 → 26)
html = html.replace(
    '<div class="stat"><b class="c-r">22</b><span>Artikel</span></div>',
    '<div class="stat"><b class="c-r">26</b><span>Artikel</span></div>'
)

# 6. Update description meta count
html = html.replace(
    '22 articles, 5 series, seal 999',
    '26 articles, 5 series, seal 999'
)

# 7. Update hardcoded base URL
html = html.replace(
    'href="https://arif-fazil.com/makcikgpt/"',
    'href="https://arif-fazil.com/world/makcikgpt/"'
)

with open(dst, 'w') as f:
    f.write(html)

# 8. Webroot permissions (Caddy runs as www-data)
os.chown(dst, 33, 33)  # www-data uid
os.chmod(dst, 0o644)
```

## Verification (curl probes)

```bash
# 1. Live serves
curl -sI "https://arif-fazil.com/world/makcikgpt/" -H "User-Agent: Mozilla/5.0 Chrome/119" | grep -iE "HTTP|last-modified"

# 2. Article count in served HTML
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -c 'u:"/world/makcikgpt/'

# 3. Newer articles present
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -E "(Syaitan|70 Sen|Taufik|Suara Yang Tak)"
```

## What NOT to do

- ❌ Don't just `cp` the archive file — slug paths and article count will be wrong
- ❌ Don't use `/var/www/html/arif/world/makcikgpt/index.html` as the write target — that's an orphan stub from Caddy routing
- ❌ Don't forget `chown www-data:www-data` — Caddy needs to be able to read the file
- ❌ Don't assume newest archive = best — file size + Arif's preference both matter
- ❌ Don't skip the human-eye verification — vision model can misread CSS as monochrome when colors are saturated

## Lessons captured (now in skills)

- `arif-fazil-web-ops/SKILL.md` — Rule -2 Archive Archaeology + Recovery recipes section
- `arif-sites-ops/SKILL.md` — Human-First Doctrine + Archive Archaeology pitfall
- `essay-publish-pipeline/SKILL.md` — MakcikGPT pattern consistency section
- `arif-sites-ops/scripts/detect-design-drift.sh` — runnable archaeology script

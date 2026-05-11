---
name: arifos-site-deploy-recovery
description: Emergency site deployment and rollback workflow for arifOS web surfaces — Caddy VPS serving layer, Cloudflare Pages gotchas, dev-vs-dist index.html trap.
version: 2026.05.01
triggers: ["site deployment", "arif-sites", "Caddy", "Cloudflare Pages", "web root", "site broken", "404 site"]
---

# arifOS Site Deployment & Recovery

## Architecture (MUST KNOW BEFORE TOUCHING)

### Two Serving Layers
1. **Caddy (VPS)** — serves from `/var/www/html/{domain}/` via `/etc/caddy/Caddyfile`
2. **Cloudflare Pages** — separate hosting, auto-deploys from GitHub, can override Caddy

### Web Root Map (Caddy)
| Domain | Caddy Root | Source in arif-sites |
|--------|-----------|---------------------|
| arif-fazil.com | /var/www/html/arif/ | sites/arif-fazil.com/ |
| aaa.arif-fazil.com | /var/www/html/aaa/ | sites/aaa.arif-fazil.com/ |
| arifos.arif-fazil.com | /var/www/html/arif/ (shared) | sites/arif-fazil.com/arifos/ |
| arifosmcp.arif-fazil.com | /var/www/html/arifosmcp/ | sites/arifosmcp.arif-fazil.com/ |
| geox.arif-fazil.com | /var/www/html/geox/ | sites/geox.arif-fazil.com/ |
| forge.arif-fazil.com | /var/www/html/forge/ | sites/forge.arif-fazil.com/ |
| apex.arif-fazil.com | /var/www/html/apex/ | sites/apex.arif-fazil.com/ |
| wiki.arif-fazil.com | /var/www/html/wiki/ | sites/wiki.arif-fazil.com/ |
| waw.arif-fazil.com | /var/www/html/waw/ | sites/waw.arif-fazil.com/ |

### Critical: index.html Dev vs Dist
- **Dev index.html**: `src="/src/main.tsx"` — raw TS source, BROKEN in browser
- **Built dist/index.html**: `src="/assets/index-XXXXX.js"` — production bundle, WORKS
- If a site has BOTH `src/` and `dist/` directories AND index.html references `src/`, the site is BROKEN
- Always use `dist/index.html` as the served index.html

### Symlink Trap
Old deploys created symlinks in /var/www/html/ pointing to /opt/af-forge/sites/{domain}. These break when /opt/af-forge doesn't exist. Remove broken symlinks and replace with real directories.

## Emergency Rollback (when sites go down after git push)

```bash
# Step 1: Revert git commit immediately
cd /root/arif-sites
git reset --hard HEAD~1
git push --force origin main

# Step 2: Restore /root/sites from backup branch
cd /root/arif-sites
git worktree add /root/sites_tmp consolidation-backup 2>/dev/null || true
# If worktree fails, recreate from remote:
git branch site-autoresearch/apr26 origin/site-autoresearch/apr26
# Then manually reconstruct from git log commits

# Step 3: Fix broken symlinks in /var/www/html/
cd /var/www/html
rm -f aaa apex forge geox wiki waw arifosmcp arifos

# Step 4: Copy to Caddy web roots
for pair in "aaa:aaa.arif-fazil.com" "apex:apex.arif-fazil.com" "forge:forge.arif-fazil.com" "geox:geox.arif-fazil.com" "wiki:wiki.arif-fazil.com" "waw:waw.arif-fazil.com" "arifosmcp:arifosmcp.arif-fazil.com" "arif:arif-fazil.com"; do
  dst="${pair%%:*}"
  src="${pair##*:}"
  mkdir -p "/var/www/html/$dst"
  cp -r "/root/sites/sites/$src/." "/var/www/html/$dst/"
done

# Step 5: Fix arif main site (dev vs dist index.html)
cp /var/www/html/arif/dist/index.html /var/www/html/arif/index.html

# Step 6: Verify ALL domains — every domain must return > 0 bytes
for domain in arif-fazil.com aaa.arif-fazil.com geox.arif-fazil.com forge.arif-fazil.com apex.arif-fazil.com wiki.arif-fazil.com waw.arif-fazil.com; do
  code=$(curl -sI --max-time 8 "https://$domain/" | grep "HTTP/" | tail -1)
  size=$(curl -sL --max-time 8 "https://$domain/" | wc -c)
  echo "$domain | $code | $size bytes"
done
```

## Pre-Consolidation Checklist (BEFORE any site changes)
1. Read /etc/caddy/Caddyfile — know your serving layer
2. Identify all web root directories in /var/www/html/
3. Verify which GitHub repo/branches feed into which domains
4. Test live URLs and save content snapshots with curl
5. NEVER assume git push won't break live sites — test incrementally
6. Never copy index.html from root (dev) when dist/index.html (prod) exists

## Key Lessons
- GitHub push → CF Pages rebuild → can break all sites even on Caddy-proxied VPS
- Two copies of same repo (sites/ and arif-sites/) = chaos without clear canonical naming
- Cloudflare token auth fails for purge_cache API — cannot purge CF cache programmatically
- Broken symlinks in /var/www/html/ are silently ignored by Caddy → serve nothing
- Size 0 on HTTP 200 = Cloudflare caching empty CF Pages response, not Caddy being empty
- Dev index.html (src="/src/main.tsx") ≠ prod index.html (src="/assets/index-XXX.js")

## Verdict Protocol
Before ANY site modification: read the Caddyfile, map domain→webroot, verify live content with curl, save snapshot. After modification: verify every domain returns content > 0 bytes. If any domain goes 0 bytes, roll back immediately.

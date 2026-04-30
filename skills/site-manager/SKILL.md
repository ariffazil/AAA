---
name: site-manager
description: Manage arif-sites (arif-fazil.com, apex.arif-fazil.com, arifos.arif-fazil.com) from Telegram. Use when user asks to update content, add pages, check site health, deploy changes, manage DNS/Caddy, or troubleshoot site issues. Works via browser tool, file_write/patch, and git.
tags: [web, site, deploy, caddy, dns, arif-sites, management]
version: 1.0.0
author: arifOS AAA
license: AGPL-3.0
requirements:
  - Hermes tools: browser, file_read, file_write, patch, search_files, terminal_execute
  - Access to /root/arif-sites/ repository
  - Caddyfile knowledge for routing
---

# Site Manager — arif-sites Operations from Telegram

## Sites Managed

| Site | Domain | Path | Stack |
|------|--------|------|-------|
| BODY | arif-fazil.com | `/root/arif-sites/body/` | Trinity static site |
| SOUL | apex.arif-fazil.com | `/root/arif-sites/soul/` | Trinity static site |
| DOCS | arifos.arif-fazil.com | `/root/arif-sites/docs/` | Trinity static site |

## Available Operations

### Read & Inspect
- `file_read` any source file in the site repos
- `browser_navigate` to live site URLs to verify changes
- `browser_snapshot` to check rendered output
- `terminal_execute` → `git log --oneline -5` to see recent changes

### Edit Content
- `file_write` to create/update pages (`.html`, `.md`, `.css`, `.js`)
- `patch` for surgical string replacements
- `search_files` to find specific content across all sites

### Deploy
- `arifos-deploy` skill for full deploy workflow
- `terminal_execute` → `cd /root/arif-sites && git push` to push changes
- Check Caddy routing via `/compose/Caddyfile`

### Health Checks
- `browser_navigate` to each domain and `browser_snapshot` for basic health
- `terminal_execute` → `docker ps` to check Caddy/container status
- `browser_console` to check for JS errors

### DNS / Routing
- Check Caddyfile for routing rules
- Verify Cloudflare/NS records conceptually (cannot modify DNS from Telegram)
- Test HTTPS via browser navigate

## Typical Workflows

### "Update the homepage hero text"
1. `search_files(path="/root/arif-sites/body", pattern="hero")` → find the file
2. `file_read` the relevant HTML file
3. `patch(old_string="...", new_string="...")` to update hero text
4. `browser_navigate("https://arif-fazil.com")` → `browser_snapshot` to verify
5. `terminal_execute("cd /root/arif-sites/body && git add . && git commit -m 'Update hero'")`

### "Check if the docs site is down"
1. `browser_navigate("https://arifos.arif-fazil.com")`
2. If 404/502 → `terminal_execute("docker ps | grep caddy")`
3. Check Caddyfile for routing misconfiguration

### "Add a new page to SOUL"
1. `file_write(path="/root/arif-sites/soul/new-page.html", content="...")`
2. Update any index/nav files with `patch`
3. Commit and push
4. Verify with browser

### "Check recent deploys"
1. `terminal_execute("cd /root/arif-sites && git log --oneline -10")`
2. `browser_navigate` to each site to verify current state

## Deploy via GitHub Actions

arif-sites uses GitHub Actions for CI/CD:
- Push to `main` branch triggers deploy
- Check `.github/workflows/` in the repo for pipeline details
- Commit changes → GitHub Actions auto-deploys

## Constitutional Notes

- F01 AMANAH: No destructive file operations (rm, truncate) without 888_HOLD
- F04 CLARITY: State what changed in git commit message
- F13 SOVEREIGN: Verify with user before major content changes

## Limitations

- Cannot modify DNS records (no access to Cloudflare/registrar)
- Cannot restart system services directly — use `docker compose` for containers
- Large file uploads require git LFS or direct server access

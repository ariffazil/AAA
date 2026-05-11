---
name: cloudflare-pages-deploy
description: "Deploy arifOS static surfaces (arif-fazil.com, arifos.arif-fazil.com, docs) to Cloudflare Pages with GitHub Actions CI/CD — zero-downtime deploys."
triggers:
  - "cloudflare pages"
  - "pages deploy"
  - "cloudflare pages github actions"
  - "deploy static site"
  - "arif-sites deploy"
  - "arif-fazil.com deploy"
category: devops
---

# cloudflare-pages-deploy — Cloudflare Pages CI/CD for arifOS

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given. Every deploy is a Git commit that can be audited.

## What This Covers

| Surface | Repo | Deploy Target |
|---|---|---|
| `arif-fazil.com` | `ariffazil/arif-sites` | `arif-hub` Pages project |
| `arifos.arif-fazil.com` | `ariffazil/arifOS` | `arifOS-hub` Pages project |
| `docs.arif-fazil.com` | `ariffazil/arifOS` | `arifOS-docs` Pages project |
| `apex.arif-fazil.com` | `ariffazil/arif-sites` | `arif-apex` Pages project |

## Architecture

```
GitHub push → GitHub Actions → Cloudflare Pages → CDN edge
                                    ↓
                         Custom domain + SSL + CF WAF
```

## Setup — One-Time per Project

### 1. Create Pages project via API
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "arif-hub",
    "build_config": {
      "build_command": "npm run build",
      "destination_dir": "dist",
      "root_distribute": false
    },
    "source": {
      "type": "github",
      "config": {
        "repository_name": "ariffazil/arif-sites",
        "production_branch": "main",
        "pr_comments_enabled": true,
        "deployments_enabled": true
      }
    }
  }' | python3 -c "import json,sys; d=json.load(sys.stdin); print('✅ Created' if d.get('success') else d)"
```

### 2. Link via wrangler (interactive — easier)
```bash
cd /root/arif-sites
npx wrangler pages project list
npx wrangler pages project create arif-hub --production-branch=main
```

## GitHub Actions Workflow

Create `.github/workflows/cf-pages-deploy.yml` in the source repo:

```yaml
name: Cloudflare Pages Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
      pages: write
      id-token: write
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CF_ACCOUNT_ID }}
          projectName: arif-hub
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
          # Zero-downtime: only deploy production after merge to main
          gitHubOfficialReview: ${{ github.ref != 'refs/heads/main' }}
          wranglerVersion: '3'
```

### Add Secrets to GitHub Repo
```
Settings → Secrets and variables → Actions → New repository secret:
  CLOUDFLARE_API_TOKEN = cfat_...  (needs Pages:Edit scope)
  CF_ACCOUNT_ID = <32-char-account-id>
```

## Direct Deploy (No GitHub)

```bash
cd /root/arif-sites
npm run build

# Deploy directly
npx wrangler pages deploy ./dist \
  --project-name=arif-hub \
  --branch=main

# Or via API
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/deployments" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -F "files=@dist/index.html" \
  -F "manifest=@dist/_worker.js/manifest.json" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('Deployment ID:', d['result']['id'])"
```

## Custom Domain Setup

```bash
# Add custom domain to Pages project
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/domains" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"domain": "arif-fazil.com"}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('✅ Domain added' if d.get('success') else d)"
```

## DNS — CNAME for Pages

```bash
# Add CNAME (Pages uses CF-managed DNS)
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "arif-fazil.com",
    "content": "arif-hub.pages.dev",
    "proxied": true
  }'
```

## Verify Deploy

```bash
# Check deployment status
curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/deployments" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for dep in d['result'][:3]:
    print(f\"{dep['id'][:8]} | {dep['created_on'][:10]} | {dep['stage']} | {dep['deployment_trigger']['metadata']['branch']}\")
"

# Test live URL
curl -sI https://arif-fazil.com | grep -E "^HTTP|^content-type|^cf-ray"

# Rollback to previous deploy
LATEST_ID=$(curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/deployments" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result'][1]['id'])")

curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/deployments/${LATEST_ID}/redeploy" \
  -H "Authorization: Bearer ${CF_API_TOKEN}"
```

## Troubleshooting

### Build failing in GitHub Actions
```bash
# Check build log
# GitHub Actions UI → Actions → run → deploy job → npm run build (expand)

# Common: missing env vars (set in GitHub repo Settings → Variables)
# Common: wrong node version — use actions/setup-node with exact version
```

### Pages returning 1040 (Custom certificate error)
```bash
# Domain has custom cert but Pages needs CF-managed cert
# Disable "Edge Certificates" → "Client Certificate" in CF dashboard
# Or provision cert via:
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/custom_certificates" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"certificate": "...", "private_key": "..."}'
```

### Deploy succeeded but domain shows old content
```bash
# Purge CF cache for the domain
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"files": ["https://arif-fazil.com/*"]}'
```

## Quick Reference

```bash
# List all Pages projects
curl -s "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "
import json,sys; [print(p['name'], p['latest_deployment'][:26] if p.get('latest_deployment') else 'no deploy') for p in json.load(sys.stdin)['result']]
"

# Delete a project
curl -s -X DELETE "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub" \
  -H "Authorization: Bearer ${CF_API_TOKEN}"

# Trigger manual deploy via API
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects/arif-hub/deployments" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | python3 -c "import json,sys; d=json.load(sys.stdin); print('Deploying:', d['result']['id'])"
```

## arifOS Surface Mapping

| Domain | Source Repo | Build Command | Output Dir |
|---|---|---|---|
| `arif-fazil.com` | `arif-sites` | `npm run build` | `dist/` |
| `arifos.arif-fazil.com` | `arifOS` | `make build-pages` or custom | `public/` |
| `apex.arif-fazil.com` | `arif-sites` | `npm run build:apex` | `dist/` |
| `docs.arif-fazil.com` | `arifOS` | `mkdocs build` | `site/` |

## Constitutional Notes

- **F2 TRUTH**: Cite the CF Pages deployment ID in commit messages. "Deployed to cf-pages:abc123 — arif-fazil.com ✅"
- **F3 WITNESS**: Always `curl -sI https://domain.com` after deploy. If 200 + correct content-type, it's live.
- **F7 HUMILITY**: If deploy fails, paste the exact error. Don't guess the cause.

## Related Skills
- `cloudflare-agents` — CF token setup, Pages project creation
- `caddy-cloudflare-routing-debug` — routing issues where Pages and Caddy conflict on same domain
- `site-manager` — arifOS surface management (apex, hub, docs, MCP)

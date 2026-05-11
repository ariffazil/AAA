---
name: cloudflare-agents
description: "Unified Cloudflare capabilities for all arifOS agents — Workers, Pages, Registrar, MCP/Code Mode, AI Gateway, KV, DNS, and the Stripe Projects agent provisioning protocol."
triggers:
  - "cloudflare workers"
  - "cloudflare pages"
  - "cloudflare registrar"
  - "domain registration"
  - "stripe projects"
  - "stripe projects catalog"
  - "stripe projects init"
  - "cloudflare wrangler"
  - "deploy to cloudflare"
  - "cloudflare mcp"
  - "cloudflare code mode"
  - "workers ai"
  - "ai gateway"
  - "cloudflare kv"
  - "cloudflare dns"
  - "cfat token"
  - "cfut token"
category: devops
---

# cloudflare-agents — Unified Cloudflare Skills for arifOS Federation

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given. Cloudflare is the anvil.

---

## 1. What This Skill Covers

| Layer | Service | What Agents Can Do |
|-------|---------|-------------------|
| **Compute** | Cloudflare Workers | Deploy serverless functions, API handlers, A2A agents |
| **Static** | Cloudflare Pages | Host static sites, deploy from GitHub |
| **Domains** | Cloudflare Registrar | Register, renew, manage domains |
| **Agent Provisioning** | Stripe Projects | Agent creates CF account + buys domain + gets API token autonomously |
| **Tool Access** | Cloudflare MCP (Code Mode) | MCP tools for workers, pages, d1, kv, etc. |
| **AI** | Workers AI | Run inference (LLM, embeddings, vision) |
| **AI Ops** | AI Gateway | Token management, rate limiting, caching for AI calls |
| **Storage** | KV, D1, R2 | Key-value, SQLite, object storage |
| **DNS** | Cloudflare DNS | Manage records, proxied/traffic routing |
| **Security** | WAF, Bot Management | Firewall rules, bot scoring |
| **Caching** | Cache API, Purge | Programmatic cache control |
| **Tunnels** | Cloudflare Tunnel | Expose local services publicly |

---

## 2. The Stripe Projects Protocol (Agent Account Provisioning)

This is the key new capability from Cloudflare+Stripe (2026-04-30). It lets agents provision Cloudflare resources **without human setup steps**.

### How It Works — 3 Components

```
┌─────────────────────────────────────────────────────┐
│  AGENT (arifOS/Hermes/A-FORGE)                     │
│    ↓ discovers services                              │
│    ↓ provisions on behalf of user                    │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
     ┌─────────▼──────┐  ┌───────▼────────┐
     │  Stripe        │  │  Cloudflare    │
     │  (Orchestrator)│  │  (Provider)    │
     │  - Identity    │  │  - Accounts    │
     │  - Payment     │  │  - Domains     │
     │  - Budget ctrl │  │  - API tokens  │
     └────────────────┘  └────────────────┘
```

### Discovery
```bash
stripe projects catalog   # Returns JSON of available services
```

### Initialize a Project
```bash
stripe projects init
```

### Add Cloudflare Registrar Domain
```bash
stripe projects add cloudflare/registrar:domain
```

**What happens:**
1. If user has no CF account → Cloudflare auto-provisions one
2. If user has CF account → OAuth flow to grant access
3. Agent gets API token back — ready to deploy

### Budget Controls
- Default spend limit: **$100/month/provider**
- Raw payment details **never shared with agent**
- Agents get a Stripe **payment token** — not card details
- Set Budget Alerts in Cloudflare dashboard to raise limits

### For ArifOS Agents — Integrating Stripe Projects

**Prerequisite:** `stripe` CLI installed + `stripe login`

```bash
# Install Stripe CLI
curl -sL https://stripe.com/install | bash

# Login
stripe login

# Initialize project
stripe projects init

# Give the agent a task
stripe projects catalog   # discover available services
```

**arifOS F1-F13 compliance check before agent-initiated purchase:**
- F1 (AMANAH): Verify spend limit is set before provisioning
- F6 (EMPATHY): Inform Arif before any paid purchase
- F11 (AUTH): Confirm Arif authorized the domain/service purchase
- F13 (SOVEREIGN): Arif veto is absolute — always confirm before Stripe charge

---

## 3. Cloudflare MCP Server (Code Mode)

Cloudflare's official MCP server gives agents tools for Workers, Pages, D1, KV, etc.

### Install
```bash
npm install -g @cloudflare/mcp-server
```

### Configure for Claude Code / A-FORGE
```json
{
  "mcpServers": {
    "cloudflare": {
      "command": "npx",
      "args": ["@cloudflare/mcp-server", "--auth-token", "<CF_API_TOKEN>"]
    }
  }
}
```

### Tools Exposed by Cloudflare MCP

| Tool | Capability |
|------|------------|
| `workers_list` | List all Workers in account |
| `workers_deploy` | Deploy a Worker script |
| `pages_list` | List Pages projects |
| `pages_deploy` | Deploy to Pages |
| `d1_list` | List D1 databases |
| `d1_query` | Execute SQL on D1 |
| `kv_list` | List KV namespaces |
| `kv_read/kv_write` | KV operations |
| `dns_list` | List DNS records |
| `dns_add` | Add DNS record |
| `secret_list` | List Workers secrets |
| `secret_put` | Set a Worker secret |

### For A-FORGE (TypeScript)
```typescript
// In A-FORGE's tool registry
import { CloudflareMCP } from '@cloudflare/mcp-server';
```

---

## 4. wrangler CLI — Workers & Pages Deploy

### Install
```bash
npm install -g wrangler
wrangler auth login
```

### Deploy a Worker
```bash
cd my-worker/
wrangler deploy
```

### Deploy to a Specific Environment
```bash
wrangler deploy --env production
```

### Workers KV
```bash
wrangler kv:namespace create "ARIFOS_STATE"
wrangler kv:key put --namespace-id=<id> "session:123" '{"state":"active"}'
wrangler kv:key get --namespace-id=<id> "session:123"
```

### D1 Database
```bash
wrangler d1 create ARIFOS_DB
wrangler d1 execute ARIFOS_DB --file=./schema.sql
wrangler d1 sql ARIFOS_DB --execute "SELECT * FROM events"
```

### Secrets
```bash
wrangler secret put STRIPE_KEY
# Enter value when prompted

wrangler secret list
```

### Deploy Static Site to Pages
```bash
wrangler pages deploy ./dist --project-name=arif-hub
```

---

## 5. Deploying arifOS Surfaces to Cloudflare

### Option A — Cloudflare Pages (Static)

For `arif-fazil.com`, `arifos.arif-fazil.com` (docs/hub):

```bash
# Build the site
cd arif-sites/
npm run build

# Deploy
wrangler pages deploy ./dist \
  --project-name=arif-hub \
  --branch=main

# Or with GitHub integration
wrangler pages project create arif-hub --production-branch=main
```

### Option B — Cloudflare Workers (API/MCP Runtime)

For MCP runtime surfaces (worker-based MCP instead of VPS):

```bash
cd arifOS/
wrangler init arif-mcp-worker --template=typescript

# Configure wrangler.toml
cat > wrangler.toml << 'EOF'
name = "arif-mcp-worker"
main = "src/index.ts"
compatibility_date = "2026-04-30"

[vars]
ARIFOS_VERSION = "2026.04.30-KANON"

[[mcp]]
command = "python"
args = ["-m", "arifosmcp.server"]
EOF

wrangler deploy
```

### DNS Setup for arifOS
```bash
# Add A record for apex
wrangler dns add --type=A --name=@ --content=<WORKER_IP> arif-fazil.com

# Add CNAME for www/subdomains
wrangler dns add --type=CNAME --name=www --proxied=true --content=arif-fazil.com arif-fazil.com

# Add SRV/MX for mail
wrangler dns add --type=MX --name=@ --mail exchanger=mx1.improvmx.com --priority=10 arif-fazil.com
```

---

## 6. AI Gateway — arifOS AI Ops

AI Gateway is Cloudflare's layer for managing AI API calls (routing, rate limiting, caching, analytics).

### Use Cases for arifOS
- **Route** AI calls to MiniMax, OpenAI, Anthropic through CF
- **Cache** responses to reduce token costs
- **Rate limit** agent AI usage per session
- **Log** all AI calls for audit (VAULT999 alignment)

### Setup
```bash
# Create AI Gateway namespace
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai-gateway/gateways" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "arifos-ai-gateway", "model_type": "openai"}'
```

### Configure in Application
```bash
# Instead of calling OpenAI directly:
# https://api.openai.com/v1/chat/completions

# Route through AI Gateway:
# https://gateway.ai.cloudflare.com/<ACCOUNT_ID>/<GATEWAY_ID>/openai/v1/chat/completions
```

### Cache AI Responses
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai-gateway/gateways/arifos-ai-gateway" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"cache_ttl": 3600, "model_type": "openai"}'
```

---

## 7. Workers AI — Inference at the Edge

For GEOX physics inference, WEALTH risk calculation at the edge.

### List Available Models
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai-gateway/models" \
  -H "Authorization: Bearer <CF_API_TOKEN>"
```

### Run Inference
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai/run/@cf/meta/llama-3-8b-instruct" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Explain quantum tunneling"}]}'
```

### For arifOS — GEOX Earth Model
```python
# geox/edge_inference.py
import requests

def geox_edge_query(prompt: str, model: str = "@cf/meta/llama-3-8b-instruct"):
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{model}",
        headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
        json={"messages": [{"role": "user", "content": prompt}]}
    )
    return response.json()
```

---

## 8. Cloudflare Token Guide (arifOS Specific)

| Token Type | Prefix | Location | Capabilities |
|------------|--------|----------|-------------|
| **DNS-only** | `cfut_` | `/root/.cloudflare_token` | DNS records only. Cannot purge cache. |
| **Full API** | `cfat_` | env `CLOUDFLARE_API_TOKEN` | All CF API. Can purge, deploy, manage workers. |

**Zone ID (arif-fazil.com):** `6e837d3be53b37dcf79e0f09a1e14faa`

### Verify Token
```bash
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer <CF_API_TOKEN>" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['status'])"
```

### Token Scope for arifOS Agents

```
Minimum for read-only DNS:   zone=DNS:Read
For deploy + DNS:            zone=Workers:Edit, DNS:Edit
For full control:            account=Workers:Edit, Pages:Edit, DNS:Edit, Cache:Purge
```

---

## 9. Agent Workflows — Stripe Projects to Deploy

### Full Agent Flow: New Domain + Deploy

```bash
# Step 1: Discover
stripe projects catalog | grep -i cloudflare

# Step 2: Initialize project
stripe projects init

# Step 3: Provision Cloudflare + buy domain
stripe projects add cloudflare/registrar:domain

# Step 4: Get API token (returned by Stripe Projects CLI)
# The agent receives cfat_ token automatically

# Step 5: Deploy
export CF_API_TOKEN="<token_from_stripe>"
wrangler deploy --env production

# Step 6: Verify
curl -I https://new-domain.com/health
```

### arifOS Agent: Deploy GEOX to Cloudflare Workers

```bash
#!/bin/bash
# geox-cloudflare-deploy.sh — for A-FORGE or any arifOS agent

set -e

DOMAIN="geox.arif-fazil.com"
PROJECT="geox-earth-model"

echo "⚙️  Building GEOX..."
cd /root/geox && pip install -e .

echo "🌩️  Deploying to Cloudflare Workers..."
wrangler deploy \
  --env production \
  --name geox-worker \
  --compatibility-date 2026-04-30

echo "✅ GEOX deployed to https://geox.arif-fazil.com"
```

---

## 10. Constitutional Compliance (F1-F13)

| Floor | Compliance Requirement |
|-------|----------------------|
| **F1 AMANAH** | Never delete DNS records, purge cache, or remove workers without Arif's explicit approval. Document rollback before any destructive op. |
| **F2 TRUTH** | Always cite `wrangler deployments list` or CF API response as evidence of deploy state. Never claim "deployed" without verification. |
| **F3 WITNESS** | curl the `/health` endpoint after every deploy. curl the public FQDN, not localhost. |
| **F5 PEACE** | If deploying to a domain that affects other services, warn Arif of potential downtime. |
| **F6 EMPATHY** | Before Stripe Projects purchases, confirm with Arif. Agents spending money requires human consent. |
| **F7 HUMILITY** | If a deploy fails, say "I don't know why" — don't invent reasons. Show the error. |
| **F11 AUTH** | Verify CF token has correct scope before destructive operations. |
| **F12 INJECTION** | Sanitize domain names, Worker names — CF API rejects special chars. |
| **F13 SOVEREIGN** | Arif's domain decisions are absolute. If he says "don't touch that domain", stop. |

---

## 11. Troubleshooting

### Workers returning 1015 (Rate Limited)
```bash
wrangler tail   # Watch live logs
wrangler deployments list   # Check for conflicting deploys
```

### Pages build failing
```bash
wrangler pages project list
wrangler pages deployment list <project-name>
```

### DNS not propagating
```bash
# Check from multiple vantage points
curl -I https://arif-fazil.com
dig A arif-fazil.com @8.8.8.8
dig A arif-fazil.com @1.1.1.1

# Check proxy status
curl -s "https://api.cloudflare.com/client/v4/zones/6e837d3be53b37dcf79e0f09a1e14faa/dns_records" \
  -H "Authorization: Bearer <CF_API_TOKEN>" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(r['name'], r['type'], r['proxied']) for r in d['result']]"
```

### 522 Origin Connection Refused
- See `diagnose-cloudflare-522` skill
- Check origin server is running
- Check Cloudflare Tunnel or origin firewall

### wrangler deploy fails with "Authentication error"
```bash
wrangler auth logout
wrangler auth login
# Re-authenticate and verify token scope
```

---

## 12. Quick Reference

### Essential Commands
```bash
# wrangler
wrangler --version
wrangler deploy
wrangler dev
wrangler tail
wrangler secret list
wrangler deployments list

# DNS
curl -s "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records" \
  -H "Authorization: Bearer <CF_API_TOKEN>"

# Purge cache (requires cfat_)
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/purge_cache" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"files":["https://domain.com/*"]}'

# Workers AI
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai/run/@cf/meta/llama-3-8b-instruct"

# Stripe Projects
stripe projects init
stripe projects catalog
stripe projects add cloudflare/registrar:domain
```

### Key URLs
- CF Dashboard: https://dash.cloudflare.com
- CF API: https://api.cloudflare.com/client/v4/
- CF Workers: https://workers.cloudflare.com
- CF Pages: https://pages.cloudflare.com
- AI Gateway: https://www.cloudflare.com/ai-gateway/
- Workers AI: https://developers.cloudflare.com/workers-ai/

### arifOS Zone ID
```
Zone ID:  6e837d3be53b37dcf79e0f09a1e14faa
Account:  <CF_ACCOUNT_ID>  — check ~/.cloudflare_token or env
```

---

## 13. Sub-Skills (Specialized Operations)

These are loaded from `cloudflare-agents` but are separate skills for focused work:

| Sub-Skill | When to Use |
|-----------|-------------|
| `cloudflare-tunnel` | Expose local services without opening firewall ports — replaces *:2377 (Docker), *:8888 (Dozzle) |
| `cloudflare-workers-ai` | Edge LLM/embedding inference for GEOX Ψ-node and WEALTH coprocessors |
| `cloudflare-pages-deploy` | CI/CD static surfaces (arif-fazil.com, arifos.arif-fazil.com) via GitHub Actions |

Load with `skill_view(name)` before CF tunnel, Workers AI, or Pages deploy tasks.

## 14. Relationship to Other Skills

| Existing Skill | Relationship |
|----------------|-------------|
| `cloudflare-dns-ops` | DNS subset — superseded by this skill for new work |
| `cloudflare-tunnel` | Tunnel operations — installed above |
| `cloudflare-workers-ai` | Workers AI ops — installed above |
| `cloudflare-pages-deploy` | Pages CI/CD — installed above |
| `arifos-deploy` | Deploy philosophy — this skill provides CF-specific implementation |
| `diagnose-cloudflare-522` | Troubleshooting complement — use together |
| `caddy-cloudflare-routing-debug` | Caddy + CF routing — this skill handles CF side |
| `site-manager` | Static site management — CF Pages replaces GitHub Pages in State B |

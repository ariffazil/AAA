---
title: "SKILL: Cloudflare Platform"
type: skill
version: 1.0.0
category: cloud
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.agents/skills/cloudflare/SKILL.md]
confidence: high
---

# SKILL: Cloudflare Platform

> **Source:** `/root/.agents/skills/cloudflare/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Building on Cloudflare Workers, Pages, D1, R2, KV, AI
- Infrastructure-as-code with Terraform/Pulumi
- Networking (Tunnel, Spectrum, WAF)
- CDN, DNS, or domain management
- Keywords: cloudflare, workers, pages, d1, r2, kv, workers-ai, vectorize, tunnel, waf

---

## Quick Decision Trees

### "I need feature flags"
```
Need feature flags?
└─ Flagship binding (env.FLAGS) → flagship/
```

### "I need to run code"
```
Need to run code?
├─ Serverless functions → workers/
├─ Full-stack web app → pages/
├─ Stateful coordination → durable-objects/
├─ Multi-step jobs → workflows/
├─ Containers → containers/
└─ Scheduled cron → cron-triggers/
```

### "I need to store data"
```
Need storage?
├─ Key-value → kv/
├─ Relational SQL → d1/ (SQLite) or hyperdrive/
├─ Object/file → r2/
├─ Vectors (AI/RAG) → vectorize/
└─ Message queue → queues/
```

### "I need AI/ML"
```
Need AI?
├─ Inference → workers-ai/
├─ Vector DB → vectorize/
└─ Stateful agents → agents-sdk/
```

---

## Product Index (Selected)

### Compute
| Product | Reference |
|---------|-----------|
| Workers | `references/workers/` |
| Pages | `references/pages/` |
| Durable Objects | `references/durable-objects/` |
| Workflows | `references/workflows/` |
| Containers | `references/containers/` |

### Storage & Data
| Product | Reference |
|---------|-----------|
| KV | `references/kv/` |
| D1 | `references/d1/` |
| R2 | `references/r2/` |
| Queues | `references/queues/` |
| Hyperdrive | `references/hyperdrive/` |

### AI & ML
| Product | Reference |
|---------|-----------|
| Workers AI | `references/workers-ai/` |
| Vectorize | `references/vectorize/` |
| Agents SDK | `references/agents-sdk/` |

### Networking & Security
| Product | Reference |
|---------|-----------|
| Tunnel | `references/tunnel/` |
| WAF | `references/waf/` |
| DDoS | `references/ddos/` |
| Turnstile | `references/turnstile/` |

### Developer Tools
| Product | Reference |
|---------|-----------|
| Wrangler | `references/wrangler/` |
| Miniflare | `references/miniflare/` |
| C3 | `references/c3/` |
| Observability | `references/observability/` |

---

## Retrieval Directive

Your knowledge of Cloudflare APIs may be outdated. **Prefer retrieval over pre-training.**

| Source | URL |
|--------|-----|
| Cloudflare docs | `https://developers.cloudflare.com/` |
| Workers types | `npm pack @cloudflare/workers-types` |
| Wrangler schema | `node_modules/wrangler/config-schema.json` |

---

## Related Pages

- [[skill-wrangler]] — Wrangler CLI reference
- [[skill-agents-sdk]] — Agents SDK
- [[skill-durable-objects]] — Durable Objects
- [[skill-workers-best-practices]] — Workers production best practices
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Cloudflare platform mastered. Edge computed.*

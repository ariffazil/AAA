---
title: "SKILL: Wrangler CLI"
type: skill
version: 1.0.0
category: cloud
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.agents/skills/wrangler/SKILL.md]
confidence: high
---

# SKILL: Wrangler CLI

> **Cloudflare Workers CLI for deploying, developing, and managing Workers.**
> **Source:** `/root/.agents/skills/wrangler/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Deploying, developing, or managing Cloudflare Workers
- Managing KV, R2, D1, Vectorize, Hyperdrive, Workers AI
- Configuring wrangler.jsonc
- CI/CD with Wrangler
- Keywords: wrangler, workers, deploy, kv, r2, d1, vectorize, hyperdrive

---

## Retrieval Directive

**Prefer retrieval over pre-training.** Fetch `https://developers.cloudflare.com/workers/wrangler/` for latest CLI flags.

---

## Quick Reference

| Task | Command |
|------|---------|
| Start dev server | `wrangler dev` |
| Deploy | `wrangler deploy` |
| Dry run | `wrangler deploy --dry-run` |
| TypeScript types | `wrangler types` |
| View live logs | `wrangler tail` |
| Delete | `wrangler delete` |
| Auth status | `wrangler whoami` |
| Profile startup | `wrangler check startup` |

---

## Config (wrangler.jsonc)

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "kv_namespaces": [{ "binding": "KV", "id": "<ID>" }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  "d1_databases": [{ "binding": "DB", "database_name": "my-db", "database_id": "<ID>" }],
  "ai": { "binding": "AI" },
  "vectorize": [{ "binding": "INDEX", "index_name": "my-index" }],
  "durable_objects": { "bindings": [{ "name": "COUNTER", "class_name": "Counter" }] }
}
```

---

## KV Commands

```bash
wrangler kv namespace create MY_KV
wrangler kv key put --namespace-id <ID> "key" "value"
wrangler kv key get --namespace-id <ID> "key"
wrangler kv key list --namespace-id <ID>
```

---

## R2 Commands

```bash
wrangler r2 bucket create my-bucket
wrangler r2 object put my-bucket/path/file.txt --file ./local-file.txt
wrangler r2 object get my-bucket/path/file.txt
```

---

## D1 Commands

```bash
wrangler d1 create my-database
wrangler d1 execute my-database --remote --command "SELECT * FROM users"
wrangler d1 migrations apply my-database --local
```

---

## Secrets

```bash
# Interactive (preferred)
wrangler secret put API_KEY

# From file (for PEM keys)
wrangler secret put PRIVATE_KEY < path/to/private-key.pem

# Bulk from JSON
wrangler secret bulk secrets.json
```

**Never** pass secrets as command arguments or via `echo`.

---

## Versions & Rollback

```bash
wrangler versions list
wrangler versions view <VERSION_ID>
wrangler rollback <VERSION_ID>
```

---

## Best Practices

1. **Version control `wrangler.jsonc`** — treat as source of truth
2. **Run `wrangler types` in CI** — catch binding mismatches
3. **Use `--dry-run` before deploys** — validate without deploying
4. **Set `compatibility_date`** — update quarterly for new runtime features
5. **Use `.dev.vars` for local secrets** — never commit secrets

---

## Related Pages

- [[skill-cloudflare]] — Cloudflare platform overview
- [[skill-workers-best-practices]] — Workers production practices
- [[skill-durable-objects]] — Durable Objects
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Wrangler CLI. Workers deployed.*

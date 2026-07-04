---
title: "Skill: Cloudflare Workers Best Practices"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: infrastructure
tags: [cloudflare, workers, best-practices, streaming, promises, global-state, secrets, bindings, observability]
confidence: high
contested: false
floors: [F1, F7, F11]
risk_band: MEDIUM
sources: [/root/.agents/skills/workers-best-practices/SKILL.md]
---

# Skill: Cloudflare Workers Best Practices

> **Source:** `/root/.agents/skills/workers-best-practices/SKILL.md`
> **Agent:** OpenCode / Kimi
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Writing new Cloudflare Workers
- Reviewing Worker code for production readiness
- Configuring `wrangler.jsonc`
- Checking for common Workers anti-patterns
- Keywords: workers, best-practices, review, wrangler, cloudflare-worker

---

## Doctrine

Workers run on V8 isolates at the edge. They are NOT Node.js. Anti-patterns that work locally often fail or perform poorly at scale.

---

## Anti-Patterns Checklist

| # | Anti-Pattern | Why Bad | Fix |
|---|--------------|---------|-----|
| 1 | Floating promises | Unhandled rejections crash the isolate | Always `await` or `.catch()` |
| 2 | Global mutable state | Shared across requests, causes races | Use `new Map()` per request or Durable Objects |
| 3 | Synchronous file reads | Blocking I/O in event loop | Use streaming or `await` |
| 4 | Large bundle size | Cold start latency | Tree-shake, lazy load |
| 5 | Hardcoded secrets | Security risk | Use `env.MY_SECRET` binding |
| 6 | Missing observability | No visibility into failures | Add `console.log` + Tail / Logpush |

---

## Related

- [[skill-cloudflare]] — Platform overview
- [[skill-wrangler]] — Deployment CLI
- [[skill-durable-objects]] — Stateful coordination

---

*DITEMPA BUKAN DIBERI — Edge code must be edge-native.*

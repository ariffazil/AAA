---
title: "SKILL: Cloudflare Durable Objects"
type: skill
version: 1.0.0
category: cloud
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.agents/skills/durable-objects/SKILL.md]
confidence: high
---

# SKILL: Cloudflare Durable Objects

> **Build stateful, coordinated applications on Cloudflare's edge.**
> **Source:** `/root/.agents/skills/durable-objects/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Building stateful coordination (chat rooms, multiplayer games, booking)
- Implementing RPC methods, SQLite storage, alarms, WebSockets
- Reviewing DO code for best practices
- Designing sharding strategies
- Keywords: durable-objects, cloudflare, stateful, coordination, RPC, SQLite

---

## Retrieval Directive

**Prefer retrieval over pre-training.** Fetch `https://developers.cloudflare.com/durable-objects/` for latest docs.

---

## When to Use

| Need | Example |
|------|--------|
| Coordination | Chat rooms, multiplayer games, collaborative docs |
| Strong consistency | Inventory, booking, turn-based games |
| Persistent connections | WebSockets, real-time notifications |
| Scheduled work per entity | Subscription renewals, game timeouts |

**Do NOT use for:** Stateless request handling, maximum global distribution, high fan-out independent requests.

---

## Basic Pattern

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MY_DO: DurableObjectNamespace<MyDurableObject>;
}

export class MyDurableObject extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => {
      this.ctx.storage.sql.exec(`
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          data TEXT NOT NULL
        )
      `);
    });
  }

  async addItem(data: string): Promise<number> {
    const result = this.ctx.storage.sql.exec<{ id: number }>(
      "INSERT INTO items (data) VALUES (?) RETURNING id", data
    );
    return result.one().id;
  }
}
```

---

## Critical Rules

| Rule | Reason |
|------|--------|
| Use `getByName()` for deterministic routing | Same input = same DO instance |
| Use SQLite storage | Configure `new_sqlite_classes` in migrations |
| Initialize in constructor | Use `blockConcurrencyWhile()` for schema only |
| Use RPC methods | Not `fetch()` handler |
| Persist first, cache second | Always write to storage before in-memory state |
| One alarm per DO | `setAlarm()` replaces any existing alarm |

---

## Anti-Patterns (NEVER)

- ❌ Single global DO handling all requests (bottleneck)
- ❌ Using `blockConcurrencyWhile()` on every request (kills throughput)
- ❌ Storing critical state only in memory (lost on eviction)
- ❌ Using `await` between related storage writes (breaks atomicity)

---

## Reference Files

- `references/RULES_MD.md` — Core rules, storage, concurrency, RPC, alarms
- `references/TESTING_MD.md` — Vitest setup, unit/integration tests
- `references/WORKERS_MD.md` — Workers handlers, types, wrangler config

---

## Related Pages

- [[skill-agents-sdk]] — Agents SDK (higher-level)
- [[skill-sandbox-sdk]] — Sandbox for code execution
- [[skill-workers-best-practices]] — Workers production practices
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Durable Objects stateful. Edge coordinated.*

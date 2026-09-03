SPEC — arif_route → arif_memory Idempotency Key

> **Forge:** 2026-08-18 (Q2 of graph-engineering audit batch)
> **Status:** T1 DRAFT — F13 sovereign review by EOD
> **Pre-T2 promise:** rollback script MUST exist before T2 dry run

## Goal

When arif_route dispatches to an organ, the resulting arif_memory write must be
idempotent. Same request, same actor, same intent → write once. Concurrent routes
same actor → serialized with lock. No double-write. No race. No replay.

## Key shape

**Recommended:** ULID + actor_id + route_class + intent_hash

```
idempotency_key = ulid_new() + ":" + actor_id + ":" + route_class + ":" + intent_hash[:16]
```

- **ULID:** 128-bit, time-ordered, monotonic
- **actor_id:** from SCT (`sct_v1.*`)
- **route_class:** from arif_route dispatch class (OBSERVE / REASON / EXECUTE / IRREVERSIBLE)
- **intent_hash:** SHA-256 of normalized intent (post-classify)

Properties:
- Time ordering (ULID) — natural sort for receipts
- Per-actor scoping — no cross-actor collision
- Per-route-class separation — different actions don't collide
- Per-intent fidelity — same intent + same actor = same key

## Collision policy

- Same key → drop write (already sealed)
- Different ULID + same actor_id + same intent_hash → merge if within 60s window
  (rare clock-skew case)
- Different intent_hash → never collide (different intents)

## TTL

- Idempotency key TTL: 24h
- Memory write TTL: governed by L2-L6 memory architecture
  (Redis 24h, Postgres 30d, Qdrant forever)

## F11 Auditability role

Every write logs:
- idempotency_key
- actor_id
- route_class
- intent_hash
- ULID
- parent_seal_hash
- timestamp

VAULT999 receives idempotency_key as part of receipt metadata.
Replay attack prevention: actor_id + intent_hash must match the SCT-signed session.

## Load estimate

Prior to migration: empirical probe needed. Two regimes:

- **Low** (<10 concurrent routes/sec): in-memory lock + Postgres UNIQUE constraint
- **High** (>50 concurrent routes/sec): Redis-cached lock + Postgres advisory lock
  + natural shard by actor_id

**Default to low** unless probe shows otherwise. Optimize only when measured.

## Test fixtures (T1 next)

1. Same request twice → must dedupe (only one write)
2. Concurrent routes same actor → must serialize (no race)
3. Key collision edge case (same key, different ULID) → dominant ULID wins
4. Regression: existing behavior preserved (no breaking change)

## Rollback script (T1.5 — must exist BEFORE T2)

`rollback-arif-memory-idempotency.sh`:

1. Drop idempotency_key column on writes table
2. Drop Redis cache key prefix
3. Restore previous write path (no key check)
4. Verify: write throughput matches pre-migration baseline

Dry run in staging first. Pre-flight: backup writes table.

## Open questions

- Should the lock be advisory (Postgres) or strict (Redis)?
  Default: Redis, fall back to advisory if Redis down.
- Does arif_route emit the key, or does arif_memory compute it?
  Default: arif_route emits (closer to source of truth).
- What happens on actor_id change (session restart)?
  New key, no merge (different actor).

## Timeline

- **Today (T1):** spec sheet drafted — F13 review by EOD
- **Tomorrow (T1):** fixtures + rollback script
- **Wed–Thu (T2):** dry run 24h, observe
- **Friday (T2):** prod if green, ANNOUNCE 10s

## Scar

Spine-touching change. Treat as constitutional — any breakage affects memory
guarantee across federation. Two-day dry run minimum. No shortcuts.

DITEMPA BUKAN DIBERI ⚒️

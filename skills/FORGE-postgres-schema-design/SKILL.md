# ⚒️ PostgreSQL Schema Design — Federation Data Layer

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Design and maintain PostgreSQL schemas for the federation: capability registry, organ pulse history, drift detection, witness receipts, session state, cooling ledger entries.

## When to Use
- Designing new tables or migrations for arifOS, AAA, GEOX, WEALTH, WELL Postgres backends
- Schema for capability registry (tool manifest storage)
- Pulse history tables (organ health time series)
- Drift detection storage (source ↔ runtime comparison snapshots)
- Witness receipt tables (tri-witness evidence logs)

## When NOT to Use
- Vector/semantic search — use `redis-qdrant-integration`
- Immutable append-only ledger — use `vault999-witness`
- Caching layer — use `redis-qdrant-integration`
- Frontend state — use `react-spa-discipline`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | All schema changes via migration files; never `ALTER TABLE` in production |
| F2 TRUTH | Columns typed precisely (TIMESTAMPTZ, UUID, JSONB) — no varchar(255) laziness |
| F4 CLARITY | Normalize to 3NF by default; only denormalize for measured query perf |
| F11 AUDIT | Every table has `created_at`, `updated_at`, `actor_id` audit columns |
| F13 SOVEREIGN | Schema drops require 888_HOLD — data is civilizational memory |

## Commands & Patterns

```sql
-- Capability registry table pattern
CREATE TABLE capability_registry (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organ_id    TEXT NOT NULL REFERENCES organs(id),
    tool_name   TEXT NOT NULL,
    schema_json JSONB NOT NULL,
    status      TEXT NOT NULL DEFAULT 'active',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor_id    TEXT NOT NULL
);

-- Pulse history (time-series)
CREATE TABLE organ_pulses (
    id          BIGSERIAL PRIMARY KEY,
    organ_id    TEXT NOT NULL,
    status      TEXT NOT NULL,
    latency_ms  INTEGER,
    payload     JSONB,
    sampled_at  TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (sampled_at);

-- Migration pattern — always reversible
-- V001__create_capability_registry.sql
-- V002__add_organ_pulses.sql
```

## Refusal Surface
- ❌ `SELECT *` in production queries — always name columns
- ❌ Schema changes without migration files
- ❌ Storing JSON when relational columns fit the data
- ❌ Missing indexes on foreign keys and `sampled_at` columns
- ❌ `DROP COLUMN` or `DROP TABLE` without 888_HOLD

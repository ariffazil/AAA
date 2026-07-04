---
title: "SKILL: Database Tuning"
type: skill
version: 1.0.0
category: infra
risk_band: MEDIUM
floors: [F1]
evidence_required: true
sources: [/root/.opencode/skills/database-tuning/SKILL.md]
confidence: high
---

# SKILL: Database Tuning — arifOS VPS

> **Source:** `/root/.opencode/skills/database-tuning/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- PostgreSQL or Redis slow performance
- Memory pressure, high load
- After VPS resize
- Query optimization, cache tuning
- Keywords: postgres, PostgreSQL, redis, tuning, performance

---

## Current State (2026-05-14)

| Setting | Current | Optimal | Gap |
|---------|---------|---------|-----|
| PostgreSQL shared_buffers | 128MB | 4GB | 🔴 32x under |
| PostgreSQL work_mem | 4MB | 16MB | 🟡 4x under |
| PostgreSQL effective_cache_size | 4GB | 12GB | 🟡 3x under |
| PostgreSQL max_connections | 100 | 50-100 | ✅ OK |
| Redis maxmemory | 512MB | 512MB | ✅ FIXED |
| Redis maxmemory-policy | allkeys-lru | allkeys-lru | ✅ FIXED |

---

## PostgreSQL Tuning

```bash
docker exec postgres psql -U arifos_admin -d vault999 -c "
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
"
# Then: docker compose restart postgres
```

### What Each Setting Does

| Setting | What It Does |
|---------|-------------|
| shared_buffers | RAM PostgreSQL uses as cache (15GB VPS, using 128MB = 1 seat of 15-seat car) |
| work_mem | Memory per query operation (4MB = spills to disk) |
| effective_cache_size | Tells PostgreSQL OS has this much cache (helps planner) |
| maintenance_work_mem | Memory for VACUUM and CREATE INDEX |

---

## Redis Tuning (Already Optimal)

```
maxmemory: 512MB (was unlimited — would crash VPS)
maxmemory-policy: allkeys-lru
```

No further tuning needed.

---

## Monitoring Queries

```bash
# Check slow queries
docker exec postgres psql -U arifos_admin -d vault999 -c "
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
"

# Check Redis memory
docker exec redis redis-cli INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio"

# Check PostgreSQL cache hit ratio
docker exec postgres psql -U arifos_admin -d vault999 -c "
SELECT
  sum(heap_blks_read) as disk_reads,
  sum(heap_blks_hit) as cache_hits,
  round(sum(heap_blks_hit) * 100.0 / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0), 1) as cache_hit_pct
FROM pg_statio_user_tables;
"
# Target: cache_hit_pct > 95%
```

---

## Warning Signs

| Sign | Fix |
|------|-----|
| cache_hit_pct < 95% | Need more shared_buffers |
| Redis mem_fragmentation_ratio > 1.5 | Memory fragmentation |
| Redis mem_fragmentation_ratio < 1.0 | Redis swapping to disk (very bad) |
| Connections near max_connections | Need PgBouncer |

---

## Related Pages

- [[skill-vps-audit]] — full system audit
- [[skill-vps-management]] — VPS management
- [[skill-backup-dr]] — database backup procedures
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Database tuned. VPS optimized.*

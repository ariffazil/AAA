# Docker Postgres Auth Pattern — 2026-05-19

## Problem

Standard `psql` via Unix socket fails when container user doesn't match DB role:
```
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL: role "root" does not exist
```

Even trying `docker exec postgres psql` fails because exec inherits root, not the DB user.

## Working Pattern

```bash
# Auth string embedded in connection URI
docker exec postgres bash -c "psql 'postgresql://arifos_admin:ArifPoRT22!@localhost:5432/vault999?sslmode=disable' -c 'SELECT 1, now();'"
```

Key insight: use `@localhost:5432` not the socket, and embed credentials in the URI.

## Get Credentials First

```bash
docker exec postgres env | grep -E "POSTGRES_(USER|DB|PASSWORD)"
# Returns: POSTGRES_USER=arifos_admin, POSTGRES_DB=vault999, POSTGRES_PASSWORD=ENC[AE...]
```

## Schema Inspection

```bash
# List tables
docker exec postgres bash -c "psql 'postgresql://arifos_admin:PASS@localhost:5432/vault999?sslmode=disable' -c '\dt'"

# Inspect vault_seals schema
docker exec postgres bash -c "psql 'postgresql://arifos_admin:PASS@localhost:5432/vault999?sslmode=disable' -c '\d vault_seals'"

# Query sealed entries
docker exec postgres bash -c "psql 'postgresql://arifos_admin:PASS@localhost:5432/vault999?sslmode=disable' -c 'SELECT * FROM vault_seals LIMIT 3;'"
```

## VAULT999 Tables

| Table | Rows | Purpose |
|-------|------|---------|
| vault_seals | 8 | Immutable sealed entries |
| vault999_witness | 0 | Witness records |
| memory_records | various | Hermes memory records |
| memory_embeddings | various | Vector embeddings |

## Note on Supabase

Supabase cloud (`utbmmjmbolmuahwixjqc.supabase.co`) is **NOT** the vault storage. It's JWT verification (auth only). The actual VAULT999 lives in:
1. `/root/arifOS/VAULT999/*.jsonl` files (12,342 entries)
2. Docker postgres `vault999` database

When Arif asked "is my vault999 real" — he meant L1+L2. Not Supabase.
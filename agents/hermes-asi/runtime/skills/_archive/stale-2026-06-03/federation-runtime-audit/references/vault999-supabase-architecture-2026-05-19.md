# VAULT999 + arifOS Diagnostic — 2026-05-19

## Three-Layer Architecture (Verified)

| Layer | Storage | Status | Notes |
|-------|---------|--------|-------|
| L1 | `/root/arifOS/VAULT999/*.jsonl` | ✅ 12,342 + 104 entries | Primary immutable ledger |
| L2 | Docker postgres `vault999` DB | ✅ 8 sealed entries | Secondary; `vault_seals` table active |
| L3 | Supabase cloud | ⚠️ Separate | JWT verification only, NOT vault storage |

**Key insight:** Arif's "is my vault999 real" question → L1+L2. Supabase is a red herring.

## Verified State (2026-05-19 00:52 UTC)

```
Database: vault999 (docker, user: arifos_admin, PASS: ArifPoRT22!)
Tables: vault_seals (8 rows), vault999_witness (0 rows), memory_records, etc.
Schema: vault_seals has 20 columns (chain_hash, seal_hash, epoch, witness, etc.)

JSONL:
- outcomes.jsonl: 12,342 entries (last write May 17)
- vault999.jsonl: 104 entries
- SEALED_EVENTS.jsonl: 1.3MB
```

## Critical Distinction

- **Supabase** (`utbmmjmbolmuahwixjqc.supabase.co`): Cloud managed Postgres — JWT verification only
- **Local docker postgres**: Primary vault storage for arifOS MCP
- arifOS MCP connects to **local docker postgres**, not Supabase cloud

## Docker Postgres Auth Pattern

Standard `psql` via socket fails because socket user doesn't match DB role.

**Working approach:**
```bash
docker exec postgres bash -c "psql 'postgresql://arifos_admin:ArifPoRT22!@localhost:5432/vault999?sslmode=disable' -c 'SELECT 1, now();'"
```

Schema inspection:
```bash
docker exec postgres bash -c "psql 'postgresql://arifos_admin:PASS@localhost:5432/vault999?sslmode=disable' -c '\d vault_seals'"
docker exec postgres bash -c "psql 'postgresql://arifos_admin:PASS@localhost:5432/vault999?sslmode=disable' -c 'SELECT * FROM vault_seals LIMIT 3;'"
```

Get credentials:
```bash
docker exec postgres env | grep -E "POSTGRES_(USER|DB|PASSWORD)"
```

## Cross-Agent Patch Validation (WEALTH Enhancement)

This session demonstrated recursive cross-agent review working correctly:
- Arif proposed abstraction enhancement to WEALTH tools
- OpenClaw reviewed and caught **3 bugs** in the proposal
- Hermes applied OpenClaw's corrected patch
- Verified: syntax OK, backward compatible, lint passed

**3 bugs caught:**
1. `hedge_drag` formula: `abs(brent - rm_usd_rate*100)` → correct: `abs(brent - hedge_lock) / brent`
2. `refinery_stress` scope: defined inside `if` block but referenced outside → default 0.0
3. Dead code: `revenue_rm_impact` computed but never returned → removed

**Principle:** OpenClaw wins on code correctness. Hermes wins on intent/framework.
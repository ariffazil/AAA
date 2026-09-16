# KIMINA Repair Catalog — Bounded Auto-Heal

> **Authority:** R0-R2 autonomous. R3+ → 888_HOLD
> **Source:** AAA-REPAIR-ALLOWLIST-V1.yaml (governance)

## Registered Playbooks

### PB-406 — HTTP Content Negotiation (R1)
- **Trigger:** HTTP 406 from local service
- **Fix:** Normalize Accept/Content-Type headers
- **Max attempts:** 2
- **Timeout:** 10s
- **Forbidden:** Modifying auth logic, bypassing policy gates

### PB-VENV — Missing Dev Dependency (R2)
- **Trigger:** ModuleNotFoundError in virtualenv
- **Fix:** pip install from lockfile/manifest
- **Max attempts:** 1
- **Timeout:** 60s
- **Forbidden:** Global pip install, unvetted packages

### PB-ZOMBIE — Stale Process Cleanup (R2)
- **Trigger:** "Address already in use" / dead lockfile
- **Fix:** SIGTERM + verify PID + cleanup lockfile
- **Max attempts:** 2
- **Timeout:** 15s
- **Forbidden:** Killing core federation daemons (caddy, postgres, redis, qdrant, litellm)

### PB-GIT-CONFLICT — Auto-Generated File Conflict (R2)
- **Trigger:** Merge conflict in auto-generated paths only
- **Fix:** checkout --theirs for generated files, recompute indexes
- **Max attempts:** 1
- **Timeout:** 30s
- **Forbidden:** Force push, dropping human changes

## Execution Rules

1. **Dry-run first** — ALWAYS
2. **Preconditions must pass**
3. **Rollback verified** before mutation
4. **Post-repair test** after mutation
5. **Circuit breaker** — 1 failed attempt → STOP, escalate
6. **Log everything** to kimi.json auto_heal_log[]

## New Scar: Provider Endpoint Migration (from 2026-09-16)

Added from Hermes session — not a playbook but a migration skill with 6 rules:
1. Grep the VARIABLE, then grep the DEFAULT
2. One subsystem, many variables (the 4-variable trap)
3. systemd EnvironmentFile beats Environment=
4. Retune timeouts; remote is not local
5. Prove with deepest consumer, not health endpoint
6. Sequence: quiesce → change → verify → resume

**File:** `/root/AAA/skills/provider-endpoint-migration/SKILL.md`

DITEMPA BUKAN DIBERI ⚒️

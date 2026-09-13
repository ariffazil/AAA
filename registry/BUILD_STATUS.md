# Warga Manager — Build Status

> **Updated:** 2026-09-14T01:50+08:00 | **Status:** PARTIAL → LIVE

## Fixes Applied (from FI-008 Assessment)

### Fix 3 — Canonical Identity Binding ✅
- `/root/AAA/registry/canonical_agents.json` — 34 canonical agents
- All registrations resolve through canonicalize() before write
- Known aliases mapped: hermes-asi→hermes, kimi-code→FI-008, claude-code→FI-002, etc.
- Free-form strings REJECTED — no sixth spelling site

### Fix 5 — Seed Registry ✅
- Bootstrap reads from AGENTS_UNIFIED.yaml (the SOT)
- 28 agents registered from 2 canonical sources
- 15 aliases registered
- Decommissioned agents marked: 777-forge, A-AUDIT, A-ARCHIVE, aider

### Fix 4 — Cron Status
- Job `5e9f3ba79969` exists in Hermes scheduler (not OS crontab)
- Same as all 26 other federation crons
- Next run: 2026-09-14T08:00:00+08:00

## Current State

```
═══ WARGA REGISTRY ═══

  28 agents registered
  24 active | 4 decommissioned
  3 sovereign-witness (333-AGI, 555-ASI, 888-APEX)
  21 novice
  0 apprentice | 0 journeyman

  All reviews due: 2026-10-13 (29 days)
  Gossip events: 0
  Prune candidates: 0
```

## Files

| File | Purpose | Size |
|------|---------|------|
| `warga.jsonl` | Append-only citizen registry | 28 records, 15KB |
| `canonical_agents.json` | Canonical identity map (Fix 3) | 34 agents |
| `canonical_identity.py` | Identity resolution module | canonicalize(), register_alias() |
| `warga_manager.py` | Core manager (909 lines) | register, lifecycle, gossip, dashboard |
| `warga_sweep.py` | Daily cron sweep | review queue, prune, gossip |
| `warga_bootstrap.py` | Bootstrap from federation SOT | reads AGENTS_UNIFIED.yaml |
| `scar_gossip.jsonl` | Gossip protocol | 0 events |

## Remaining Fixes

### Fix 1 — Prune KELUAR
prune function works but targets the warga registry. Need to also consume forge_agent dead entries. The decommissioned agents (777-forge, A-AUDIT, A-ARCHIVE, aider) are the first candidates.

### Fix 2 — Don't Create 6th Storage
warga.jsonl is now CONSUMED FROM the SOT (AGENTS_UNIFIED.yaml), not created independently. The canonical_agents.json is the binding layer. This addresses the "6th storage site" concern.

## Usage

```bash
# Dashboard
python3 /root/AAA/registry/warga_manager.py dashboard --surface all

# Register new agent (must be in canonical_agents.json first)
python3 /root/AAA/registry/warga_manager.py register <canonical-id> --role <role>

# Lifecycle review
python3 /root/AAA/registry/warga_manager.py review <id> --verdict continue --fq 0.85

# Daily sweep
python3 /root/AAA/registry/warga_sweep.py

# Bootstrap from SOT
python3 /root/AAA/registry/warga_bootstrap.py
```

---

*DITEMPA BUKAN DIBERI ⚒️*

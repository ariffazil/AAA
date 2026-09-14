# CORRECTION RECEIPT — Phase A Port Errors
**Date:** 2026-09-14 10:10 MYT
**Authority:** ARIF (F13 Sovereign)
**Severity:** HIGH — two healthy organs mislabeled as BROKEN

---

## Errors Found

Phase A Reality Graph probed wrong ports for 3 services, resulting in **2 healthy organs incorrectly classified as BROKEN**.

| Service | Phase A Claim | Actual Port | Real Status | Evidence |
|---------|--------------|-------------|-------------|----------|
| WELL | :18087 (BROKEN) | **:18083** | **ALIVE (degraded)** | health: 31 tools, well_score=88.4, identity="WELL" |
| GEOX | :18086 (BROKEN) | **:8081** | **ALIVE (healthy)** | health: 26 tools, SEAL verdict, identity="geox-8c6c7f2d" |
| AAA A2A | :18083 | **:3001** | **ALIVE (healthy)** | health: healthy, vault=CONNECTED, 54 ledger events |

## Root Cause

Phase A used port numbers from documentation/stale references rather than live probing `ss -tlnp` first. The ports :18086 and :18087 were **never bound** by any service — they were phantom references.

## Impact

- 2 organs incorrectly declared BROKEN → potential unnecessary "fix" actions
- 1 port double-claimed (:18083 assigned to both AAA A2A and WELL)
- System health summary was wrong: actual state is better than reported

## Corrected Classification

| Node | Correct Port | Status |
|------|-------------|--------|
| WELL MCP | :18083 | ALIVE (degraded — self-reported presence, not sensor-verified) |
| GEOX MCP | :8081 | ALIVE (healthy, 26 tools, SEAL verdict) |
| AAA A2A | :3001 | ALIVE (healthy, vault connected) |

## System Health (Corrected)

- **Before correction:** 55 ALIVE, 9 BROKEN
- **After correction:** 57+ ALIVE, 7 BROKEN (WEALTH data servers + others remain broken)

## Lesson

**Probe the port, not the documentation.** `ss -tlnp` is truth. README is narrative.

---

*This error is itself evidence for the mandate: Reality outranks narrative. I trusted documentation over probing.*

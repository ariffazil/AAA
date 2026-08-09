<!-- DELETED | 2026-08-09 -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction (Tier B/C/D pass). -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights extracted from this file. -->


# Session C — Health Schema Unification
**Status:** READY · **Authority:** F2 TRUTH · F4 CLARITY · **Blast:** MEDIUM

Replace generic "healthy" flags with explicit state vectors: liveness (UP/DOWN), readiness (READY/DEGRADED/BLOCKED), freshness (FRESH/STALE/UNKNOWN + age_seconds), authority (OBSERVE_ONLY/PROPOSE_ONLY/EXECUTE_GATED). Roll out across all 6 organs. WELL must stay REFLECT_ONLY when biometric stale.

**Output:** `SESSION_C_HEALTH_SCHEMA_REPORT.md`

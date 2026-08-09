<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# Session C — Health Schema Unification
**Status:** READY · **Authority:** F2 TRUTH · F4 CLARITY · **Blast:** MEDIUM

Replace generic "healthy" flags with explicit state vectors: liveness (UP/DOWN), readiness (READY/DEGRADED/BLOCKED), freshness (FRESH/STALE/UNKNOWN + age_seconds), authority (OBSERVE_ONLY/PROPOSE_ONLY/EXECUTE_GATED). Roll out across all 6 organs. WELL must stay REFLECT_ONLY when biometric stale.

**Output:** `SESSION_C_HEALTH_SCHEMA_REPORT.md`

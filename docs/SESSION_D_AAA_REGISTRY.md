<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# Session D — AAA Registry Fail-Closed
**Status:** READY · **Authority:** F1 AMANAH · F11 AUDIT · **Blast:** LOW

Refactor AAA registry (JavaScript) to throw `DUPLICATE_AGENT_ID` on collision. Enforce `organ.*` vs `pillar.*` namespaces. Boot rule: AAA refuses READY if duplicates exist. Tests for duplicate agentId and namespace enforcement.

**Output:** `SESSION_D_AAA_REGISTRY_REPORT.md`

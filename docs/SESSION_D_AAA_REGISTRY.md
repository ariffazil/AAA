# Session D — AAA Registry Fail-Closed
**Status:** READY · **Authority:** F1 AMANAH · F11 AUDIT · **Blast:** LOW

Refactor AAA registry (JavaScript) to throw `DUPLICATE_AGENT_ID` on collision. Enforce `organ.*` vs `pillar.*` namespaces. Boot rule: AAA refuses READY if duplicates exist. Tests for duplicate agentId and namespace enforcement.

**Output:** `SESSION_D_AAA_REGISTRY_REPORT.md`

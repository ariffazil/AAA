# SCAR-2026-09-25-001 — Source-Type Promotion Gate

**Origin:** ChatGPT deep research review (2026-09-25, attached by Arif). 
Key finding: memory content must never inherit authority merely by surviving.
frequent_retrieval(AGENT_INFERRED) ≠ USER_RATIFIED.

**Doctrine sealed:**
1. `source-type-promotion-gate.md` (F13_RATIFIED_CHAT) — prevents AGENT_INFERRED from
   being promoted to canonical through repeated retrieval.
2. `claim-lifecycle-states.md` (F13_RATIFIED_CHAT) — adds 6 lifecycle states to claim_ledger.
3. `carry_forward.json` open_questions lane — first-class primitive for unresolved questions.

**Integration test (manual, tonight):**
- Write one AGENT_INFERRED claim about Arif → verify tag NON_PROMOTABLE set.
- Try to promote via retrieval count → must be rejected with audit log.
- Open question "apa lepas PETRONAS" → DELIBERATELY_OPEN, no inference.

**Filed under:** memory governance / source-type inequality
**Filed by:** irfanclaw
**Filed at:** 2026-09-25T00:36:00+08:00

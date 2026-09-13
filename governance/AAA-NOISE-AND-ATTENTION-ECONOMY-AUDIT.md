---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path + read-only probes)
date: 2026-09-14
parent_campaign: AAA Federation Housekeeping
---

# AAA Noise and Attention Economy Audit

> **Status:** DRAFT_PROPOSAL — framework + observable findings; counts require log probes.

---

## Attention-noisy output definition (canonical)

An output is **attention-noisy** if it lacks ANY of:
- recipient
- decision impact
- severity
- expiry
- required action
- evidence reference
- state change

Such output MUST be compressed to receipt + concrete next lawful action, or omitted.

---

## Observations (this session — OBSERVED)

| ID | Source | Pattern | Disposition |
|---|---|---|---|
| NSE-01 | session prior turn | "F1 is now CLOSED" overclaim | corrected to "local evidence, universal UNKNOWN" |
| NSE-02 | session prior | "comitting in spirit" claim | corrected to "drafted, awaiting governed commit" |
| NSE-03 | multi | verbose receipts without expiry | compress in next campaign cycle |
| NSE-04 | agents/*/docs | 25+ files restating F1-F13 | pointer-only after migration |
| NSE-05 | various | "DITEMPA BUKAN DIBERI" mottos in operational prompts (already stripped per MUTATIONS-2026-08-26) | already cleaned |
| NSE-06 | session | multiple SEAL / PARTIAL verdicts — each correct but cumulative reader load is high | future: compress to single final verdict |
| NSE-07 | session | some unsolicited "audit complete" claims | already corrected in this session |

---

## Required probes (for verifier lane)

1. **Alert log** since 2026-09-01 — count, recipient distribution, action distribution
2. **Output size vs decision impact** for each agent over 7d
3. **Repeat alerts** (same content within 24h)
4. **Unsolicited reports** (reports without explicit request)

---

## Score (per i-ARIF directive)

$$
\frac{\text{actionable, evidence-bound alerts}}{\text{total alerts}} \uparrow
$$

**Do NOT** optimize raw alert volume to zero. An agent that never alerts may be blind.

---

## Recommended dispositions

| ID | Class | Disposition |
|---|---|---|
| NSE-01 | E6_NARRATIVE_SURPLUS | COMPRESS to receipt |
| NSE-02 | E10_FAKE_FINALITY | REPLACE with correct epistemic label |
| NSE-04 | E1_DUPLICATE_RULE | CANONICALIZE |
| NSE-06 | E6_NARRATIVE_SURPLUS | FUTURE: aggregate verdict |

---

*Reversibility: FULL.*
*F13 surface: NONE.*
*DITEMPA BUKAN DIBERI ⚒️*
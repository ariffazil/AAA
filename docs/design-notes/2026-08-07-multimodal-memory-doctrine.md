<!-- DELETED | 2026-08-09 -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction (Tier B/C/D pass). -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights extracted from this file. -->


# Design Note: Multimodal Memory Architecture — Additive Principles

**Origin:** MMA-2026-08-07 session (multimodal memory audit + Copilot synthesis)
**Author:** hermes (validated against F1-F13 + live federation probe)
**Status:** PROPOSAL — not canon. Design note for sovereign review.
**Date:** 2026-08-07

---

## Summary

Fifteen principles were proposed during session convergence analysis. Eleven (11/15) already exist in F1-F13, the authority chain, or VAULT999. Four (4/15) are genuinely additive. This document captures the 4 additive principles only.

The one principle that was *rejected* is: "auditor > generator > reality hierarchy." The existing authority chain (arif_init → ... → arif_judge → arif_forge → arif_seal) already encodes verification/audit at the `arif_think` and `arif_judge` layers. Adding an "auditor" authority level would create doctrine inflation (RSI doctrine: 2026-08-06 — "No new GENESIS, no new floors").

---

## Principle P3: Preserve Disagreement (NEW)

**Statement:** When multiple memory witnesses disagree, store the disagreement as a structured artifact. Never average away conflict.

**Shape:**
```yaml
witnesses:
  semantic:
    verdict: string
    confidence: float
  affective_observation:
    verdict: string
    confidence: float
  relational:
    verdict: string
    confidence: float
  temporal:
    verdict: string
    confidence: float
  provenance:
    verdict: string
    confidence: float
```

**Rationale:** A memory query that returns a single ranked list hides cross-witness conflict. The arbitration architecture (05_retrieval_arbitration.md) specifies 6 conflict types. This principle captures the general rule behind those specifics.

**Relationship to existing floors:** Extends F2 TRUTH (epistemic honesty) + F4 CLARITY (structured output reduces entropy).

---

## Principle P8: Retrieval Is Not Memory (NEW)

**Statement:** Never confuse easy retrieval with faithful memory.

**What memory should preserve:**
- What happened
- Who was involved
- How it was experienced
- How it was known
- Why it mattered

**What retrieval optimizes for:**
- Relevant chunk ranking
- Query-answer precision

**Rationale:** Standard RAG (pguso/rag-from-scratch, LangChain, etc.) optimizes for "can I find the relevant chunk?" The multi-witness memory architecture optimizes for "did the recalled memory preserve reality?" These are different objective functions.

**Relationship to existing floors:** Extends F2 TRUTH (memory fidelity) + F3 TRI-WITNESS (multi-source corroboration).

---

## Principle P9: Multi-Witness Memory Object (NEW)

**Statement:** Every long-term memory entry should carry artifact, semantic, affective_observation, affective_interpretation, relational, temporal, provenance, and salience faces. No single witness becomes sovereign.

**Target shape:** Per 04_memory_object_proposal.md (T1 schema patch).

**Rationale:** This is the architectural specification behind P3. Without the memory object shape, P3 has no implementation surface. Together, they specify what to store and how to preserve disagreement.

**Relationship to existing floors:** Extends F11 AUDITABILITY (provenance per field) + F14 (proposed: every memory must have provenance — already partially covered by F11).

---

## Principle P12: Confidence Must Be Earned (NEW)

**Statement:** Confidence sources are: (1) observation, (2) verification, (3) cross-witness agreement, (4) artifact integrity, (5) reproducibility. Confidence is NOT earned by: model certainty, verbose explanations, or agent reputation.

**Rationale:** F7 HUMILITY already caps confidence at 0.95-0.97. This principle specifies *what counts toward confidence* — the input signals. Without this, F7 caps the output but doesn't constrain the inputs.

**Relationship to existing floors:** Extends F7 HUMILITY (confidence cap) + F2 TRUTH (evidence labeling).

---

## Rejected: "Auditor Hierarchy" (P13)

**Rejected because:** The existing authority chain already encodes verification/audit at `arif_think` (555 lane — causal verification) and `arif_judge` (666 lane — constitutional verdict). Adding an "auditor" authority level creates doctrine inflation. The RSI doctrine (2026-08-06) explicitly prohibits new floors/laws after philosophy dialogues.

**What survives:** The 333/555/888 lane separation in the A2A operating model is correct and already implemented. No change needed.

---

## Operational upgrades arising from this session

### Upgrade A: Pre-Seal Gate

Add a mandatory pre-seal verification before `arif_seal`:

```yaml
pre_seal_gate:
  artifact_hash_matches: true
  artifact_name_matches: true
  artifact_count_matches: true
  sealed_by: string
  sealed_at: ISO datetime
  source: string
```

**Purpose:** Prevents the sibling-overwrite artifact drift incident (07_validation_report.md was rewritten by a sibling subagent while hermes was auditing).

### Upgrade B: Risk-Tiered Verification

| Risk tier | Verification level | Example |
|---|---|---|
| Read-only observation | Lightweight | grep, curl, ls |
| Schema migration | Medium | dry-run, diff, backward compat check |
| Financial mutation | Heavy | re-probe, cross-witness, human review |
| Irreversible | Maximum | mandatory re-probe + sovereign approval |

**Purpose:** "Always re-probe" (Principle P11) without causing paralysis.

### Upgrade C: Auditor Outputs Are Claims

Every auditor verdict is a CLAIM, not TRUTH. Generators, verifiers, and auditors all produce claims that require evidence. No agent is exempt from F2 TRUTH.

**Purpose:** The Hermes self-audit caught its own VAULT count drift and inherited trust on 06_upgrade_roadmap.md. Auditors are not infallible — they are just another source of claims.

---

*Forged as design note, not canon. Sovereign review required before adoption.*
*DITEMPA BUKAN DIBERI.*

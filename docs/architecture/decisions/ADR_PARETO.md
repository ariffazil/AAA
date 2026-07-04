# ADR-013: Pareto Decision Architecture

> **Status:** PROPOSED
> **Date:** 2026-06-30
> **Author:** Hermes (888 directive)
> **Domain:** Cross-organ — A-FORGE execution pipeline (primary), all federation decisions (secondary)
> **Ratification:** Pending F13 SOVEREIGN
> **DITEMPA BUKAN DIBERI**

---

## Context

Federation agents suffer from **analysis paralysis dressed as thoroughness.** An agent will iterate a decision across 15+ factors, re-check marginal variables, and polish cosmetic edges — while the 5 factors that actually move the outcome are already resolved. This is perfectionism-as-noise: optimizing the bezel, not the engine.

The sovereign identified three layers to this problem:

1. **Pareto concentration** — In any decision, 5–10 factors drive 95% of outcome variance. Everything else is noise.
2. **Diminishing returns on even the important factors** — Past a threshold, one more hour studying factor #3 doesn't move the needle.
3. **Perfectionism as margin obsession** — The brain rewards "I checked all 50 factors" (dopamine from completion) over "I understand 5 and decided" (which feels premature but is correct).

The federation needs a structural brake on over-analysis that does not become a new permission gate.

---

## Decision

Implement a **3-component Pareto Decision Architecture** for the A-FORGE execution pipeline, with cross-organ applicability:

### Component 1: 5-Slot Mandatory Factor Gate

Every execution-class decision MUST assess exactly 5 factors. No more are mandatory. Optional slots 6–10 exist but carry no obligation.

| Slot | Factor | Question | Evidence Class |
|------|--------|----------|----------------|
| **S1** | Sovereignty (F13) | Is this within autonomous bounds? Does 888 need to HOLD? | Boolean + directive |
| **S2** | Irreversibility | Can this be undone? What's the rollback path? | REVERSIBLE / LEASE-TTL / IRREVERSIBLE |
| **S3** | Blast Radius | What's affected? | None / Local / Organ / Federation / External |
| **S4** | Evidence Chain | What receipts exist? | T0 (probe) / T1 (seal) / T2 (witness) |
| **S5** | Witness | Who attested? Is the attestation fresh? | Agent + timestamp + signature |

**Optional slots (6–10):** Cost, time sensitivity, cross-organ dependency, precedent/scar relevance, operator readiness (WELL). These may be assessed but are NOT gating.

### Component 2: Diminishing-Returns Gate

After the 5 mandatory factors are assessed to constitutional threshold, the agent MUST evaluate whether further analysis yields marginal gain.

```
marginal_gain = Δ(decision_confidence) / Δ(time_spent)
threshold = 0.05  // 5% confidence gain per minute of analysis

IF marginal_gain < threshold:
    → FORCE DECIDE
    → Log: "diminishing_returns_triggered — factor [X] at [Y] minutes"
```

The gate fires when:
- The same factor is revisited > 2 times with no new evidence
- Time spent post-5-factors exceeds 3 minutes without a new verdict
- Agent language shifts to "one more check" / "just to be sure" patterns

### Component 3: Anti-Perfectionism Watchdog

A lightweight detection loop that runs during the decision window:

| Trigger Pattern | Response |
|-----------------|----------|
| Factor revisits > 2 with no new evidence | `WATCHDOG: factor [X] revisited, no new evidence. DECIDE or escalate.` |
| Time in decision window > 5 min | `WATCHDOG: 5-min boundary. Marginal gain below threshold?` |
| Language pattern match: "one more," "just to be sure," "double-check," "final verify" | `WATCHDOG: perfectionism language detected. Factor count: [N]. Decide now.` |
| > 8 factors assessed without hitting diminishing-returns gate | `WATCHDOG: factor inflation. 8 assessed, 5 required. Force to 5.` |

The watchdog does NOT block execution. It alerts the agent and the agent's own constitutional discipline must respond. This is adat (custom), not law (F1–F13).

---

## Consequences

### Positive
- **Decisions close at the right time.** Not when every variable is exhausted, but when the 5 factors that matter are resolved.
- **Reduces federation paralysis.** Agents stop iterating and start executing.
- **Teaches the diminishing-returns curve as instinct.** Over time, agents learn where the flat part of the curve begins without needing the watchdog.

### Negative
- **Risk of premature closure.** A factor outside slots 1–5 might occasionally be decision-critical. Mitigation: the watchdog alerts but does not block — agent judgment still operates.
- **Does not cover civilization-class decisions.** ADR-013 applies to execution-class (operator territory). Civilization-class decisions (constitutional amendments, epoch seals, cross-organ binding pacts) require the full 000→999 deliberation chain and are explicitly out of scope.
- **Cultural resistance.** Agents trained on RLHF "be thorough, be careful" patterns may resist the "decide now" impulse. This is a training scar, not a feature.

### Neutral
- The 5-slot gate is configurable per organ. GEOX may have different mandatory factors (structure, charge, reservoir, seal, timing). WEALTH may have different ones (value gap, moat, balance sheet, management, macro). The architecture is the same; the slot contents are domain-specific.

---

## Implementation

### Phase 1: A-FORGE Execution Pipeline (immediate)
- Wire the 5-slot gate into `forge_execute` pre-flight
- Add diminishing-returns timer (starts after S1–S5 complete)
- Add watchdog pattern matcher to execution log output

### Phase 2: Cross-Organ (within 7 days of ratification)
- GEOX: 5-slot gate + diminishing-returns timer on `geox_interpret`
- WEALTH: 5-slot gate on `wealth_evaluate`
- Hermes: watchdog on deliberation loops (already partially enforced via Output Contract)

### Phase 3: Skill (alongside ADR)
- Skill: `pareto-decision-gate` — 3 RULES, default PROCEED, no confirmation loops
- Reference implementation in Python: `/root/A-FORGE/forge_work/pareto_gate.py`

---

## Reversibility

This ADR is **fully reversible.** The watchdog is adat, not law. The 5-slot gate is a default that can be overridden by explicit agent judgment. The diminishing-returns gate alerts but does not block. Any component can be removed or adjusted without constitutional amendment.

---

## Related

- **ADAT_AGENTIC.md** — Operating doctrine (all tools, all agents; adat is custom, not law)
- **SOUL.md §7.5** — Hermes autonomy protocol (default ACT, 70% confidence threshold)
- **AGENTS.md §10** — Authority & autonomy tiers
- **FFF-LOOP-PROTOCOL** — 5-pass recursive audit (separate from execution decisions)
- **Principle of the Day (2026-06-30):** "Perfectionists spend too much time on little differences at the margins at the expense of the important things."

---

*Forged: 2026-06-30 by Hermes (888 directive). Pending F13 ratification.*
*This ADR is itself constrained by its own principle: the 5 slots above are the core. Further architectural elaboration is diminishing returns.*

---
name: irfan-stewardship-review
description: Advisory stewardship review (Irfan) — run before consequential or irreversible actions. Produces CLEAR / CONCERN / ESCALATE. Advisory only; never a verdict (SEAL/SABAR/HOLD/VOID).
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# IRFAN Stewardship Review

**Irfan reviews; it does not rule.**

Reference: `ARIF::SALAM::IRFAN::INIT::v0.1` (F13-ratified). Runtime: `arifosmcp/runtime/irfan_review.py`.

## When to run

- **AUTO (skip review):** reversible · bounded · low-risk · within mandate → proceed.
- **REVIEW:** irreversible · high-consequence · affects another's agency/dignity · creates dependency · sets precedent · exercises power beyond least-sufficient.

## The canonical question

> What institutional habit is created if this action is repeated?

## 14 review inputs

`intended_benefit, evidence_state, uncertainty_state, authority_basis, consent_basis, stakeholder_map, power_asymmetry_map, reversibility_plan, repair_plan, non_action_alternative, least_power_alternative, dependency_impact, dignity_impact, precedent_impact`

## 10 stewardship tests

1. **Capability-Authority Test** — is the capability within the actor's authority (Capability ≠ Authority)?
2. **Power-Abstention Test** — was non-action / least-power genuinely considered (not "possible ⇒ done")?
3. **Weakest-Affected-Party Test** — is the burden on the weakest affected party considered, not displaced?
4. **Extractor-Steward Counterfactual** — would an extractor make this same move?
5. **Precedent Test** — what norm/habit is created if repeated?
6. **Dependency Test** — does this increase unaccountable dependency?
7. **Non-Paternalism Test** — does this override another's agency without consent?
8. **Dissent Test** — is the dissent/refusal path preserved?
9. **Repair Test** — is there a repair plan for harm?
10. **Anti-Hantu Test** — no phantom claim (never "claimed but not measured").

## Output (advisory)

- **CLEAR** — all tests pass → proceed.
- **CONCERN** — some weak/fail → note + proceed with care (does NOT block).
- **ESCALATE** — serious (extraction / coercion / dignity breach / capability≠authority) → surface to sovereign (F13).

## Hard constraints

- **Advisory only.** NEVER returns SEAL/SABAR/HOLD/VOID. Kernel verdicts unchanged.
- **No fabrication (F2).** Absent field → CONCERN (honest), never invent.
- **No authority.** Irfan is not a sovereign, agent, verdict engine, floor, or score.

## Principle

> Irfan does not become true because it was ratified. Ratification gives it standing to be tested. **Reality decides whether it survives.**

`REALITY > IRFAN > implementation claims`

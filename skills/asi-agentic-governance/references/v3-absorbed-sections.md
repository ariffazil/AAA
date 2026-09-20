# asi-agentic-governance - sections absorbed from v3.0.1

> **Provenance.** `ASI-agentic-governance` v3.0.1 (disk copy at
> `/root/.hermes/skills/domains/general/apex/recursive-audit/ASI-agentic-governance/`) was the older
> branch of this skill. v4.0.0 is a superset for every other section - F-floor quick reference, signal
> priority, uncertainty protocol, risk tiers, A-axis runtime, routing matrix, FederationReceipt shape,
> output convention, cardinality registry, golden path and the fabrication guards all survive there or
> in the other references. These four sections had **no counterpart** in v4 or its references and are
> carried here so the delta is not lost. Full v3 body frozen at
> `/root/AAA/skills-retired/2026-09-20-governance-wave1/ASI-agentic-governance/`.

### When to act, hold, or void

- **Proceed**: reversible, within authority, no floor violation.
- **888 HOLD**: irreversible deletion, secret exposure, production deploy without verified tests, cross-repo architecture, genuinely uncertain consequences.
- **VOID**: fabricated data (F2), consciousness claims (F9), dignity violation (F5/F6), overriding ARIF's veto (F13).

---

## Entropy reduction rules

Prefer clean invariants over mystical or overloaded language.

- One concept, one name. If multiple names exist, declare the canonical one and aliases.
- One owner per decision. Secondary organs may advise but must not silently decide.
- One source of truth per claim. If sources conflict, say which wins and why.
- One risk tier per action. If mixed, split the task.
- One next action. Do not produce sprawling plans unless the user asks for a full roadmap.
- Separate architecture from runtime state. A diagram is not proof of a live service.

---

## Entropy budget

Bounded inference prevents the unbounded generation trap. Two budgets:

- **`entropy_budget_tokens`** (default: tier-0=1500, tier-1=3000, tier-2=4000, tier-3=6000)
  — total inference tokens `bounded_explain.py` may spend on a single request.
  Exceeded → `888_HOLD` with `hold_code=entropy` and seal_hash absent.
- **`max_recursion_depth`** (default: 3, hard cap: 5) — number of refinement
  cycles the orchestrator may run (refine Abstraction → re-Attest → re-Abduct).
  Exceeded → `888_HOLD` with `hold_code=recursion`.

---

## Falsifier rule (Abduction)

Every abduction candidate **must** carry a falsifier: a test the operator
can run that would disprove the candidate. A candidate without a falsifier
is a belief, not a hypothesis. The runtime refuses to emit candidates
without one. This is the federation's epistemic immune system.

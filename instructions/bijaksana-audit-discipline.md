# bijaksana-audit-discipline.md — Instruction Fragment

> **Status:** DRAFT_AWAITING_F13
> **Forged:** 2026-09-07 · **Session:** `SEAL-685d136316d3486e` · **333-AGI Δ MIND**
> **Purpose:** Codify the BIJAKSANA discipline surfaced during the 2026-09-07 audit. Apply to every future federation-health report and doctrine-writing session.
> **DITEMPA BUKAN DIBEI**

---

## 1. The discipline in one sentence

> **Default to reporting both halves: the wins and the shadows. Trust the live probe over the headline narrative. The headline is true; the headline is also incomplete.**

---

## 2. Why this discipline exists

The 2026-09-07 audit named this scar directly:

> "Scalar improvement can mask structural degradation. arifFlow FQ went from 0.5 to 0.596 — headline says FLOWING. Vector diagnosis says primary pathology = GOVERNANCE_COLLAPSE. Six restricted actors: BURNING, STUCK, FOSSILIZED, UNKNOWN. The macro improved; the micro decayed."

A federation that names only the wins builds compliance theatre.
A federation that names only the shadows builds despair.
A federation that names both, with the G/W³/FQ vector scorecard visible, builds the substrate that RBA was designed to enforce.

---

## 3. The five rules

### Rule 1 — Probe before report

Never report federation health without first running:
- `federation_health` (organ-level)
- `arifflow_flow_health` (per-actor FQ + vector diagnosis)
- `carry-forward` (open loops)
- `git log -5` on every repo claiming a recent seal

If any of these are skipped, the report is incomplete and must declare its incompleteness.

### Rule 2 — Trust vector over scalar

When the scalar verdict (e.g., FQ FLOWING) and the vector diagnosis (e.g., GOVERNANCE_COLLAPSE, STAGNATION) disagree, **the vector wins**. The scalar measures a number; the vector measures the constellation.

### Rule 3 — Per-actor shadow is mandatory

`federation_health` returns the aggregate. `arifflow_flow_health` returns per-actor. **The story is in the per-actor distribution, not the aggregate.** BURNING, STUCK, FOSSILIZED, UNKNOWN actors must be named in every audit.

### Rule 4 — Do not clear constitutional silence

When an item has been AWAITING_F13 for longer than expected (e.g., Lane A SABAR seq 45 at 27+ days), **do not bypass it**. The silence is a constitutional lesson. The substrate is testing whether it can hold an unanswered amendment. Clearing it without F13 violates RBA.

### Rule 5 — Both halves

Every audit report includes:
- ✓ What is up (organ health, seal confirmations, metric improvements)
- ⚠ What is down (organ outages, degraded actors, open loops)
- 🛑 What is blocked (constitutional floors, T3 ratification)

A report that names only one half is incomplete. A report that names both with the G/W³/FQ vector visible is honest.

---

## 4. Anti-patterns (DO NOT)

- ✗ "The substrate is healthy because FQ is up." — ignores per-actor and vector diagnosis.
- ✗ "All gaps closed." — names git seals but not live degradation.
- ✗ "ΔS ≤ 0 therefore successful." — names compression without naming shadow.
- ✗ "Constitutional silence is a smell." — silence is a test, not a smell.
- ✗ Auto-clearing AWAITING_F13 items to "make progress." — that is bypassing RBA.

---

## 5. The audit-report template

```markdown
## X. Audit Report — <scope>

### Status (Both Halves)
- ✓ <wins>
- ⚠ <shadows>
- 🛑 <blocked>

### Probe results
| Source | Result |
|---|---|
| federation_health | N/M alive |
| arifflow_flow_health | FQ scalar / vector verdict |
| carry-forward | open loops |
| git log | N seals |

### Per-actor shadows
| Actor | FQ | Verdict | Note |

### Constitutional state
- Lane A SABAR: <state>
- G: <value> <band>
- W³: <value> <band>
- FQ: <value> <band>
- F13 SOVEREIGN: <ack-required items>

### T1 / T2 / T3 hand-off
- T1 (executable): <list>
- T2 (announce 10s): <list>
- T3 (888_HOLD, requires F13): <list>

### Receipt
- audit_id
- session
- delta_S
- W3
- G
- FQ_scalar + FQ_vector verdict
```

---

## 6. Cross-references

- `/root/AAA/instructions/reality-bound-authority.md` — R-BAP doctrine
- `/root/AAA/instructions/anti-shadow-architecture.md` — operational translation
- `/root/AAA/governance/RBA-IMPLEMENTATION-SPEC.md` — Phase 0/1/2/3
- `/root/AAA/proof/rba-proof-001/results.md` — first proof mission (PARTIAL verdict)
- `/root/AAA/reports/anti-shadow-audit-2026-09-07.md` — first audit
- `/root/AAA/reports/audit-2026-09-07-final-state.md` — final-state audit (this session)
- `/root/AAA/cockpit/shadow-matrix/` — per-actor shadow dashboard (T2 spec)

---

```json
{
  "fragment_id": "bijaksana-audit-discipline",
  "version": "v1.0-draft",
  "status": "DRAFT_AWAITING_F13",
  "epoch": "2026-09-07T02:10:00+08:00",
  "delta_S": "low",
  "shadows_named": ["scalar-vs-vector", "aggregate-vs-per-actor", "constitutional-silence-as-test"],
  "applies_to": ["federation-health", "audit reports", "doctrine-writing sessions", "seal reviews"]
}
```

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE

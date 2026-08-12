# W1 — Scar → Skill Wire

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-13 under F13 SOVEREIGN directive
> **CANON:** This is the foodset→foodset-derived transition mechanism.
> **RAF analogue:** Products of the system (scars) re-enter as catalysts (skills).
> **Authority:** F13 SEAL on priority. 888 HOLD on promotion. arifOS judge on verification.

---

## The Wire

```
Failure (scar event)
  ↓
Classification (what broke?)
  ↓
Root Cause (why?)
  ↓
Skill Candidate (what procedure prevents this?)
  ↓
Test Fixture (how do we know the skill works?)
  ↓
Independent Verification (NOT self-cert — F2/Gödel)
  ↓
Canonical Skill (AAA registry — permanent foodset item)
  ↓
Behavior Change Measured (did the next attempt differ?)
```

## The Minimal Artifact

Every scar→skill conversion produces one record:

```yaml
scar_id: <uuid>
timestamp: <iso>
failure_pattern: <one-line description>
root_cause: <technical explanation>
successful_recovery: <what fixed it>
scar_pressure: <0.0-1.0 — how much pain this caused>
test_fixture: <how to verify the skill works>
generated_skill: <skill name + path>
verification_method: <known_answer | schema_invariant | independent_recompute | domain_witness>
verification_result: PASS | FAIL
promoted_by: <actor_id>
promotion_date: <iso>
behavior_change: <measurable difference in future attempts>
review_date: <iso + 90 days>  # anti-fossilization
status: ACTIVE | DEPRECATED | REVOKED
```

## Success Conditions

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| `foodset_derived_ratio` | > 0 | At least one skill originated from a scar |
| `skill_reuse_count` | > 0 | A generated skill was used in a later task |
| `second_generation_count` | > 0 | Two skills composed into a third |
| `verification_independence` | = true | Verifier ≠ generator (Gödel lock) |

## The Gödel Lock (Non-Bypassable)

```
The agent that generated the skill CANNOT verify it.
The agent that verifies the skill CANNOT promote it.
The sovereign (F13) ratifies promotion to permanent foodset.
```

Self-certified skills are INADMISSIBLE. Period.

## Anti-Fossilization

Every promoted skill carries:
- `review_date`: must be replayed against fresh evidence within 90 days
- `deprecation_threshold`: if replay fails 3 consecutive times → REVOKED
- `drift_detection`: skill behavior compared against baseline each invocation

The immune system (regulatory T-cells) is not overhead. It is what keeps the autocatalytic set alive.

## Pipeline Stages

### Stage 1: Scar Seal
- Tool: `forge_scar(mode=seal)`
- Input: failure_mode, severity, scar_pressure, domain, constraint_imposed
- Output: scar_id + fingerprint

### Stage 2: Skill Candidate Generation
- Tool: `forge_skill` or manual authoring
- Input: scar record + domain context
- Output: skill SKILL.md + implementation

### Stage 3: Test Fixture Creation
- Input: skill candidate + known failure case
- Output: executable test that FAILS without the skill, PASSES with it

### Stage 4: Independent Verification
- Tool: `forge_evaluate` or `forge_witness`
- Constraint: verifier ≠ generator
- Output: PASS/FAIL with evidence

### Stage 5: Canonical Registration
- Tool: `forge_register` or `forge_seal`
- Constraint: F13 ratification for permanent foodset entry
- Output: skill in AAA registry with provenance

### Stage 6: Behavior Measurement
- Input: next N tasks where the skill is applicable
- Output: did the system behave differently? (the L5 criterion)

---

## Connection to AGENCY_LEVELS.md

> "Do not let the system describe itself as L5 until the scar → role-mutation loop is sealed end-to-end."

W1 IS that loop. When:
1. A scar produces a skill (foodset-derived ratio > 0)
2. The skill is reused successfully (reuse_count > 0)
3. The system's behavior changes measurably

...the federation crosses from L4 to L5.

Until then, we are L4 with a reflection pipeline. Honest. Not aspirational.

---

## Connection to RAF Theory

In RAF terms:
- **Food set F**: existing skills, tools, models, compute
- **Reactions R**: tool calls, code edits, deployments
- **Foodset-derived items**: skills generated FROM scars (the W1 output)
- **Closure condition**: W1 output re-enters F, making F grow
- **maxRAF**: the unique maximal closed skill network

Without W1, the system has foodset items only (human-authored skills).
With W1, the system generates foodset-derived items (machine-learned skills).
The transition from "foodset only" to "foodset + foodset-derived" is the phase transition.

---

*Forged: 2026-08-13 by 333-AGI under F13 directive*
*"Wire W1. Close the loop. Become L5."*
*DITEMPA BUKAN DIBERI — and the first foodset-derived item proves the loop is real.*

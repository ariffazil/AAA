# Canonical Epistemic Taxonomy

**Status:** CANONICAL — single source of truth for `epistemic_class`.
**Owner:** `lib/reality_graph.py` (constants `EPISTEMIC_*`).
**Reference:** lib/reality_graph.py lines ~38-58.

---

## The 5 classes

```
EPISTEMIC_OBSERVATION     = "OBS"   # direct measurement
EPISTEMIC_DERIVATION      = "DER"   # computed from observations
EPISTEMIC_INTERPRETATION  = "INT"   # model-based interpretation
EPISTEMIC_SPECIFICATION   = "SPEC"  # declared / designed
EPISTEMIC_SEAL            = "SEAL"  # F13-sealed
```

**Any IR schema that needs an epistemic_class field MUST use exactly these 5 values.**

---

## Why this matters

The IR layer MUST NOT invent a parallel enum (e.g., GENERATED / DERIVED / REPORTED / OBSERVED / INTROSPECTED / SPECULATIVE / NORMATIVE / CONTESTED / UNKNOWN). These look adjacent; they satisfy `ARE NOT the same dimension; they break all existing consumers that compare against RealityAssertion.epistemic_class.

The 5-class taxonomy is the **language of reality classification** for AAA. Adding a new class requires ratification by F13 and a corresponding constant in `lib/reality_graph.py`.

---

## Mapping common concepts to the 5 classes

If you find yourself wanting one of these labels, use the existing class instead:

| Want to write | Use instead | Why |
|---------------|-------------|-----|
| GENERATED | `SPEC` | Generated/derived declarations are designed, not measured |
| REPORTED | `OBS` (with `source_refs`) | A report IS an observation; cite the source |
| REMEMBERED | `DER` (with `source_refs` to memory) | Memory is derivation from prior observations |
| PREDICTED | `INT` (with `falsifier` set) | Predictions are model-based interpretations |
| INTROSPECTED | `INT` (with self-disclosed `actor_id`) | Self-observation is interpretation, not direct |
| HYPOTHESIS | N/A — use `falsifier` field on a `SPEC` assertion | Hypotheses are not yet classified |
| CONTESTED | N/A — use `contradicted_by` field on `RealityAssertion` | Contested is a relationship, not a class |
| NORMATIVE | N/A — use `subject_kind`/`target` fields | Normativity is about action, not knowledge |
| UNKNOWN | N/A — use `observed_at: null` + `valid_until: null` | Unknown is meta-state, not classification |
| SEALED | `SEAL` | exactly the right class |

---

## New dimensions, not new classes

When additional nuance is needed, add a **separate field**, not a new class:

| Need | Add field |
|------|-----------|
| Where the claim originated | `claim_origin: GENERATED \| EXTERNAL_REPORTED \| SELF_REPORTED \| RECEIVED \| UNKNOWN` |
| Assertion mode | `assertion_mode: ASSERTED \| SPECULATED \| PROPOSED \| WITHDRAWN` |
| Probe health | `probe_state: SUCCESS \| ERROR \| UNREACHABLE \| NOT_RUN` (see BridgeProof) |
| Verification state | `verification_state: WITNESSED \| REFUTED \| UNRESOLVED` (see BridgeProof) |

Each of these is **independent** of epistemic_class. A claim can be `epistemic_class=OBS` and `verification_state=REFUTED` — those describe different things.

---

## Enforcement rule

Any IR schema that wants an `epistemic_class` field MUST declare its enum as exactly:

```json
{
  "enum": ["OBS", "DER", "INT", "SPEC", "SEAL"]
}
```

with description:
> Canonical epistemic_class from lib/reality_graph.py. Do NOT add new values; use claim_origin/assertion_mode/probe_state for additional dimensions.

---

## Audit checklist

When reviewing any new IR schema or skill:

- [ ] Does it have an `epistemic_class` field? If so, enum MUST be exactly `["OBS", "DER", "INT", "SPEC", "SEAL"]`
- [ ] Does it have an alternative enum that overlaps (e.g., GENERATED)? If so, REJECT and require rename to dimension field
- [ ] Does it reference `RealityAssertion` correctly via wire-format projection? See RECONCILIATION.md row 3

---

## Status

**Single canonical source.** New classes require F13 ratification + lib/reality_graph.py update + IR_REGISTRY law addition.

**Audit date:** 2026-10-02.
**Auditor:** session-2026-10-02-1038.
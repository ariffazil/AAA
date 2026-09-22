# Verdict-Field Axes — when "one concept, three booleans" is the bug class

A reconciliation or judgment payload often reports the **same concept** across multiple boolean
fields. When two of them disagree, the defect class is real, but the fix is **not** to make them
agree — it is to recognise they are independent dimensions and split the plane.

This file gives the worked shape and the rule.

## The three-plane shape (from arifOS `arif_judge` response)

A reconciled judgment has three independent dimensions. They are NOT the same plane.

| Plane | Meaning | Who sets it |
|---|---|---|
| `seal_eligible` | Judgment reconciles to SEAL (consistent, no epistemic violations) | The reconciler |
| `authority_enabled` | Human authority verified (Ed25519 signature on a single-use grant) | The authority service |
| `execution_enabled` | Grant + state recheck passed at execution time | The executor |

A consistent SEAL returns:
```json
{
  "verdict": "SEAL",
  "seal_eligible": true,
  "authority_enabled": false,
  "execution_enabled": false
}
```

These three planes are **independent**. A reconciled verdict that says "judgment is sound" is
distinct from "human said yes" (authority) and "mutation persisted" (execution). The split was the
right outcome of the crack #6+#2 discussion.

## The bug class: collapsing the planes

Common collapse shapes observed in federation payloads:

1. **One field, two meanings.** A `verdict` field that is read as both the judgment's verdict AND
   the execution's permission. The reconciler says SEAL, but authority was never verified. The bug
   is **the field is doing two jobs**. Fix: split into `seal_eligible` (judgment) and
   `authority_enabled` (authority).
2. **Free-text hint mistaken for verdict.** A `summary` or `next_safe_action` field mentioning the
   word "SEAL" is not a SEAL. Treat free text as `UNSTRUCTURED_DECISION_SIGNAL` (hint only), not as
   authoritative. Rule: walk only structured verdict-bearing keys (`verdict`, `effective_verdict`,
   `decision`, `disposition`, `outcome`); do not token-extract from free text.
3. **Multiple verdict fields, one canonical.** A response carrying `verdict=HOLD`,
   `effective_verdict=HOLD`, `kernel_intercept.decision=ALLOW`, `judge_postcondition.verdict=SEAL`.
   The two structured verdict fields agree (HOLD); the kernel_intercept says ALLOW; the postcondition
   says SEAL. Three different surfaces, three different decisions. **This is not a fix-by-field-collapse
   bug** — it is a fix-by-reconciler bug. A reconciler that walks the whole payload, collects every
   verdict-bearing value, and counts distinct values will surface `INCONSISTENT_DECISION_STATE`. A
   reconciler that only compares `verdict` and `effective_verdict` will accept this as consistent.

## The reconciliation procedure that catches all three

```python
def reconcile_payload(payload):
    observations = []
    issues = []
    kernel_decisions = set()
    const_verdicts = set()
    unclassified_tokens = []
    for path, key, raw in walk(payload):
        if key not in VERDICT_BEARING_KEYS:
            continue
        if not isinstance(raw, str):
            issues.append("NON_STRING_DECISION_VALUE")
            continue
        token = raw.strip().upper()
        # Layer inference by path. Default to constitutional; if path
        # contains "kernel", classify as kernel layer.
        layer = "kernel" if "kernel" in path.lower() else "constitutional"
        if token in RAW_TO_KERNEL:
            kernel_decisions.add(RAW_TO_KERNEL[token])
        elif token in RAW_TO_CONSTITUTIONAL:
            const_verdicts.add(RAW_TO_CONSTITUTIONAL[token])
        else:
            unclassified_tokens.append(token)
        observations.append({"path": path, "key": key, "layer": layer, "raw": token})
    # ... accumulate ALL issues, no early return ...
    # Cross-layer: any disagreement is fail-closed
    if kernel_decisions and const_verdicts:
        issues.append("CROSS_LAYER_DECISION_PRESENT")
    # Single canonical verdict; mismatches → HOLD
    if not issues and len(const_verdicts) == 1 and not kernel_decisions:
        verdict = next(iter(const_verdicts))
        seal_eligible = (verdict == SEAL)
    else:
        verdict = HOLD
        seal_eligible = False
    return ReconciliationResult(
        verdict=verdict,
        seal_eligible=seal_eligible,
        authority_enabled=False,    # PR-1: ALWAYS False here
        execution_enabled=False,   # PR-1: ALWAYS False here
        issues=tuple(issues),
        observations=tuple(observations),
    )
```

Two non-obvious rules:

- **Accumulate all violations; do not early-return on the first.** A payload with 4 distinct
  issue classes (unknown token, kernel/constitutional disagreement, unmeasured floor_passed, claim
  provenance mismatch) should report all 4. Each one is a separate finding; collapsing them into
  the first one hides 3 of 4 defects.
- **Recursive walk, no fixed path list.** Verdict-bearing fields can be nested anywhere
  (`meta.some_new_guard.decision`). A path list goes stale the first time a new component emits
  a deep verdict. Walk the whole payload; filter by schema-recognized verdict-bearing keys
  (`verdict`, `effective_verdict`, `decision`, `disposition`, `outcome`); do NOT token-extract from
  free text. The next contract version should annotate fields with `x-arifos-verdict-bearing:
  true` so the walk is schema-validated, not best-effort.

## Closed vocabulary (the layer inference table)

```python
class ConstitutionalVerdict(str, Enum):
    SEAL = "SEAL"
    HOLD = "HOLD"
    SABAR = "SABAR"
    VOID = "VOID"
    OBSERVE_ONLY = "OBSERVE_ONLY"

class KernelDecision(str, Enum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"

# Explicit raw → canonical mapping. Missing mapping = HOLD.
RAW_TO_CONSTITUTIONAL = {
    "SEAL": ConstitutionalVerdict.SEAL,
    "HOLD": ConstitutionalVerdict.HOLD,
    "SABAR": ConstitutionalVerdict.SABAR,
    "VOID": ConstitutionalVerdict.VOID,
    "OBSERVE_ONLY": ConstitutionalVerdict.OBSERVE_ONLY,
    # QUALIFY, RETAK, SYUBHAH: layer-specific; map only when owner
    # declares them equivalent. Default: unknown → HOLD.
}
RAW_TO_KERNEL = {
    "ALLOW": KernelDecision.ALLOW,
    "HOLD": KernelDecision.HOLD,
}
```

**Why two enums:** `ALLOW` (kernel-intercept result) and `SEAL` (constitutional verdict) are
semantically different layers, not interchangeable. A flat enum that maps both to SEAL would let a
disagreement vanish by syntactic accident.

## Rule

> When a payload reports the same concept across multiple booleans or verdict fields, the right
> fix is not to make them agree — it is to recognise they are independent dimensions, give each
> a clear name (`seal_eligible` vs `authority_enabled` vs `execution_enabled`), and let a separate
> agent set each one.

## Cross-reference

- `surface-consistency-audit` SKILL — Step 3 "Separate the axes before calling a value wrong"
- `live-system-audit-discipline` SKILL — Step 4 "Two-call isolation" + Step 5 "Audit the
  instrument, not only the comparison" + Step 7 "A comparator must fail closed on missing inputs"
- `divergent-claim-reconciliation` SKILL — Step 4 "Check the axes before calling something a
  paradox"

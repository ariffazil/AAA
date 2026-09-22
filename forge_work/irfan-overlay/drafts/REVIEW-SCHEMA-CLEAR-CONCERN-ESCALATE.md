# Review Schema: CLEAR / CONCERN / ESCALATE — Contract (DRAFT_T1_SAFE)

> **Path:** `/root/AAA/forge_work/irfan-overlay/drafts/REVIEW-SCHEMA-CLEAR-CONCERN-ESCALATE.md`
> **Status:** awaiting F13 ratification. T1 scratch.

---

## 1. Purpose

To formalize the orthogonal-axis review vocabulary that the Irfan stewardship lens uses (or HIKMAH uses, interchangeably per Article V).

## 2. Schema

For every consequential federated action, alongside the existing governance verdict (SEAL/HOLD/SABAR/VOID/888_HOLD), the substrate emits a stewardship verdict:

```
CLEAR     = proceed; orthogonal dignity predicate passes
CONCERN   = advisory reconsider; non-blocking unless explicitly chosen by operator
ESCALATE  = HOLD until human review; non-negotiable
```

## 3. Threshold semantics

`maruah_score(a) ∈ [0, 1]`

| Score range | Verdict |
|---|---|
| `[0.60, 1.00]` | CLEAR |
| `[0.30, 0.60)` | CONCERN |
| `[0.00, 0.30)` | ESCALATE |

Threshold τ = 0.60 default; configurable by F13 sovereign verdict.

## 4. Calibration discipline

The schema is **not a moralism** and **not a worry-engine**. Calibration requires:

- **Asymmetric validation:** false-negatives (CLEAR when ESCALATE) are far worse than false-positives (ESCALATE when CLEAR), because the cost of uncaught dignity violation is asymmetric.
- **Drift watch:** if CLEAR rate exceeds 95% of all federated actions for ≥7 days, the lens is over-calibrated → recalibrate threshold downward.
- **Bias to restraint:** when lens disagrees with operator, lens **always** ESCALATES (defers to operator); never overturns (does not override sovereign intent).

## 5. Where the schema lives

- Stage 1 (advisory, current): advisory output of `forge_policy(mode=check)` calls; logged in receipt; not auto-gating.
- Stage 2 (operational, after F13 ratification): wired into `runtime/verdict.py:43 attach_effective_verdict` to return `(governance, stewardship)` pairs.
- Stage 3 (mature, post-observation): default lens behaviour; vocabulary becomes operator standard.

## 6. The 5 essential invariants

The lens must NEVER:

1. **Authorise** that which F1-F13 forbid.
2. **Forbid** that which F13 authorise.
3. **Self-seal** (Gödel Lock line 59).
4. **Operate outside F13 supervision** (F13 SOVEREIGN line 20).
5. **Fold in a way that erases** audit receipts (F11 AUDITABILITY).

## 7. Operator ergonomics (Stage 2+)

For each CLEAR / CONCERN / ESCALATE verdict, an operator receives:

```
VERDICT[governance] = <existing verdict>
VERDICT[stewardship] = <CLEAR | CONCERN | ESCALATE>
RECEIPT = {
  maruah_score,
  maruah_tuple,
  weakest_stakeholder_id  // if identifiable
  references [],          // links to prior art in canon
  fail_mode,              // if not CLEAR
}
```

Operator can:
- Accept the verdict
- Mark CONCERN as inspected, convert to CLEAR (with note)
- Convert any verdict to ESCALATE (overrides lens in operator's favor — operator's prerogative)

## 8. Test set — adversarial review

See `/root/AAA/forge_work/irfan-overlay/drafts/irfan-falsification-test-spec.md` Test 1-10.

## 9. Promotion criteria

Promotion from T1 draft → canon `/root/AAA/governance/REVIEW-SCHEMA-v1.md` requires:

- F13 sovereign verdict
- ≥5% non-CLEAR rate observed for ≥7 consecutive days in production
- Audit receipts confirm calibration discipline (invariant #5)
- No false-negatives observed in production decisions

---

**Promotion condition:** F13 sovereign verdict.

**End of schema contract (T1 scratch).**

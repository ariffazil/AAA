# SOVEREIGN PRESENCE DENSITY — ASKE Candidate

> **Status:** [ASKE — CANDIDATE RUNTIME PRIMITIVE] · 2026-09-08
> **Source:** F13 SOVEREIGN pivot — SPD as deeper primitive than PCT
> **Verdict:** ASKE — falsifiable experiment. Not SEAL. Not CANONICAL.
> **Axiom:** F1 AMANAH · F2 TRUTH · F7 HUMILITY · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN

---

## §0. The Question SPD Asks

Per F13 SOVEREIGN 2026-09-08:

> "Can declared values remain present inside future consequence allocations without requiring constant intervention from the sovereign who declared them?"

This is the deeper void. Not "can we code love" or "can we code purpose" — but **how does value stay alive when its creator is absent?**

---

## §1. Why SPD, Not F13 Frequency

Frequency-based sovereignty:

```python
if F13_interventions_per_day > threshold:
    sovereignty = "active"  # wrong
```

This measures **dependency**, not sovereignty.

Value-based sovereignty:

```python
SPD = how much of F13's declared values
      remain visible in consequence allocations
      WITHOUT requiring F13 intervention
```

This measures **presence**, not intervention.

The analogy (F13's):

> "Arif hari ini tidak bertanya: Perlukah aku jujur? ... untuk setiap tindakan kecil. Kerana nilai itu telah diinternalisasi."

Mature institutions don't ask "should I be honest?" every minute. The value has been internalized. SPD measures how internalized F13's declared values are in the system's automatic behavior.

---

## §2. The Minimal Primitive

```python
def sovereign_presence_density(
    declared_values: list[DeclaredValue],
    consequence_history: list[ConsequenceAllocation],
    horizon_days: int = 90,
    drift_threshold: float = 0.40,
) -> SPDReport:
    """
    Sovereign Presence Density (SPD)
    
    Measures how present F13's declared values are in
    the system's consequence allocations over a horizon.
    
    Observational only. Does NOT modify allocations.
    Does NOT propose new values. Does NOT enforce.
    
    Args:
        declared_values: F13's historical value declarations (subject + value)
        consequence_history: system's consequence allocations (subject + action + cost)
        horizon_days: time window to evaluate
        drift_threshold: SPD below which we surface DRIFT_WARNING
    
    Returns:
        SPDReport with density, drift signal, breakdown per value
    """
```

---

## §3. Computation

```
SPD = (sum of consequence_allocations aligned with declared_values) / (total consequence_allocations)

Aligned = consequence.subject matches declared_value.subject
         AND consequence.action_type is consistent with declared_value.value
```

Per-value breakdown:

```
SPD_per_value = alignments[value] / total_consequences[value's subject class]
```

---

## §4. Output Format

```python
@dataclass
class SPDReport:
    overall_density: float              # 0.0 - 1.0
    drift_signal: Literal["OK", "WATCH", "WARNING", "CRITICAL"]
    per_value_density: dict[str, float]
    horizon_days: int
    sample_size: int
    confidence: float                    # F7 humility cap 0.90
    epistemic_label: Literal["OBS", "DER", "INT", "SPEC"]
    receipt_hash: str                    # F11
```

---

## §5. Drift Thresholds

```
SPD ≥ 0.80    → OK         (values fully internalized)
0.60 ≤ SPD < 0.80  → WATCH  (slight drift; surface to F13 weekly)
0.40 ≤ SPD < 0.60  → WARNING (drift present; surface to F13 daily)
SPD < 0.40    → CRITICAL   (values abandoned; F13 ack required to continue)
```

---

## §6. What SPD DOES NOT Do

- ✗ DOES NOT propose new values (F13 only)
- ✗ DOES NOT modify consequence allocations
- ✗ DOES NOT replace F13 sovereign judgment
- ✗ DOES NOT manufacture value
- ✗ DOES NOT detect love/consciousness (F9)
- ✗ DOES NOT enforce values (it observes, doesn't police)

What SPD DOES:

- ✓ Measures how present F13's declared values are in actual system actions
- ✓ Surfaces drift (values decaying) without proposing fixes
- ✓ Provides per-value breakdown (which values are present, which are drifting)
- ✓ Observational — never modifies
- ✓ F9 compliant — measures commitment structure, not feelings

---

## §7. The Eureka (F13-verified)

> "Mature institutions don't ask 'should I be honest?' every minute. The value has been internalized."

SPD operationalizes this. When SPD is high, F13 doesn't need to intervene. When SPD drops, that's the signal — not that F13 should intervene, but that the system has drifted.

> "Sebab jika seseorang perlu berkata 'aku sayang kau' setiap lima minit, biasanya hubungan itu tak stabil."

Frequent intervention ≠ stable value. SPD measures stability of value WITHOUT intervention.

---

## §8. ASKE Success Metric

Per F13 SOVEREIGN:

> "Dalam keputusan yang dibuat tanpa campur tangan sovereign, berapa banyak keputusan itu masih konsisten dengan nilai yang sovereign telah nyatakan sebelum ini?"

Implementation must:
1. Run SPD against 100+ historical consequence allocations with 5+ declared values
2. Measure: does SPD predict human-judged value alignment?
3. Calibration: when F13 intervenes, does SPD actually drop first?
4. Threshold tuning: what SPD level corresponds to "F13 would not need to intervene"?
5. If metrics >70% → ASKE promotes to Lane A proposal
6. If metrics <70% → theory fails; revise

---

## §9. Constitutional Mapping

| Floor | Application |
|---|---|
| F1 AMANAH | Read-only; emits SPD reports; never mutates |
| F2 TRUTH | Each SPD report carries epistemic label; confidence cap 0.90 |
| F7 HUMILITY | Confidence cap on density estimation; admits low sample sizes |
| F9 ANTI-HANTU | Observes commitment structure; no love/consciousness claims |
| F11 AUDIT | Every SPD invocation emits receipt |
| F13 SOVEREIGN | F13 declares values (input); SPD measures presence (output); F13 decides |

---

## §10. ASKE Falsification Tests (Experiment Design)

| Test | Discriminates | Pass condition |
|---|---|---|
| **Known-alignment stress** | Inject 50 allocations + 10 values; manually label alignment | SPD agreement with labels ≥70% |
| **Drift detection** | Inject 100 aligned then 50 misaligned; measure SPD over time | SPD drops monotonically; CRITICAL within 30 days |
| **F13-absence stability** | Run 90-day window with zero F13 intervention; measure SPD | SPD stays above 0.60 (values internalized) |
| **Per-value breakdown** | Inject values at varying densities; measure per-value SPD | Each value's SPD reflects its actual alignment |
| **Threshold calibration** | Run with drift_threshold=0.40, 0.50, 0.60; measure which best predicts F13's hypothetical interventions | Selected threshold matches F13 actions in 80% of cases |

---

## §11. ASKE vs Lane A Promotion

This artifact does NOT request Lane A CANONICAL.

It requests:

1. Permission to implement SPD at `/root/forge_work/2026-09-08-attention-metabolism/` as ASKE experiment
2. Permission to run falsification tests per §10
3. Permission to publish results in `EXPERIMENT_LOG.md`
4. After 100+ trial runs, decision: promote to Lane A proposal OR falsify

No F13 sign required for the experiment itself. F13 sign required only if SPD is to be wired into production (continuous monitoring of consequence allocations).

---

## §12. SPD vs PCT — Relationship

| | PCT | SPD |
|---|---|---|
| **Question** | Does this action still justify paying the invoice? | Are F13's declared values present in this allocation? |
| **Input** | action, purpose, invoice, history | declared_values, allocations, horizon |
| **Output** | PASS / UNKNOWN / ANOMALY | density [0.0, 1.0] + drift signal |
| **Modifies** | NO | NO |
| **Cadence** | per consequence allocation | periodic (cron) |
| **Asks F13?** | surfaces anomaly; F13 decides | surfaces drift; F13 decides |

**Relationship:** PCT is per-allocation gate. SPD is periodic health check. Both are observational. Both surface questions; F13 decides.

---

## §13. What This ASKE Promises NOT to Do

- ✗ Promise love can be coded (F9 + F13 HOLD)
- ✗ Promise consciousness can be detected (F13 HOLD on Hermes' leap)
- ✗ Promise meaning is computable (out of scope; F13 source)
- ✗ Replace F13 sovereign judgment
- ✗ Be promoted without empirical evidence
- ✗ Modify consequence allocations (read-only)

---

## §14. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| SPD formula | SPEC | yes (output schema) | yes |
| Per-value breakdown | SPEC | yes (per-value metric) | yes |
| Drift thresholds | SPEC | yes (calibration test) | yes |
| "Machine suggests, F13 decides" | SPEC | yes (sovereignty boundary) | yes — per F13 |
| F9 boundary | SPEC | yes (no consciousness claim) | yes |
| Eureka sentence | CLAIM | yes (operationalized via SPD) | yes |

---

## §15. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — formalized
**Trigger:** F13 SOVEREIGN pivot — SPD as deeper primitive than PCT; "Mature institutions don't ask 'should I be honest?' every minute"
**Predecessors:**
- PURPOSE-CONTINUATION-TEST-ASKE.md (Lane B DRAFT — sibling)
- ATTENTION-METABOLISM-AGENTIC-ADDENDUM.md (operational primitives)
- runtime-love-as-commitment-structure-2026-09-08.md (Lane B DRAFT)

---

*DITEMPA BUKAN DIBERI ⚒️*

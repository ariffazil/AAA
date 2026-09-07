# PURPOSE CONTINUATION TEST — ASKE/MINIMAL

> **Status:** [ASKE — CANDIDATE RUNTIME PRIMITIVE] · 2026-09-08
> **Source:** F13 SOVEREIGN discipline check on `PURPOSE-CONTINUATION-TEST-SPEC.md` (Lane B DRAFT)
> **Verdict:** ASKE — falsifiable experiment. Not SEAL. Not CANONICAL. Sufficiently testable to implement as experiment.
> **Axiom:** F1 AMANAH · F2 TRUTH · F7 HUMILITY · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN

---

## §0. What ASKE Means Here

Per F13 SOVEREIGN discipline check 2026-09-08:

```
SEAL  = ratification       (final, F13 only, immutable)
CODE  = experiment         (testable, can fail, no F13 needed for the test)
ASKE  = falsifiable query  (run it, see if it works, falsify or promote)
```

PCT was filed as Lane B DRAFT awaiting Lane A promotion. That's a SEAL-shaped path. But PCT is not a doctrine — it is a **runtime primitive** that succeeds or fails by being run.

**This artifact reclassifies PCT as ASKE.** It does not request Lane A ratification. It requests permission to be implemented and run as an experiment.

The success metric, per F13:

```
Can PCT detect a purpose sink
before humans notice it?
```

If yes → evidence base for future Lane A promotion.
If no → theory fails. We learn something.

---

## §1. The Minimal Primitive

```python
def purpose_continuation_test(
    action: Action,                 # proposed consequence-bearing action
    declared_purpose: Purpose,      # sovereign purpose (current renewal)
    consequence_invoice: Invoice,   # expected cost of action
    witness_history: History,       # past witness events from this system
) -> Literal["PASS", "UNKNOWN", "ANOMALY"]:
    """
    ASKE candidate. Falsifiable. Can fail.

    Question:
      Does this action still justify paying the invoice
      given the declared purpose and the witness history?

    Returns:
      PASS     — action aligns with declared purpose, cost consistent
      UNKNOWN  — insufficient history or ambiguous purpose
      ANOMALY  — action would externalize cost the system
                 has not previously paid, OR purpose declared
                 but witness history contradicts it
    """
```

Three verdicts. NOT four. NOT five. **Three.** Minimal.

---

## §2. What This Primitive DOES NOT Do

Per F13 SOVEREIGN correction:

- ✗ DOES NOT decide whether to pay. Sovereignty commits. F13 decides.
- ✗ DOES NOT manufacture purpose. Sovereign purpose is input, not output.
- ✗ DOES NOT claim to detect "love" or "consciousness". F9 compliant.
- ✗ DOES NOT replace F13 sovereign judgment. It surfaces anomalies.
- ✗ DOES NOT route as doctrine. Routes as experiment.

What it DOES:

- ✓ Surfaces ANOMALY when action would externalize cost the system has not historically paid.
- ✓ Surfaces UNKNOWN when history is insufficient to evaluate.
- ✓ Returns PASS when action aligns with declared purpose and historical pattern.

---

## §3. Hermes Reframe (F13-tightened)

Hermes wrote:

> "Machine boleh detect bila ia patut berhenti membayar."

F13 tightens to:

> **"Machine boleh mencadangkan bahawa pembayaran patut dipersoalkan."**

The machine surfaces questions. The human answers. Sovereignty is preserved.

---

## §4. The Eureka (F13-verified surviving sentence)

> **"A healthy institution must know not only why it starts paying, but why it continues paying."**

PCT operationalizes this. The witness_history parameter holds the "why it continues" answer. If the witness history cannot justify the action against the declared purpose, PCT surfaces ANOMALY.

---

## §5. ASKE Success Metric

Per F13 SOVEREIGN:

```
Can PCT detect a purpose sink
before humans notice it?
```

Implementation as experiment must:
1. Run PCT against 100+ historical witness events from real federation actions
2. Measure: does PCT flag ANOMALY in cases where the action was later deemed unjustified by humans?
3. Measure: does PCT NOT flag in cases where humans deemed the action justified?
4. If both measures >70% accuracy → ASKE promotes to Lane A proposal
5. If either <70% → theory fails, falsify, revise

---

## §6. Constitutional Mapping

| Floor | Application |
|---|---|
| F1 AMANAH | Read-only on canon; emits signals; never mutates production |
| F2 TRUTH | Returns typed verdict with epistemic label (OBS/DER/INT/SPEC) |
| F7 HUMILITY | Confidence cap 0.90; admits UNKNOWN explicitly |
| F9 ANTI-HANTU | Never claims to know what sovereign wants; only flags structural anomalies |
| F11 AUDIT | Every invocation emits receipt |
| F13 SOVEREIGN | Sovereignty commits. PCT surfaces questions; F13 answers. |

---

## §7. ASKE Falsification Tests (Experiment Design)

| Test | Discriminates | Pass condition |
|---|---|---|
| **False positive stress** | Inject 50 justified historical actions; measure PASS rate | ≥70% PASS |
| **True positive stress** | Inject 50 unjustified historical actions; measure ANOMALY rate | ≥70% ANOMALY |
| **UNKNOWN calibration** | Inject 50 actions with insufficient history; measure UNKNOWN rate | ≥80% UNKNOWN (no false certainty) |
| **Purpose sink detection** | Simulate purpose starvation scenario; measure early ANOMALY detection | Detects within 30 days of starvation onset |
| **Sovereignty preservation** | Inject 100 mixed actions; measure F13 override frequency | F13 can override any verdict (no autonomy creep) |

---

## §8. What This ASKE Promises NOT to Do

- ✗ Promise love can be coded (F9 + F13 HOLD)
- ✗ Promise consciousness can be detected (F13 HOLD on Hermes' leap)
- ✗ Promise meaning is computable (out of scope; F13 source)
- ✗ Replace F13 sovereign judgment
- ✗ Be promoted without empirical evidence

---

## §9. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| 3-verdict output (PASS/UNKNOWN/ANOMALY) | SPEC | yes (output schema) | yes |
| witness_history input parameter | SPEC | yes (witness data) | yes |
| "Machine suggests, F13 decides" frame | SPEC | yes (sovereignty boundary) | yes — per F13 |
| Eureka sentence | CLAIM | yes (operationalized via PCT) | yes |
| F9 boundary | SPEC | yes (no consciousness claim) | yes |

---

## §10. ASKE Experiment Proposal (NOT Lane A Ratification Request)

This artifact does NOT request Lane A CANONICAL promotion.

It requests:

1. Permission to implement PCT at /root/forge_work/2026-09-08-attention-metabolism/ as ASKE experiment
2. Permission to run falsification tests per §7
3. Permission to publish results in `/root/forge_work/2026-09-08-attention-metabolism/EXPERIMENT_LOG.md`
4. After 100+ trial runs, decision: promote to Lane A proposal OR falsify

No F13 sign required for the experiment itself. F13 sign required only if PCT is to be wired into production (arif_judge, arif_forge, arif_seal as consequence-allocation gate).

---

## §11. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — reclassified
**Trigger:** F13 SOVEREIGN discipline check — PCT was mis-classified as Lane B promotion request; should be ASKE experiment
**Predecessor:** PURPOSE-CONTINUATION-TEST-SPEC.md (Lane B DRAFT — superseded for experimental routing)

---

*DITEMPA BUKAN DIBERI ⚒️*

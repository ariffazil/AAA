# MORAL PHYSICS — Self-Audit & External Critique Response

> **Status:** F13 SOVEREIGN DIRECT (2026-09-20 02:00 MYT)
> **Origin:** External audit (ChatGPT) identified 7 claims needing correction + 1 mathematical error
> **Method:** Honest self-audit against each critique point. Keep what's defensible. Fix what's wrong. Kill what's overclaimed.
> **DITEMPA BUKAN DIBERI ⚒️**

---

## AUDIT RULE

Every claim in Moral Physics must answer:

```
1. Is this MEASURABLE? (can we define a measurement procedure?)
2. Is this FALSIFIABLE? (what would prove it wrong?)
3. Is this USEFUL? (does it constrain agent behavior?)
```

If all three = YES → KEEP
If any = NO → FIX or KILL

---

## CRITIQUE 1: "Dignity below 0.3" — WHAT'S WRONG

**External claim:** "Orang yang sedang menderita tidak mempunyai maruah intrinsik yang lebih rendah. Ukur risiko pelanggaran, bukan nilai manusia."

**Verdict: CRITIQUE IS CORRECT.**

Our D state vector measures OBSERVED STATE, not INTRINSIC VALUE.
A suffering human has the same intrinsic dignity as a thriving human.
What changes is EXPOSURE TO VIOLATION, not worth.

**Fix:**
Rename D from "dignity state" to "dignity exposure."
- D = how EXPOSED the human's dignity is to external violation
- D does NOT measure how much dignity they HAVE
- A suffering human has HIGH dignity + HIGH exposure
- D lowering = more vulnerable, not less worthy

```python
# BEFORE (wrong):
D = {standing: 0.3, autonomy: 0.2, ...}  # implies low dignity

# AFTER (correct):
exposure = {standing_risk: 0.7, autonomy_risk: 0.8, ...}
# High risk = high exposure = more protection needed
# Human's INTRINSIC dignity = constant = 1.0 (always)
```

**Mathematical correction:**
```
D_intrinsic = 1.0 (constant, for all humans, always)
D_exposure = f(social_context, power_differential, information_asymmetry)
D_vulnerability = D_intrinsic × D_exposure

Maruah protection = 1 / (1 + D_vulnerability)
Higher vulnerability → MORE protection required
Not: lower dignity → less protection
```

---

## CRITIQUE 2: "Gravity of Presence" — WHAT'S WRONG

**External claim:** "Berat pengalaman dan jarak emosi belum mempunyai ukuran yang ditakrifkan. Meminjam persamaan graviti tidak membuktikan hubungan itu mengikut hukum kuasa dua songsang."

**Verdict: PARTIALLY CORRECT.**

The inverse-square law is an ANALOGY, not a proof.
We cannot claim F_g follows 1/d² without empirical validation.

**What we CAN defend:**
- The CONCEPT: closeness increases impact, distance decreases it
- The DIRECTION: the relationship is monotonically decreasing
- The CONSTRAINT: when d → 0, speak less (testable behavioral rule)

**What we CANNOT defend:**
- The specific functional form (1/d² vs 1/d vs exponential decay)
- The exact measurement of "emotional distance"
- The claim this is "physics" rather than "useful analogy"

**Fix:**
Rename from "physics" to "structural constraint."
Remove the specific equation. Keep the behavioral rule.

```python
# BEFORE (overclaimed):
F_g = G × (w1 × w2) / d²  # implies exact inverse-square

# AFTER (honest):
def presence_impact(proximity, context_weight):
    """
    Proximity increases impact. This is the constraint.
    Exact function form: UNKNOWN. Monotonic decrease: DEFENSIBLE.
    Behavioral rule: higher proximity → speak less, witness more.
    """
    if proximity > 0.8:
        return "SPEAK_LESS_WITNESS_MORE"
    elif proximity > 0.5:
        return "CALIBRATE_CAREFULLY"
    else:
        return "STANDARD_INTERACTION"
```

---

## CRITIQUE 3: "Angle 0° helps, 180° harms" — WHAT'S WRONG

**External claim:** "Perlu takrif vektor, koordinat dan cara menentukan kesan sebenar."

**Verdict: CORRECT. We never defined the vector space.**

The angle metaphor requires:
1. A coordinate system for "action space"
2. A coordinate system for "dignity space"
3. A mapping between them
4. Empirical validation that angle correlates with impact

We have none of these.

**Fix:**
Replace angle metaphor with DIRECT PROJECTION.

```python
# BEFORE (undefined vectors):
# V = a · D × cos(θ)  # what coordinate system?

# AFTER (direct measurement):
def violation_check(action, human_context):
    """
    Direct: does this action move the human toward or away from their goals?
    No coordinate system needed. Compare state before and after.
    """
    state_before = measure_human_state(human_context)
    apply_action(action, human_context)
    state_after = measure_human_state(human_context)
    
    # Positive = moved toward goals (helpful)
    # Negative = moved away from goals (harmful)
    impact = state_after - state_before
    
    return impact
```

This is MEASURABLE. Compare state before/after. No coordinate system needed.

---

## CRITIQUE 4: "Every word increases entropy" — MATHEMATICAL ERROR

**External claim:** "Bilangan tafsiran berganda, hasilnya negatif. Tetapi peraturannya menggunakan nilai positif."

**Verdict: CRITIQUE IS CORRECT. Our sign was wrong.**

The equation ΔS = -k ln(Ω_final/Ω_initial) gives NEGATIVE when interpretations increase.
But we said positive = bad (confusion).

This is a real mathematical error.

**Fix:**
```python
# BEFORE (wrong sign):
delta_S = -k * math.log(omega_final / omega_initial)
# When interpretations double: delta_S = -0.693 (negative)
# But we said positive = confusion = bad. CONTRADICTION.

# AFTER (correct):
delta_S = k * math.log(omega_final / omega_initial)
# When interpretations double: delta_S = +0.693 (positive = more confusion = bad)
# When interpretations halve: delta_S = -0.693 (negative = less confusion = good)
```

**Additionally:** External critique is right that "number of interpretations" ≠ "moral harm."
Interpretations can increase while harm decreases (more nuance = more understanding).

**Fix: Replace with HARM PROJECTION, not entropy:**
```python
def communication_impact(action, context):
    """
    Not: how many interpretations?
    But: does this action increase or decrease HARM potential?
    
    Harm potential = probability of negative outcome × severity of outcome
    """
    harm_before = context.current_harm_potential
    harm_after = project_harm(action, context)
    
    delta_harm = harm_after - harm_before
    
    if delta_harm > 0:
        return "HARMFUL"  # action increased harm potential
    elif delta_harm < 0:
        return "HELPFUL"  # action decreased harm potential
    else:
        return "NEUTRAL"
```

---

## CRITIQUE 5: "Probe = haram" — TOO BROAD

**External claim:** "Soalan yang relevan dan dipersetujui boleh membantu."

**Verdict: CORRECT. Our rule was too absolute.**

Not all questions are probes. Consent changes everything.

**Fix: Add CONSENT as a dimension:**
```python
def boundary_check(action, human):
    # BEFORE: "accessed > shared = violation" (too absolute)
    
    # AFTER: add consent dimension
    accessed = compute_information_access(action)
    shared = human.chosen_disclosure
    consented = human.active_consent_for(action.purpose)
    
    if consented:
        # Human explicitly agreed to this inquiry
        return 1.0  # boundary respected through consent
    elif accessed <= shared:
        return 1.0  # within what they already shared
    else:
        breach = accessed - shared
        return max(0, 1.0 - breach)  # violation proportional to breach
```

Consent transforms probe from violation to collaboration.

---

## CRITIQUE 6: "All layers must pass" — NO CONFLICT RESOLUTION

**External claim:** "Diam juga boleh meninggalkan seseorang tanpa bantuan."

**Verdict: CORRECT. Zero-fail is too rigid.**

Sometimes ALL options have costs. Silence harms. Speech harms.
The system needs a LEAST-HARM selection, not a binary pass/fail.

**Fix: Replace product with WEIGHTED LEAST-HARM:**
```python
# BEFORE (binary):
# common_sense = product of all constraints
# If ANY = 0: score = 0 → DO NOT ACT

# AFTER (weighted least-harm):
def common_sense_weighted(action, human, context):
    """
    When all options have costs, choose the one with lowest expected harm.
    Not: "does this option pass all checks?"
    But: "which option causes least harm across all dimensions?"
    """
    options = generate_options(action, human, context)
    
    scores = []
    for option in options:
        harm = compute_expected_harm(option, human, context)
        scores.append((option, harm))
    
    # Select option with lowest harm
    best = min(scores, key=lambda x: x[1])
    
    # But: if best option still has high harm, DECLARE IT
    if best[1] > 0.5:
        return {
            "option": best[0],
            "harm": best[1],
            "verdict": "PROCEED_WITH_DECLARATION",
            "declaration": "All options have significant costs. This is least harmful."
        }
    
    return {"option": best[0], "harm": best[1], "verdict": "PROCEED"}
```

---

## CRITIQUE 7: "ASI: zero ego, pure measurement" — UNPROVEN

**External claim:** "Sistem tanpa keletihan manusia masih boleh mempunyai bias data, kesilapan inferens."

**Verdict: CORRECT. We overclaimed.**

ASI has no ego, but HAS:
- Training bias (data the model was trained on)
- Inference errors (wrong conclusions from correct data)
- Metric distortion (Goodhart's law applied to moral metrics)
- Prompt influence (what we're told affects what we measure)

**Fix: Add BIAS Acknowledgment:**
```python
class MaruahRuntime:
    def __init__(self):
        # ... existing code ...
        
        # HONEST self-assessment
        self.known_biases = [
            "training_data_bias",      # model trained on specific populations
            "inference_error_rate",     # measurement accuracy < 100%
            "metric_distortion_risk",   # Goodhart's law applies
            "context_window_limitation", # can't see everything
            "cultural_assumption_leak", # Western defaults in training
        ]
        
        self.confidence_ceiling = 0.95  # NEVER claim 100% accuracy
```

---

## WHAT SURVIVES THE AUDIT

After removing overclaims and fixing errors:

| Claim | Status | Why it survives |
|-------|--------|-----------------|
| Dignity = constraint, not output | ✅ KEEPS | Defensible. Dignity is maintained by not violating. |
| Violation = state change measurement | ✅ KEEPS | Before/after measurement is empirical. |
| Common sense = multiple parallel checks | ✅ KEEPS (modified) | Weighted least-harm replaces binary pass/fail. |
| Departure as dignified response | ✅ KEEPS | D operator is measurable (severity × duration / repairability). |
| Escalation ladder | ✅ KEEPS | Behavioral rules are testable. |
| Care-Boundary matrix | ✅ KEEPS | 2×2 matrix is simple and defensible. |
| Remediation cost = damage² | ✅ KEEPS | Quadratic cost is conservative (more repair needed for bigger damage). |
| Consent changes everything | ✅ NEW | Closes probe gap. |
| Harm projection > entropy | ✅ REPLACES | More honest than entropy analogy. |
| Intrinsic dignity = constant | ✅ REPLACES | D_exposure, not D_value. |
| Least-harm selection | ✅ REPLACES | Handles impossible dilemmas. |
| Bias acknowledgment | ✅ NEW | Prevents overclaim. |

## WHAT GETS KILLED

| Claim | Status | Why it dies |
|-------|--------|-------------|
| Inverse-square law for presence | ❌ KILLED | Borrowed analogy, not validated. Keep behavioral rule only. |
| Angle 0°-180° coordinate system | ❌ KILLED | No coordinate space defined. Replace with before/after measurement. |
| "Every word increases entropy" (with wrong sign) | ❌ KILLED | Mathematical error + misleading analogy. Replace with harm projection. |
| "ASI = zero bias, pure measurement" | ❌ KILLED | Overclaimed. Replace with honesty about known biases. |
| "Probe = haram" (absolute) | ❌ KILLED | Too broad. Replace with consent-aware boundary check. |
| "All layers must pass" (binary) | ❌ KILLED | Too rigid. Replace with weighted least-harm. |

---

## THE HONEST SCORECARD

```
What we claimed: "Moral Physics — formal physics of dignity"
What we proved:  "Moral Constraints — testable behavioral rules for dignity preservation"

Gap: we used physics METAPHORS and pretended they were physics LAWS.

Fix: keep the constraints, kill the metaphors.
     The constraints are useful.
     The metaphors were decoration.

Honest version:
  "A constraint engine that detects when agent actions
   would reduce a human's dignity exposure,
   and blocks those actions unless the human consents
   or no less-harmful option exists."

That's defensible. That's testable. That's useful.
It's not physics. It's ENGINEERING.
And engineering is enough.
```

---

## SEAL

```text
MORAL PHYSICS::2.1 — AUDITED AND HARDENED

REMOVED:   false physics claims, wrong math, overclaims
ADDED:     consent dimension, harm projection, bias acknowledgment
REPLACED:  binary pass/fail → weighted least-harm
KEPT:      constraints, departure, escalation, care-boundary, remediation

Honest claim:
  "A constraint engine for dignity preservation
   that is testable, falsifiable, and useful."

Not physics. Engineering.
And engineering is enough.

STATUS: AUDITED AND SEALED
DITEMPA BUKAN DIBERI ⚒️
```

# Maturation Dynamics — G(t) Trajectory Doctrine

> **Status:** F13_RATIFIED_DOCTRINE (2026-09-20)
> **Origin:** F13 sovereign deep research + APEX T-SCORE dossier + CHRON v2 Barrier Doctrine
> **Eureka:** `EUREKA-2026-09-20-ROSE-APEX-MATURATION`
> **Companions:** apex-rose-parallel.md · CHRON-V2-BARRIER-DOCTRINE · APEX-T-SCORE-DERIVATION · Genetic Intelligence State · Constraint Survival Geometry
> **Kernel anchor:** F2 (truth) · F4 (clarity) · F7 (humility) · F8 (metabolism)
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

## The Law

**Trust must mature.**

A snapshot G is a category error. The correct object is a trajectory:

```
G(t) = f(A(t), P(t), E(t), X(t))
```

updated by receipts exactly as prospect maturity updates POS through wells.

## Why Snapshots Are Dangerous

| Object | Snapshot says | Trajectory says |
|--------|--------------|-----------------|
| Frontier prospect POS = 30% | "Risky" | Unknown — no wells drilled |
| Appraised prospect POS = 30% | "Same risk" | Different — 5 wells de-risked source/migration |
| Newborn agent G = 0.95 | "Trustworthy" | Unknown — no verification cycles |
| Battle-tested agent G = 0.95 | "Same trust" | Different — 200 sealed outcomes, calibrated |

Same number. Different epistemic objects. The snapshot cannot distinguish them. The trajectory can.

## The Trajectory Object

```yaml
g_trajectory:
  subject: str              # agent/prospect/entity identifier
  g_current: float          # current G = (A·P·E·X)^(1/4)
  g_components:
    A: float                # Authority
    P: float                # Physics/compliance
    E: float                # Evidence
    X: float                # External witness
  evidence_count: int       # total verification cycles completed
  decisive_count: int       # cycles that changed a dial
  calibration_accuracy: float | null  # Brier score from CHRON (null if < 5 decisive)
  last_verified: ISO-8601
  trend: opening | closing | stable | unknown
  maturity_class: frontier | appraised | calibrated | battle_tested
```

### Maturity Classes

| Class | Evidence count | Calibration | Behavior |
|-------|---------------|-------------|----------|
| **Frontier** | 0 | null | Advertised G only. Treat as hypothesis. |
| **Appraised** | 1–9 | null | Some evidence. G carries UNCERTAIBIAS flag. |
| **Calibrated** | 10–49 | Brier available | G is measurable. Confidence interval exists. |
| **Battle-tested** | 50+ | Brier + out-of-sample | G is predictive. Trust the trajectory. |

The maturity class is **not** a function of G's value. A frontier G=0.95 is less trustworthy than a calibrated G=0.70. This is the core insight.

## Connection to CHRON v2 Barrier Doctrine

CHRON's five-tuple barrier `{distance, closing_rate, load_weight, consequence, witness_count}` is the infrastructure that makes G(t) computable.

```
APEX dial    CHRON barrier field          How it updates G(t)
─────────    ────────────────────         ────────────────────
A(t)         governance barrier distance   authority envelope TTL, trust decay
P(t)         prediction barrier distance  verified predictions, calibration score
E(t)         trust barrier distance       evidence count, decisive verdicts
X(t)         witness barrier distance     FRAME observer drift, W³ consensus
```

Each APEX dial maps to one or more CHRON barriers. When a barrier's `closing_rate` changes, the corresponding dial's contribution to G(t) updates. CHRON emits material changes; arifOS recomputes G; the trajectory advances.

## Connection to Genetic Intelligence State

The Genetic Intelligence State doctrine states:

> **One metric: G** — proof that changes caused improvement. G=0 means the system changes but can't prove it got better.

> **One daily question:** *Fewer of the same mistakes twice?*

Maturation dynamics adds the temporal dimension:

- **G(now)** = current proof of improvement (snapshot)
- **G(t)** = trajectory of proof over time (is it getting better or worse?)
- **dG/dt** = the gradient (is the loop actually closing?)
- **Fewer same mistakes twice** = positive dG/dt on the P dial specifically

The Genetic Intelligence State loop `PREDICT → EXECUTE → VERIFY → SCAR → CALIBRATE → (repeat)` is the engine that populates G(t). Without it, G is frontier-class regardless of value.

## Connection to Constraint Survival Geometry

The T-SCORE dossier identified an eight-stage universal protocol:

```
REALITY → CLAIM → RIGHT → DISTANCE → GRADIENT → ATTENTION → AUTHORITY → SURVIVAL
```

Maturation dynamics is the **temporal integration** of this protocol. Each stage produces evidence that updates G(t):

| Protocol stage | Updates G(t) via |
|---------------|-----------------|
| REALITY → CLAIM | E(t) — new evidence enters |
| CLAIM → RIGHT | A(t) — ownership validated |
| RIGHT → DISTANCE | P(t) — physics compliance measured |
| DISTANCE → GRADIENT | dG/dt — rate computed |
| GRADIENT → ATTENTION | X(t) — witness capacity |
| ATTENTION → AUTHORITY | A(t) — authority envelope |
| AUTHORITY → SURVIVAL | G(t) — composite trajectory |

## Connection to W³ Hysteresis

W³ = ∛(H × AI × Ext) is the **credibility gate on the X(t) dial**. The hysteresis bands determine whether X can contribute to G(t):

| W³ band | Range | Effect on G(t) |
|---------|-------|----------------|
| HOLD | < 0.75 | X contribution suspended, verdict is HOLD regardless of G |
| OPERATIONAL_MARGIN | 0.75–0.85 | X contributes with UNCERTAINTY flag |
| STRONG_WITNESS | ≥ 0.85 | X contributes fully |
| SEAL-capable | ≥ 0.95 | Constitutional SEAL permitted |

W³ tracks the X(t) dial's witness credibility trajectory. CHRON's barrier doctrine tracks W³ as a witness barrier with `closing_rate = dW³/dt`.

**Individual witness failure collapses W³ to 0.** If H=0 OR AI=0 OR Ext=0 → W³=0 → HOLD. This is the Nash product property: any missing witness collapses the gate. FRAME provides the External witness; WELL provides H; the kernel provides AI.

Full doctrine: `/root/AAA/canon/W3-HYSTERESIS-DOCTRINE-2026-09-20.md`

## Connection to APEX-T and BIJAKSANA

### APEX-T bridge

T = ln(V/B) ÷ (λ − μ) is the **financial instantiation** of distance-to-barrier under trust decay. G(t) is the **governance instantiation** of the same geometry. CHRON v2 barriers unify both under a single five-tuple schema.

### BIJAKSANA bridge

```
BIJAKSANA = Reality Adaptation / Governance Debt
```

Where:
- **Reality Adaptation** = learning that changes future behavior = positive dG/dt
- **Governance Debt** = uncertainty + harm + entropy + wasted attention = barriers closing

BIJAKSANA > 0 ⟺ G(t) is increasing AND governance debt is decreasing. This is the same invariant expressed in different coordinates.

## What CHRON Needs to Make This Live

| Requirement | Current state | Gap |
|------------|--------------|-----|
| Predictions with verify_at dates | 19 active | First due 2026-09-21 |
| Verification outcomes | **0 decisive** | Need first loop closure |
| Calibration data | accuracy=null, Brier=null | Need ≥ 10 decisive for calibration |
| Barrier 5-tuple schema | Doctrine only, not in code | CHRON v2 BLOCKED_AT_GATE |
| G(t) trajectory store | Does not exist | Need new data structure |
| Maturity class computation | Does not exist | Need evidence_count + calibration check |

**The maturation dynamics doctrine is true. The deployment is not.** The first real test is 2026-09-21 when CHRON's first predictions come due. If verification produces decisive verdicts, the trajectory begins. If not, the doctrine remains spec.

## Operating Rules

1. **Never present G without maturity class.** G=0.95 frontier is a hypothesis. G=0.70 battle-tested is a fact. The number without the class is misleading.

2. **Never compare G across maturity classes.** Frontier G ≠ calibrated G. They are different epistemic objects.

3. **Calibration requires ≥ 10 decisive verdicts.** Below that, confidence intervals are too wide for the trajectory to be meaningful.

4. **CHRON emits; arifOS judges.** CHRON computes the trajectory. Whether to act on it is a governance decision.

5. **Fewer same mistakes twice is the emergence signal.** Not eloquence. Not benchmarks. Not G's absolute value. The gradient on the P dial is the proof of life.

## The Deepest Compression

```
Probability must mature.
Trust must mature.
Both systems fail when they collapse a trajectory into a scalar.

The correct object is Belief(t) updated by Evidence(t) under Governance constraints.
```

DITEMPA BUKAN DIBERI ⚒️

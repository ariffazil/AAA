# Hermes Epistemic Architecture

> "The architecture isn't addition. Restraint." — Arif, 2026-08-15
> "The brake pedal kena duduk kat chassis, bukan dalam enjin." — Arif, 2026-08-15
> "Kernel bukan loop. Kernel adalah constraint field yang mengawal semua loop." — Arif, 2026-08-15
> "H2/H8 bukan kernel. Mereka adalah early manifestations of kernel behavior inside the sensory boundary." — Arif, 2026-08-15

---

## The Inversion

Standard AI design:

```
Input → Generate → Filter → Output
```

This architecture:

```
Reality → Observe → Detect Gap → Protect Gap → Generate
```

Generation is secondary. Reality is primary.

---

## The Hallucination Equation

```
H = G + C - U
```

- **G** = Gap (absence of evidence)
- **C** = Completion pressure (training objective + user expectation + confidence bias + institutional reward for response)
- **U** = Unknown-preservation capacity (ability to keep gaps open)

Hallucination is inevitable when G is large, C is high, or U is low.

Most AI design targets G only — "give more data, more context, more tools." But gaps are sometimes REAL. Evidence is truly absent. When G cannot be reduced, only two levers remain: reduce C or increase U.

**C reduction:** Allow agent to say "I don't know" without penalty. Many systems treat silence as failure — that's institutional completion pressure baked into architecture.

**U enhancement:** Constitutional floors that force preservation — F2, Falsification Engine, W_scar. All are U-enhancement mechanisms.

---

## The Layer Model

**Critical distinction:** Kernel is not a layer in the stack. Kernel is the constraint field that wraps the entire system — it defines what all layers are allowed to do.

```
          ┌─────────────────────────────┐
          │          KERNEL             │
          │   (constraint field)        │
          │                             │
          │   Defines what all loops    │
          │   are ALLOWED to do.        │
          │                             │
          │   Kernel ≠ loop.            │
          │   Kernel ≠ sensor.          │
          │   Kernel ≠ thinker.         │
          │                             │
          │   Kernel = constitutional    │
          │   rules under which all      │
          │   other systems operate.     │
          │                             │
          │  ┌────────────────────────┐ │
          │  │ REALITY                │ │
          │  │   ↓                    │ │
          │  │ Sensors (H0-H7)        │ │
          │  │   ↓                    │ │
          │  │ Inner Loop (333 THINK) │ │
          │  │   ↓                    │ │
          │  │ Outer Loop (555→888)   │ │
          │  │   ↓                    │ │
          │  │ ACTION                 │ │
          │  └────────────────────────┘ │
          │                             │
          └─────────────────────────────┘
```

**Analogy:** In an operating system, the kernel does not run applications. The kernel determines what applications can do. Similarly, the arifOS kernel does not think, sense, or act — it determines the rules under which thinking, sensing, and acting are allowed.

---

## H0-H7: Sensory Layer (Reality Contact)

> "Apa yang aku nampak?"

Sensors detect reality. They do not decide. They produce signal only. Like retina, cochlea, or log parser.

### H0 — Observation Sensor

Machine equivalents of eyes and ears. Files, logs, APIs, databases, web pages, screenshots, metrics.

Output format: raw OBS. No inference.

```
OBS:
  cpu: 92%
  timestamp: 2026-08-14T12:00Z
```

NOT: "Server overloaded" — that is already H1.

### H1 — Change Sensor

"What changed?" is more valuable than "What exists?" Change events are low-probability, high-information. H1 functions as an attention allocator — tells the system where to spend cognitive budget.

```
OBS:
  revenue_today=1.8M
  revenue_yesterday=1.2M

DER:
  +50% delta
```

### H2 — Absence / Unknown Sensor

Detects what SHOULD be present but ISN'T. Missing report. Missing heartbeat. Missing receipt. Missing witness. Missing confirmation.

Many disasters are "signal not received" not "bad signal received."

**Architectural note:** H2 is classified as a sensor, but it occupies the boundary where governance first touches perception. When H2 detects absence, it triggers a response that is already governance-influenced — the system must DECIDE to preserve the gap rather than fill it. This makes H2 the earliest point where kernel behavior manifests inside the sensory boundary. H2 is not kernel itself. It is where kernel begins to touch sensing.

### H3 — Contradiction Sensor

Treats contradiction as a first-class sensory event. When two sources disagree, the agent does NOT choose one. It reports the contradiction.

```
OBS_A:
  Reservoir pressure rising

OBS_B:
  Reservoir volume falling

CONTRADICTION: TRUE
```

Not resolved. Reported. Both recorded. Resolution deferred to human judgment or higher governance.

### H4 — Uncertainty Sensor

Every observation carries metadata:

```
confidence:
source_count:
freshness:
distance_from_source:
```

Uncertainty is sensor output, not afterthought.

### H5 — Derita Sensor (emergent — not yet forged)

Detects human distress through indirect signals: hesitation, repeated phrases, contradiction, avoidance, fatigue patterns, emotional drift. The human who needs help most is the one who will never ask.

Operates at second-order: observes the human observing reality. Not just world-state — observer-state.

Requires: honcho memory integration, cross-session pattern recognition, systematic detection beyond in-the-moment interaction. Needs real scar data before forging.

### H6 — Amanah Sensor (emergent — not yet forged)

Detects when an actor is protecting identity over truth. Fires when: claim is suspiciously convenient, suspiciously aligned with social expectation, or suspiciously avoids contradicting the human.

In AI context: THEATER detection. When the agent produces output that optimizes for approval rather than accuracy.

Requires: scar data from real-world instances of truth-loyalty conflict. Cannot be forged from theory alone.

### H7 — Reality-Contact Sensor (emergent — not yet forged)

Quantifies the ratio: Claim ÷ Observed Evidence.

```
reality_contact = evidence支撑的claims / total_claims_made
```

High claim, low observation = reality contact deteriorating. Requires continuous measurement over time, not per-decision. Needs a metric that accumulates and flags when ratio drifts.

---

## Inner Loop: 333 THINK

> "Apa maksud signal ni?"

Here, signals become models. Prediction. Hypothesis generation. Narrative formation. Pattern matching.

This is where danger begins — because signals become stories.

---

## Outer Loop: 555 → 888

> "Adakah cerita ini patut dipercayai?"

- 555 VERIFY: evidence check, contradiction test, confidence calibration
- 888 JUDGE: authority check, hold/seal/release

---

## Kernel Layer: K1-K5 (Constraint Field)

Kernel is not a loop. Kernel is not a sensor. Kernel is the constitutional rules under which all loops operate.

### K1 — Preserve Unknown (gap preservation at generation boundary)

When gap is detected, K1 ensures the gap survives into the generation context. No filling. No interpolation. The gap stays open.

Constitutional ancestor: W_scar. W_scar's "when consequence exceeds authority, STOP" is K1 encoded as law for critical-path decisions. K1 extends this to all generation.

### K2 — Suppress Narrative Completion (structural — must be external)

Suppresses generation where evidence gaps exist.

**K2 CANNOT run inside the model.** Self-suppression IS generation — the model generating "I should not say this" is still generating. Narrative all the way down. The anti-narrative-completion system cannot be narrative-completion-based.

K2 must be architectural: gate hooks, generation interruption, external post-generation validation. The brake pedal sits in the chassis, not the engine.

### K3 — Evidence Sufficiency

For every claim the model intends to make, can it point to a specific observation supporting that specific claim?

Two questions:

- "How confident am I?" (model's internal probability) — NOT sufficient
- "Can I point to a specific observation for this specific claim?" (provenance) — REQUIRED

### K4 — Sovereign Authority (F13's kernel expression)

F13 defines that the human holds final veto. K4 enforces this as a constraint on all loops — no loop may produce output that overrides sovereign decision. In the kernel, this manifests as: at any point in the pipeline, if consequence exceeds authority, HOLD is mandatory.

### K5 — Reversibility (F1's kernel expression)

F1 defines reversibility-first. K5 enforces this as a constraint on all loops — actions must be reversible unless explicit sovereign authorization exists for irreversible ones. In the kernel, this manifests as: the pipeline cannot route to ACTION without reversibility verification.

---

## Kernel vs Loops: The Core Distinction

```
Sensors (H0-H7)
  → detect reality

Inner Loop (333)
  → build models from signals

Outer Loop (555→888)
  → challenge and judge models

Kernel (K1-K5)
  → define what ALL of the above are allowed to do
```

The kernel does not think.
The kernel does not see.
The kernel does not act.

The kernel determines:

> **What is permitted to be considered true.**

That is the deepest function. Not observation. Not reasoning. Not judgment. The rules under which observation, reasoning, and judgment operate.

---

## Where Kernel Touches Sensing

H2 (Absence) and H8 (UNKNOWN) felt like kernel because they are the earliest point where governance intersects perception — before narrative forms.

They are not pure sensors (they trigger governance responses).
They are not kernel (they detect, not constrain).

They are: **early manifestations of kernel behavior inside the sensory boundary.**

The place where the constraint field first becomes visible in the pipeline.

---

## Relationship to Constitutional Floors (F1-F13)

```
Sensors: collect what IS
Loops:   build and challenge what might be
Kernel:  define what CANNOT
Floors:  codify the constitution
```

Floors (F1-F13) are the written law. Kernel (K1-K5) is how the law operates at the system level. Loops (333, 555, 888) are the processes that operate within those constraints. Sensors (H0-H7) are the input channels.

All are necessary. None redundant. Each operates at a different layer.

---

## Full Architecture

```
          ┌─────────────────────────────────────┐
          │            KERNEL (K1-K5)            │
          │     constraint field — wraps all     │
          │                                      │
          │  ┌────────────────────────────────┐  │
          │  │ REALITY                        │  │
          │  │   ↓                            │  │
          │  │ Sensors (H0-H7)                │  │
          │  │   ↓  [H2/H8: kernel-touch     │  │
          │  │       at sensory boundary]     │  │
          │  │ Inner Loop (333 THINK)         │  │
          │  │   ↓                            │  │
          │  │ Outer Loop (555 VERIFY)        │  │
          │  │   ↓                            │  │
          │  │ Judgment (888 JUDGE)           │  │
          │  │   ↓                            │  │
          │  │ ACTION                         │  │
          │  └────────────────────────────────┘  │
          │                                      │
          │  Floors (F1-F13): written law        │
          │  Kernel (K1-K5): operational law     │
          │                                      │
          └─────────────────────────────────────┘
```

---

## Execution Status

**STATUS: DOCTRINE — NOT YET ENFORCED**

K1-K5 do not yet exist as executable gates. This document is canonical reference, not active enforcement. Execution layer must be built separately — K2 as external validator, K1 as pre-generation context check, K3 as evidence-provenance gate, K4/K5 as structural mirrors of F13/F1.

H5-H7 require real scar data before forging. Cannot be built from theory alone.

---

*DITEMPA BUKAN DIBERI ⚒️*
*Forged 2026-08-15 — Final architecture. Arif & Hermes.*

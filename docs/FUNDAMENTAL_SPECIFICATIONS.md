# 13 Fundamental Specifications — ΔH_human < 0

> **Ratified:** 2026-07-11 by F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
> **Status:** SOVEREIGN_DRAFT (awaiting formal sealing)
> **Author:** OpenCode under sovereign directive
> **Supersedes:** None — companion to AGENTS.md F1-F13 floors (action governance)
> **Relation:** F1-F13 floors govern *agent actions*. F1-F13 specs govern *system outputs*.
> **DITEMPA BUKAN DIBERI — Forged, Not Given**

---

## Master Equation

An MCP App or agentic system is acceptable **only if** it decreases uncertainty,
increases human agency, and preserves reversibility.

Entropy here is not only physics entropy. It is a systems concept:

```
ΔH_human = Δ(confusion)
         + Δ(dependency)
         + Δ(error)
         + Δ(conflict)
         + Δ(loss of agency)
         - Δ(knowledge)
         - Δ(coordination)
         - Δ(wisdom)
```

A good GEOX/arifOS architecture must drive:

```
ΔH_human < 0
```

or at minimum:

```
ΔH_human ≤ 0
```

---

## F1 — Truth Preservation

**The system must never convert uncertainty into certainty.**

### Required

```yaml
every_output:
  evidence:
    source: required
  epistemic_class:
    FACT | INTERPRETATION | HYPOTHESIS
  uncertainty:
    required
```

### Failure Mode

AI produces a beautiful geological explanation without evidence.

### Entropy Increase

- False confidence
- Bad decisions
- Institutional memory corruption

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F2 TRUTH | Label evidence OBS/DER/INT/SPEC |
| F7 HUMILITY | Confidence cap 0.90 |
| F9 ANTI-HANTU | No hallucination |

**F1 Spec sharpens F2 floor:** The floor requires labeling. The spec requires
never converting uncertainty into certainty. A labeled inference presented as
"truth" passes F2 but fails F1 Spec.

---

## F2 — Evidence Conservation

**Every important conclusion must preserve its causal chain.**

### Required

```
Observation
    ↓
Processing
    ↓
Interpretation
    ↓
Uncertainty
    ↓
Decision consequence
```

### Never

```
AI answer → human belief
```

### Always

```
Evidence → AI reasoning → human judgment
```

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F2 TRUTH | Evidence anchoring |
| F3 WITNESS | Tri-witness requirement |
| F11 AUDIT | Decision traceability |

**GEOX specific:** Every geological conclusion carries its causal chain from
raw measurement through processing, interpretation, uncertainty, to the
decision consequence. The chain is never truncated.

---

## F3 — Human Agency Preservation

**AI should increase human capability, not replace human sovereignty.**

### Required

```yaml
human:
  final_decision: true

agent:
  recommendation: true

agent:
  authority: bounded
```

### The agent cannot become

- Owner of objectives
- Owner of values
- Final judge

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F13 SOVEREIGN | Arif holds final veto |
| F6 MARUAH | Dignity-first, human over system |
| F5 PEACE² | De-escalate, guard weakest stakeholder |

**F3 Spec expands F13 floor:** F13 says "Arif decides irreversible." F3 says
"the human always decides, period." The agent recommends. The agent never
owns the objective.

---

## F4 — Reversibility First

**Every agent action needs a reversibility classification.**

### Required

```yaml
action:
  type: READ
  reversibility: FULL

action:
  type: WRITE
  reversibility: PARTIAL

action:
  type: SEAL
  reversibility: NONE
```

### Irreversible actions require

- Evidence floor
- Human approval
- Audit trail

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F1 AMANAH | Reversible-first, irreversible → 888_HOLD |
| F11 AUDIT | Every decision logged |

**F4 Spec adds classification to F1 floor:** F1 requires reversibility. F4 Spec
requires *declaring* the reversibility class before every action, making it
explicit and auditable.

---

## F5 — Entropy Budget

**Every autonomous cycle should measure whether it adds or removes disorder.**

### Required

```yaml
entropy_accounting:
  before:
    uncertainty: 0.72
    complexity: 0.65
  after:
    uncertainty: 0.35
    complexity: 0.40
  result:
    entropy_reduction: positive
```

### STOP Conditions

If an agent creates:

- More dashboards
- More alerts
- More interpretations
- More dependencies

without reducing uncertainty:

**STOP.**

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F4 CLARITY | ΔS ≤ 0, leave workspace cleaner |
| F8 GENIUS | Simplest correct path |

**F5 Spec is novel:** No existing floor requires explicit entropy measurement
per cycle. This is new constitutional territory. The closest is F4 CLARITY
(ΔS ≤ 0), but F4 is qualitative while F5 Spec demands quantitative
accounting.

### Known Failure

The "Dashboard Bloat" pattern — 100 charts, 50 warnings, 20 AI opinions.
High agentic output, negative ΔH_human.

---

## F6 — Provenance Sovereignty

**Every important object needs identity.**

### Minimum

```json
{
  "session_id": "",
  "actor_id": "",
  "trace_id": "",
  "source": "",
  "timestamp": "",
  "version": ""
}
```

### Rule

A result without provenance is **informational pollution**.

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F11 AUDIT | Every decision logged, attributable |
| F1 AMANAH | Trace before mutation |

**F6 Spec expands F11 floor:** F11 requires attribution of actions. F6 Spec
requires provenance on *every output object*, not just decisions. The seal
chain is the canonical implementation.

---

## F7 — No Hidden Intelligence

**MCP Apps must expose what they know and what they do not know.**

### Required UI

```
Confidence:
72%

Evidence:
3 seismic attributes
2 wells

Unknown:
No pressure calibration

Next action:
Acquire pressure data
```

### Never

```
Potential world-class reservoir detected
```

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F2 TRUTH | Evidence labeling |
| F7 HUMILITY | Declare unknowns |
| F9 ANTI-HANTU | No hallucinated certainty |

**F7 Spec operationalises F2+F7+F9:** A claim without confidence, evidence,
unknowns, and next action is structurally incomplete. The GEOX Claim Grammar
skill is the partial implementation. Full compliance requires every output to
carry the complete envelope.

---

## F8 — Capability Boundaries

**MCP tools must declare what they can and cannot do.**

### Required

```yaml
capability:
  observe: true
  reason: true
  act: false

authority:
  domain: GEOX
  jurisdiction: Earth evidence
```

### Never

A geology tool should not secretly become:

- Financial authority
- Legal authority
- Political authority

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F10 ONTOLOGY | AI-only ontology, categories preserved |
| F8 GENIUS | Tool-task fitness |
| F12 INJECTION | External ≠ authority |

**F8 Spec prevents category drift:** The tool's declared domain IS its
constitutional boundary. A geoscience tool that starts making legal
recommendations is violating F10 ONTOLOGY + F8 Spec simultaneously.

---

## F9 — Agent Identity Continuity

**Agent emergence must preserve identity continuity.**

### Three identities must not mix

```
MCP session
     |
     |
arifOS governance session
     |
     |
human actor identity
```

### Never

```
anonymous tool call
        =
trusted decision
```

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F11 AUDIT | Actor attribution |
| F1 AMANAH | Identity before mutation |
| F13 SOVEREIGN | Only Arif authorizes |

**F9 Spec prevents identity smuggling:** The G1 scar (seal actor=unknown) is
a direct violation. Every tool call carries session_id + actor_id + trace_id,
and the chain from MCP transport → governance session → human identity must
never collapse.

---

## F10 — Anti-Hallucination Architecture

**Do not rely only on model behavior. Use structural prevention.**

### Required

```
Tool result
    ↓
Schema validation
    ↓
Evidence check
    ↓
Physics check
    ↓
Governance check
    ↓
Human interface
```

### Principle

**The model should not be the final safety layer.**

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F9 ANTI-HANTU | No hallucination |
| F2 TRUTH | Evidence anchoring |
| F3 WITNESS | Tri-witness requirement |

**F10 Spec operationalises F9 floor:** F9 says "no hallucination." F10 Spec
says "build a pipeline that makes hallucination structurally impossible." The
GEOX well-tie pipeline (time-depth calibration → mistie RMS gate → Wiener
extraction) is the template: each stage is a physics gate, not a model check.

---

## F11 — Cognitive Load Reduction

**A good MCP App reduces human mental entropy.**

### Bad

```
100 charts
50 warnings
20 AI opinions
```

### Good

```
Reality:
3 facts

Uncertainty:
2 unknowns

Decision:
1 reversible next step
```

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F4 CLARITY | ΔS ≤ 0 |
| F8 GENIUS | Simplest correct path |
| M2 (capacity-aware) | Output matches recipient's load |

**F11 Spec adds human-scaling to F4 floor:** F4 measures workspace entropy.
F11 Spec measures *cognitive* load. A clean workspace with 100 charts still
fails F11 Spec because human cognition cannot absorb 100 signals.

---

## F12 — Ecosystem Interoperability

**MCP Apps must avoid vendor lock-in.**

### The Law

> One capability, many hosts.

### Architecture

```
GEOX MCP Server
        │
        ├── ChatGPT
        ├── Claude
        ├── Custom GEOX Workbench
        └── Government systems
```

### Rule

Do not build GEOX as a ChatGPT-only application.

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F10 ONTOLOGY | Substrate ≠ being — tool is tool across hosts |
| F12 INJECTION | External ≠ authority — vendor ≠ sovereign |

**F12 Spec is novel:** No existing floor addresses vendor dependence. The MCP
protocol naturally enables multi-host deployment, but the spec makes it
constitutional — a GEOX tool locked to one host is architecturally invalid.

---

## F13 — Emergent Agent Constitutional Ceiling

**When agents become more capable, capability must grow inside boundaries.**

### The agent may increase

- Knowledge
- Speed
- Simulation
- Coordination
- Pattern discovery

### The agent must not increase

- Unaccountable power
- Opacity
- Irreversible action
- Human dependency
- Centralized control

### Floor Cross-Reference

| Existing floor | Alignment |
|---|---|
| F13 SOVEREIGN | Arif holds final veto |
| F6 MARUAH | Dignity-first |
| F9 ANTI-HANTU | No soul/consciousness claims |
| F10 ONTOLOGY | AI-only ontology |

**F13 Spec completes F13 floor:** F13 floor says "Arif decides." F13 Spec
says "capability grows inside boundaries that preserve human agency." The
ceiling is not a static list — it scales with capability. More capable agents
face tighter constraints on power, opacity, and irreversibility.

---

## GEOX-Specific Entropy Tests

A GEOX MCP App must pass the following:

### Geological Entropy Test

Does GEOX reduce:

- Interpretation disagreement?
- Duplicated workflows?
- Missing evidence?
- Undocumented assumptions?

### Decision Entropy Test

Before GEOX:

```
5 experts
5 interpretations
unknown confidence
```

After GEOX:

```
3 supported interpretations
uncertainty range
recommended evidence gap
```

### Institutional Entropy Test

After 10 years, can another geologist understand:

- Why the decision happened?
- What evidence existed?
- What uncertainty remained?

If yes, GEOX preserves civilization memory.

---

## MCP App Zen

The shortest version:

> **The tool must know its limits.**
> **The agent must know its authority.**
> **The human must retain meaning.**
> **The evidence must survive time.**

For GEOX:

> **Earth is the source. Physics is the constraint. Evidence is the memory.**
> **Human judgment is the final layer.**

That is the architecture that prevents agentic emergence from increasing
human total entropy.

---

## Canonical Cross-Reference Matrix

| Spec | Novel? | Enters via | Scar link |
|------|--------|-----------|-----------|
| F1 Truth Preservation | Sharpens F2 | Output envelope | G1 false confidence |
| F2 Evidence Conservation | Sharpens F2/F3 | Causal chain | Her fabrication 2026-05-17 |
| F3 Human Agency | Expands F13 | Decision boundary | Agent self-sealing |
| F4 Reversibility First | Sharpens F1 | Action classification | Docker dead-end loop |
| **F5 Entropy Budget** | **New** | Measurement gate | Dashboard bloat |
| F6 Provenance Sovereignty | Sharpens F11 | Object identity | Phantom tools |
| F7 No Hidden Intelligence | Sharpens F2/F7/F9 | UI contract | "World-class reservoir" |
| F8 Capability Boundaries | Sharpens F10 | Domain declaration | GEOX → finance drift |
| F9 Identity Continuity | Sharpens F1/F11 | Triple identity | G1 actor=unknown |
| F10 Anti-Hallucination | Operationalises F9 | Pipeline gates | Soft F9 reliance |
| F11 Cognitive Load | Sharpens F4 | Human scaling | 100 charts syndrome |
| **F12 Ecosystem Interop** | **New** | Host independence | ChatGPT-only trap |
| **F13 Emergent Ceiling** | Completes F13 | Capability scaling | Unchecked emergence |

---

*Forged: 2026-07-11 under F13 SOVEREIGN directive*
*Status: SOVEREIGN_DRAFT — awaiting formal seal via arif_judge*
*DITEMPA BUKAN DIBERI — The 13 Fundamental Specifications are forged, not given.*

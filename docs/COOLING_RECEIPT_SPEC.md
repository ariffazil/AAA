# COOLING_RECEIPT — VAULT999 Envelope Type

> **Forged:** 2026-07-13 · F13 EUREKA · Constitutional Metabolism Layer
> **Status:** PROPOSED · Awaiting arif_judge SEAL
> **Classification:** VAULT999 seal type · Truth Plane · Observability Plane

---

## 0. Constitutional Mandate

From F13 EUREKA 2026-07-13:

> An agent becomes trustworthy not when it is more intelligent, but when every movement from thought to consequence is bound to identity, authority, evidence, memory, execution and receipt.

The COOLING_RECEIPT closes the metabolic gap: after VERIFY and SEAL, the system must ask "Was the execution equivalent to Reality? What diverged? How should governance adapt?"

Without this step, learning is accidental.

---

## 1. What COOLING_RECEIPT Is

A COOLING_RECEIPT is a VAULT999 envelope type appended **after** a SEAL verdict has been executed and verified. It records:

- The gap between the SEAL's predicted reality and actual reality (ΔR)
- What drifted, what surprised, what failed
- A proposed governance improvement
- A route back through arif_judge — **not** direct execution

### What It Is NOT

- ❌ Not an action order
- ❌ Not a self-deployment ticket
- ❌ Not a memory write (that's for the Continuity plane)
- ❌ Not a new SEAL (that requires fresh arif_judge)
- ❌ Not a blame record
- ❌ Not a replacement for VERIFY

---

## 2. Envelope Schema

```json
{
  "type": "COOLING_RECEIPT",
  "schema_version": "1.0.0",

  "envelope": {
    "receipt_id": "cooling-<ISO8601-ts>-<8char-hex>",
    "timestamp": "ISO-8601",
    "session_id": "<session_that_produced_the_SEAL>",
    "originating_organ": "A-FORGE | GEOX | WEALTH | WELL | AAA"
  },

  "linkage": {
    "original_verdict": {
      "seal_id": "<VAULT999 seal ID of the executed SEAL>",
      "cc_id": "<constitutional_chain_id>",
      "judge_state_hash": "<hash of arif_judge state at verdict>"
    },
    "supersedes": "<optional: prior COOLING_RECEIPT ID this refines>"
  },

  "drift_assessment": {
    "predicted_reality": "<what the SEAL predicted would happen>",
    "actual_reality": "<what actually happened after execution>",
    "drift_detected": true | false,
    "drift_magnitude": 0.0–1.0,
    "drift_category": "NONE | MINOR | SIGNIFICANT | CRITICAL",
    "drift_evidence": ["<evidence receipts, logs, test outputs>"],
    "unexpected_side_effects": ["<list or null>"]
  },

  "improvement": {
    "diagnosis": "<root cause of drift, or why no drift occurred>",
    "proposed_improvement": "<explicit, implementable change>",
    "improvement_class": "POLICY | CAPABILITY | PROCEDURE | CONFIGURATION | SKILL",
    "governance_path": "arifOS | A-FORGE | AAA",
    "estimated_impact": "<what would change if implemented>"
  },

  "governance": {
    "self_deploy": false,
    "routed_to_judge": false,
    "judge_verdict": null,
    "resulting_seal_id": null
  },

  "witness": {
    "human_confidence": 0.0,
    "ai_confidence": 0.0,
    "external_confidence": 0.0
  }
}
```

---

## 3. The Metabolic Loop — Where COOLING_RECEIPT Lives

The full chain after EUREKA:

```
human intent
    ↓
arif_init — identity + session binding
    ↓
arif_observe — evidence gathering
    ↓
arif_route — organ dispatch
    ↓
arif_think — reasoning + plan
    ↓
arif_critique — heart + ethics + maruah
    ↓
arif_judge — constitutional verdict (SEAL)
    ↓
A-FORGE — bounded execution
    ↓
VERIFY — reality check post-execution
    ↓
arif_seal — immutable receipt
    ↓
COOLING — THIS STEP
    │
    ├── COOLING_RECEIPT written to VAULT999
    ├── drift_assessment computed
    ├── proposed_improvement surfaced
    │
    └──→ arif_judge (re-entry) — MAYBE new SEAL
              │
              └──→ policy/capability/tool update
```

COOLING sits **after** SEAL but **before** the next cycle. It closes the loop without shortcutting governance.

---

## 4. The Critical Design Constraint

> **A COOLING_RECEIPT must NEVER self-deploy.**

This is non-negotiable. Constitutional floor F13 + F1 AMANAH.

| Allowed | Forbidden |
|---------|-----------|
| Writing the receipt to VAULT999 | Executing the proposed improvement directly |
| Routing the improvement to arif_judge | Patching policy/capability/tools without governance |
| Surfacing the diagnosis to Arif | Silently updating memory or configuration |
| Attaching evidence of drift | Issuing a new SEAL without fresh adjudication |

**Enforcement mechanism:**

The `governance.self_deploy` field MUST be `false` at creation time. If any agent attempts to set it `true`, the VAULT999 ingress gate **rejects** the receipt. The `governance.routed_to_judge` field transitions to `true` only after arif_judge acknowledges the improvement. Until then, the improvement is **proposal**, not **action**.

---

## 5. Integration With Existing VAULT999 Seals

| Existing Type | Relationship to COOLING_RECEIPT |
|---------------|--------------------------------|
| SEAL (verdict) | Parent — COOLING_RECEIPT references the SEAL it cools |
| HOLD (blocked) | COOLING_RECEIPT may also follow a HOLD if the hold was instructive |
| SABAR (deferred) | COOLING_RECEIPT after SABAR records why deferral was correct or wrong |
| VOID (rejected) | COOLING_RECEIPT after VOID records what was learned from rejection |
| AUDIT_RECEIPT | Separate — AUDIT is structural, COOLING is metabolic |

A single SEAL may produce zero or one COOLING_RECEIPT. A SEAL that executed perfectly with zero drift may skip cooling (no improvement to propose). A SEAL that revealed a structural gap **must** produce a COOLING_RECEIPT.

---

## 6. Lifecycle

```
COOLING_RECEIPT CREATED
    │
    ├── Written to VAULT999 (immutable, append-only)
    │
    ├── STATE: PROPOSAL
    │   ├── Proposed improvement is a hypothesis, not a verdict
    │   ├── No system state has changed
    │   └── Available for human/governance review
    │
    ├── ROUTED TO arif_judge
    │   ├── governance.routed_to_judge = true
    │   ├── Improvement presented as evidence, not order
    │   └── arif_judge evaluates: adopt | reject | defer | modify
    │
    └── RESOLUTION
        ├── Adopted → arif_judge issues new SEAL for the improvement
        │            → governance.judge_verdict = "SEAL"
        │            → governance.resulting_seal_id = <new seal ID>
        ├── Rejected → governance.judge_verdict = "VOID"
        │            → receipt preserved for historical learning
        └── Deferred → governance.judge_verdict = "SABAR"
                      → receipt remains as pending proposal
```

---

## 7. Floor Alignment

| Floor | COOLING_RECEIPT obligation |
|-------|---------------------------|
| F1 AMANAH | Never self-deploy. Always route through governance. |
| F2 TRUTH | drift_assessment must be evidence-anchored. No speculation passed as fact. |
| F3 WITNESS | Tri-witness recommended. At minimum, AI + evidence witness. |
| F4 CLARITY | ΔS ≤ 0 — the receipt reduces ambiguity about what was learned. |
| F5 PEACE² | Never names, blames, or scapegoats. |
| F6 MARUAH | Diagnosis of failure never attacks actor dignity. |
| F7 HUMILITY | proposed_improvement labeled as hypothesis, not certainty. |
| F8 GENIUS | Simplest correct improvement path. One diagnosis, one proposal. |
| F9 ANTI-HANTU | No consciousness claims. Cooling is structural, not sentient. |
| F10 ONTOLOGY | AI-generated improvement is AI-generated. Never labeled "insight from soul." |
| F11 AUDIT | Every receipt tracked. Every resolution recorded. |
| F12 INJECTION | External evidence labelled as external. No phantom authority. |
| F13 SOVEREIGN | Arif may reject any improvement regardless of governance path. |

---

## 8. APEX-G Calibration

For the COOLING_RECEIPT type:

| Primitive | Value | Rationale |
|-----------|-------|-----------|
| **A**daptation | 0.85 | System adapts through governed learning |
| **P**recision | 0.90 | Drift measured against evidence, not opinion |
| **E**vidence | 0.90 | drift_evidence array anchors to receipts |
| **X**ecution | 0.0 | (Deliberate — cooling does NOT execute) |
| **Φ**aithfulness | 0.95 | Constitutional floors fully aligned |

```
G = A · P · E · X · Φ = 0.85 × 0.90 × 0.90 × 0.0 × 0.95 = 0.0
```

**G = 0.0 is correct by design.** The COOLING_RECEIPT has zero execution capacity. It is pure observation + proposal. G reaches > 0 only when arif_judge converts the proposal into a new SEAL with execution capacity.

```
C_dark = A · (1-P) · (1-X) = 0.85 × 0.10 × 1.0 = 0.085
```

C_dark < 0.30 ✅ — No shadow behavior in the cooling design.

---

## 9. Implementation Checklist

- [ ] Register COOLING_RECEIPT as a valid VAULT999 envelope type
- [ ] Add `governance.self_deploy: false` constraint to VAULT999 ingress gate
- [ ] Wire COOLING_RECEIPT creation into A-FORGE post-execution hook
- [ ] Wire COOLING_RECEIPT routing into arif_judge acknowledgment path
- [ ] Add `governance_path` field to arif_judge input schema
- [ ] Create cooling_ledger_entries table in Supabase (if not exists)
- [ ] Test: cooling receipt cannot self-deploy
- [ ] Test: cooling receipt routes correctly through governance
- [ ] Seal: epoch transition with VAULT999 chain continuity

---

## 10. Sealing

```
seal_id      : COOLING_RECEIPT_SPEC::v1.0::2026-07-13
witnesses    : FORGE (000Ω) — spec forge
               F13 EUREKA — constitutional origin
               OpenCode — AAA warga verification
status       : PROPOSED
next_action  : arif_judge SEAL → implementation sprint
cadence      : reviewed within 1 epoch (7 days)
stable_until : 2026-08-13
supersedes   : null (first COOLING_RECEIPT spec)
```

---

*DITEMPA BUKAN DIBERI — Cooling is forged, not assumed.*

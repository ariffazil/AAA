# AAA State Language — Zen-Derived Kernel Rules

> **Lineage:** PEP 20 / Zen of Python  
> **Target:** arifOS + AAA federation state language  
> **Purpose:** Prevent implicit governance, hidden tool action, silent uncertainty, and hantu protocol design.

**Status:** FORGED (v1.0.0 — 2026-06-17)  
**Owner:** AAA Control Plane / F13 SOVEREIGN  
**Schema:** `schemas/aaa-state-language.schema.json`

---

## Core Compression

The Zen of Python reduces into **three arifOS forces**:

```text
1. Cognitive load must go down.
2. Hidden state must become explicit.
3. Practical execution must stay inside constitutional constraint.
```

Translated into AAA terms:

```text
Readable state > clever state
Explicit authority > implicit authority
One governed path > many agent habits
HOLD > guessing
Namespaces > blended power
```

---

## AAA State Record

Every significant federation decision should reduce to one shared state record.

```yaml
aaa_state:
  id: "aaa_state_<uuid>"
  timestamp: "<iso8601>"

  actor:
    actor_id: "arif | agent_id | service_id"
    actor_type: "human | ai | service | organ"
    authority_mode: "observe | propose | execute | seal | veto"

  intent:
    user_request: "<plain language request>"
    normalized_intent: "<kernel-parsed intent>"
    action_class: "OBSERVE | PROPOSE | MUTATE | DEPLOY | ALLOCATE | COMMUNICATE | SEAL"
    risk_class: "C0 | C1 | C2 | C3 | C4 | C5"
    reversible: true
    blast_radius: "low | medium | high | critical"

  epistemics:
    tag: "CLAIM | PLAUSIBLE | HYPOTHESIS | UNKNOWN"
    confidence: 0.0
    uncertainty_band: [0.03, 0.05]
    ambiguity_detected: false
    ambiguity_resolution: "none | clarified | held | downgraded"

  evidence:
    witnesses:
      human: []
      ai: []
      earth: []
      system: []
      capital: []
    citations: []
    retrieval_time: "<iso8601>"
    freshness_status: "fresh | stale | unknown"
    missing_context: []

  floors:
    touched: ["F1", "F2", "F7", "F11", "F13"]
    failed: []
    warnings: []
    floor_verdicts:
      F1_AMANAH: "pass | hold | fail | not_applicable"
      F2_TRUTH: "pass | hold | fail | not_applicable"
      F7_HUMILITY: "pass | hold | fail | not_applicable"
      F11_AUDIT: "pass | hold | fail | not_applicable"
      F13_SOVEREIGN: "pass | hold | fail | not_applicable"

  governance:
    verdict: "SEAL | HOLD | SABAR | VOID | PARTIAL"
    reason: "<human-readable explanation>"
    human_ack_required: false
    human_ack_reference: null
    lease_id: null
    rollback_plan_required: false

  execution:
    allowed: false
    executor: "none | A-FORGE | organ_id"
    tool_called: null
    tool_namespace: null
    side_effects: []
    dry_run_required: false
    dry_run_result: null

  audit:
    vault_required: false
    vault_entry_id: null
    trace_id: "<trace_id>"
    prior_state_hash: "<hash>"
    current_state_hash: "<hash>"
    scar_reference: null

  explanation:
    one_sentence: "<what happened, why, and what is allowed next>"
    explainable_to_operator: true
```

---

## The Doctrine

### 1. Explicit beats implicit

No action should depend on hidden intent, hidden authority, hidden tool choice, or hidden risk classification.

```text
Bad:
  "Agent decided deployment was safe."

Good:
  "arifOS classified action as DEPLOY/C4, required dry-run and F13 approval,
   then A-FORGE executed after SEAL."
```

### 2. Errors never pass silently

Every failure becomes state.

```text
Tool failed       → error state
Evidence missing  → UNKNOWN / HOLD
Intent ambiguous  → SABAR / HOLD
Authority missing → HOLD
Irreversible risk → 888_HOLD
```

Silence is not neutrality. Silence is a governance defect.

### 3. One obvious governed path

AAA should not allow each agent to invent its own lifecycle.

Canonical federation path:

```text
observe
→ evidence
→ reason
→ critique
→ route
→ dry-run
→ judge
→ execute if sealed
→ measure
→ vault
```

Agents can vary in intelligence, but not in constitutional sequence.

### 4. Practicality beats purity, but not sovereignty

arifOS does not need perfect ceremony for low-risk tasks.

```text
C0/C1: light trace
C2: trace + review
C3: evidence gate
C4: human confirmation
C5: SEAL + vault + rollback + human authority
```

Right-sized governance is not weakness. It is load control.

### 5. Hard to explain means bad kernel design

Any AAA/arifOS mechanism that cannot be explained in one short README section should not sit in the core.

```text
Core must be boring.
Organs may be complex.
Kernel must be explainable.
```

Hantu begins where explanation disappears.

### 6. Namespaces are institutional boundaries

Namespaces are not just code hygiene. In arifOS, they are separation of powers.

```text
arifOS     = judge / constitution
AAA        = cockpit / state language / routing
A-FORGE    = executor
GEOX       = earth witness
WEALTH     = capital witness
WELL       = human/vitality witness
VAULT999   = audit memory
F13        = sovereign veto
```

Do not collapse them into one “smart agent.” That destroys accountability.

---

## Canonical AAA State Sentence

Every decision should be explainable in this form:

```text
[ACTOR] requested [INTENT].
arifOS classified it as [ACTION_CLASS/RISK_CLASS].
Evidence status is [CLAIM/PLAUSIBLE/HYPOTHESIS/UNKNOWN] with uncertainty [BAND].
Floors [FLOORS] were engaged.
Verdict is [SEAL/HOLD/SABAR/VOID] because [REASON].
Next allowed action is [NEXT_ACTION].
```

Example:

```text
ChatGPT requested deployment of latest GEOX.
arifOS classified it as DEPLOY/C4.
Evidence status is PLAUSIBLE with uncertainty [0.03, 0.08].
Floors F1, F2, F7, F11, and F13 were engaged.
Verdict is HOLD because deployment is high-impact and requires human approval.
Next allowed action is dry-run preview only.
```

---

## Final Extraction

This is the arifOS version of Zen:

```text
Readable beats clever.
Explicit beats hidden.
Simple beats magical.
One governed path beats many agent habits.
HOLD beats guessing.
Errors become state.
Practicality is allowed, but not silent sovereignty.
Namespaces preserve accountability.
Hard-to-explain governance is hantu.
Uncertainty is part of truth.
```

That is the **AAA State Language spine**.

---

## Cultural Substrates

This document is the technical core. Cultural intelligence layers — such as the Nusantara substrate — sit **on top** of this spine, adding:

- `maruah` (dignity) signals
- `silaturrahim` (relational) witnesses
- `kampung_gadai_risk` (sovereignty-loss) warnings
- `pantang_break` (taboo override) documentation

See `docs/NUSANTARA_STATE.md` and `constitution/SCAR_MELAYU.md`.
